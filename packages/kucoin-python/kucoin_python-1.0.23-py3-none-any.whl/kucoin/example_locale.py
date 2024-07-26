import time

from kucoin.client import Margin, Trade, Lending, Earn, Market


def test_Trade():

    trade = Trade(key='', secret='', passphrase='')
    #res=client.get_interest_rates("BTC")
    res =trade.create_market_order(symbol='FRM-USDT',side='buy',clientOid=f'clientid-{time.time()*1000}',size=5)
    print(res)

def test_Lending():
    lending = Lending(key='668aac1303b7f800017a7c33', secret='bcb25e2a-77db-4e39-85a2-4369f78edc9c', passphrase='abc,123*')
    #client2.TCP_NODELAY=1
    s=time.time_ns()
    ns=5
    for n in range(ns):
      res= lending.get_currency_information(currency='BTC')
      #print(n)
    e1=time.time_ns()-s
    print(e1)

    trade = Trade(key='668aac1303b7f800017a7c33', secret='bcb25e2a-77db-4e39-85a2-4369f78edc9c', passphrase='abc,123*')
    #client2.TCP_NODELAY=1
    s=time.time_ns()
    for n in range(ns):
        res= trade.get_recent_orders()
        #print(n)
    e1=time.time_ns()-s
    print(e1)



def test_Margin():
    client1 = Margin(key='668aac1303b7f800017a7c33', secret='bcb25e2a-77db-4e39-85a2-4369f78edc9c', passphrase='abc,123*')

    res= client1.get_active_hf_order_symbols(tradeType='MARGIN_TRADE')
    print(res)
    res= client1.get_cross_margin_trading_pairs_configuration()
    print(res)
    res= client1.get_cross_margin_trading_pairs_configuration(symbol='BTC-USDT')
    print(res)

    res= client1.modify_leverage_multiplier(leverage=2)
    print(res)

    #res= client1.get_information_onoff_exchange_funding_and_loans()
    print(res)

    #res= client1.get_information_on_accounts_involved_in_off_exchange_loans()
    print(res)

    #res= client1.cancel_hf_order_by_orderid(orderId='xxx',symbol='BTC-USDT')
    print(res)

    #res= client1.cancel_hf_order_by_clientoid(clientOid='xxx',symbol='BTC-USDT')
    print(res)

    res= client1.get_hf_order_details_by_orderid(orderId='xxxxxxxxxxxxxxxxxxxxxxxx',symbol='BTC-USDT')
    print(f'1-{res}')

    client2 = Market(key='668aac1303b7f800017a7c33', secret='bcb25e2a-77db-4e39-85a2-4369f78edc9c', passphrase='abc,123*')
    res=client2.get_currency_detail_v3(currency='BTC',chain='ERC20')
    print(f'2-{res}')







def test_Earn():
    #earn = Earn(key='668aac1303b7f800017a7c33', secret='bcb25e2a-77db-4e39-85a2-4369f78edc9c', passphrase='abc,123*')
    earn = Earn(key='668ab8122d2e920001dc579c', secret='77bdf571-993a-4e6d-9a64-49ea6f243a51', passphrase='1234567',url='https://openapi-v2.sit.kucoin.net')

    # res= earn.get_earn_eth_staking_products()
    # print(res)
    # res= earn.get_earn_savings_products()
    # print(res)
    # res= earn.get_earn_fixed_income_current_holdings(currency='USDT')
    # print(res)
    # res= earn.get_earn_kcs_staking_products(currency='KCS')
    # print(res)

    # res= earn.get_earn_limited_time_promotion_products(currency='ADA')
    # print(res)
    res= earn.get_earn_staking_products()
    print(res)

    # res= earn.subscribe_to_earn_fixed_income_products(productId='994',amount='10',accountType='MAIN')
    # print(res)



