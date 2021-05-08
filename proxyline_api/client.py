import requests
import aiohttp
import asyncio
from . import exceptions

API_URL = "https://panel.proxyline.net/api"


class ProxyLine:
    available_ip_versions = [4, 6]
    available_proxy_types = ["dedicated", "shared", "for-sites"]
    available_countryes = [
        "ru", "us", "fr", "de", "ua", "ne", "cz", "uk", "sp", "be", "kz", "es", "sw", "sn", "br",
        "it", "oa", "ch", "po", "fi", "au", "jp", "in", "tu", "pt", "bl", "vi", "no", "az", "ar", "ge",
        "mo", "ba", "li", "la", "is", "gr", "sd", "qa", "ma", "ca", "ro", "ci", "pe"]
    available_periods = [5, 10, 20, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
    session = aiohttp.ClientSession()

    def __init__(self, api_key):
        self.api_key = api_key

    async def balance(self):
        path = "balance/"
        return await self.__requests(path)

    async def new_order(self, *args, **kwargs):
        path = "new-order/"
        params = self.__order_check_params(*args, **kwargs)
        response =  await self.__requests(path, params=params, method="POST")

        if "non_field_errors" in response:
            raise exceptions.NonFieldErrors(response["non_field_errors"])

        return response

    async def new_order_amount(self, *args, **kwargs):
        path = "new-order-amount/"
        params = self.__order_check_params(*args, **kwargs)
        return await self.__requests(path, params=params, method="POST")

    async def countries(self):
        path = 'countries/'
        return await self.__requests(path)

    async def orders(self, date_after, date_before):
        path = 'orders/'
        params = {
            'date_after': date_after,
            'date_before': date_before
        }
        return await self.__requests(path, params=params)

    async def ips_count(self, proxy_type, ip_version, country):
        self.__check_proxy_type_ip_version_available_countryes(proxy_type, ip_version, country)
        path = "ips_count/"
        params = {
            "type": proxy_type,
            "ip_version": ip_version,
            "country": country,
        }
        return await self.__requests(path, params=params)

    async def ips(self, proxy_type, ip_version, country):
        self.__check_proxy_type_ip_version_available_countryes(proxy_type, ip_version, country)

        path = "ips/"
        params = {
            "type": proxy_type,
            "ip_version": ip_version,
            "country": country,
        }
        return await self.__requests(path, params=params)

    async def proxies(self, status=None, proxy_type=None, ip_version=None, country=None, date_after=None, date_before=None,
                date_end_after=None, date_end_before=None, orders=None, format=None, limit=200, offset=None):
        path = "proxies/"
        params = {
            "status": status,
            "proxy_type":  proxy_type,
            "ip_version": ip_version,
            "country": country,
            "date_after": date_after,
            "date_before": date_before,
            "date_end_after": date_end_after,
            "date_end_before": date_end_before,
            "orders": orders,
            "format": format,
            "limit": limit,
            offset: offset,
        }
        return await self.__requests(path, params=params)

    async def renew(self, proxy_id):
        path = "renew/"

        params = {
            "proxy_id": proxy_id,
            "period": 30
        }
        return await self.__requests(path, params=params)


    def __order_check_params(self, proxy_type, ip_version, country, quantity, period, coupon=None, new_ips=None):
        self.__check_proxy_type_ip_version_available_countryes(proxy_type, ip_version, country)

        params = {
            "type": proxy_type,
            "ip_version": ip_version,
            "country": country,
            "quantity": quantity,
            "period": period,
            "coupon": coupon,
            "new_ips": new_ips,
        }
        return params

    def __check_proxy_type_ip_version_available_countryes(self, proxy_type, ip_version, country):
        if proxy_type not in self.available_proxy_types:
            text = "Invalid {} proxy type. Available proxy types".format(self.available_proxy_types)
            raise exceptions.InvalidProxyType(text)

        if int(ip_version) not in self.available_ip_versions:
            text = "Invalid {} ip version. Available ip versions".format(self.available_ip_versions)
            raiseexceptions.InvalidIpVersion(text)

        if country not in self.available_countryes:
            raise exceptions.invalidCountry("Invalid {} country. Available countryes".format(self.available_countryes))

    async def __requests(self, path, params=None, method="GET"):
        headers = {
            "API-KEY": self.api_key,
        }
        url = "{}/{}".format(API_URL, path)
        async with self.session.get(url, params=params, data=params, headers=headers) if method == 'GET' else self.session.post(url, params=params, data=params, headers=headers) as response:
            #response = requests.request(method, url, params=params, data=params, headers=headers).json()
            result = await response.json()
            if "detail" in result and "incorrect api key" == result["detail"]:
                raise exceptions.InvalidApiKey()
            return result
