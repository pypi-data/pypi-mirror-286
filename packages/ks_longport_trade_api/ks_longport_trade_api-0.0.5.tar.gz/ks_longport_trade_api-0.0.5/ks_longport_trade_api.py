# todo 1. 对于查询的持仓，空的也要推送空的，否则orderplit无法回调.  这对于http请求很容易实现，但是如果是websocket回调，也许空的不会回调？例如ibk

import pandas as pd
from datetime import datetime
from longport.openapi import *
from typing import Union, Tuple, Optional
import itertools
from ks_trade_api.object import ContractData, MyAccountData, MyErrorData, MyPositionData, MyTradeData, MyOrderData
from ks_trade_api.constant import (
    Currency as KsCurrency,
    Exchange as KsExchange,
    Direction as KsDirection, 
    OrderType as ksOrderType, 
    Direction as KsDirection,
    SubscribeType as KsSubscribeType,
    Offset as KsOffset, 
    TimeInForce as KsTimeInForce,
    ErrorCode as KsErrorCode,
    Status as KsStatus,
    RetCode,
    RET_OK, 
    RET_ASYNC,
    RET_ERROR, 
    CHINA_TZ,
    
)
from ks_trade_api.base_trade_api import BaseTradeApi, RateLimitChecker
from ks_trade_api.utility import extract_vt_symbol, extract_vt_orderid
import sys
from decimal import Decimal
import uuid
from logging import DEBUG, WARNING, ERROR

RATES_INTERVAL: int = 30

EXCHANGE_MY2KS = {
    'US': 'SMART',
    'HK': 'SEHK'
}

SUBTYPE_KS2MY = {
    KsSubscribeType.USER_ORDER: KsSubscribeType.USER_ORDER,
    KsSubscribeType.USER_TRADE: KsSubscribeType.USER_TRADE,
    KsSubscribeType.USER_POSITION: KsSubscribeType.USER_POSITION,
}

# # 长桥的港股前面的0不需要
def raw_symbol_ks2my(raw_symbol: str):
    return raw_symbol.lstrip('0')

def raw_symbol_my2ks(raw_symbol: str, exchange: KsExchange):
    ret_symbol = raw_symbol
    if exchange == KsExchange.SEHK:
        ret_symbol = '0'*(5-len(raw_symbol)) + raw_symbol
    
    return ret_symbol

def extract_my_symbol(my_symbol: str):
    symbol, exchange_str = my_symbol.split('.')
    exchange = KsExchange(EXCHANGE_MY2KS.get(exchange_str))
    symbol = raw_symbol_my2ks(symbol, exchange)

    return symbol, exchange

MARKET_KS2MY = {
    KsExchange.SEHK: 'HK',
    KsExchange.SMART: 'US'
}

MARKET_MY2KS = { v:k for k,v in MARKET_KS2MY.items() }

def symbol_ks2my(vt_symbol: str):
    if not vt_symbol:
        return ''
    symbol, ks_exchange = extract_vt_symbol(vt_symbol)
    # 港股前面的0不需要，否则查询不到持仓
    symbol = raw_symbol_ks2my(symbol)
    return f'{symbol}.{MARKET_KS2MY.get(ks_exchange)}'

ORDERTYPE_MY2KS = {
    str(OrderType.LO): ksOrderType.LIMIT,
    str(OrderType.MO): ksOrderType.MARKET
}

ORDERTYPE_KS2MY = { 
    ksOrderType.LIMIT: OrderType.LO,
    ksOrderType.MARKET: OrderType.MO
}


STATUS_MY2KS = {
    str(OrderStatus.NotReported): KsStatus.NOTTRADED,
    str(OrderStatus.ReplacedNotReported): KsStatus.NOTTRADED,
    str(OrderStatus.ProtectedNotReported): KsStatus.NOTTRADED,
    str(OrderStatus.VarietiesNotReported): KsStatus.NOTTRADED,
    str(OrderStatus.Filled): KsStatus.ALLTRADED,
    str(OrderStatus.WaitToNew):  KsStatus.NOTTRADED,
    str(OrderStatus.New): KsStatus.NOTTRADED,
    str(OrderStatus.WaitToReplace): KsStatus.NOTTRADED,
    str(OrderStatus.PendingReplace): KsStatus.NOTTRADED,
    str(OrderStatus.Replaced): KsStatus.NOTTRADED,
    str(OrderStatus.PartialFilled): KsStatus.PARTTRADED,
    str(OrderStatus.WaitToCancel): KsStatus.NOTTRADED,
    str(OrderStatus.PendingCancel): KsStatus.NOTTRADED,
    str(OrderStatus.Rejected): KsStatus.REJECTED,
    str(OrderStatus.Canceled): KsStatus.CANCELLED,
    str(OrderStatus.Expired): KsStatus.CANCELLED,
    str(OrderStatus.PartialWithdrawal): KsStatus.CANCELLED
}

