import uuid
from faker import Faker
import datetime
from dataclasses import dataclass, asdict
import pandas as pd
from pyspark.sql import SparkSession
from fakers.bl.retail.user import FakeUser
from fakers.bl.retail.product import FakeProduct


@dataclass
class FakeOrderDto:
    order_id: str
    order_date: datetime.datetime
    user: 'FakeUser'
    product: 'FakeProduct'
    quantity: int

    def dict(self):
        # Return a dictionary representation of the object and its nested dataclasses
        return asdict(self)


class FakeOrders:
    # A class container that holds multiple FakeOrderDto instances
    def __init__(self, count: int, locale: str = 'en_US'):
        # Initialize the container with the count and the locale
        self.count = count
        self.locale = locale
        self.fake_orders = []

        fake = Faker(locale)  # Create a Faker instance with the given locale
        for _ in range(count):
            # Create a fake product DTO for each count and append it to the list
            order_dto = FakeOrderDto(
                order_id=str(uuid.uuid4()),
                order_date=fake.date_time_between(start_date='-2y'),
                user=FakeUser(locale=locale).retrieve(),
                product=FakeProduct(locale=locale).retrieve(),
                quantity=fake.random_int(min=1, max=10)
            )
            self.fake_orders.append(order_dto)

    def __len__(self):
        # Return the number of addresses in the container
        return len(self.fake_orders)

    def __getitem__(self, index):
        # Return the address at the given index
        return self.fake_orders[index]

    def __repr__(self):
        # Return a string representation of the container
        return f"FakeProducts({self.count}, {self.locale})"

    def dict(self):
        fake_orders = []
        for user in self.fake_orders:
            fake_orders.append(user.dict())
        return fake_orders

    def to_pandas(self):
        fake_orders = self.dict()
        return pd.DataFrame(fake_orders)

    def to_spark(self, spark: SparkSession):
        fake_orders = self.dict()
        return spark.createDataFrame(fake_orders)


class FakeOrder:
    def __init__(self, locale='en_US'):
        self.__fake_order = FakeOrders(1, locale=locale)

    def retrieve(self):
        return self.__fake_order[0]

    def dict(self):
        return self.__fake_order[0].dict()
