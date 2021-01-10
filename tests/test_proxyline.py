import random
import proxyline_api


def test_balance(api_key):
    assert isinstance(proxyline_api.ProxyLine(api_key).balance()["balance"], int)


def test_ips(api_key):
    proxy_type = random.choice(proxyline_api.ProxyLine.available_proxy_types)
    ip_version = random.choice(proxyline_api.ProxyLine.available_ip_versions)
    country = random.choice(proxyline_api.ProxyLine.available_countryes)

    assert isinstance(proxyline_api.ProxyLine(api_key).ips(proxy_type, ip_version, country), list)


def test_new_order_amount(api_key):
    proxy_type = random.choice(proxyline_api.ProxyLine.available_proxy_types)
    ip_version = random.choice(proxyline_api.ProxyLine.available_ip_versions)
    country = random.choice(proxyline_api.ProxyLine.available_countryes)
    period = random.choice(proxyline_api.ProxyLine.available_periods)

    response = proxyline_api.ProxyLine(api_key).new_order_amount(proxy_type, ip_version, country, 1, period)
    assert isinstance(response, dict)


def test_new_order(api_key):
    """
    Чтоб случайно не совершить заказ
    """
    proxyline = proxyline_api.ProxyLine(api_key)

    balance = proxyline.balance()["balance"]
    need_amount_proxies = 1

    _sum = proxyline.new_order_amount("dedicated", 4, "ru", need_amount_proxies, 90)["amount"]
    if _sum <= balance:
        need_amount_proxies = round(balance / _sum) + 1

    try:
        proxyline.new_order("dedicated", 4, "ru", need_amount_proxies, 90)["non_field_errors"][0]
    except proxyline_api.exceptions.NonFieldErrors as e:
        assert "Not enough money on balance" == e.args[0][0]