STATUS_KS2MY = { v:k for k,v in STATUS_MY2KS.items() }

SIDE_KS2MY = {
    f'{KsDirection.LONG.value},{KsOffset.OPEN.value}': OrderSide.Buy,
    f'{KsDirection.SHORT.value},{KsOffset.CLOSE.value}': OrderSide.Sell,
    f'{KsDirection.SHORT.value},{KsOffset.CLOSETODAY.value}': OrderSide.Sell,
    f'{KsDirection.SHORT.value},{KsOffset.CLOSEYESTERDAY.value}': OrderSide.Sell,

    f'{KsDirection.SHORT.value},{KsOffset.OPEN.value}': OrderSide.Sell,
    f'{KsDirection.LONG.value},{KsOffset.CLOSE.value}': OrderSide.Buy,
    f'{KsDirection.LONG.value},{KsOffset.CLOSETODAY.value}': OrderSide.Buy,
    f'{KsDirection.LONG.value},{KsOffset.CLOSEYESTERDAY.value}': OrderSide.Buy,
}

def side_ks2my(direction: KsDirection, offset: KsOffset):
    key = f'{direction.value},{offset.value}'
    return SIDE_KS2MY.get(key)

def sides_ks2my(directions: list[KsDirection], offsets: list[KsOffset]):
    sides_map = {}
    combinations = itertools.product(directions, offsets)
    for direction, offset in combinations:
        sides_map[side_ks2my(direction, offset)] = 1
    sides = list(sides_map.keys())
    return sides

def side_my2ks(side: OrderSide):
    # 为啥原来会是对的？
    if side == OrderSide.Buy:
        direction = KsDirection.LONG
        offset = KsOffset.OPEN
    else:
        direction = KsDirection.SHORT
        offset = KsOffset.CLOSE
    return direction, offset


TIF_KS2MY = {
    KsTimeInForce.GTD: TimeInForceType.Day
}

