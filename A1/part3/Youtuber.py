import sys
import pika
import json

hostname = '34.170.100.8'
portnum = 5672
queue_name = 'youtuber'
exchange_name = 'upload_video'

def publishVideo(youtuber_name, video_name):
    credentials = pika.PlainCredentials('myuser', 'mypassword')  # Use the credentials you've set up

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=hostname, port=portnum, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)

    message = {
        'youtuber': youtuber_name,
        'video': video_name
    }
    
    # print(json.dumps(message))
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=json.dumps(message))
    print(" [x] SUCCESS")
    connection.close()

# Example usage
utuber, video_name = sys.argv[1], " ".join(sys.argv[2:])
publishVideo(utuber, video_name)