from web3 import Web3
from solcx import compile_standard, install_solc
import json
from dotenv import load_dotenv
import os
from functools import lru_cache

load_dotenv()

infura_url = os.getenv('INFURA_URL')
private_key = os.getenv('PRIVATE_KEY')
account_address = os.getenv('ACCOUNT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(infura_url))
chain_id = 4

assert web3.isConnected(), "Fail to connect to Ethereum network."

install_solc('0.8.0')

solidity_src = """
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

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"MetaSpace.sol": {"content": solidity_src}},
    "settings": {"outputSelection": {
        "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]}
    }},
}, solc_version="0.8.0")

bytecode = compiled_sol['contracts']['MetaSpace.sol']['MetaSpace']['evm']['bytecode']['object']
abi = json.loads(compiled_sol['contracts']['MetaSpace.sol']['MetaSpace']['metadata'])['output']['abi']

meta_space_contract = web3.eth.contract(abi=abi, bytecode=bytecode)

def deploy_contract():
    nonce = get_nonce(account_address)
    
    transaction = meta_space_contract.constructor().buildTransaction({
        "chainId": chain_id,
        "from": account_address,
        "nonce": nonce,
        "gasPrice": web3.toWei("50", "gwei")
    })
    
    signed_tx = web3.eth.account.signTransaction(transaction, private_key)
    
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    
    return tx_receipt.contractAddress

@lru_cache(maxsize=None)
def get_contract(contract_address):
    return web3.eth.contract(
        address=contract_address,
        abi=abi
    )

def create_room(contract_address, room_name):
    contract = get_contract(contract_address)
    nonce = get_nonce(account_address)
    
    transaction = contract.functions.createRoom(room_name).buildTransaction({
        "chainId": chain_id,
        "from": account_address,
        "nonce": nonce,
        "gasPrice": web3.toWei("50", "gwei")
    })
    
    signed_tx = web3.eth.account.signTransaction(transaction, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    
    return tx_receipt

def get_room(contract_address, index):
    contract = get_contract(contract_address)
    
    return contract.functions.getRoom(index).call()

@lru_cache(maxsize=None)
def get_nonce(account_address):
    return web3.eth.getTransactionCount(account_address)