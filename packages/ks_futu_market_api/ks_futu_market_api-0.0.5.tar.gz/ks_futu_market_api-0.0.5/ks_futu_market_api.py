from futu import *
from datetime import datetime, timedelta
from ks_trade_api.utility import extract_vt_symbol
from ks_trade_api.constant import Exchange as KsExchange, Product as KsProduct, SubscribeType as KsSubscribeType, RetCode as KsRetCode, RET_OK as KS_RET_OK, RET_ERROR as KS_RET_ERROR, ErrorCode as KsErrorCode
from ks_trade_api.object import MyErrorData, ContractData, MyTickData, MyBookData, MyRawTickData
from ks_utility import datetimes
from decimal import Decimal
from dateutil.parser import parse
from ks_trade_api.base_market_api import BaseMarketApi
from typing import Optional
from logging import DEBUG, INFO, WARNING, ERROR


RET_KS2MY = {
    KS_RET_OK: RET_OK,
    KS_RET_ERROR: RET_ERROR
}

RET_MY2KS = { v:k for k,v in RET_KS2MY.items() }

MARKET_KS2MY = {
    KsExchange.SEHK: TrdMarket.HK,
    KsExchange.SMART: TrdMarket.US 
}

MARKET_MY2KS = { v:k for k,v in MARKET_KS2MY.items() }

def symbol_ks2my(vt_symbol: str):
    if not vt_symbol:
        return ''
    symbol, ks_exchange = extract_vt_symbol(vt_symbol)
    return f'{MARKET_KS2MY.get(ks_exchange)}.{symbol}'

SUBTYPE_KS2MY = {
    KsSubscribeType.USER_ORDER: KsSubscribeType.USER_ORDER,
    KsSubscribeType.USER_TRADE: KsSubscribeType.USER_TRADE,
    KsSubscribeType.USER_POSITION: KsSubscribeType.USER_POSITION,
    KsSubscribeType.TRADE: SubType.TICKER,
    KsSubscribeType.BOOK: SubType.ORDER_BOOK
}

def extract_my_symbol(my_symbol: str):
    my_exchange_str, symbol = my_symbol.split('.')
    return symbol, MARKET_MY2KS.get(my_exchange_str)


