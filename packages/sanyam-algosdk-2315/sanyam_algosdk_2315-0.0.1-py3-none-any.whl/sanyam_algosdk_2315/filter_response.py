from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
import base64
import random
from Send_data_to_bus import send_data_to_bus
from Receive_data_from_bus import receive_data_from_bus





# Function to process the ABITransactionResponse-like object
def filter_response(response, algod_address, algod_token, indexer_address, APP_ID ,NAMESPACE_CONNECTION_STR, QUEUE_NAME):
    algod_client = AlgodClient(algod_token, algod_address)
    indexer_client = IndexerClient("", indexer_address)

    # Filter all data from response
    applicationid = response.tx_info["txn"]["txn"]["apid"]
    gasfees = response.tx_info["txn"]["txn"]["fee"]
    blocknum = response.confirmed_round
    transactionid = response.tx_id
    sender_wallet = response.tx_info['txn']['txn']['snd']
    block_number = response.confirmed_round
    block_info = algod_client.block_info(block_number)
    block_timestamp = block_info["block"]["ts"]

    print(f"Application ID: {applicationid}, Gas Fees: {gasfees}, Block Number: {blocknum}, Transaction ID: {transactionid}")
    print(f"Sender Wallet: {response.tx_info['txn']['txn']['snd']}")
    print(f"Application ID: {response.tx_info['txn']['txn']['apid']}")
    print(f"Gas Fees: {response.tx_info['txn']['txn']['fee']}")
    print(f"Block Number: {response.confirmed_round}")
    print(f"Transaction ID: {response.tx_id}")

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
        "UUID" : random.randint(5125 , 9579),
        "wallet_address": sender_wallet,
        "transaction_id": transactionid,
        "app_id": applicationid,
        "gas_fees": gasfees,
        "block_number": blocknum,
        "block_timestamp": block_timestamp,
        "Blockchain_data": filtered_transaction
    }

    # Send the transaction data to azure bus 
    send_data_to_bus(json_data=all_transactions,namespace_string=NAMESPACE_CONNECTION_STR , queue_name=QUEUE_NAME)

    # Receive the data from bus 
    received_data_from_queue = receive_data_from_bus(namespace_connection_string= NAMESPACE_CONNECTION_STR , queue_name= QUEUE_NAME)

    return received_data_from_queue

