from fakers.providers import ClientLogger
from fakers.bl.retail.user import FakeUser, FakeUsers
from fakers.bl.retail.order import FakeOrder, FakeOrders
from fakers.bl.retail.product import FakeProduct, FakeProducts
from fakers.bl.retail.sales import FakeSale, FakeSales


class Retail:
    @staticmethod
    def fake_user(locale='en_US'):
        ClientLogger.locale_validator(locale)
        fake_user = FakeUser(locale)
        return fake_user.retrieve()

    @staticmethod
    def fake_users(user_count=5, locale='en_US'):
        ClientLogger.locale_validator(locale)
        fake_users = FakeUsers(user_count, locale)
        return fake_users

    @staticmethod
    def fake_product(locale='en_US'):
        ClientLogger.locale_validator(locale)
        fake_product = FakeProduct(locale)
        return fake_product.retrieve()

    @staticmethod
    def fake_products(user_count=5, locale='en_US'):
        ClientLogger.locale_validator(locale)
        fake_products = FakeProducts(user_count, locale)
        return fake_products

    @staticmethod
    def fake_order(locale='en_US'):
        ClientLogger.locale_validator(locale)
        fake_order = FakeOrder(locale)
        return fake_order.retrieve()

    @staticmethod
    def fake_orders(user_count=5, locale='en_US'):
        ClientLogger.locale_validator(locale)
        fake_orders = FakeOrders(user_count, locale)
        return fake_orders

    @staticmethod
    def fake_sale(locale='en_US'):
        ClientLogger.locale_validator(locale)
        fake_sale = FakeSale(locale)
        return fake_sale.retrieve()

    @staticmethod
    def fake_sales(user_count=5, locale='en_US'):
        ClientLogger.locale_validator(locale)
        fake_sales = FakeSales(user_count, locale)
        return fake_sales
