# Import necessary libraries and modules
import random
import math
import time
from concurrent.futures import ThreadPoolExecutor
from ztp_consensus import ZTPConsensus
from ztp_key_data_accumulation import ZTPKeyDataAccumulation
from ztp_quorum import ZTPQuorum

# Define helper functions (e.g., for key and data distribution)
def generate_aes_key(block):
    return bytes(random.getrandbits(8) for _ in range(32))  # 256-bit key

def fragment_key(aes_key, shape):
    num_fragments = 4  # Assume the shape dictates the number of fragments
    return [aes_key[i:i+8] for i in range(0, len(aes_key), 8)]

def encrypt_key_with_abe(key_fragments, policy):
    return [f"ABE_encrypted_{fragment}" for fragment in key_fragments]

# AES encryption for key fragments
def encrypt_aes(data, key):
    """
    AES encryption for key fragments using a given AES key.
    """
    # Padding to make sure data is a multiple of 16 (required for AES block size)
    while len(data) % 16 != 0:
        data += ' '  # Padding with space, could be improved with proper padding scheme
    
    # AES encryption
    cipher = AES.new(key, AES.MODE_CBC)  # Using CBC mode for AES
    ciphertext = cipher.encrypt(data.encode('utf-8'))
    return ciphertext, cipher.iv  # Return ciphertext and the initialization vector (iv)

def encrypt_chunk(chunk, chunk_key):
    """
    Encrypt data chunks using AES for key fragments and ABE for data chunks.
    """
    # Check if chunk_key is a valid AES key (a 16-byte key)
    if len(chunk_key) != 16:
        raise ValueError("AES key must be 16 bytes long.")
    
    # Encrypt using AES for chunk_key (key fragment)
    encrypted_key_fragment, iv = encrypt_aes(chunk_key, chunk_key)  # For simplicity, using the chunk_key as AES key itself
    
    # Simulate ABE encryption for the chunk data
    encrypted_data_chunk = encrypt_abe(chunk, "some_access_policy")

    return encrypted_data_chunk, encrypted_key_fragment, iv

def generate_identifiers(fragments):
    return [f"identifier_{i}" for i in range(len(fragments))]

def select_nodes_for_key(fragment, redundancy, leaders):
    return random.sample(leaders, redundancy)

def distribute_fragment(fragment, nodes):
    """
    Implementing the 2-phase commit protocol for distributing key fragments to nodes.
    """
    # Phase 1: Prepare
    print(f"Phase 1: Prepare - Sending prepare request to nodes: {nodes}")
    
    # Collect responses from nodes
    responses = {}
    with ThreadPoolExecutor(max_workers=len(nodes)) as executor:
        futures = {executor.submit(self.send_prepare_request, node, fragment): node for node in nodes}
        for future in futures:
            node = futures[future]
            try:
                response = future.result()
                responses[node] = response
                print(f"Node {node} response: {response}")
            except Exception as e:
                responses[node] = "no"
                print(f"Failed to get response from node {node}: {e}")

    # Check if all responses are "yes"
    if all(response == "yes" for response in responses.values()):
        # Phase 2: Commit
        print("Phase 2: Commit - All nodes are ready. Sending commit request.")
        with ThreadPoolExecutor(max_workers=len(nodes)) as executor:
            futures = {executor.submit(self.send_commit_request, node, fragment): node for node in nodes}
            for future in futures:
                node = futures[future]
                try:
                    future.result()  # Ensures the node has received the commit request
                    print(f"Node {node} committed to storing fragment.")
                except Exception as e:
                    print(f"Failed to commit fragment to node {node}: {e}")
    else:
        # Phase 2: Rollback
        print("Phase 2: Rollback - Not all nodes are ready. Sending rollback request.")
        with ThreadPoolExecutor(max_workers=len(nodes)) as executor:
            futures = {executor.submit(self.send_rollback_request, node, fragment): node for node in nodes}
            for future in futures:
                node = futures[future]
                try:
                    future.result()  # Ensures the node has received the rollback request
                    print(f"Node {node} rolled back the fragment distribution.")
                except Exception as e:
                    print(f"Failed to send rollback to node {node}: {e}")
    
    # Final status
    print("Fragment distribution process completed.")

