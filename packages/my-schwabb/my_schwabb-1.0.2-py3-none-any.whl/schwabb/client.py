# Standard library imports
from asyncio import gather
from os import environ
from datetime import datetime, date, timedelta
from functools import cached_property, wraps

# Third-party imports
from asynchronizer import Asynchronizer
import requests
import aiohttp

# Relative imports
from .enums import TransactionType
from .models import Accounts, Orders, Order, Positions, QuoteData, Transactions, UserPreferences
from ._token import Token
from .urls import urls
from .utils import ratelimit

SEVEN_DAYS = 604800

def validate_response(func):
    @wraps(func)
    def request(self, *args, **kwargs):
        try:
            response = func(self, *args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            print(f"Request timed out: {e}, retrying...")
            return request(self, *args, **kwargs)

        if not str(response.status_code).startswith('2'):
            print(f"Request failed: {response.text}")
            raise Exception(f"Request failed.")
        return response
    return request

async def validate_async_response(response):
    if not str(response.status).startswith('2'):
        raise Exception(f"Request failed: {await response.text()}")
    return await response.json()

def get_account_number(func):
    @wraps(func)
    def request(self, account_number=None, *args, **kwargs):
        account_number = account_number or self.primary_account
        return func(self, account_number=account_number, *args, **kwargs)
    return request


class BaseClient:
    urls = urls

    @ratelimit(120, 60)
    def _request(self, method, url, *args, **kwargs):
        method = method.upper()
        if method not in {'GET', 'POST', 'PUT', 'DELETE'}:
            raise ValueError(f"Invalid method '{method}'. Method must be one of {'GET', 'POST', 'PUT', 'DELETE'}")
        return self.session.request(method=method, url=url, *args, **kwargs)

    async def _async_request(self, session, method, url, *args, **kwargs):
        method = method.upper()
        if method not in {'GET', 'POST', 'PUT', 'DELETE'}:
            raise ValueError(f"Invalid method '{method}'. Method muse be one of {'GET', 'POST', 'PUT', 'DELETE'}")
        async with session.request(method=method, url=url, *args, **kwargs) as response:
            return await validate_async_response(response)

    @validate_response
    def _get_request(self, url, params=None, headers=None, **kwargs):
        headers = headers or self.token.headers
        return self._request(method='GET', url=url, params=params, headers=headers)

    @validate_response
    def _post_request(self, url, data, headers=None, **kwargs):
        headers = headers or self.token.headers
        return self._request(method='POST', url=url, json=data, headers=headers)

    @validate_response
    def _put_request(self, url, data, headers=None, **kwargs):
        headers = headers or self.token.headers
        return self._request(method='PUT', url=url, json=data, headers=headers)

    @validate_response
    def _delete_request(self, url, headers=None, **kwargs):
        headers = headers or self.token.headers
        return self._request(method='DELETE', url=url, headers=headers)

    async def _async_get_request(self, session, url, params=None, headers=None, **kwargs):
        headers = headers or self.token.headers
        return await self._async_request(session=session, method='GET', url=url, params=params, headers=headers)

    async def _async_post_request(self, session, url, data, headers=None, **kwargs):
        headers = headers or self.token.headers
        return await self._async_request(session=session, method='POST', url=url, json=data, headers=headers)

    async def _async_put_request(self, session, url, data, headers=None, **kwargs):
        headers = headers or self.token.headers
        return await self._async_request(session=session, method='PUT', url=url, json=data, headers=headers)

    async def _async_delete_request(self, session, url, headers=None, **kwargs):
        headers = headers or self.token.headers
        return await self._async_request(session=session, method='DELETE', url=url, headers=headers)

class Client(BaseClient):
    urls = urls

    def __init__(self, primary_account=None, provider='redis', encrypt=False, app_key=None, secret=None, fetch=False, asyncio=False, **kwargs):
        self.asyncio = asyncio
        self.app_key = app_key or environ.get("SCHWABB_APP_KEY")
        if self.app_key is None:
            self.app_key = input('Enter your Schwabb API app key: ')

        self.secret = secret or environ.get("SCHWABB_SECRET")
        if self.secret is None:
            self.secret = input('Enter your API secret: ')


        if asyncio:
            from asynchronizer import Asynchronizer
            self.executor = Asynchronizer()

        self.session = requests.Session()

        self.token = Token(
            provider=provider,
            encrypt=encrypt,
            session=self.session,
            app_key=self.app_key,
            secret=self.secret,
            **kwargs
        )

        if fetch:
            # Setup account information
            self.accounts = Accounts(self._accounts(account_numbers=True))

            if primary_account is not None:
                primary_account = int(primary_account)
                self.accounts.set_primary(primary_account)

                for account in self.accounts:
                    if account.number == primary_account:
                        self.primary_account = account
                        break
            else:
                self.primary_account = self.accounts[0]
                print(f"\033[91m[Warning]\033[0m: Primary account not specified. Using {self.primary_account.number} as primary")
                print(f"           Methods not given an exclusive account_number as a parameter will default to primary account number: {self.primary_account.number}")
                print('           You\'ve been warned.')

            # Retrieve current positions
            self.positions = self._positions(self.primary_account)
        else:
            self.accounts = Accounts([])
            self.positions = Positions([])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_traceback:
            import traceback
            traceback.print_exc()
        return

    ##########################################################################
    # Websocket
    ##########################################################################

    @cached_property
    def user_preferences(self):
        preferences = self._get_request(self.urls.user_preference_url).json()
        preferences = preferences['streamerInfo'][0]
        return UserPreferences(
            ws_url=preferences['streamerSocketUrl'],
            client_customer_id=preferences['schwabClientCustomerId'],
            client_correl_id=preferences['schwabClientCorrelId'],
            client_channel=preferences['schwabClientChannel'],
            client_function_id=preferences['schwabClientFunctionId'],
        )

    def get_user_preferences(self):
        return self.user_preferences

    ##########################################################################
    # Accounts
    ##########################################################################

    def _accounts(self, account_number=None, account_numbers=False, positions=True, **kwargs):
        params = None
        if not account_numbers and account_number is None:
            url = urls.accounts_url
        elif account_number is not None:
            url = f"{urls.accounts_url}/{account_number}"
            params = {'fields': 'positions' if positions else ''}
        else:
            url = f"{urls.accounts_url}/accountNumbers"
        response = self._get_request(url=url, params=params)
        return response.json()

    def account_numbers(self, **kwargs):
        return self._accounts(account_numbers=True, **kwargs)

    @get_account_number
    def account(self, account_number=None, **kwargs) -> Accounts:
        return self._accounts(account_number=account_number)

    def get_accounts(self, account_number=None, account_numbers=False, **kwargs) -> Accounts:
        return self._accounts(account_number=account_number, account_numbers=account_numbers, **kwargs)

    ##########################################################################
    # Positions
    ##########################################################################

    @get_account_number
    def _positions(self, account_number=None, **kwargs) -> Positions:
        return Positions(self._accounts(account_number=account_number)['securitiesAccount']['positions'])

    @get_account_number
    def get_positions(self, account_number=None, **kwargs) -> Positions:
        return self._positions(account_number=account_number, **kwargs)

    ##########################################################################
    # Transactions
    ##########################################################################

    @get_account_number
    def transactions(
        self,
        account_number = None,
        symbol=None,
        from_date: datetime = None,
        to_date: datetime = None,
        types='trade',
        **kwargs) -> Transactions:

        if from_date is not None:
            from_date = from_date.isoformat() + 'Z'
        else:
            from_date = (datetime.now() - timedelta(days=14)).isoformat() + 'Z'
        if to_date is not None:
            to_date = to_date.isoformat() + 'Z'
        else:
            to_date = datetime.now().isoformat() + 'Z'

        params = dict(
            startDate=from_date,
            endDate=to_date,
            symbol=symbol,
            types=TransactionType(types.lower()).name,
        )

        if params['symbol'] is None:
            params.pop('symbol')

        transactions = self._get_request(urls.transactions_url(account_number), params=params).json()
        return Transactions(transactions)

    def get_transactions(self, *args, **kwargs) -> Transactions:
        return self.transactions(*args, **kwargs)

    def get_transaction(self):
        pass

    ##########################################################################
    # Orders
    ##########################################################################

    def orders(
        self,
        account_number = None,
        from_date: datetime = None,
        to_date: datetime = None,
        **kwargs) -> Orders:

        if from_date is not None:
            from_date = from_date.isoformat() + 'Z'
        else:
            from_date = (datetime.now() - timedelta(days=14)).isoformat() + 'Z'
        if to_date is not None:
            to_date = to_date.isoformat() + 'Z'
        else:
            to_date = datetime.now().isoformat() + 'Z'

        url = urls.all_orders_url if account_number is None else urls.orders_url(account_number)
        params = dict(
            fromEnteredTime=from_date,
            toEnteredTime=to_date
        )
        orders = self._get_request(url, params=params).json()
        return Orders(orders)

    def get_orders(self, *args, **kwargs) -> Orders:
        return self.orders(*args, **kwargs)

    @get_account_number
    def place_order(self, account_number=None, **kwargs):
        data = Order.build(**kwargs)
        return self._post_request(urls.orders_url(account_number), data)

    @get_account_number
    def place_orders(self, account_number=None, orders=None):
        orders = orders or []
        if self.asyncio:
            from aiohttp import ClientSession

            async def send(session, order):
                order = Order.build(**order)
                return await self._async_post_request(session=session, url=urls.orders_url(account_number), data=order)
            async def send_all():
                async with ClientSession() as session:
                    return await gather(*(send(session, order) for order in orders))
            return self.executor.run(send_all())
        else:
            return [self.place_order(**order) for order in orders]

    @get_account_number
    def preview_order(self, account_number=None, **kwargs):
        data = Order.build(**kwargs)
        return self._post_request(urls.preview_order_url(account_number), data)

    @get_account_number
    def preview_orders(self, account_number=None, *, orders, **kwargs):
        orders = orders or []
        if self.asyncio:
            from aiohttp import ClientSession

            async def send(session, order):
                order = Order.build(**order)
                return await self._async_post_request(session=session, url=urls.preview_order_url(account_number), data=order)
            async def send_all():
                async with ClientSession() as session:
                    return await gather(*(send(session, order) for order in orders))
            return self.executor.run(send_all())
        else:
            return [self.preview_order(**order) for order in orders]

    def place_market_order(self, symbol, account_number=None, *, qty, side, **kwargs):
        kwargs.pop('order_type', None)
        account_number = account_number or self.primary_account
        return self.place_order(symbol=symbol, account_number=account_number, qty=qty, side=side, order_type='market', **kwargs)

    def place_limit_order(self, symbol, account_number=None, *, qty, side, **kwargs):
        kwargs.pop('order_type', None)
        return self.place_order(symbol=symbol, account_number=account_number, qty=qty, side=side, order_type='limit', **kwargs)

    @get_account_number
    def cancel_order(self, account_number=None, order_id=None):
        url = f"{url.orders_url(account_number)}/{order_id}"
        return self._delete_request(url)

    @get_account_number
    def replace_order(self, account_number=None, order_id=None, order=None, **kwargs):
        url = f"{urls.orders_url(account_number)}/{order_id}"
        if order is None:
            order = Order.build(**kwargs)
        return self._put_request(url)

    ##########################################################################
    # Market Data
    ##########################################################################

    def quote(self, symbol, fields=('quote', 'reference'), all=False, **kwargs):
        if all:
            fields = ('quote', 'fundamental', 'extended', 'reference', 'regular')
        params = {'fields': ','.join(fields)}
        quote = self._get_request(urls.quote_url(symbol), params=params).json()
        quote = quote[symbol]
        return QuoteData.new(symbol, quote, fields)

    def quotes(self, symbols, fields=('quote', 'reference'), all=False, **kwargs):
        if all:
            fields = ('quote', 'fundamental', 'extended', 'reference', 'regular')
        params = {'fields': ','.join(fields)}

        quotes = self._get_request(urls.quotes_url(symbols), params=params).json()
        if (errors := quotes.pop('errors', None)) is not None:
            print(f"Error fetching quotes: {errors}")
        return {symbol: QuoteData.new(symbol, quote, fields) for symbol, quote in quotes.items()}

    def get_quote(self, *args, **kwargs):
        return self.quote(*args, **kwargs)

    def get_quotes(self, *args, **kwargs):
        return self.quotes(*args, **kwargs)