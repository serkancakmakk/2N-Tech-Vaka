import random
import faker
from faker import Faker

faker.Faker()


class CommonFunction:
    @staticmethod
    def generate_custom_email(full_name):
        # Generate a unique identifier (you can use UUID or any other method)
        unique_id = str(Faker().uuid4()).replace("-", "")[:6]  # Extract the first 10 characters

        # Combine full name and unique identifier
        email_prefix = f"{full_name.lower().replace(' ', '_')}{unique_id}"

        # Append a random domain from a list of domains (you can customize this)
        domains = ["@example.net", "@example.com", "@example.org", "@example.gov"]
        domain = random.choice(domains)
        email = f"{email_prefix}{domain}"
        return email
