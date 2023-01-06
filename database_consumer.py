# Use this file to setup the database consumer that stores the ride information in the database
import json
import pika
import pymongo
import time

time.sleep(10)

client = pymongo.MongoClient("mongodb://mongodb:27017")
db = client['ride_matching']
collection = db['ride_details']

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='database', durable=True)
print('Database consumer started...', flush=True)


def callback(ch, method, properties, body):
    body = json.loads(body)
    body['_id'] = properties.message_id
    print(f'Consumed {body} from database queue', flush=True)

    collection.insert_one(body)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='database', on_message_callback=callback)

channel.start_consuming()