def send_prepare_request(self, node, fragment):
    """
    Simulate sending a prepare request to a node. The node either accepts or rejects based on availability.
    """
    # Simulating the node's decision to accept or reject the fragment distribution
    time.sleep(random.uniform(0.1, 0.3))  # Simulate some delay
    decision = "yes" if random.random() > 0.1 else "no"  # 90% chance to accept
    return decision

def send_commit_request(self, node, fragment):
    """
    Simulate sending a commit request to a node to store the fragment.
    """
    time.sleep(random.uniform(0.1, 0.3))  # Simulate some delay
    print(f"Node {node} is committing the fragment.")

def send_rollback_request(self, node, fragment):
    """
    Simulate sending a rollback request to a node to discard the fragment.
    """
    time.sleep(random.uniform(0.1, 0.3))  # Simulate some delay
    print(f"Node {node} is rolling back the fragment.")

def split_block(block, chunk_size):
    return [block[i:i+chunk_size] for i in range(0, len(block), chunk_size)]

def generate_chunk_key(chunk):
    return bytes(random.getrandbits(8) for _ in range(32))  # 256-bit key for chunk

def encrypt_chunk(chunk, chunk_key):
    return chunk  # Dummy encryption for simplicity

def select_nodes_for_data(chunk, redundancy, leaders):
    return random.sample(leaders, redundancy)

def distribute_chunk(chunk, nodes):
    print(f"Distributing data chunk to nodes: {nodes}")

def record_metadata(leaders, fragments_or_chunks):
    print(f"Recording metadata for leaders: {leaders}")

