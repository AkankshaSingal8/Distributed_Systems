import sys
import pika
import json

hostname = '0.0.0.0'
portnum = 5672

# youtuber90
queue_name_youtuber = 'youtuber'
exchange_name_youtuber = 'upload_video'

# user 
queue_name_user = 'user'
exchange_notifications = 'notifications'

# user lists
user_sub = {}       # dictionary containing user:subscriptions
utuber_vid = {}     # dictionary containing youtuber:video pairs

# declare channels
connection = pika.BlockingConnection(pika.ConnectionParameters(hostname, portnum))
channel = connection.channel()

# queues
channel.queue_delete(queue = queue_name_user)
channel.queue_delete(queue = queue_name_youtuber)

channel.queue_declare(queue = queue_name_user, durable = True)
channel.queue_declare(queue = queue_name_youtuber, durable = True)

# exchange for fanout subscription
channel.exchange_delete(exchange = exchange_notifications)

channel.exchange_declare(exchange = exchange_notifications,
                         exchange_type = 'direct',
                         durable = True)

def notify_users(youtuber, video):
    for user, youtubers in user_sub.items():
        if youtuber in youtubers:
            print("Sending message to:", user, youtuber)
            # send message
            info = {'youtuber': youtuber, 'video': video}
            msg = json.dumps(info)
            
            channel.basic_publish(exchange = exchange_notifications,
                                    routing_key = user,
                                    body = msg,
                                    properties=pika.BasicProperties(
                                        delivery_mode=2,
                                    ),
                                    )
            
def callback_youtuber(ch, method, properties, body):
    processed_msg = json.loads(body)
    youtuber_name = processed_msg['youtuber']
    video_name = processed_msg['video']
    print(f" [x] YouTuber '{youtuber_name}' uploaded '{video_name}'")

    # send notifications here
    notify_users(youtuber_name, video_name)
    
    # Simulate some work
    print(" [x] SUCCESS")
    
def callback_user(ch, method, properties, body):
    processed_msg = json.loads(body)
    username = processed_msg['user']
    
    if len(processed_msg.keys()) == 3: 
        # subscribe/unsubscribe 
        youtuber_name = processed_msg['youtuber']
        subscription = processed_msg['subscribe']
        if username not in user_sub.keys():
            user_sub[username] = []
        
        if subscription == True:
            # subscribe here
            user_sub[username].append(youtuber_name)
            print(f" [x] {username} subscribed to {youtuber_name}")
        else:
            # unsubscribe here
            try:
                user_sub[username].remove(youtuber_name)
            except ValueError:
                print(f" [x] {username} has not subscribed to {youtuber_name}!")

            print(f" [x] {username} unsubscribed to {youtuber_name}")        


# Start consuming
channel.basic_consume(queue=queue_name_user,
                        auto_ack=True,
                        on_message_callback=callback_user)

channel.basic_consume(queue=queue_name_youtuber,
                        auto_ack=True,
                        on_message_callback=callback_youtuber)


print("Server started. Waiting for messages.")
channel.start_consuming()