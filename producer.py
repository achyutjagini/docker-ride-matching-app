# Code for Producer
from flask import Flask, request
import json
import pika
from uuid import uuid4

#pika is rabbitMQ client library for python

# curl -X POST -d "location=hsr&destination=btm&time=7&seats=4&cost=100" localhost:54321/new_ride

#The form field in the request body is a dictionary-like object that contains the keys and values 
# of the form data in the request.
#additional field 'ip_address' whose value is the IP address of the request sender.

consumers = []

app = Flask(__name__)


#server that accepts request for ride

@app.route('/new_ride', methods=['POST'])
def new_ride():
    
    body = json.dumps(request.form)
    task_id = 'task_' + uuid4().hex

    # Connect to rabbitmq over tcp
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    
    # Create channel to publish to ride_match queue

    channel = connection.channel()

    channel.queue_declare(queue='ride_match', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='ride_match',
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            message_id=task_id
        ))
    
    
    print(f'Received task {body} via POST, published to queue', flush=True)

    # Create new channel to publish to database queue
    channel = connection.channel()

    channel.queue_declare(queue='database', durable=True)
    
    channel.basic_publish(
        exchange='',
        routing_key='database',
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            message_id=task_id
        ))

    connection.close()

    return ''


@app.route('/new_ride_matching_consumer', methods=['POST'])

def new_ride_matching_consumer():
    consumers.append({**request.form, 'ip_address': request.remote_addr})
    print(f'List of consumers: {consumers}', flush=True)

    return ''