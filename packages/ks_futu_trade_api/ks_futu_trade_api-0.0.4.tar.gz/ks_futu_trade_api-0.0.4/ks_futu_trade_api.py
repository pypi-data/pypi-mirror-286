# todo 1. 对于查询的持仓，空的也要推送空的，否则orderplit无法回调.  这对于http请求很容易实现，但是如果是websocket回调，也许空的不会回调？例如ibk

import pandas as pd
from datetime import datetime
from futu import *
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
    RetCode as KsRetCode,
    RET_OK as KS_RET_OK, 
    RET_ASYNC as KS_RET_ASYNC,
    RET_ERROR as KS_RET_ERROR, 
    CHINA_TZ,
    
)
from dateutil.parser import parse
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
    exchange_str, symbol = my_symbol.split('.')
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
    return f'{MARKET_KS2MY.get(ks_exchange)}.{symbol}'

ORDERTYPE_MY2KS = {
    str(OrderType.NORMAL): ksOrderType.LIMIT,
    str(OrderType.ABSOLUTE_LIMIT): ksOrderType.LIMIT,
    str(OrderType.MARKET): ksOrderType.MARKET
}

ORDERTYPE_KS2MY = { 
    ksOrderType.LIMIT: OrderType.NORMAL,
    ksOrderType.MARKET: OrderType.MARKET
}


STATUS_MY2KS = {
    str(OrderStatus.NONE): KsStatus.NOTTRADED,
    str(OrderStatus.UNSUBMITTED): KsStatus.NOTTRADED,
    str(OrderStatus.WAITING_SUBMIT): KsStatus.NOTTRADED,
    str(OrderStatus.SUBMITTING): KsStatus.NOTTRADED,
    str(OrderStatus.SUBMIT_FAILED): KsStatus.REJECTED,
    str(OrderStatus.TIMEOUT): KsStatus.REJECTED,
    str(OrderStatus.SUBMITTED):  KsStatus.NOTTRADED,
    str(OrderStatus.FILLED_PART): KsStatus.PARTTRADED,
    str(OrderStatus.FILLED_ALL): KsStatus.ALLTRADED,
    str(OrderStatus.CANCELLING_PART): KsStatus.NOTTRADED,
    str(OrderStatus.CANCELLING_ALL): KsStatus.NOTTRADED,
    str(OrderStatus.CANCELLED_PART): KsStatus.CANCELLED,
    str(OrderStatus.CANCELLED_ALL): KsStatus.CANCELLED,
    str(OrderStatus.FAILED): KsStatus.REJECTED,
    str(OrderStatus.DISABLED): KsStatus.REJECTED,
    str(OrderStatus.DELETED): KsStatus.REJECTED,
    str(OrderStatus.FILL_CANCELLED): KsStatus.CANCELLED
}

STATUS_KS2MY = { v:k for k,v in STATUS_MY2KS.items() }

