import uuid
from fakers.utils import CommonFunction
from faker import Faker
from dataclasses import dataclass, asdict
import pandas as pd
from pyspark.sql import SparkSession


@dataclass
class FakeUserDto:
    user_id: str
    user_name: str
    first_name: str
    last_name: str
    email: str
    full_name: str
    password: str

    def dict(self):
        # Return a dictionary representation of the object and its nested dataclasses
        return asdict(self)


class FakeUsers:
    # A class container that holds multiple FakeAddressDto instances
    def __init__(self, count: int, locale: str = 'en_US'):
        # Initialize the container with the count and the locale
        self.count = count
        self.locale = locale
        self.users = []
        fake = Faker(locale)  # Create a Faker instance with the given locale
        for _ in range(count):
            fake_full_name = fake.name()

            fake_full_name_split = fake_full_name.split()
            fake_email = CommonFunction.generate_custom_email(fake_full_name)

            # Create a fake address DTO for each count and append it to the list
            user_dto = FakeUserDto(
                user_id=str(uuid.uuid4()),
                full_name=fake_full_name,
                first_name=" ".join(fake_full_name_split[:-1]),
                last_name=fake_full_name_split[-1],
                email=fake_email,
                user_name=fake_email.split('@')[0],
                password=fake.password()
            )
            self.users.append(user_dto)

    def __len__(self):
        # Return the number of addresses in the container
        return len(self.users)

    def __getitem__(self, index):
        # Return the address at the given index
        return self.users[index]

    def __repr__(self):
        # Return a string representation of the container
        return f"FakeUsers({self.count}, {self.locale})"

    def dict(self):
        fake_users = []
        for user in self.users:
            fake_users.append(user.dict())
        return fake_users

    def to_pandas(self):
        fake_users = self.dict()
        return pd.DataFrame(fake_users)

    def to_spark(self, spark: SparkSession):
        fake_users = self.dict()
        return spark.createDataFrame(fake_users)


class FakeUser:
    def __init__(self, locale='en_US'):
        self.__fake_user = FakeUsers(1, locale=locale)

    def retrieve(self):
        return self.__fake_user[0]

    def dict(self):
        return self.__fake_user[0].dict()
