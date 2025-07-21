import hashlib
from typing import List, Optional

class IPHashLoadBalancer:
    def __init__(self, servers: List[str]):
        """
        Initialize with list of server names/addresses
        servers: ['Server-1', 'Server-2', 'Server-3']
        """
        self.servers = servers
        self.server_count = len(servers)
    
    def hash_ip(self, ip_address: str) -> int:
        """
        Generate hash value from IP address
        Uses MD5 hash for consistent results
        """
        # Create hash of IP address
        hash_object = hashlib.md5(ip_address.encode())
        hash_hex = hash_object.hexdigest()
        
        # Convert to integer
        hash_int = int(hash_hex, 16)
        
        return hash_int
    
    def get_server_for_ip(self, client_ip: str) -> Optional[str]:
        """
        Get server assignment for given IP address
        Same IP will always return same server
        """
        if not self.servers:
            return None
        
        # Generate hash and map to server
        ip_hash = self.hash_ip(client_ip)
        server_index = ip_hash % self.server_count
        
        return self.servers[server_index]
    
    def add_server(self, server: str):
        """Add new server to the pool"""
        if server not in self.servers:
            self.servers.append(server)
            self.server_count = len(self.servers)
    
    def remove_server(self, server: str):
        """Remove server from the pool"""
        if server in self.servers:
            self.servers.remove(server)
            self.server_count = len(self.servers)

# Example usage
if __name__ == "__main__":
    servers = ['Server-A', 'Server-B', 'Server-C']
    lb = IPHashLoadBalancer(servers)
    
    # Test with different IP addresses
    test_ips = [
        '192.168.1.10',
        '192.168.1.11', 
        '10.0.0.15',
        '172.16.0.25',
        '192.168.1.10'  # Same IP again
    ]
    
    print("=== IP Hash Load Balancing Demo ===")
    ip_to_server = {}
    
    for ip in test_ips:
        server = lb.get_server_for_ip(ip)
        ip_to_server[ip] = server
        print(f"IP {ip} → {server}")
    
    print(f"\nConsistency Check:")
    print(f"192.168.1.10 always goes to: {ip_to_server['192.168.1.10']}")
