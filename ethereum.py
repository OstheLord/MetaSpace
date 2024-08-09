from web3 import Web3
from solcx import compile_standard, install_solc
import json
from dotenv import load_dotenv
import os
from functools import lru_cache

load_dotenv()

CONFIG = {
    'infura_url': os.getenv('INFURA_URL'),
    'private_key': os.getenv('PRIVATE_KEY'),
    'account_address': os.getenv('ACCOUNT_ADDRESS'),
    'chain_id': 4,
    'solc_version': '0.8.0',
    'gas_price': '50'
}

web3 = Web3(Web3.HTTPProvider(CONFIG['infura_url']))

assert web3.isConnected(), "Fail to connect to Ethereum network."

install_solc(CONFIG['solc_version'])

SOLIDITY_SRC = """
pragma solidity ^0.8.0;

contract MetaSpace {
    struct Room {
        string name;
        address owner;
    }

    Room[] public rooms;

    function createRoom(string calldata name) external {
        rooms.push(Room(name, msg.sender));
    }

    function getRoom(uint index) external view returns (string memory, address) {
        require(index < rooms.length, "Room index out of bounds");
        return (rooms[index].name, rooms[index].owner);
    }
}
"""

def compile_source():
    return compile_standard({
        "language": "Solidity",
        "sources": {"MetaSpace.sol": {"content": SOLIDITY_SRC}},
        "settings": {"outputSelection": {
            "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]}
        }},
    }, solc_version=CONFIG['solc_version'])

compiled_sol = compile_source()

bytecode = compiled_sol['contracts']['MetaSpace.sol']['MetaSpace']['evm']['bytecode']['object']
abi = json.loads(compiled_sol['contracts']['MetaSpace.sol']['MetaSpace']['metadata'])['output']['abi']

@lru_cache(maxsize=None)
def deploy_contract():
    nonce = get_nonce(CONFIG['account_address'])
    contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    
    transaction = contract.constructor().buildTransaction({
        "chainId": CONFIG['chain_id'],
        "from": CONFIG['account_address'],
        "nonce": nonce,
        "gasPrice": web3.toWei(CONFIG['gas_price'], "gwei")
    })
    
    signed_tx = web3.eth.account.signTransaction(transaction, CONFIG['private_key'])
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    return tx_receipt.contractAddress

@lru_cache(maxsize=32)
def get_contract(contract_address):
    return web3.eth.contract(address=contract_address, abi=abi)

def create_room(contract_address, room_name):
    contract = get_contract(contract_address)
    nonce = get_nonce(CONFIG['account_address'])
    
    transaction = contract.functions.createRoom(room_name).buildTransaction({
        "chainId": CONFIG['chain_id'],
        "from": CONFIG['account_address'],
        "nonce": nonce,
        "gasPrice": web3.toWei(CONFIG['gas_price'], "gwei")
    })
    
    signed_tx = web3.eth.account.signTransaction(transaction, CONFIG['private_key'])
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    return tx_receipt

def get_room(contract_address, index):
    contract = get_contract(contract_address)
    return contract.functions.getRoom(index).call()

@lru_cache(maxsize=32)
def get_nonce(account_address):
    return web3.eth.getTransactionCount(account_address)