SIDE_KS2MY = {
    f'{KsDirection.LONG.value},{KsOffset.OPEN.value}': TrdSide.BUY,
    f'{KsDirection.SHORT.value},{KsOffset.CLOSE.value}': TrdSide.SELL,
    f'{KsDirection.SHORT.value},{KsOffset.CLOSETODAY.value}': TrdSide.SELL,
    f'{KsDirection.SHORT.value},{KsOffset.CLOSEYESTERDAY.value}': TrdSide.SELL,

    f'{KsDirection.SHORT.value},{KsOffset.OPEN.value}': TrdSide.SELL,
    f'{KsDirection.LONG.value},{KsOffset.CLOSE.value}': TrdSide.BUY,
    f'{KsDirection.LONG.value},{KsOffset.CLOSETODAY.value}': TrdSide.BUY,
    f'{KsDirection.LONG.value},{KsOffset.CLOSEYESTERDAY.value}': TrdSide.BUY,
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

def side_my2ks(side: TrdSide):
    # 为啥原来会是对的？
    if side == TrdSide.BUY:
        direction = KsDirection.LONG
        offset = KsOffset.OPEN
    else:
        direction = KsDirection.SHORT
        offset = KsOffset.CLOSE
    return direction, offset


TIF_KS2MY = {
    KsTimeInForce.GTD: TimeInForce.DAY
}

# 定义一个自定义错误类
class MyError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        # futu没有错误代码。。只能用文字先替代
        self.code = self.message

class KsFutuTradeApi(BaseTradeApi):
    gateway_name: str = "KS_FUTU"

    ERROR_CODE_MY2KS: dict = {
        '账户购买力不足': KsErrorCode.BUY_POWER_EXCEEDED
    }

    def __init__(self, setting: dict):
        self.security_firm = setting.get('security_firm')
        self.trd_env = setting.get('trd_env', 'REAL')
        self.exchange_id_map: dict = {
            KsExchange.SMART: setting.get('acc_id.us'),
            KsExchange.SEHK: setting.get('acc_id.hk')
        }
        dd_secret = setting.get('dd_secret')
        dd_token = setting.get('dd_token')
        gatway_name: str = setting.get('gateway_name', self.gateway_name)
        
        super().__init__(gateway_name=gatway_name, dd_secret=dd_secret, dd_token=dd_token)

        self.orders = {} # 用来记录成交数量
        self.order_id_status_map: dict = {} # 用于记录order_id和status的映射
        self.api_name_error_time_map: dict = {} # 用于记录api出错时间，限制超频访问
        
        self.init_handlers()

    def order_data_my2ks(self, data) -> MyOrderData:
            symbol, exchange = extract_my_symbol(data.code)
            dt: datetime = parse(data.create_time)
            dt: datetime = dt.astimezone(CHINA_TZ)
            direction, offset = side_my2ks(data.trd_side)
            type = ORDERTYPE_MY2KS.get(str(data.order_type))

            price = data.price
            volume = data.qty
            
            order: MyOrderData = MyOrderData(
                symbol=symbol,
                exchange=exchange,
                orderid=data.order_id,
                type=type,
                direction=direction,
                offset=offset,
                price=Decimal(str(price)),
                volume=Decimal(str(volume)),
                traded=Decimal(str(data.dealt_qty)),
                status=STATUS_MY2KS[str(data.order_status)],
                error=data.last_err_msg,
                datetime=dt,
                reference=data.remark,
                gateway_name=self.gateway_name
            )
            return order
    
    def trade_data_my2ks(self, data) -> MyTradeData:
            symbol, exchange = extract_my_symbol(data.code)
            dt: datetime = parse(data.create_time)
            dt: datetime = dt.astimezone(CHINA_TZ)
            direction, offset = side_my2ks(data.trd_side)

            price = data.price
            volume = data.qty
            
            trade: MyTradeData = MyTradeData(
                symbol=symbol,
                exchange=exchange,
                orderid=data.order_id,
                tradeid=str(uuid.uuid4()),
                direction=direction,
                offset=offset,
                price=Decimal(price),
                volume=Decimal(volume),
                datetime=dt,
                gateway_name=self.gateway_name
            )
            return trade

    # 初始化行回调和订单回调
    def init_handlers(self):
        trade = self

        # self.quote_ctx = quote_ctx = QuoteContext(self.conn_config)
        self.trd_ctx = OpenSecTradeContext(host='127.0.0.1', port=11111, filter_trdmarket=TrdMarket.NONE, security_firm=self.security_firm)  # 创建交易对象

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
        #         if ret_code != KS_RET_OK:
        #             return KS_RET_ERROR, data
        #         trade.on_cur_kline(data)
        #         return KS_RET_OK, data
        # handler = CurKlineHandler()
        # quote_ctx.set_handler(handler) 

        # # 分时 callback
        # class RTDataHandler(RTDataHandlerBase):
        #     def on_recv_rsp(self, rsp_pb):
        #         ret_code, data = super(RTDataHandler,self).on_recv_rsp(rsp_pb)
        #         if ret_code != KS_RET_OK:
        #             trade.log({'msg': data}, level=ERROR, name='on_rt_data')
        #             return KS_RET_ERROR, data
        #         data = Munch.fromDict(data.to_dict('records')[0])
        #         # trade.log(data, name='on_rt_data')
        #         trade.on_rt_data(data)
        #         return KS_RET_OK, data
        # handler = RTDataHandler()
        # quote_ctx.set_handler(handler)

        # order callback
        

     # 订阅行情
    def subscribe(self, vt_symbols, vt_subtype_list, extended_time=True) -> tuple[KsRetCode, Optional[MyErrorData]]:
        if isinstance(vt_symbols, str):
            vt_symbols = [vt_symbols]

        my_symbols = [symbol_ks2my(x) for x in vt_symbols]
        my_subtype_list = [SUBTYPE_KS2MY.get(x) for x in vt_subtype_list]

        me = self
        trd_ctx = self.trd_ctx
        if KsSubscribeType.USER_ORDER in my_subtype_list:
            # order callback
            class TradeOrderHandler(TradeOrderHandlerBase):
                """ order update push"""
                def on_recv_rsp(self, rsp_pb):
                    ret_code, data = super(TradeOrderHandler, self).on_recv_rsp(rsp_pb)
                    if ret_code != RET_OK:
                        return ret_code, me.get_error(e=MyError(data)) 
                    # 然后进行订单回调
                    order: MyOrderData = me.order_data_my2ks(data.iloc[0])
                    me.on_order(order)
                    # 如果是测试环境，不会发生成交回调，使用全部成交这次order回调来fake成交回调
                    if not me.trd_env == 'REAL':
                        if order.status == KsStatus.ALLTRADED:
                            trade: MyTradeData = me.trade_data_my2ks(data.iloc[0])
                            me.on_trade(trade)
                    return RET_OK, data

            handler = TradeOrderHandler()
            trd_ctx.set_handler(handler)

        if KsSubscribeType.USER_TRADE in my_subtype_list:
            # deal callback
            class TradeDealHandler(TradeDealHandlerBase):
                """ order update push"""
                def on_recv_rsp(self, rsp_pb):
                    ret_code, data = super(TradeDealHandler, self).on_recv_rsp(rsp_pb)
                    if ret_code != RET_OK:
                        return ret_code,  me.get_error(e=MyError(data)) 
                    trade: MyTradeData = me.trade_data_my2ks(data.iloc[0])
                    me.on_trade(trade)
                    return RET_OK, data
                
            handler = TradeDealHandler()
            trd_ctx.set_handler(handler)

        return KS_RET_OK, None

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
    ) -> Tuple[KsRetCode, Union[str, MyErrorData]]:
        try:
            my_symbol = symbol_ks2my(vt_symbol)
            symbol, exchange = extract_vt_symbol(vt_symbol)
            order_type = ORDERTYPE_KS2MY.get(type)
            side = side_ks2my(direction, offset)
            time_in_force = TIF_KS2MY.get(time_in_force)
            longport_volume = int(volume) # longport接受的事整型
            ret, data = self.trd_ctx.place_order(
                order_type=order_type,
                price=price or 0, # futu 不支持传入None
                qty=volume,
                code=my_symbol,
                trd_side=side,
                trd_env=self.trd_env,
                acc_id=self.exchange_id_map[exchange],
                remark=reference,
                time_in_force=time_in_force,
                fill_outside_rth=True
            )

            if ret == RET_ERROR:
                raise MyError(data)
            
            order_id = data['order_id'][0]
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
            return KS_RET_OK, order.vt_orderid
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
            return KS_RET_ERROR, error
        
    # My.add 直接向服务器请求合约数据
    @RateLimitChecker(RATES_INTERVAL)
    def request_cancel_orders(
            self,
            vt_symbol: Optional[str] = None,
            direction: KsDirection = None,
            offset: KsOffset = None
        ) -> tuple[KsRetCode,  list[MyOrderData]]:
        ret = KS_RET_OK
        orders = []
        
        ret_query, open_orders = self.query_open_orders(vt_symbol=vt_symbol, direction=direction, offset=offset)
        if ret_query == KS_RET_ASYNC:
            # todo 异步尚未处理好
            return ret_query, open_orders
        
        if ret_query == KS_RET_OK:  
            for order in open_orders:
                order: MyOrderData
                ret_cancel, cancel_res = self.cancel_order(order.vt_orderid)
                # todo这里没有处理异步
                if ret_cancel == KS_RET_OK:
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
    def cancel_order(self, vt_orderid: str) -> Tuple[KsRetCode, Optional[MyErrorData]]:
        self.log({'vt_orderid': vt_orderid}, level=DEBUG)
        try:
            gateway_name, orderid = extract_vt_orderid(vt_orderid)
            data = self.trd_ctx.modify_order(
                modify_order_op=ModifyOrderOp.CANCEL, 
                orderid=orderid,
                trd_env=self.trd_env
            )
        except Exception as e:
            error = self.get_error(orderid, e=e)
            return KS_RET_ERROR, error

        return KS_RET_OK, vt_orderid

    # 获取账号信息
    def query_account(self, currency: KsCurrency = KsCurrency.USD) -> tuple[KsRetCode, Union[MyAccountData, MyErrorData]]:
        accounts: dict[MyAccountData] = []

        try:
            ret, data = self.trd_ctx.accinfo_query(trd_env=self.trd_env, acc_id=self.exchange_id_map[KsExchange.SEHK])
            if ret == RET_ERROR:
                raise MyError(data)
        except Exception as e:
            error = self.get_error(currency=currency, e=e)
            return KS_RET_ERROR, error
        
        if len(data):
            account_data = data.iloc[0]
            account: MyAccountData = MyAccountData(
                accountid='',
                balance=account_data.total_assets,
                frozen=0,
                currency=KsCurrency.HKD,
                gateway_name=self.gateway_name,
            )
            account.available = account_data.power
            accounts.append(account)

        try:
            ret, data = self.trd_ctx.accinfo_query(trd_env=self.trd_env, acc_id=self.exchange_id_map[KsExchange.SMART])
            if ret == RET_ERROR:
                raise MyError(data)
        except Exception as e:
            error = self.get_error(currency=currency, e=e)
            return KS_RET_ERROR, error
        
        if len(data):
            account_data = data.iloc[0]
            account: MyAccountData = MyAccountData(
                accountid='',
                balance=account_data.total_assets,
                frozen=0,
                currency=KsCurrency.USD,
                gateway_name=self.gateway_name,
            )
            account.available = account_data.power
            accounts.append(account)

        return KS_RET_OK, accounts
        


    # 获取持仓信息
    @RateLimitChecker(RATES_INTERVAL)
    def query_position(self, vt_symbols=[], directions: list[KsDirection] = []):
        try:
            # my_symbols = [symbol_ks2my(x) for x in vt_symbols]
            ret, data_us = self.trd_ctx.position_list_query(code=None, trd_env=self.trd_env, acc_id=self.exchange_id_map[KsExchange.SMART])
            if ret == RET_ERROR:
                raise MyError(data_us)
        except Exception as e:
            error = self.get_error(vt_symbols, e=e)
            self.send_dd(error.msg, f'持仓查询错误')
            return KS_RET_ERROR, error

        try:
            my_symbols = [symbol_ks2my(x) for x in vt_symbols]
            ret, data_hk = self.trd_ctx.position_list_query(code=None, trd_env=self.trd_env, acc_id=self.exchange_id_map[KsExchange.SEHK])
            if ret == RET_ERROR:
                raise MyError(data_hk)
        except Exception as e:
            error = self.get_error(vt_symbols, e=e)
            self.send_dd(error.msg, f'持仓查询错误')
            return KS_RET_ERROR, error 
        
        data_df = pd.concat([data_hk, data_us], ignore_index=True)
        positions = []
        if len(data_df):
            for index, position_data in data_df.iterrows():
                symbol, exchange = extract_my_symbol(position_data.code)
                direction = KsDirection.NET
                position = MyPositionData(
                    symbol=symbol,
                    exchange=exchange,
                    direction=direction,
                    price=Decimal(str(position_data.cost_price)),
                    volume=Decimal(str(position_data.qty)),
                    available=Decimal(str(position_data.can_sell_qty)),
                    gateway_name=self.gateway_name
                )
                positions.append(position)

        # 去除多查询的持仓
        if vt_symbols:
            positions = [x for x in positions if x.vt_symbol in vt_symbols]

        # 补齐空持仓
        ret_ks_symbols = [x.vt_symbol for x in positions]
        lack_ks_symbols = [x for x in vt_symbols if not x in ret_ks_symbols]
        for lack_ks_symbol in lack_ks_symbols:
            if not lack_ks_symbol:
                continue
            symbol, exchange = extract_vt_symbol(lack_ks_symbol)
            lack_postion = MyPositionData(symbol=symbol, exchange=exchange, direction=KsDirection.NET, gateway_name=self.gateway_name)
            positions.append(lack_postion)

        return KS_RET_OK, positions
    
    # 获取今日订单
    def query_orders(self, 
        vt_symbol: Optional[str] = None, 
        direction: Optional[KsDirection] = None, 
        offset: Optional[KsOffset] = None,
        status: Optional[list[KsStatus]] = None,
        orderid: Optional[str] = None,
        reference: Optional[str] = None 
    ) -> tuple[KsRetCode, Union[list[MyOrderData], MyErrorData]]:
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
                    my_status += [k for k,v in STATUS_MY2KS.items() if v == KsStatus.NOTTRADED]
                if KsStatus.CANCELLED in status:
                    my_status += [k for k,v in STATUS_MY2KS.items() if v == KsStatus.CANCELLED]
                if KsStatus.REJECTED in status:
                    my_status += [k for k,v in STATUS_MY2KS.items() if v == KsStatus.REJECTED]

                if KsStatus.PARTTRADED in status:
                    my_status += [k for k,v in STATUS_MY2KS.items() if v == KsStatus.PARTTRADED]

                if KsStatus.ALLTRADED in status:
                    my_status += [k for k,v in STATUS_MY2KS.items() if v == KsStatus.ALLTRADED]
            else:
                my_status = None

            # 制定代码则查代码，没有指定则查美股和港股
            if my_symbol:
                symbol, exchange = extract_vt_symbol(vt_symbol)
                ret, orders = self.trd_ctx.order_list_query(
                    order_id=orderid or '',
                    code=my_symbol or '',
                    trd_env=self.trd_env,
                    acc_id=self.exchange_id_map[exchange],
                    status_filter_list=my_status or []
                )
                if ret == RET_ERROR:
                    raise MyError(orders)
            else:
                ret, hk_orders = self.trd_ctx.order_list_query(
                    order_id=orderid or '',
                    code='',
                    trd_env=self.trd_env,
                    acc_id=self.exchange_id_map[KsExchange.SEHK],
                    status_filter_list=my_status or []
                )
                if ret == RET_ERROR:
                    raise MyError(hk_orders)
                
                ret, us_orders = self.trd_ctx.order_list_query(
                    order_id=orderid or '',
                    code='',
                    trd_env=self.trd_env,
                    acc_id=self.exchange_id_map[KsExchange.SEHK],
                    status_filter_list=my_status or []
                )
                if ret == RET_ERROR:
                    raise MyError(us_orders)
                
                orders = pd.concat([hk_orders, us_orders], ignore_index=True)


        except Exception as e:
            error = self.get_error(vt_symbol, direction, offset, status, orderid, reference, e=e)
            return KS_RET_ERROR, error
        
        orders = [self.order_data_my2ks(x) for i,x in orders.iterrows() if reference == None or reference == x.remark]
        return KS_RET_OK, orders

        
    # 获取今日订单 # todo get_orders没有实现
    def query_open_orders(self, 
            vt_symbol: Optional[str]=None, 
            direction: Optional[KsDirection] = None, 
            offset: Optional[KsOffset] = None,
            status: Optional[list[KsStatus]] = None,
            orderid: Optional[str] = None,
            reference: Optional[str] = None
    ) -> tuple[KsRetCode, Union[list[MyOrderData], MyErrorData]]:
        status = [KsStatus.SUBMITTING, KsStatus.NOTTRADED, KsStatus.PARTTRADED]
        return self.query_orders(
            vt_symbol=vt_symbol,
            direction=direction,
            offset=offset,
            orderid=orderid,
            status=status,
            reference=reference
        )


    def close(self):
        self.trd_ctx.close()


        