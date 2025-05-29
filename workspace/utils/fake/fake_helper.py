from faker import Faker

faker = Faker()


def fake_username():
    return faker.user_name()


def fake_password():
    return faker.password()


def fake_email():
    return faker.email()


def fake_product_title():
    return faker.word().capitalize()


def fake_product_description():
    return faker.sentence(nb_words=8)


def fake_product_price():
    return round(faker.pyfloat(left_digits=2, right_digits=2, positive=True), 2)


def fake_cart_quantity():
    return faker.random_int(min=1, max=10)


def fake_cart_date():
    return faker.date(pattern="%Y-%m-%d")
