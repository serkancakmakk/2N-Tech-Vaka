from faker import Faker
from dataclasses import dataclass, asdict
from fakers.bl.address import FakeAddress
import pandas as pd
import uuid
from pyspark.sql import SparkSession


@dataclass
class FakePersonDto:
    person_id: str
    first_name: str
    last_name: str
    address: 'FakeAddress'
    phone_number: str

    def dict(self):
        # Return a dictionary representation of the object and its nested dataclasses
        return asdict(self)


class FakePersons:
    # A class container that holds multiple FakeOrderDto instances
    def __init__(self, count: int, locale: str = 'en_US'):
        # Initialize the container with the count and the locale
        self.count = count
        self.locale = locale
        self.fake_persons = []

        fake = Faker(locale)  # Create a Faker instance with the given locale
        for _ in range(count):
            # Create a fake product DTO for each count and append it to the list
            fake_person_dto = FakePersonDto(
                person_id=str(uuid.uuid4()),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                address=FakeAddress(locale).retrieve(),
                phone_number=fake.phone_number()
            )
            self.fake_persons.append(fake_person_dto)

    def __len__(self):
        # Return the number of addresses in the container
        return len(self.fake_persons)

    def __getitem__(self, index):
        # Return the address at the given index
        return self.fake_persons[index]

    def __repr__(self):
        # Return a string representation of the container
        return f"FakePersons({self.count}, {self.locale})"

    def dict(self):
        fake_persons = []
        for user in self.fake_persons:
            fake_persons.append(user.dict())
        return fake_persons

    def to_pandas(self):
        fake_persons = self.dict()
        return pd.DataFrame(fake_persons)

    def to_spark(self, spark: SparkSession):
        fake_persons = self.dict()
        return spark.createDataFrame(fake_persons)


class FakePerson:
    def __init__(self, locale='en_US'):
        self.__fake_person = FakePersons(1, locale=locale)

    def retrieve(self):
        return self.__fake_person[0]

    def dict(self):
        return self.__fake_person[0].dict()
