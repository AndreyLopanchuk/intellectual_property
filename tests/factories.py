from datetime import timedelta

import factory
from faker import Faker
import random

fake = Faker()


class AuthorFactory(factory.Factory):
    class Meta:
        model = dict

    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    birth_date = factory.LazyAttribute(lambda _: fake.date_of_birth())


class BookFactory(factory.Factory):
    class Meta:
        model = dict

    title = factory.LazyAttribute(lambda _: fake.catch_phrase())
    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=50))
    author_id = factory.LazyAttribute(lambda _: random.choice(authors_id_from_db))
    available = factory.LazyAttribute(lambda _: random.randint(0, 10))


class BorrowFactory(factory.Factory):
    class Meta:
        model = dict

    book_id = factory.LazyAttribute(lambda _: random.choice(books_id_from_db))
    reader_name = factory.LazyAttribute(lambda _: fake.name())
    borrow_date = factory.LazyAttribute(lambda _: fake.date_time_this_year())
    return_date = factory.LazyAttribute(lambda _: fake.date_time_this_year() + timedelta(days=random.randint(1, 30)))


class FakeGenerator:
    def __init__(self):
        pass
