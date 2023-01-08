
# Code for Ride Matching Consumer
import json
import os
import pika
import requests
import time

CONSUMER_ID = os.environ['CONSUMER_ID']
PRODUCER_ADDRESS = os.environ['PRODUCER_ADDRESS']

#The consumer then sends a POST request to the /new_ride_matching_consumer endpoint of the producer server, 
# passing a consumer_id parameter with the value of CONSUMER_ID.


#The time.sleep(10) function is called to make the consumer wait
#  for 10 seconds before sending the POST request to the producer.


time.sleep(10)

#The requests.post function sends a POST request to the
#  specified URL
#  and returns a Response object. The URL is constructed by
#  concatenating the PRODUCER_ADDRESS
# variable and the endpoint path using an f-string 
# (f'http://{PRODUCER_ADDRESS}/new_ride_matching_consumer').


#The data parameter is used to specify the request body. 
# In this case,
# it is set to a string in the 'consumer_id=value' format, 
# where value is the value of the CONSUMER_ID variable

response = requests.post(
    f'http://{PRODUCER_ADDRESS}/new_ride_matching_consumer',
    data=f'consumer_id={CONSUMER_ID}')

#The assert statement is a debugging tool that allows you to check 
# if a certain condition is true. If the condition is true,
#  the assert statement does nothing and the program continues
#  to execute.


assert response.status_code == 200


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()


channel.queue_declare(queue='ride_match', durable=True)


print(f'Consumer {CONSUMER_ID} started...', flush=True)


#Next, the consumer establishes a connection to the RabbitMQ server and declares the ride_match queue. 
# It then defines a callback function that will be called every time a message is consumed from the queue.

#The callback function takes four arguments:

#ch: the channel object that the message was consumed from.

#method: the method of the message, which includes the delivery_tag property that can be used to acknowledge the message.

#properties: the message properties.

#body: the content of the message.
#The callback function first decodes the body of the message and loads it into a
# 3 Python dictionary using the json.loads function. It then adds a new field '_id' 
# to the dictionary and sets its value to the message_id property of the properties object.


def callback(ch, method, properties, body):

    body = json.loads(body.decode())
    body['_id'] = properties.message_id

    print(f'Consumed {body} from ride_match queue', flush=True)

    #simulates ride matching time
    time.sleep(int(body['time']))

    print(f'Consumer ID: {CONSUMER_ID}, Task ID: {properties.message_id}', flush=True)

    ch.basic_ack(delivery_tag=method.delivery_tag)


#consumer will only consume one message at a time
channel.basic_qos(prefetch_count=1)


#Finally, the consumer starts consuming
#  messages from the ride_match queue
# by calling the basic_consume method
#of the channel object and passing the 
# callback function as an argument.

# It then enters a loop by calling the
#start_consuming method of the channel object, which waits for messages to arrive and calls the callback 
#function for each message.

channel.basic_consume(queue='ride_match', on_message_callback=callback)

channel.start_consuming()