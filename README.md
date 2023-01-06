# CloudHack_2

Team members details:

A Spoorthi Alva - PES2UG19CS001 <br />
A R Manyatha - PES2UG19CS002 <br />
Achyut Jagini - PES2UG19CS013 <br />
Amulya S Dinesh - PES2UG19CS035 <br />

Commands used:

docker-compose up <br />
curl -X POST -d "location=hsr&destination=btm&time=7&seats=4&cost=100" localhost:54321/new_ride <br />
curl -X POST -d "location=kormangala&destination=indiranagar&time=9&seats=6&cost=100" localhost:54321/new_ride <br />

Procedure: 
1. Start rabbitmq container <br />
2. Start producer server <br />
3. Start ride matching consumer after waiting for 10 seconds (wait for rabbitmq to fully start) <br />
4. Make a request from ride matching consumer to producer (new_ride_matching_consumer) <br />
5. Make a curl request from my terminal to the producer (new_ride) with task details. <br />
6. Here, the producer publishes the task on the rabbitmq queue and then the consumer receives it. It then sleeps for the given time and prints task id and consumer id <br />
7. Also the same data get consumed by database consumer, which writes to a mongodb server running on a mongo container <br />
