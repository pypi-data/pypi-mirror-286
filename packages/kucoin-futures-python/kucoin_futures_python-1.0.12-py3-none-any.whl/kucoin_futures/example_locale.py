import time

from kucoin_futures.client import Trade


def test_Lending():
    client1 = Trade(key='668aac1303b7f800017a7c33', secret='bcb25e2a-77db-4e39-85a2-4369f78edc9c', passphrase='abc,123*')
    #client2.TCP_NODELAY=1
    res=client1.get_max_withdraw_margin(symbol='XBTUSDTM')
    print(f'1-{res}')
    res=client1.remove_margin_manually(symbol='XBTUSDTM',withdrawAmount=1)
    print(f'2-{res}')
    res=client1.trading_pair_actual_fee_futures(symbol='XBTUSDTM')
    print(f'3-{res}')
    res=client1.get_positions_history(symbol='XBTUSDTM')
    print(f'4-{res}')
