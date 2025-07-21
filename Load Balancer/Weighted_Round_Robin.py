class WeightedRoundRobinLoadBalancer:
    def __init__(self, servers_with_weights):
        """
        Initialize with servers and their weights
        servers_with_weights: list of tuples [(server_name, weight), ...]
        Example: [('Server-1', 5), ('Server-2', 3), ('Server-3', 2)]
        """
        self.servers = []
        self.weights = []
        self.current_weights = []
        
        for server, weight in servers_with_weights:
            if weight <= 0:
                raise ValueError(f"Weight for {server} must be positive")
            
            self.servers.append(server)
            self.weights.append(weight)
            self.current_weights.append(0)
        
        self.total_weight = sum(self.weights)
    
    def get_server(self):
        """
        Get next server using weighted round robin algorithm
        Uses the smooth weighted round robin algorithm
        """
        if not self.servers:
            return None
        
        # Increase current weights by their respective weights
        for i in range(len(self.servers)):
            self.current_weights[i] += self.weights[i]
        
        # Find server with highest current weight
        max_weight_index = self.current_weights.index(max(self.current_weights))
        
        # Decrease the selected server's current weight by total weight
        self.current_weights[max_weight_index] -= self.total_weight
        
        return self.servers[max_weight_index]
    
    def add_server(self, server, weight):
        """Add a new server with specified weight"""
        if weight <= 0:
            raise ValueError(f"Weight for {server} must be positive")
        
        self.servers.append(server)
        self.weights.append(weight)
        self.current_weights.append(0)
        self.total_weight += weight
    
    def remove_server(self, server):
        """Remove a server from the pool"""
        if server not in self.servers:
            return False
        
        index = self.servers.index(server)
        self.total_weight -= self.weights[index]
        
        self.servers.pop(index)
        self.weights.pop(index)
        self.current_weights.pop(index)
        
        return True
    
    def update_weight(self, server, new_weight):
        """Update weight for an existing server"""
        if server not in self.servers:
            return False
        
        if new_weight <= 0:
            raise ValueError(f"Weight for {server} must be positive")
        
        index = self.servers.index(server)
        old_weight = self.weights[index]
        
        self.weights[index] = new_weight
        self.total_weight = self.total_weight - old_weight + new_weight
        
        return True
    
    def get_server_info(self):
        """Get information about all servers"""
        return [
            {
                'server': server,
                'weight': weight,
                'current_weight': current_weight,
                'percentage': round((weight / self.total_weight) * 100, 2)
            }
            for server, weight, current_weight in zip(self.servers, self.weights, self.current_weights)
        ]

if __name__ == "__main__":
    # Create load balancer with servers and weights
    servers = [
        ('Server-A', 5),  # High-performance server
        ('Server-B', 3),  # Medium-performance server  
        ('Server-C', 2)   # Lower-performance server
    ]
    
    lb = WeightedRoundRobinLoadBalancer(servers)
    
    print("=== Weighted Round Robin Distribution ===")
    print("Server-A: weight=5 (50% of traffic)")
    print("Server-B: weight=3 (30% of traffic)")
    print("Server-C: weight=2 (20% of traffic)")
    print()
    
    server_count = {'Server-A': 0, 'Server-B': 0, 'Server-C': 0}
    
    for i in range(20):
        server = lb.get_server()
        server_count[server] += 1
        print(f"Request {i+1:2d} → {server}")
    
    print("\n=== Final Distribution ===")
    for server, count in server_count.items():
        percentage = (count / 20) * 100
        print(f"{server}: {count}/20 requests ({percentage:.1f}%)")
