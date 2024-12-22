import uuid
from faker import Faker
from dataclasses import dataclass, asdict
import pandas as pd
from pyspark.sql import SparkSession


@dataclass
class FakeProductDto:
    product_id: str
    product_name: str
    price: float
    description: str

    def dict(self):
        # Return a dictionary representation of the object and its nested dataclasses
        return asdict(self)


class FakeProducts:
    # A class container that holds multiple FakeAddressDto instances
    def __init__(self, count: int, locale: str = 'en_US'):
        # Initialize the container with the count and the locale
        self.count = count
        self.locale = locale
        self.fake_products = []

        fake = Faker(locale)  # Create a Faker instance with the given locale
        for _ in range(count):
            # Create a fake product DTO for each count and append it to the list
            product_dto = FakeProductDto(
                product_id=str(uuid.uuid4()),
                product_name=fake.word(),
                price=fake.random_number(digits=2),
                description=fake.text()
            )
            self.fake_products.append(product_dto)

    def __len__(self):
        # Return the number of addresses in the container
        return len(self.fake_products)

    def __getitem__(self, index):
        # Return the address at the given index
        return self.fake_products[index]

    def __repr__(self):
        # Return a string representation of the container
        return f"FakeProducts({self.count}, {self.locale})"

    def dict(self):
        fake_products = []
        for product in self.fake_products:
            fake_products.append(product.dict())
        return fake_products

    def to_pandas(self):
        fake_products = self.dict()
        return pd.DataFrame(fake_products)

    def to_spark(self, spark: SparkSession):
        fake_products = self.dict()
        return spark.createDataFrame(fake_products)


class FakeProduct:
    def __init__(self, locale='en_US'):
        self.__fake_product = FakeProducts(1, locale=locale)

    def retrieve(self):
        return self.__fake_product[0]

    def dict(self):
        return self.__fake_product[0].dict()