# Updated ZTPSmartContract class integrating Key and Data Fragmentation
class ZTPSmartContract:
    def __init__(self):
        self.nodes = []  # Placeholder for nodes in the network
        self.block = ""  # Placeholder for the data block
        self.shape = ""  # Placeholder for the shape of fragmentation
        self.chunk_size = 0  # Placeholder for the chunk size
        self.redundancy = 0  # Placeholder for redundancy factor
        self.access_policy = ""  # Placeholder for the access policy
    
    def get_available_nodes(self):
        """
        Function to dynamically collect available nodes in the network using MPI parameters or network discovery.
        """
        self.nodes = [f"node_{i}" for i in range(1, 11)]  # Simulate 10 nodes
    
    def quorum_election_and_leader_selection(self):
        """
        Function to simulate quorum election and leader selection.
        Select 51% of nodes dynamically to form the quorum and select leaders within the quorum.
        """
        print("Running Optimized Quorum Election and Leader Selection...")
        quorum_size = math.ceil(0.51 * len(self.nodes))  # Select 51% of total nodes for quorum
        elected_nodes = random.sample(self.nodes, quorum_size)  # Select quorum nodes randomly
        
        # Select leaders within the quorum
        leaders = elected_nodes[:quorum_size // 2]  # For simplicity, use the first half as leaders
        
        print(f"Elected nodes: {elected_nodes}")
        print(f"Selected leaders: {leaders}")
        return elected_nodes, leaders
    
    def parallel_data_key_distribution(self, block, s, c, r, P):
        """
        Function to simulate parallel data and key distribution across blockchain nodes.
        """
        print(f"Running Parallel Data and Key Distribution for block {block}...")
        
        # 1. Run quorum election and leader selection
        elected_nodes, leaders = self.quorum_election_and_leader_selection()
        
        # 2. Generate AES key for the block
        aes_key = generate_aes_key(block)
        
        # 3. Fragment the AES key into parts based on shape
        key_fragments = fragment_key(aes_key, s)
        
        # 4. Encrypt the key fragments using ABE with the access policy
        encrypted_key_fragments = encrypt_key_with_abe(key_fragments, P)
        
        # 5. Generate unique identifiers for key fragments
        fragment_identifiers = generate_identifiers(key_fragments)
        
        # 6. Distribute key fragments to nodes (based on redundancy)
        for i, fragment in enumerate(encrypted_key_fragments):
            selected_nodes_for_key = select_nodes_for_key(fragment, r, leaders)
            distribute_fragment(fragment, selected_nodes_for_key)
        
        # 7. Record metadata for key distribution
        record_metadata(leaders, fragment_identifiers)
        
        # 8. Split the block into smaller chunks
        data_chunks = split_block(block, c)
        
        # 9. For each chunk, generate a key and encrypt it
        for chunk in data_chunks:
            chunk_key = generate_chunk_key(chunk)
            encrypted_chunk = encrypt_chunk(chunk, chunk_key)
            
            # 10. Select nodes for storing the data chunk, ensuring no overlap with key nodes
            selected_nodes_for_data = select_nodes_for_data(chunk, r, leaders)
            distribute_chunk(encrypted_chunk, selected_nodes_for_data)
        
        # 11. Record metadata for chunk distribution
        record_metadata(leaders, data_chunks)
        
        return data_chunks, encrypted_key_fragments, key_fragments
    
    def execute(self):
        """
        Main function to execute the full ZTP Smart Contract operation.
        """
        self.get_available_nodes()
        
        # Sample data block, shape, chunk size, redundancy, and access policy
        self.block = "This is a sample block of data to be processed by the ZTP Smart Contract."
        self.shape = "some_shape"
        self.chunk_size = 16
        self.redundancy = 2
        self.access_policy = "some_access_policy"
        
        distributed_data, encrypted_key_fragments, key_fragments = self.parallel_data_key_distribution(
            self.block, self.shape, self.chunk_size, self.redundancy, self.access_policy
        )

        print(f"Distributed Data Chunks: {distributed_data}")
        print(f"Encrypted Key Fragments: {encrypted_key_fragments}")
        print(f"Original Key Fragments: {key_fragments}")

# ZTP class for managing the consensus and smart contract execution
class ZTP:
    def __init__(self, data_blocks, transaction_file):
        self.nodes = self.get_available_nodes()  # Get dynamically available nodes
        self.data_blocks = data_blocks
        self.transaction_file = transaction_file
        self.consensus = ZTPConsensus(self.nodes)
        self.key_data_accumulation = ZTPKeyDataAccumulation(self.nodes)
        self.smart_contract = ZTPSmartContract()

    def get_available_nodes(self):
        """
        Function to simulate the collection of available nodes in the network.
        """
        return [f"node_{i}" for i in range(1, 11)]  # Simulate 10 nodes

    def parallel_data_key_distribution(self, block, s, c, r, P):
        """
        Simulate parallel distribution of data and keys to the nodes from a stream of transaction data.
        """
        print(f"Running Parallel Data and Key Distribution for block {block}...")
        block_data = self.create_block_from_file()

        # Using ThreadPoolExecutor for parallel distribution
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_node = {executor.submit(self.distribute_block_data, block_data, node): node for node in self.nodes}
            for future in future_to_node:
                node = future_to_node[future]
                try:
                    future.result()
                    print(f"Data successfully distributed to node {node}")
                except Exception as e:
                    print(f"Failed to distribute data to node {node}: {e}")
        return block

    def create_block_from_file(self):
        """
        Simulate creating a block from transaction data streamed from a file.
        """
        block_data = []
        with open(self.transaction_file, 'r') as file:
            for line in file:
                transaction = self.process_transaction_line(line)
                block_data.append(transaction)
        print(f"Block created with {len(block_data)} transactions.")
        return block_data

    def process_transaction_line(self, line):
        """
        Process a line from the transaction file and return the transaction data.
        """
        transaction_data = line.strip().split(',')
        return {"transaction_id": transaction_data[0], "amount": transaction_data[1]}

    def distribute_block_data(self, block_data, node):
        """
        Simulate distributing the block data to a specific node.
        """
        print(f"Distributing block data to node {node}...")
        time.sleep(random.uniform(0.1, 0.5))  # Simulate delay
        print(f"Data distributed to {node}.")


if __name__ == "__main__":
    contract = ZTPSmartContract()
    contract.execute()
