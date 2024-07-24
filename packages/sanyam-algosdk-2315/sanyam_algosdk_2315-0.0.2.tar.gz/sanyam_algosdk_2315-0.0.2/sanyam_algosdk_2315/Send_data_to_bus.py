from azure.servicebus import ServiceBusClient, ServiceBusMessage
import json

def send_single_message(sender, json_data):
    '''Pushes the data to Queue'''
    json_string = json.dumps(json_data) # Make the json object 
    message = ServiceBusMessage(json_string) # Convert the json to service bus message object
    sender.send_messages(message) # Sends the message
    print("Successfully pushed the data to queue ....")
    return 1

def run(json_data, namespace_string, queue_name):
    '''Creates the Sender Client'''

    # Create a Service Bus client using the connection string
    with ServiceBusClient.from_connection_string(
        conn_str=namespace_string, logging_enable=True
    ) as servicebus_client:
        # Get a Queue Sender object to send messages to the queue
        with servicebus_client.get_queue_sender(queue_name=queue_name) as sender:
            # Send one message
            print("Client created ...")
            send_single_message(sender, json_data)


def send_data_to_bus(json_data , namespace_string , queue_name):
    run(json_data , namespace_string , queue_name)

