import sys
import pika
import json

hostname = 'localhost'
portnum = 5672
queue_name = 'youtuber'
exchange_name = 'upload_video'

def publishVideo(youtuber_name, video_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(hostname, portnum))
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