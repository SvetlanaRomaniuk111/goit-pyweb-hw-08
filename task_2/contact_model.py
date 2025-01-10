from mongoengine import Document, StringField, BooleanField, connect
from faker import Faker

# Підключення до бази даних MongoDB
connect('contact_db')

# Модель для контакту
class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    phone = StringField()
    preferred_contact_method = StringField(choices=["email", "sms"])
    message_sent = BooleanField(default=False)

# Генерація фейкових контактів з використанням Faker
def generate_fake_contacts(n):
    fake = Faker()
    contacts = []
    for _ in range(n):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            preferred_contact_method=fake.random_element(elements=("email", "sms"))
        )
        contact.save()
        contacts.append(contact)
    return contacts
