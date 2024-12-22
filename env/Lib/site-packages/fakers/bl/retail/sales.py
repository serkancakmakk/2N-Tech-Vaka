import uuid
from faker import Faker
import datetime
from dataclasses import dataclass, asdict
import pandas as pd
from pyspark.sql import SparkSession
from fakers.bl.retail.product import FakeProduct


@dataclass
class FakeSaleDto:
    sales_id: str
    sale_date: datetime.datetime
    product: 'FakeProduct'
    quantity: int
    total_price: float

    def dict(self):
        # Return a dictionary representation of the object and its nested dataclasses
        return asdict(self)


class FakeSales:
    # A class container that holds multiple FakeOrderDto instances
    def __init__(self, count: int, locale: str = 'en_US'):
        # Initialize the container with the count and the locale
        self.count = count
        self.locale = locale
        self.fake_sales = []

        fake = Faker(locale)  # Create a Faker instance with the given locale
        for _ in range(count):
            # Create a fake product DTO for each count and append it to the list
            sale_dto = FakeSaleDto(
                sales_id=str(uuid.uuid4()),
                sale_date=fake.date_time_between(start_date='-2y'),
                product=FakeProduct(locale=locale).retrieve(),
                quantity=fake.random_int(min=1, max=10),
                total_price=fake.random_number(digits=2)
            )
            self.fake_sales.append(sale_dto)

    def __len__(self):
        # Return the number of addresses in the container
        return len(self.fake_sales)

    def __getitem__(self, index):
        # Return the address at the given index
        return self.fake_sales[index]

    def __repr__(self):
        # Return a string representation of the container
        return f"FakeProducts({self.count}, {self.locale})"

    def dict(self):
        fake_sales = []
        for user in self.fake_sales:
            fake_sales.append(user.dict())
        return fake_sales

    def to_pandas(self):
        fake_sales = self.dict()
        return pd.DataFrame(fake_sales)

    def to_spark(self, spark: SparkSession):
        fake_sales = self.dict()
        return spark.createDataFrame(fake_sales)


class FakeSale:
    def __init__(self, locale='en_US'):
        self.__fake_sale = FakeSales(1, locale=locale)

    def retrieve(self):
        return self.__fake_sale[0]

    def dict(self):
        return self.__fake_sale[0].dict()
