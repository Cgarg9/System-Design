class RoundRobinLoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current_index = 0
    
    def get_server(self):
        """Get next server in round robin fashion"""
        if not self.servers:
            return None
        
        # Get current server
        server = self.servers[self.current_index]
        
        # Move to next server (with wraparound)
        self.current_index = (self.current_index + 1) % len(self.servers)
        
        return server
    
    def add_server(self, server):
        """Add a new server to the pool"""
        self.servers.append(server)
    
    def remove_server(self, server):
        """Remove a server from the pool"""
        if server in self.servers:
            # Adjust current index if needed
            removed_index = self.servers.index(server)
            if removed_index < self.current_index:
                self.current_index -= 1
            elif removed_index == self.current_index and self.current_index >= len(self.servers) - 1:
                self.current_index = 0
            
            self.servers.remove(server)

# Example usage
servers = ['Server-1', 'Server-2', 'Server-3']
lb = RoundRobinLoadBalancer(servers)

for i in range(10):
    server = lb.get_server()
    print(f"Request {i+1} → {server}")
