# Import all necessary libraries
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import base64
import json

# Function to process the ABITransactionResponse-like object
def filter_response(response, algod_address, algod_token, indexer_address, APP_ID, NAMESPACE_CONNECTION_STR, QUEUE_NAME):
    algod_client = AlgodClient(algod_token, algod_address)
    indexer_client = IndexerClient("", indexer_address)

    # Filter all data from response
    application_id = response.tx_info["txn"]["txn"]["apid"]
    gas_fees = response.tx_info["txn"]["txn"]["fee"]
    block_num = response.confirmed_round
    transaction_id = response.tx_id
    sender_wallet = response.tx_info['txn']['txn']['snd']
    block_info = algod_client.block_info(block_num)
    block_timestamp = block_info["block"]["ts"]

    print(f"Application ID: {application_id}, Gas Fees: {gas_fees}, Block Number: {block_num}, Transaction ID: {transaction_id}")
    print(f"Sender Wallet: {sender_wallet}")
    print(f"Application ID: {application_id}")
    print(f"Gas Fees: {gas_fees}")
    print(f"Block Number: {block_num}")
    print(f"Transaction ID: {transaction_id}")

    def fetch_transactions(address):
        all_transaction_details = []
        response = indexer_client.search_transactions(address=address, application_id=APP_ID)
        transactions = response["transactions"]
        print("--------------------------------------------------")
        print(f"All the transactions of {address} user:")
        print("--------------------------------------------------")
        for txn in transactions:
            if 'global-state-delta' in txn:
                encoded_string = txn['global-state-delta'][0]['value']['bytes']
                # Decode the base64-encoded string to bytes
                decoded_bytes = base64.b64decode(encoded_string)
                # Decode the bytes to a JSON string
                decoded_json_string = decoded_bytes.decode('utf-8')
                all_transaction_details.append(decoded_json_string)
        return all_transaction_details

    filtered_transaction = fetch_transactions(sender_wallet)

    all_transactions = {
        "wallet_address": sender_wallet,
        "transaction_id": transaction_id,
        "app_id": application_id,
        "gas_fees": gas_fees,
        "block_number": block_num,
        "block_timestamp": block_timestamp,
        "Blockchain_data": filtered_transaction
    }

    # Send the transaction data to azure bus
    send_data_to_bus(json_data=all_transactions, namespace_string=NAMESPACE_CONNECTION_STR, queue_name=QUEUE_NAME)

    # Receive the data from bus
    received_data_from_queue = receive_data_from_bus(namespace_connection_string=NAMESPACE_CONNECTION_STR, queue_name=QUEUE_NAME)

    return received_data_from_queue

def send_single_message(sender, json_data):
    '''Pushes the data to Queue'''
    json_string = json.dumps(json_data)  # Make the json object
    message = ServiceBusMessage(json_string)  # Convert the json to service bus message object
    sender.send_messages(message)  # Sends the message
    print("Successfully pushed the data to queue ....")
    return 1

def run_send(json_data, namespace_string, queue_name):
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

def send_data_to_bus(json_data, namespace_string, queue_name):
    run_send(json_data, namespace_string, queue_name)

def receive_messages(receiver):
    '''Receive the latest unread message from the queue'''
    for message in receiver:
        print("Data Received in queue...")
        print("\nLatest unread message from queue is:\n")
        receiver.complete_message(message)  # This marks the message as read, so next time new data from queue is read
        return message

def run_receive(namespace_connection_string, queue_name):
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

def receive_data_from_bus(namespace_connection_string, queue_name):
    '''Main function to create the receive client and receive messages'''
    try:
        received_message = run_receive(namespace_connection_string=namespace_connection_string, queue_name=queue_name)
        return received_message
    except Exception as e:
        print(f"Error: {e}")
