from azure.servicebus import ServiceBusClient


def receive_messages(receiver):
    '''This code runs continuously to receive the data until there is some keybord interruption or break statement '''
    for message in receiver:
        print("Data Received in queue... ")
        print("\n Latest unread message from queue is :- \n")
        receiver.complete_message(message) # This marks the message as read , so next time new data from queue is read
        return message
        # Here we getting the latest "UNREAD" data from queue 
        # Add the break statement if this code is to be hosted on cloud to avoid 504 gateway error for long response time

def run_receive(namespace_connection_string , queue_name):
    '''Creates Service Bus client from the given Connection string and Queue Name to receive message'''
    with ServiceBusClient.from_connection_string(
        conn_str=namespace_connection_string, logging_enable=True
    ) as servicebus_client:
        receiver = servicebus_client.get_queue_receiver(queue_name=queue_name)
        with receiver:
            print("Client created successfully...")
            print("Waiting for the data to be pushed in queue..")
            received_message = receive_messages(receiver)
            return received_message


def receive_data_from_bus(namespace_connection_string , queue_name):
    ''' Main function to call the create receive client and receive messages'''
    try :
        received_message = run_receive(namespace_connection_string=namespace_connection_string , queue_name=queue_name)
        return received_message
    except Exception as e:
        print(f"Error:-{e}")

