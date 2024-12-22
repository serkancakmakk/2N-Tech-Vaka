from fakers.bl.address import FakeAddress, FakeAddresses
from fakers.bl.person import FakePerson, FakePersons
from fakers.providers import ClientLogger


class Person:
    @staticmethod
    def fake_address(locale='en_US'):
        ClientLogger.locale_validator(locale)
        fake_address = FakeAddress(locale)
        return fake_address

    @staticmethod
    def fake_addresses(address_count=5, locale='en_US'):
        ClientLogger.locale_validator(locale)
        fake_addresses = FakeAddresses(address_count, locale)
        return fake_addresses

    @staticmethod
    def fake_person(locale='en_US'):
        ClientLogger.locale_validator(locale)
        fake_person = FakePerson(locale)
        return fake_person

    @staticmethod
    def fake_persons(address_count=5, locale='en_US'):
        ClientLogger.locale_validator(locale)
        fake_persons = FakePersons(address_count, locale)
        return fake_persons