class KsLongportTradeApi(BaseTradeApi):
    gateway_name: str = "KS_LONGPORT"

    ERROR_CODE_MY2KS: dict = {
        429002: KsErrorCode.RATE_LIMITS_EXCEEDED,
        603059: KsErrorCode.LIQUIDITY_LACKED
    }

    def __init__(self, setting: dict):
        app_key = setting.get('app_key')
        app_secret = setting.get('app_secret')
        access_token = setting.get('access_token')
        dd_secret = setting.get('dd_secret')
        dd_token = setting.get('dd_token')
        gateway_name = setting.get('gateway_name', self.gateway_name)
        
        super().__init__(gateway_name=gateway_name, dd_secret=dd_secret, dd_token=dd_token)

        self.orders = {} # 用来记录成交数量
        self.order_id_status_map: dict = {} # 用于记录order_id和status的映射
        self.api_name_error_time_map: dict = {} # 用于记录api出错时间，限制超频访问
        
        self.conn_config = Config(
            app_key,
            app_secret,
            access_token,
            # http_url='https://openapi.longportapp.cn',
            # quote_ws_url='wss://openapi-quote.longportapp.cn/v2',
            # trade_ws_url = "wss://openapi-trade.longportapp.cn/v2",
        )
        self.init_handlers()

    def order_data_my2ks(self, data) -> MyOrderData:
            symbol, exchange = extract_my_symbol(data.symbol)
            dt: datetime = data.submitted_at
            dt: datetime = dt.astimezone(CHINA_TZ)
            direction, offset = side_my2ks(data.side)
            type = ORDERTYPE_MY2KS.get(str(data.order_type))

            price = data.price if isinstance(data, Order) else data.submitted_price
            volume = data.quantity if isinstance(data, Order) else data.submitted_quantity
            
            order: MyOrderData = MyOrderData(
                symbol=symbol,
                exchange=exchange,
                orderid=data.order_id,
                type=type,
                direction=direction,
                offset=offset,
                price=Decimal(str(price)),
                volume=Decimal(str(volume)),
                traded=Decimal(str(data.executed_quantity)),
                status=STATUS_MY2KS[str(data.status)],
                error=data.msg,
                datetime=dt,
                reference=data.remark,
                gateway_name=self.gateway_name
            )
            return order

    # 初始化行回调和订单回调
    def init_handlers(self):
        trade = self

        # self.quote_ctx = quote_ctx = QuoteContext(self.conn_config)
        self.trd_ctx = trd_ctx = TradeContext(self.conn_config)

        # # 实时行情回调
        # def on_quote(symbol: str, data: PushQuote):
        #     self.on_quote(symbol, data)
        # quote_ctx.set_on_quote(on_quote)

        # # 盘口 callback
        # # 实时行情回调
        # def on_depth(symbol: str, data: PushDepth):
        #     self.on_depth(symbol, data)
        # quote_ctx.set_on_depth(on_depth)
        
        # # 分笔 callback
        # def on_trades(symbol: str, data: PushTrades):
        #     self.on_trades(symbol, data)
        # quote_ctx.set_on_trades(on_trades)

        # kline callback
        # class CurKlineHandler(CurKlineHandlerBase):
        #     def on_recv_rsp(self, rsp_pb):
        #         ret_code, data = super(CurKlineHandler,self).on_recv_rsp(rsp_pb)
        #         if ret_code != RET_OK:
        #             return RET_ERROR, data
        #         trade.on_cur_kline(data)
        #         return RET_OK, data
        # handler = CurKlineHandler()
        # quote_ctx.set_handler(handler) 

        # # 分时 callback
        # class RTDataHandler(RTDataHandlerBase):
        #     def on_recv_rsp(self, rsp_pb):
        #         ret_code, data = super(RTDataHandler,self).on_recv_rsp(rsp_pb)
        #         if ret_code != RET_OK:
        #             trade.log({'msg': data}, level=ERROR, name='on_rt_data')
        #             return RET_ERROR, data
        #         data = Munch.fromDict(data.to_dict('records')[0])
        #         # trade.log(data, name='on_rt_data')
        #         trade.on_rt_data(data)
        #         return RET_OK, data
        # handler = RTDataHandler()
        # quote_ctx.set_handler(handler)

        # order callback
        

     # 订阅行情
    def subscribe(self, vt_symbols, vt_subtype_list, extended_time=True) -> tuple[RetCode, Optional[MyErrorData]]:
        if isinstance(vt_symbols, str):
            vt_symbols = [vt_symbols]

        my_symbols = [symbol_ks2my(x) for x in vt_symbols]
        my_subtype_list = [SUBTYPE_KS2MY.get(x) for x in vt_subtype_list]

        trade = self
        trd_ctx = self.trd_ctx
        if KsSubscribeType.USER_ORDER in my_subtype_list:
            def on_order_changed(data: PushOrderChanged):
                # 先进行成交回调
                # if data.executed_quantity:
                # breakpoint() # todo
                # print('tttttt:', data.status, data.msg)
                order_id = data.order_id
                order = self.orders.get(order_id, None)
                if not order:
                    self.orders[order_id] = order = { 'last_executed_quantity': data.executed_quantity, 'last_share': data.executed_quantity }
                else:
                    last_share = data.executed_quantity - self.orders[order_id]['last_executed_quantity']
                    # 某种情况下，前面的订单状态回调比后续的状态还快，这个时候不能再推送成交
                    if last_share > 0:
                        order['last_share'] = last_share
                        order['last_executed_quantity'] = data.executed_quantity
                    else:
                        order['last_share'] = 0

                if order['last_share']:
                    symbol, exchange = extract_my_symbol(data.symbol)
                    direction, offset = side_my2ks(data.side)
                    price = Decimal(str(data.last_price)) if data.last_price else Decimal('0')
                    volume = Decimal(str(order['last_share']))
                    trade: MyTradeData = MyTradeData(
                        symbol=symbol,
                        exchange=exchange,
                        orderid=data.order_id,
                        tradeid=str(uuid.uuid4()),
                        direction=direction,
                        offset=offset,
                        price=price,
                        volume=volume,
                        datetime=data.updated_at,
                        gateway_name=self.gateway_name
                    )
                    # breakpoint() # todo
                    self.on_trade(trade)

                # 然后进行订单回调
                order: MyOrderData = self.order_data_my2ks(data)
                self.on_order(order)
                self.log(order, level=DEBUG) # todo! 是否影藏吊
                self.order_id_status_map[data.order_id] = order.status

        trd_ctx.set_on_order_changed(on_order_changed)
        trd_ctx.subscribe([TopicType.Private])

        return RET_OK, None

    # 下单
    @RateLimitChecker(RATES_INTERVAL)
    def send_order(
            self, 
            vt_symbol: str,
            price: Decimal,
            volume: Decimal,
            type: ksOrderType = ksOrderType.LIMIT,
            direction: KsDirection = KsDirection.LONG,
            offset: KsOffset = KsOffset.OPEN,
            time_in_force: KsTimeInForce = KsTimeInForce.GTC,
            reference: str = ''
    ) -> Tuple[RetCode, Union[str, MyErrorData]]:
        try:
            my_symbol = symbol_ks2my(vt_symbol)
            order_type = ORDERTYPE_KS2MY.get(type)
            side = side_ks2my(direction, offset)
            time_in_force = TIF_KS2MY.get(time_in_force)
            longport_volume = int(volume) # longport接受的事整型
            data = self.trd_ctx.submit_order(symbol=my_symbol, order_type=order_type, side=side, submitted_quantity=longport_volume, submitted_price=price, time_in_force=TimeInForceType.Day, remark=reference)
            order_id = data and data.order_id
            if order_id:
                symbol, exchange = extract_vt_symbol(vt_symbol)
                order: MyOrderData = MyOrderData(
                    symbol=symbol,
                    exchange=exchange,
                    orderid=order_id,
                    type=type,
                    direction=direction,
                    offset=offset,
                    price=price,
                    volume=volume,
                    reference=reference,
                    gateway_name=self.gateway_name
                )
                if not self.order_id_status_map.get(order_id):
                    self.on_order(order)
                else:
                    self.log(f'由于订单回调已经先于send_order返回，跳过执行on_order。order_id={order_id},current_status={self.order_id_status_map.get(order_id)}', level=WARNING)
            self.log({
                'symbol': my_symbol,
                'order_type': order_type,
                'side': side,
                'submitted_quantity': volume,
                'submitted_price': price,
                'time_in_force': time_in_force,
                'remark': reference,
                'order_id': order_id
            })
            return RET_OK, order.vt_orderid
        except Exception as e:
            error = self.get_error(params={
                'symbol': my_symbol,
                'order_type': order_type,
                'side': side,
                'submitted_quantity': volume,
                'submitted_price': price,
                'time_in_force': time_in_force,
                'remark': reference,
            }, e=e)
            return RET_ERROR, error
        
    # My.add 直接向服务器请求合约数据
    @RateLimitChecker(RATES_INTERVAL)
    def request_cancel_orders(
            self,
            vt_symbol: Optional[str] = None,
            direction: KsDirection = None,
            offset: KsOffset = None
        ) -> tuple[RetCode,  list[MyOrderData]]:
        ret = RET_OK
        orders = []
        
        ret_query, open_orders = self.query_open_orders(vt_symbol=vt_symbol, direction=direction, offset=offset)
        if ret_query == RET_ASYNC:
            # todo 异步尚未处理好
            return ret_query, open_orders
        
        if ret_query == RET_OK:  
            for order in open_orders:
                order: MyOrderData
                ret_cancel, cancel_res = self.cancel_order(order.vt_orderid)
                # todo这里没有处理异步
                if ret_cancel == RET_OK:
                    order.status = KsStatus.CANCELLED
                    orders.append(order)
                else:
                    ret = ret_cancel
                    orders = cancel_res
                    break
        else:
            ret = ret_query
            orders = open_orders
            

        return ret, orders

    # 撤单
    @RateLimitChecker(RATES_INTERVAL)
    def cancel_order(self, vt_orderid: str) -> Tuple[RetCode, Optional[MyErrorData]]:
        self.log({'vt_orderid': vt_orderid}, level=DEBUG)
        try:
            gateway_name, orderid = extract_vt_orderid(vt_orderid)
            data = self.trd_ctx.cancel_order(orderid)
        except Exception as e:
            error = self.get_error(orderid, e=e)
            return RET_ERROR, error

        return RET_OK, vt_orderid

    # 获取账号信息
    def query_account(self, currency: KsCurrency = KsCurrency.USD) -> tuple[RetCode, Union[MyAccountData, MyErrorData]]:
        try:
            data = self.trd_ctx.account_balance(currency.value)
        except Exception as e:
            error = self.get_error(currency=currency, e=e)
            return RET_ERROR, error
        

        account = None
        if data:
            account_data = data[0]
            account: MyAccountData = MyAccountData(
                accountid='',
                balance=account_data.net_assets,
                frozen=0,
                currency=currency,
                gateway_name=self.gateway_name,
            )
            account.available = account_data.total_cash
            return RET_OK, account


    # 获取持仓信息
    @RateLimitChecker(RATES_INTERVAL)
    def query_position(self, vt_symbols=[], directions: list[KsDirection] = []):
        try:
            my_symbols = [symbol_ks2my(x) for x in vt_symbols]
            data = self.trd_ctx.stock_positions(symbols=my_symbols)
        except Exception as e:
            error = self.get_error(vt_symbols, e=e)
            self.send_dd(error.msg, f'持仓查询错误')
            return RET_ERROR, error 
        
        positions = []
        if data and data.channels and data.channels[0].positions:
            for position_data in data.channels[0].positions:
                symbol, exchange = extract_my_symbol(position_data.symbol)
                direction = KsDirection.NET
                position = MyPositionData(
                    symbol=symbol,
                    exchange=exchange,
                    direction=direction,
                    price=position_data.cost_price,
                    volume=Decimal(str(position_data.quantity)),
                    available=Decimal(str(position_data.available_quantity)),
                    gateway_name=self.gateway_name
                )
                positions.append(position)

        # 补齐空持仓
        ret_ks_symbols = [x.vt_symbol for x in positions]
        lack_ks_symbols = [x for x in vt_symbols if not x in ret_ks_symbols]
        for lack_ks_symbol in lack_ks_symbols:
            if not lack_ks_symbol:
                continue
            symbol, exchange = extract_vt_symbol(lack_ks_symbol)
            lack_postion = MyPositionData(symbol=symbol, exchange=exchange, direction=KsDirection.NET, gateway_name=self.gateway_name)
            positions.append(lack_postion)

        return RET_OK, positions
    
    # 获取今日订单
    def query_orders(self, 
        vt_symbol: Optional[str] = None, 
        direction: Optional[KsDirection] = None, 
        offset: Optional[KsOffset] = None,
        status: Optional[list[KsStatus]] = None,
        orderid: Optional[str] = None,
        reference: Optional[str] = None 
    ) -> tuple[RetCode, Union[list[MyOrderData], MyErrorData]]:
        try:
           
            if vt_symbol:
                my_symbol = symbol_ks2my(vt_symbol)
            else:
                my_symbol = None

            if not direction or not offset:
                side = None
            else:
                side = side_ks2my(direction, offset)

            if status:
                my_status = []
                if KsStatus.NOTTRADED in status:
                    my_status += [
                        OrderStatus.NotReported,
                        OrderStatus.ReplacedNotReported,
                        OrderStatus.ProtectedNotReported,
                        OrderStatus.VarietiesNotReported,
                        OrderStatus.WaitToNew,
                        OrderStatus.New,
                        OrderStatus.WaitToReplace,
                        OrderStatus.PendingReplace,
                        OrderStatus.Replaced,
                        OrderStatus.WaitToCancel,
                        OrderStatus.PendingCancel
                    ]
                if KsStatus.CANCELLED in status:
                    my_status += [
                        OrderStatus.Canceled,
                        OrderStatus.Expired,
                        OrderStatus.PartialWithdrawal
                    ]
                if KsStatus.REJECTED in status:
                    my_status += [OrderStatus.Rejected]

                if KsStatus.PARTTRADED in status:
                    my_status += [OrderStatus.PartialFilled]

                if KsStatus.ALLTRADED in status:
                    my_status += [OrderStatus.Filled]
            else:
                my_status = None

            # my_status = None

            orders = self.trd_ctx.today_orders(symbol=my_symbol, side=side, order_id=orderid, status=my_status, market=None)
        except Exception as e:
            error = self.get_error(vt_symbol, direction, offset, status, orderid, reference, e=e)
            return RET_ERROR, error
        
        ks_orders = [self.order_data_my2ks(x) for x in orders if reference == None or reference == x.remark]
        return RET_OK, ks_orders

        
    # 获取今日订单 # todo get_orders没有实现
    def query_open_orders(self, 
            vt_symbol: Optional[str]=None, 
            direction: Optional[KsDirection] = None, 
            offset: Optional[KsOffset] = None,
            status: Optional[list[KsStatus]] = None,
            orderid: Optional[str] = None,
            reference: Optional[str] = None
    ) -> tuple[RetCode, Union[list[MyOrderData], MyErrorData]]:
        status = [KsStatus.SUBMITTING, KsStatus.NOTTRADED, KsStatus.PARTTRADED]
        return self.query_orders(
            vt_symbol=vt_symbol,
            direction=direction,
            offset=offset,
            orderid=orderid,
            status=status,
            reference=reference
        )


    # 关闭上下文连接
    def close(self):
        pass
        # self.quote_ctx.close()
        # self.trd_ctx.close()


        