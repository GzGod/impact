from web3 import Web3, Account
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def mint(private):
    abi = [
        {
            "constant": True,
            "inputs": [
                {
                    "name": "account",
                    "type": "address"
                }
            ],
            "name": "balanceOf",
            "outputs": [
                {
                    "name": "",
                    "type": "uint256"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        }
    ]
    
    usdt_api = [
        {"constant": False, "inputs": [], "payable": False, "stateMutability": "nonpayable", "type": "constructor"},
        {"constant": False, "inputs": [{"indexed": True, "internalType": "address", "name": "owner", "type": "address"},
                                       {"indexed": True, "internalType": "address", "name": "spender", "type": "address"},
                                       {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}], 
         "name": "Approval", "payable": False, "type": "event"},
        {"constant": False, "inputs": [{"indexed": True, "internalType": "address", "name": "previousOwner", "type": "address"},
                                       {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}], 
         "name": "OwnershipTransferred", "payable": False, "type": "event"},
        {"constant": False, "inputs": [{"indexed": True, "internalType": "address", "name": "from", "type": "address"},
                                       {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
                                       {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}], 
         "name": "Transfer", "payable": False, "type": "event"},
        {"constant": True, "inputs": [], "name": "_decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], 
         "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": True, "inputs": [], "name": "_name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], 
         "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": True, "inputs": [], "name": "_symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], 
         "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": True, "inputs": [{"indexed": False, "internalType": "address", "name": "owner", "type": "address"},
                                      {"indexed": False, "internalType": "address", "name": "spender", "type": "address"}], 
         "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], 
         "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": False, "inputs": [{"indexed": False, "internalType": "address", "name": "spender", "type": "address"},
                                        {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], 
         "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], 
         "payable": False, "stateMutability": "nonpayable", "type": "function"},
        {"constant": True, "inputs": [{"indexed": False, "internalType": "address", "name": "account", "type": "address"}], 
         "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], 
         "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], 
         "name": "burn", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], 
         "payable": False, "stateMutability": "nonpayable", "type": "function"},
        {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], 
         "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": False, "inputs": [{"indexed": False, "internalType": "address", "name": "spender", "type": "address"},
                                        {"indexed": False, "internalType": "uint256", "name": "subtractedValue", "type": "uint256"}], 
         "name": "decreaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], 
         "payable": False, "stateMutability": "nonpayable", "type": "function"},
        {"constant": True, "inputs": [], "name": "getOwner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], 
         "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": False, "inputs": [{"indexed": False, "internalType": "address", "name": "spender", "type": "address"},
                                       {"indexed": False, "internalType": "uint256", "name": "addedValue", "type": "uint256"}], 
         "name": "increaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], 
         "payable": False, "stateMutability": "nonpayable", "type": "function"},
        {"constant": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], 
         "name": "mint", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], 
         "payable": False, "stateMutability": "nonpayable", "type": "function"},
        {"constant": True, "inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], 
         "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": True, "inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], 
         "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": False, "inputs": [], "name": "renounceOwnership", "outputs": [], 
         "payable": False, "stateMutability": "nonpayable", "type": "function"},
        {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], 
         "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], 
         "payable": False, "stateMutability": "view", "type": "function"},
        {"constant": False, "inputs": [{"indexed": False, "internalType": "address", "name": "recipient", "type": "address"},
                                       {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], 
         "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], 
         "payable": False, "stateMutability": "nonpayable", "type": "function"},
        {"constant": False, "inputs": [{"indexed": False, "internalType": "address", "name": "sender", "type": "address"},
                                       {"indexed": False, "internalType": "address", "name": "recipient", "type": "address"},
                                       {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], 
         "name": "transferFrom", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], 
         "payable": False, "stateMutability": "nonpayable", "type": "function"},
        {"constant": False, "inputs": [{"indexed": False, "internalType": "address", "name": "newOwner", "type": "address"}], 
         "name": "transferOwnership", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}
    ]
    
    web3 = Web3(Web3.HTTPProvider("https://endpoints.omniatech.io/v1/bsc/mainnet/public"))
    private_key = private
    account = Account.from_key(private_key)
    addr = account.address
    
    # 步骤1：批准 USDT
    usdt = web3.eth.contract(
        address=web3.to_checksum_address("0x55d398326f99059fF775485246999027B3197955"),
        abi=usdt_api,
    )
    
    approve1 = usdt.functions.approve(web3.to_checksum_address("0x087bf9d5cefed9a727b2ad5fffe8adf42db30aa4"),
                                      1000000000000000000).build_transaction(
        {
            "from": account.address,
            "value": 0,
            "nonce": web3.eth.get_transaction_count(account.address),
            "gasPrice": web3.eth.gas_price,
            "chainId": 56,
        }
    )
    
    approve1["gas"] = int(web3.eth.estimate_gas(approve1)) + 1000
    signed_txn = web3.eth.account.sign_transaction(approve1, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction).hex()
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    print(f"{addr} | 等待批准交易完成...")
    
    if receipt.status != 1:
        print(f"{addr} | 交易 {transaction_hash} 失败！")
    
    print(f"{addr} | 批准交易哈希: {transaction_hash}")

    # 步骤2：购买
    tx = {
        "from": account.address,
        "to": web3.to_checksum_address("0x34616bf39f910797d7e51BF2D87230794aDDDcdF"),
        "nonce": web3.eth.get_transaction_count(account.address),
        "gasPrice": web3.eth.gas_price,
        "chainId": 56,
        "data": "0x73e888fd0000000000000000000000000000000000000000000000000000000000000000"
    }
    
    tx["gas"] = int(web3.eth.estimate_gas(tx)) + 1000
    signed_txn = web3.eth.account.sign_transaction(tx, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction).hex()
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    print(f"{addr} | 等待购买交易完成...")
    
    if receipt.status != 1:
        print(f"{addr} | 交易 {transaction_hash} 失败！")
    
    print(f"{addr} | 购买交易哈希: {transaction_hash}")
    
    contract = web3.eth.contract(
        address=web3.to_checksum_address("0x34616bf39f910797d7e51bf2d87230794adddcdf"),
        abi=abi,
    )
    
    # 步骤3：检查余额
    balance = contract.functions.balanceOf(account.address).call()
    print(f"{addr} | 余额是 {balance / 100000000000000000}")

if __name__ == "__main__":
    # 从 wallet.txt 读取私钥
    with open('wallet.txt', 'r') as file:
        private_keys = [line.strip() for line in file if line.strip()]

    # 询问用户线程数
    while True:
        try:
            num_threads = int(input("请输入线程数（建议5到10，避免RPC崩溃）："))
            if 1 <= num_threads <= 20:  # 限制最大线程数为20以确保安全
                break
            else:
                print("请输入1到20之间的数字。")
        except ValueError:
            print("这不是有效的数字，请重新输入。")

    print(f"使用 {num_threads} 个线程。请注意，过多的线程可能会导致RPC崩溃。")

    # 使用 ThreadPoolExecutor 进行多线程处理
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for private in private_keys:
            executor.submit(mint, private)
