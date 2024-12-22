from dataclasses import dataclass
from faker import Faker
import pandas as pd
from pyspark.sql import SparkSession


@dataclass
class FakeAddressDto:
    building_number: str
    city: str
    country: str
    country_code: str
    postcode: str
    street_address: str

    @property
    def full_address(self):
        return f"{self.street_address}, #{self.building_number}  \n{self.city} {self.postcode}, {self.country}"


class FakeAddresses:
    # A class container that holds multiple FakeAddressDto instances
    def __init__(self, count: int, locale: str):
        # Initialize the container with the count and the locale
        self.count = count
        self.locale = locale
        self.addresses = []
        fake = Faker(locale)  # Create a Faker instance with the given locale
        for _ in range(count):
            # Create a fake address DTO for each count and append it to the list
            address_dto = FakeAddressDto(
                building_number=fake.building_number(),
                city=fake.city(),
                country=fake.current_country(),
                country_code=fake.current_country_code(),
                postcode=fake.postcode(),
                street_address=fake.street_address()
            )
            self.addresses.append(address_dto)

    def __len__(self):
        # Return the number of addresses in the container
        return len(self.addresses)

    def __getitem__(self, index):
        # Return the address at the given index
        return self.addresses[index]

    def __repr__(self):
        # Return a string representation of the container
        return f"FakeAddresses({self.count}, {self.locale})"

    def dict(self):
        fake_addresses = []
        for address in self.addresses:
            fake_addresses.append(address.__dict__)
        return fake_addresses

    def to_pandas(self):
        fake_addresses = self.dict()
        return pd.DataFrame(fake_addresses)

    def to_spark(self, spark: SparkSession):
        fake_addresses = self.dict()
        return spark.createDataFrame(fake_addresses)


class FakeAddress:
    def __init__(self, locale='en_US'):
        self.__fake_addresses = FakeAddresses(1, locale=locale)

    def retrieve(self):
        return self.__fake_addresses[0]

    def dict(self):
        return self.__fake_addresses[0].__dict__
