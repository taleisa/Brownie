from brownie import *
from web3 import Web3
import time

def main():
    NFT = TicketNFT.deploy("Kevin Hart","KVN","Boulevard","Stand-up comedy",1676332800,1676678400,{"from": accounts[0]})
    NFT.grantRole(Web3.solidityKeccak(["bytes32"],[str.encode("MINTER_ROLE")]) ,accounts[0])
    NFT.grantRole(Web3.solidityKeccak(["bytes32"],[str.encode("GEA_ACCOUNTS")]) ,accounts[2])#Pose as GEA acc
    NFT.grantRole(Web3.solidityKeccak(["bytes32"],[str.encode("VERIFIED_ACCOUNTS")]) ,accounts[3])#Pose as customer 1
    NFT.grantRole(Web3.solidityKeccak(["bytes32"],[str.encode("VERIFIED_ACCOUNTS")]) ,accounts[4])#Pose as customer 2
    NFT.safeMint(accounts[2],"whfljkwef",500000000000000000,260,{"from":accounts[0]})
    NFT.safeMint(accounts[2],"whfljkwef",1000000000000000000,260,{"from":accounts[0]})
    try:
        NFT.safeTransferFrom(accounts[2],accounts[3],1,"")# Should not work transfer method overriden
    except:
        print("Transfer from disabled-----------------------------------------------------------------------------\n")
    try:
        NFT.buy(1,"",{"from":accounts[5],"amount":1000000000000000000})#Should not work accounts[5] is not verified yet price is correct
    except:
        print("Account 5 not verified unable to purchase-------------------------------------------------------------\n")
    NFT.buy(0,"",{"from":accounts[4],"amount":500000000000000000})#Should work accounts[4] is verified amount is in gwei(equal to 0.5 ether)
    try:
        NFT.buy(1,"",{"from":accounts[3],"amount":500000000000000000})#Should not work accounts[3] is verified, but incorrect price
    except:
        print("Incorrect price--------------------------------------------------------------------------------------------\n")
    NFT.buy(1,"",{"from":accounts[3],"amount":1000000000000000000})#Should work accounts[3] is verified and correct price
    try:
        NFT.buy(1,"",{"from":accounts[4],"amount":500000000000000000})#Should not work accounts[4] is verified and correct price but ticket with id 1 should be not for sale
    except:
        print("Ticket not for sale-----------------------------------------------------------------------------\n")
    NFT.sale(True,1,{"from":accounts[3]})# Enable sale of ticket
    NFT.grantRole(Web3.solidityKeccak(["bytes32"],[str.encode("VERIFIED_ACCOUNTS")]) ,accounts[5])#Verify account 5
    NFT.buy(1,"",{"from":accounts[5],"amount":1000000000000000000})#Should work accounts[5] is verified , price is correct and token is for sale
    time.sleep(1)# Notorious brownie error if this is not added
    
    

