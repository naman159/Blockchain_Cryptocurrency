import datetime                                                                                     #timestamp or the date when a block is created
import hashlib                                                                                      #to hash the blocks, working with the hash funtions
import json                                                                                         #to deal with json files (encoding the blocks before hashing them)
from flask import Flask, jsonify

#1 - Building a blockchain
class blockchain:
    def __init__(self):
        self.chain = []                                                                             #The chain that will contain blocks, rn it is empty
        self.create_block(proof = 1, prev_hash = '0')                                               #create_block is a function we will create further, which has parameter proof (proof of work) and previous hash. proof and previous_hash are given an arbitrary value since the line introduces the genesis(1st) block of the blockchain.

    def create_block(self, proof, prev_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash': prev_hash
        }
        self.chain.append(block)
        return block

    def get_prev_block(self):                                                                   #Function to get the last block of a chain, which is also the previous block for the block currently being mined
        return self.chain[-1]

    def pow(self, prev_proof):                                                                      #Here, we define the cryptographic puzzle that the miners will have to solve to find the proof of work
        new_proof = 1                                                                               #Here, we are initializing new_proof and proof_check, the values of which will be updated through the while loop
        proof_check = False

        while(proof_check == False):
            hash_op = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()        #any function including new_proof and prev_proof can be used but its not good to use symmetric functions like new_proof+prev_proof since the values will be repeated (any non-symmetric function is useable). The hashlib function only accepts string inputs and the encode function just adds a b before the string (by dafult, utf-8 version of the string). hexdigest() converts the returned resource to a hexadecimal number.
            print(hash_op)
            if(hash_op[:2] == '00'):                                                              #The more the number of leading 0s, the more difficult it becomes for the nodes in the system to mine each block.
                proof_check = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):                                                                          #This function converts a block into hash code.
        encoded_block = json.dumps(block, sort_keys = True).encode()                                #json.dumps() converts an object (here, dictionary block) into a string
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self, chain):                                                                   #Checks the validity of the chain - 1. if the prev_hash of a block matches with the hash of the previous block, 2. if the proof of each block comforms with the pow function for that block.
        prev_block = chain[0]
        block_index = 1

        while(block_index < len(chain)):
            block = chain[block_index]

            if(block['previous_hash'] != self.hash(prev_block)):
                return False

            prev_proof = prev_block['proof']
            current_proof = block['proof']
            hash_op = hashlib.sha256(str(current_proof**2 - prev_proof**2).encode()).hexdigest()

            if(hash_op[:2] != '00'):
                return False

            prev_block = block
            block_index += 1
        return True

#2 - Mining the blockchain

#Web App with flask
app = Flask(__name__)

bchain = blockchain()                                              #Making the blockchain instance

@app.route('/block_mine', methods = ['GET'])                        #Web page for mining a new block
def block_mine():
    prev_block = bchain.get_prev_block()
    prev_proof = prev_block['proof']
    proof = bchain.pow(prev_proof)
    prev_hash = bchain.hash(prev_block)
    block = bchain.create_block(proof, prev_hash)
    response = {'msg': 'Successfully mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200                                   #jsonify(response) converts the dictionary response to a json file and code 200 is an http status code which means the request was successful.

@app.route('/chain_get', methods = ['GET'])
def chain_get():
    response = {'chain': bchain.chain,
                'length': len(bchain.chain)
    }
    return jsonify(response), 200

app.run(host = '0.0.0.0', port = 5000)                              #Runs the app publicly on your server
