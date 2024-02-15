import sys
import pika
import json

portnum = 5672
hostname = 'localhost'
queue_name = 'user'

exchange_subscribe = 'user_subscribe'

queue_listen = 'notifications'
exchange_notifications = 'notifications'

def notification_callback(ch, method, properties, body):
    processed_msg = json.loads(body)

    utuber = processed_msg['youtuber']
    video = processed_msg['video']
    
    print(f"New Notification: {utuber} uploaded {video}")

def updateSubscription(username, youtuber_name, status):
    connection = pika.BlockingConnection(pika.ConnectionParameters(hostname, portnum))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    message = {
        'user': username,
        'youtuber': youtuber_name,
        'subscribe': status
    }

    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=json.dumps(message))
    print("[x] SUCCESS")
    connection.close()
    
def receiveNotifications(username):
    connection = pika.BlockingConnection(pika.ConnectionParameters(hostname, portnum))
    channel = connection.channel()
    
    channel.exchange_declare(exchange=exchange_notifications,
                             exchange_type='direct',
                             durable=True)
    
    # Ensure the queue for this user exists and is bound to the exchange
    q = 'myqueue' #username + '_notifications'  # Unique queue name for each user
    channel.queue_declare(queue=q)
    channel.queue_bind(queue=q,
                       exchange=exchange_notifications,
                       routing_key=username)
    
    channel.basic_consume(queue=q, on_message_callback=notification_callback, auto_ack=True)
    channel.start_consuming()


# Example usage
username = sys.argv[1]
if len(sys.argv) > 2:
    status = sys.argv[2]
    youtuber = sys.argv[3]
    assert status.strip() in ['s', 'u']
    status = True if status.strip() == 's' else False

if len(sys.argv) == 2:
    # receive notifications
    print("Awaiting Notifications")
    receiveNotifications(username)
    
else:
    # update subscription status
    print("Updating Subscription")
    updateSubscription(username, youtuber, status)