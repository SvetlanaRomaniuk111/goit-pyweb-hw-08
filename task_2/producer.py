import json
from mongoengine import connect
from faker import Faker
import pika
from contact_model import Contact  # Імпорт моделі Contact

# Підключення до бази даних MongoDB
connect('contact_db')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)
channel.queue_declare(queue='sms_queue', durable=True)

def create_task(nums: int):
    fake = Faker()
    for _ in range(nums):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            preferred_contact_method=fake.random_element(elements=("email", "sms"))
        )
        contact.save()
        message = {
            'id': str(contact.id)
        }
        if contact.preferred_contact_method == 'email':
            channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(message).encode())
        else:
            channel.basic_publish(exchange='', routing_key='sms_queue', body=json.dumps(message).encode())

    connection.close()

if __name__ == '__main__':
    create_task(100)
