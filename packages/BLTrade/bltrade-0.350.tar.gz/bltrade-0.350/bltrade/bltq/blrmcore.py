

# 一键平仓
# 以超价一键平仓
def blEmpty(api:any):
    position = api.get_position()
    #print("----------------position---------------")
    #print(position)

    print("----------------1 检测当前仓位信息------------------------------------------------------")
    for n,p in position.items():
        #print("name=",n,"p=",p)
        print("品种:",n,"浮盈：",p.float_profit_long + p.float_profit_short,"   多仓:",p.pos_long,"空仓:",p.pos_short)
        quote = api.get_quote(n)
        #print(quote)
        print("合约代码：",quote.instrument_id,"卖1:",quote.ask_price1,"买1:",quote.bid_price1)
        
        print("开始平仓：",quote.instrument_id,"------------------------------------------------")

        if p.pos_long>0:
            print("需要平仓多仓",p.pos_long,"手")
            order = api.insert_order(symbol=quote.instrument_id, direction="SELL", offset="CLOSETODAY", limit_price=quote.bid_price1-2*quote.price_tick,
                volume=p.pos_long)

            while order.status != "FINISHED":
                api.wait_update()
                print("合约代码：",quote.instrument_id,"已平仓")


        if p.pos_short>0:
            print("需要平仓空仓",p.pos_short,"手")
            order = api.insert_order(symbol=quote.instrument_id, direction="BUY", offset="CLOSETODAY", limit_price=quote.ask_price1+2*quote.price_tick,
                volume=p.pos_short)

            while order.status != "FINISHED":
                api.wait_update()
                print("合约代码：",quote.instrument_id,"已平仓")

# 一键撤销
# 撤销所有status为"ALIVE"的单
def blQuash(api:any):
    orders=api.get_order()
    #print(orders)
    for i,o in orders.items():
        #print("i=",i,"o=",o)
        if o['status']=="ALIVE":
            api.cancel_order(o)