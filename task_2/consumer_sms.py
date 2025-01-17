import json
import os
import sys
import time
from mongoengine import connect
import pika
from contact_model import Contact  # Імпорт моделі Contact

# Підключення до бази даних MongoDB
connect('contact_db')

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='sms_queue', durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        contact_id = message['id']
        contact = Contact.objects(id=contact_id).first()
        if contact:
            print(f" [x] Sending SMS to {contact.full_name} ({contact.phone})")
            time.sleep(0.5)  # Функція-заглушка для імітації надсилання SMS
            contact.message_sent = True
            contact.save()
            print(f" [x] SMS sent to {contact.full_name}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='sms_queue', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
