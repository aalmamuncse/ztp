from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import random
import hashlib
import json


# Simplified AES encryption and ABE encryption placeholders
def aes_encrypt(data, key):
    """
    AES encryption function with PKCS7 padding.
    """
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
    return cipher.iv + ciphertext  # Prepend IV for decryption


def aes_decrypt(data, key):
    """
    AES decryption function with PKCS7 unpadding.
    """
    iv = data[:AES.block_size]  # Extract IV from the encrypted data
    ciphertext = data[AES.block_size:]  # Extract ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data.decode()


def abe_encrypt(data, policy):
    """
    Simplified ABE encryption: hash the data with policy to simulate encryption.
    This is a placeholder for a real ABE encryption scheme.
    """
    return hashlib.sha256((policy + data).encode()).hexdigest()


class BlockchainNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.metadata = {}  # Metadata storage for fragments/chunks

    def receive_data(self, data):
        # Simulate receiving data (chunks or key fragments)
        print(f"Node {self.node_id} received data: {data}")


class Blockchain:
    def __init__(self, num_nodes, data_block, geometric_shape, chunk_size, redundancy, access_policy):
        self.nodes = [BlockchainNode(i) for i in range(num_nodes)]
        self.data_block = data_block
        self.geometric_shape = geometric_shape
        self.chunk_size = chunk_size
        self.redundancy = redundancy
        self.access_policy = access_policy

    def select_leaders(self, data_block):
        """
        Select dynamic leader nodes for distributing data and keys.
        This uses a simple random selection of leaders from the network.
        """
        num_leaders = int(len(self.nodes) * 0.2)  # 20% of nodes are leaders for simplicity
        leaders = random.sample(self.nodes, num_leaders)
        return leaders

    def generate_aes_key(self, data_block):
        """
        Generate a unique AES key for the data block.
        For simplicity, we use random bytes as the key.
        """
        return get_random_bytes(16)  # AES requires 16, 24, or 32 bytes key

    def fragment_key(self, aes_key, shape):
        """
        Split AES key into segments based on geometric shape.
        For simplicity, we split the key into equal-sized segments.
        """
        num_fragments = len(aes_key) // 16  # Assuming each fragment is 16 bytes (128 bits)
        return [aes_key[i:i + 16] for i in range(0, len(aes_key), 16)]

    def encrypt_key_with_abe(self, key_fragments, policy):
        """
        Encrypt each AES key fragment using ABE (Attribute-Based Encryption).
        Placeholder: hash the key fragment with policy to simulate ABE.
        """
        return [abe_encrypt(frag, policy) for frag in key_fragments]

    def generate_identifiers(self, key_fragments):
        """
        Generate unique identifiers for each key fragment.
        For simplicity, we use hashes of the fragments as identifiers.
        """
        return [hashlib.sha256(frag.encode()).hexdigest() for frag in key_fragments]

    def select_nodes_for_key(self, key_fragment, redundancy, leaders):
        """
        Select nodes for distributing the ABE-encrypted key fragment.
        Ensure redundancy by selecting 'r' leaders from the list of dynamic leaders.
        """
        return random.sample(leaders, redundancy)

    def distribute_fragment(self, key_fragment, nodes):
        """
        Simulate distributing the ABE-encrypted key fragment to the selected nodes.
        """
        for node in nodes:
            node.receive_data(key_fragment)

    def split_block(self, data_block, chunk_size):
        """
        Split the data block into chunks based on the given chunk size.
        """
        return [data_block[i:i + chunk_size] for i in range(0, len(data_block), chunk_size)]

    def generate_chunk_key(self, chunk):
        """
        Generate a unique AES key for each data chunk.
        For simplicity, use a hash of the chunk as the key.
        """
        return hashlib.sha256(chunk.encode()).hexdigest()

    def encrypt_chunk(self, chunk, chunk_key):
        """
        Encrypt a data chunk using AES encryption.
        """
        return aes_encrypt(chunk, chunk_key)

    def select_nodes_for_data(self, chunk, redundancy, leaders):
        """
        Select nodes for distributing the data chunk.
        Ensure redundancy by selecting 'r' nodes from the leaders, without overlap with key nodes.
        """
        return random.sample(leaders, redundancy)

    def distribute_chunk(self, chunk, nodes):
        """
        Distribute the encrypted chunk to the selected nodes.
        """
        for node in nodes:
            node.receive_data(chunk)

    def record_metadata(self, leaders, data):
        """
        Record metadata about the distribution of fragments/chunks to leader nodes.
        """
        for leader in leaders:
            leader.metadata["distribution"] = data  # Simplified metadata recording

    def ZTP_Data_Key_Dist(self):
        """
        Main function for Parallel Data and Key Distribution
        """
        # Step 1: Select dynamic leader nodes
        leaders = self.select_leaders(self.data_block)

        # Step 2: Generate AES key and fragment it based on geometric shape
        aes_key = self.generate_aes_key(self.data_block)
        key_fragments = self.fragment_key(aes_key, self.geometric_shape)

        # Step 3: Encrypt each key fragment using ABE with the given access policy
        abe_encrypted_keys = self.encrypt_key_with_abe(key_fragments, self.access_policy)

        # Step 4: Generate unique identifiers for each key fragment
        identifiers = self.generate_identifiers(key_fragments)

        # Step 5: Distribute the encrypted key fragments
        for i, key_fragment in enumerate(abe_encrypted_keys):
            selected_nodes_for_key = self.select_nodes_for_key(key_fragment, self.redundancy, leaders)
            self.distribute_fragment(key_fragment, selected_nodes_for_key)

        # Step 6: Record metadata for key distribution
        self.record_metadata(leaders, identifiers)

        # Step 7: Split the data block into chunks
        data_chunks = self.split_block(self.data_block, self.chunk_size)

        # Step 8: Encrypt each chunk and distribute to selected nodes
        for chunk in data_chunks:
            chunk_key = self.generate_chunk_key(chunk)
            encrypted_chunk = self.encrypt_chunk(chunk, chunk_key)
            selected_nodes_for_data = self.select_nodes_for_data(chunk, self.redundancy, leaders)
            self.distribute_chunk(encrypted_chunk, selected_nodes_for_data)

        # Step 9: Record metadata for chunk distribution
        self.record_metadata(leaders, data_chunks)

        return data_chunks, abe_encrypted_keys, key_fragments


# # Example usage:
# if __name__ == "__main__":
#     blockchain = Blockchain(
#         num_nodes=10,
#         data_block="This is a large data block that needs to be distributed.",
#         geometric_shape="some shape",  # Geometric shape is simplified here
#         chunk_size=20,
#         redundancy=3,
#         access_policy="policy1"
#     )

#     data_chunks, abe_encrypted_keys, key_fragments = blockchain.ZTP_Data_Key_Dist()

#     # Display the results
#     print("Data chunks:", data_chunks)
#     print("ABE Encrypted Keys:", abe_encrypted_keys)
#     print("Key fragments:", key_fragments)
