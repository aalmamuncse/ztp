import random
import bisect

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.local_blockchain = []  # Simulating local blockchain data
        self.pending_queue = []     # Queue for pending requests
        self.active_queue = []      # Queue for active requests

    def request_access(self, user, data_block):
        """
        Simulate a node's request to validate the access of a data seeker.
        """
        # Randomly return True (valid) or False (invalid) for simplicity
        return random.choice([True, False])


class BlockchainCluster:
    def __init__(self, total_nodes):
        self.nodes = [Node(i) for i in range(total_nodes)]
        self.total_nodes = total_nodes
        self.bst = [i for i in range(total_nodes)]  # Initialize BST with all node IDs
    
    def select_nodes(self, num_nodes):
        """
        Select a dynamic subset of nodes using binary search for efficient node selection.
        """
        return random.sample(self.bst, num_nodes)


class OptimizedZTPConsensus:
    def __init__(self, total_nodes, seeker, owner, data_block, approved_seeker_list, cluster_key, seeker_key):
        self.cluster = BlockchainCluster(total_nodes)
        self.seeker = seeker
        self.owner = owner
        self.data_block = data_block
        self.approved_seeker_list = approved_seeker_list
        self.cluster_key = cluster_key
        self.seeker_key = seeker_key
        self.count = 0
    
    def ztp_consensus(self):
        """
        Implement the Optimized ZTP Consensus protocol for data access validation.
        """
        while True:
            # 1. Initialize counters and BST
            count = 0
            bst = self.cluster.bst
            # 2. Process data request from the seeker
            while count < self.cluster.total_nodes // 2:
                # 3. Select a dynamic subset of nodes using binary search
                selected_nodes = self.cluster.select_nodes(self.cluster.total_nodes // 2)
                # 4. Send request to nodes for validation
                for node_id in selected_nodes:
                    node = self.cluster.nodes[node_id]
                    # Push the user into node's active queue
                    node.active_queue.append(self.seeker)
                    # Request access to the block
                    valid = node.request_access(self.seeker, self.data_block)
                    if valid:
                        # If valid, update BST and increment count
                        bisect.insort(bst, node_id)  # Insert in sorted order for BST-like behavior
                        count += 1
                    # If count is enough (50% or more nodes), proceed to the next phase
                    if count >= self.cluster.total_nodes // 2:
                        break
            
            # 5. If enough nodes validate the seeker
            if count >= self.cluster.total_nodes // 2:
                # 6. Execute key accumulation and transmit data block
                self.ztp_key_accumulation()
                print(f"Data block {self.data_block} is transmitted to user {self.seeker}")
                self.log_access()
                self.release_from_active_queue()
                break
            else:
                # Push seeker to the pending queue if not validated
                self.cluster.nodes[self.seeker].pending_queue.append(self.seeker)
    
    def ztp_key_accumulation(self):
        """
        Simulate the key accumulation process (can be replaced with real cryptographic operations).
        """
        print("Executing ZTP-Key-Accumulation protocol...")

    def log_access(self):
        """
        Simulate logging the access record.
        """
        print(f"Access granted to user {self.seeker} for data block {self.data_block}")

    def release_from_active_queue(self):
        """
        Release the seeker from the active queue once access is granted.
        """
        seeker_node = self.cluster.nodes[self.seeker]
        seeker_node.active_queue.remove(self.seeker)
        print(f"User {self.seeker} has been released from active queue.")


if __name__ == "__main__":
    # Initialize a blockchain cluster with 10 nodes, and a seeker and owner
    total_nodes = 10
    seeker = 5  # User 5 is requesting data
    owner = 0  # Owner of the data block
    data_block = "data_block_12345"
    approved_seeker_list = [5, 8, 2]  # Approved seekers
    cluster_key = "cluster_key_abc"
    seeker_key = "seeker_key_xyz"

    # Initialize and run the Optimized ZTP Consensus
    consensus_protocol = OptimizedZTPConsensus(
        total_nodes=total_nodes,
        seeker=seeker,
        owner=owner,
        data_block=data_block,
        approved_seeker_list=approved_seeker_list,
        cluster_key=cluster_key,
        seeker_key=seeker_key
    )
    consensus_protocol.ztp_consensus()
