import random
import bisect

class BlockchainNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.reputation = 0

    def participate_in_verification(self):
        # Simulate node participation in the verification process
        # This can be adjusted based on how you would implement verification
        pass

    def update_reputation(self):
        # Simulate reputation update based on verification
        # In this case, it randomly assigns a new reputation value
        self.reputation = random.randint(0, 100)

class Blockchain:
    def __init__(self, nodes, initial_leader_ratio, reputation_threshold, target_degree):
        self.nodes = [BlockchainNode(i) for i in range(nodes)]
        self.reputation_threshold = reputation_threshold
        self.target_degree = target_degree
        self.leader_ratio = initial_leader_ratio
        self.reputation = {node.node_id: 0 for node in self.nodes}

    def random_leader_selection(self):
        # Select initial leaders based on the initial leader ratio
        num_leaders = int(len(self.nodes) * self.leader_ratio)
        leaders = random.sample(self.nodes, num_leaders)
        return leaders

    def initialize_reputation(self):
        # Initialize reputation scores for all nodes
        for node in self.nodes:
            node.reputation = 0

    def binary_search_update(self, reputation_list, node, new_reputation):
        # Update node's reputation in the sorted reputation list
        index = bisect.bisect_left(reputation_list, (node.node_id, node.reputation))
        if index < len(reputation_list) and reputation_list[index][0] == node.node_id:
            reputation_list[index] = (node.node_id, new_reputation)
        else:
            bisect.insort_left(reputation_list, (node.node_id, new_reputation))

    def binary_search_threshold(self, reputation_list):
        # Select leaders above the reputation threshold using binary search
        leaders = [node for node, rep in reputation_list if rep >= self.reputation_threshold]
        return leaders

    def quorum_commit_consensus(self, dynamic_leaders):
        # Simulate two-phase quorum commit consensus
        prepare_phase = self.prepare_phase(dynamic_leaders)
        commit_phase = self.commit_phase(prepare_phase)
        return commit_phase

   def prepare_phase(self, dynamic_leaders):
    # Simulate preparing the dynamic leaders (e.g., checking their readiness for the commit)
    prepared_leaders = dynamic_leaders
    print(f"Prepared leaders for commit: {[leader.node_id for leader in prepared_leaders]}")
    return prepared_leaders


    def commit_phase(self, prepared_leaders):
        committed_leaders = prepared_leaders
        print(f"Committed leaders: {[leader.node_id for leader in committed_leaders]}")
        return committed_leaders

    def sync_leaders_across_network(self, final_leaders):
        """
        Sync the final leader list across the network by using two-phase commit.
        """
        print("Syncing leaders across the network using two-phase commit.")
        
        # Phase 1: Prepare phase
        prepared_leaders = self.prepare_phase(final_leaders)
        
        # Phase 2: Commit phase
        committed_leaders = self.commit_phase(prepared_leaders)
        
        # After commit phase, propagate the final leader list
        self.gossip_propagation(committed_leaders)

    def gossip_propagation(self, final_leaders):
        """
        Simulate gossip propagation after the commit phase to ensure all nodes are synchronized.
        """
        print(f"Gossip propagation complete. Leaders synchronized: {[leader.node_id for leader in final_leaders]}")


    def calculate_average_degree(self, dynamic_leaders):
        """
        Calculate the average degree of leader nodes in the dynamic leader set.
        """
        total_degrees = sum(len(leader.connections) for leader in dynamic_leaders)
        average_degree = total_degrees / len(dynamic_leaders) if dynamic_leaders else 0
        print(f"Average degree of leaders: {average_degree}")
        return average_degree

    def expand_leaders(self, dynamic_leaders):
        # Add more leaders to ensure sufficient connectivity (simplified)
        additional_leaders = self.random_leader_selection()
        dynamic_leaders.extend(additional_leaders)
        return dynamic_leaders

    def reduce_leaders(self, dynamic_leaders):
        # Reduce the number of leaders (simplified)
        dynamic_leaders = dynamic_leaders[:len(dynamic_leaders) // 2]
        return dynamic_leaders

    def select_leaders(self):
        # Main function to select leaders and adjust based on reputation
        L_initial = self.random_leader_selection()
        self.initialize_reputation()

        # Create and sort the reputation list
        reputation_list = [(node.node_id, node.reputation) for node in self.nodes]
        reputation_list.sort(key=lambda x: x[1], reverse=True)

        for node in self.nodes:
            node.participate_in_verification()
            node.update_reputation()
            self.binary_search_update(reputation_list, node, node.reputation)

        L_dynamic = self.binary_search_threshold(reputation_list)
        d_avg = self.calculate_average_degree(L_dynamic)

        while d_avg != self.target_degree:
            if d_avg < self.target_degree:
                L_dynamic = self.expand_leaders(L_dynamic)
            else:
                L_dynamic = self.reduce_leaders(L_dynamic)

            d_avg = self.calculate_average_degree(L_dynamic)

        L_final = self.quorum_commit_consensus(L_dynamic)
        self.sync_leaders_across_network(L_final)

        return L_final


# # Example usage
# if __name__ == "__main__":
#     # Initialize blockchain with 100 nodes, initial leader ratio of 10%, reputation threshold of 50, and target degree of 5
#     blockchain = Blockchain(nodes=100, initial_leader_ratio=0.1, reputation_threshold=50, target_degree=5)

#     # Select final leaders after applying the algorithm
#     final_leaders = blockchain.select_leaders()

#     # Output the selected final leaders
#     print(f"Final leaders selected: {[leader.node_id for leader in final_leaders]}")