class KsFutuMarketApi(BaseMarketApi):
    gateway_name: str = 'KS_FUTU'

    def __init__(self, setting: dict):
        security_firm = setting.get('security_firm')
        gateway_name = setting.get('gateway_name', self.gateway_name)
        dd_secret = setting.get('dd_secret')
        dd_token = setting.get('dd_token')
        super().__init__(gateway_name=gateway_name, dd_secret=dd_secret, dd_token=dd_token)

        self.init_handlers(security_firm)


    # 初始化行回调和订单回调
    def init_handlers(self, security_firm):
        trade = self

        self.quote_ctx = quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        self.trd_ctx = trd_ctx = OpenSecTradeContext(host='127.0.0.1', port=11111, filter_trdmarket=TrdMarket.NONE, security_firm=security_firm)  # 创建交易对象

        # 盘口 callback
        class OrderBookHandler(OrderBookHandlerBase):
            def on_recv_rsp(self, rsp_pb):
                ret_code, data = super(OrderBookHandler,self).on_recv_rsp(rsp_pb)
                if ret_code != RET_OK:
                    trade.log({'msg': data}, level=ERROR, name='on_order_book')
                    return ret_code, data
                
                book: MyBookData = trade.book_my2ks(data)
                # symbol, exchange = extract_my_symbol(data['code'])
                # book: MyBookData = MyBookData(
                #     symbol=symbol,
                #     exchange=exchange,
                #     datetime=datetimes.now(),
                #     name=symbol,
                #     gateway_name=trade.gateway_name
                # )

                # for index, bid_item in enumerate(data['Bid']):
                #     i = index + 1
                    
                #     bid_price = Decimal(str(bid_item[0]))
                #     bid_volume = Decimal(str(bid_item[1]))
                    
                #     setattr(book, f'bid_price_{i}', bid_price)
                #     setattr(book, f'bid_volume_{i}', bid_volume)
                   
                #     if data['Ask']:
                #         ask_item = data['Ask'][index]
                #         ask_price = Decimal(str(ask_item[0]))
                #         ask_volume = Decimal(str(ask_item[1]))
                #         setattr(book, f'ask_price_{i}', ask_price)
                #         setattr(book, f'ask_volume_{i}', ask_volume)

                trade.on_book(book)
                return RET_OK, data
        handler = OrderBookHandler()
        quote_ctx.set_handler(handler)
        
        # 分笔 callback
        class TickerHandler(TickerHandlerBase):
            def on_recv_rsp(self, rsp_pb):
                ret_code, data_df = super(TickerHandler,self).on_recv_rsp(rsp_pb)
                if ret_code != RET_OK:
                    trade.log({'msg': data_df}, level=ERROR, name='on_tick')
                    return RET_ERROR, data_df
                
                if not len(data_df):
                    return ret_code, data_df
                
                data = data_df.to_dict('records')[0]
                # trade.log(data, name='on_ticker')
                
                symbol, exchange = extract_my_symbol(data['code'])
                dt: datetime = parse(data['time'])
                tick: MyRawTickData = MyRawTickData(
                    symbol=symbol,
                    exchange=exchange,
                    datetime=datetime.now(),
                    name=symbol,
                    volume=Decimal(str(data['volume'])),
                    turnover=Decimal(str(data['turnover'])),
                    last_price=Decimal(str(data['price'])),
                    gateway_name=trade.gateway_name
                )
                tick.last_volume = tick.volume
                trade.on_tick(tick)
                return RET_OK, data_df
        handler = TickerHandler()
        quote_ctx.set_handler(handler)

        

    # 订阅行情
    def subscribe(self, vt_symbols, vt_subtype_list, extended_time=True) -> tuple[KsRetCode, Optional[MyErrorData]]:
        if isinstance(vt_symbols, str):
            vt_symbols = [vt_symbols]

        my_symbols = [symbol_ks2my(x) for x in vt_symbols]
        my_subtype_list = [SUBTYPE_KS2MY.get(x) for x in vt_subtype_list]

        trade = self
        trd_ctx = self.trd_ctx
        if KsSubscribeType.USER_ORDER in my_subtype_list:
            my_subtype_list.remove(KsSubscribeType.USER_ORDER)     

        if KsSubscribeType.USER_TRADE in my_subtype_list:
            my_subtype_list.remove(KsSubscribeType.USER_TRADE)

        # futu没有持仓回调
        if KsSubscribeType.USER_POSITION in my_subtype_list:
            my_subtype_list.remove(KsSubscribeType.USER_POSITION)

        # 剩下的是订阅行情
        if my_subtype_list:
            ret, data = self.quote_ctx.subscribe(my_symbols, my_subtype_list, extended_time=extended_time)   # 订阅 K 线数据类型，FutuOpenD 开始持续收到服务器的推送
            if ret == RET_ERROR:
                error = self.get_error(vt_symbols, vt_subtype_list, extended_time, code=KsErrorCode.SUBSCRIPTION_ERROR, msg=data)
                self.send_dd(error.msg, f'订阅行情错误')
                return KS_RET_ERROR, error
            return KS_RET_OK, data

        return KS_RET_OK, None

              
    def get_error(self, *args, **kvargs):
        method = sys._getframe(1).f_code.co_name
        error = MyErrorData(
            code=kvargs.get('code'),
            msg=kvargs.get('msg'),
            method=method,
            args=args,
            kvargs=kvargs,
            traceback=traceback.format_exc(),
            gateway_name=self.gateway_name
        )
        self.log(error, tag=f'api_error.{method}', level=ERROR)
        return error

    # 获取静态信息
    def query_contract(self, vt_symbol: str) -> tuple[KsRetCode, ContractData]:
        symbol, exchange = extract_vt_symbol(vt_symbol)
        my_symbol = symbol_ks2my(vt_symbol)
        MARKET_KS2MY.get(exchange)
        ret, data = self.quote_ctx.get_stock_basicinfo(MARKET_KS2MY.get(exchange), code_list=[my_symbol])
        if ret == RET_ERROR:
            error = self.get_error(vt_symbol, data, msg=data)
            return KS_RET_ERROR, error
        
        contract_data = data.iloc[0]
        contract = ContractData(
            symbol=symbol,
            exchange=exchange,
            product=KsProduct.EQUITY,
            size=Decimal('1'),
            min_volume=Decimal(str(contract_data.lot_size)),
            pricetick=Decimal('0.01'), # todo! 低价股是0.001这里以后要处理
            name=contract_data.get('name'),
            gateway_name=self.gateway_name
        )
        return KS_RET_OK, contract
    
    def query_book(self, vt_symbol: str) -> tuple[KsRetCode,  MyBookData]:
        my_symbol = symbol_ks2my(vt_symbol)
        ret_sub, sub_data = self.quote_ctx.subscribe([my_symbol], [SubType.ORDER_BOOK], subscribe_push=False)
        # 先订阅买卖摆盘类型。订阅成功后 OpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
        ret_code = RET_ERROR
        ret_data = None
        if ret_sub == RET_OK:  # 订阅成功
            ret, data = self.quote_ctx.get_order_book(my_symbol, num=5)  # 获取一次 3 档实时摆盘数据
            if ret == RET_OK:
                ret_code = KS_RET_OK
                ret_data = self.book_my2ks(data)
            else:
                ret_data = ret_data
        else:
            ret_data = sub_data
        return ret_code, ret_data
    
    def book_my2ks(self, data) -> MyBookData:
        symbol, exchange = extract_my_symbol(data['code'])
        book: MyBookData = MyBookData(
            symbol=symbol,
            exchange=exchange,
            datetime=datetimes.now(),
            name=symbol,
            gateway_name=self.gateway_name
        )

        for index, bid_item in enumerate(data['Bid']):
            i = index + 1
            
            bid_price = Decimal(str(bid_item[0]))
            bid_volume = Decimal(str(bid_item[1]))
            
            setattr(book, f'bid_price_{i}', bid_price)
            setattr(book, f'bid_volume_{i}', bid_volume)
            
            if data['Ask']:
                ask_item = data['Ask'][index]
                ask_price = Decimal(str(ask_item[0]))
                ask_volume = Decimal(str(ask_item[1]))
                setattr(book, f'ask_price_{i}', ask_price)
                setattr(book, f'ask_volume_{i}', ask_volume)
        return book


    # 关闭上下文连接
    def close(self):
        self.quote_ctx.close()
        self.trd_ctx.close()


        