from fakers.providers.person import Person

fake_persons = Person.fake_persons(5, locale='hi_IN')
print(fake_persons.to_pandas())
