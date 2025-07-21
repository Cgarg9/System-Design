import threading
import time
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ConnectionInfo:
    """Information about a connection"""
    connection_id: str
    start_time: float
    client_info: str = ""

class LeastConnectionsServer:
    def __init__(self, name: str, url: str, max_connections: int = 100):
        self.name = name
        self.url = url
        self.max_connections = max_connections
        self.active_connections: Dict[str, ConnectionInfo] = {}
        self.total_connections = 0
        self.lock = threading.Lock()
    
    def get_connection_count(self) -> int:
        """Get current number of active connections"""
        with self.lock:
            return len(self.active_connections)
    
    def can_accept_connection(self) -> bool:
        """Check if server can accept new connections"""
        return self.get_connection_count() < self.max_connections
    
    def add_connection(self, connection_id: str, client_info: str = "") -> bool:
        """Add a new connection to this server"""
        with self.lock:
            if not self.can_accept_connection():
                return False
            
            self.active_connections[connection_id] = ConnectionInfo(
                connection_id=connection_id,
                start_time=time.time(),
                client_info=client_info
            )
            self.total_connections += 1
            return True
    
    def remove_connection(self, connection_id: str) -> bool:
        """Remove a connection from this server"""
        with self.lock:
            if connection_id in self.active_connections:
                del self.active_connections[connection_id]
                return True
            return False
    
    def get_connection_details(self) -> Dict:
        """Get detailed information about connections"""
        with self.lock:
            return {
                'server': self.name,
                'active_connections': len(self.active_connections),
                'total_processed': self.total_connections,
                'max_connections': self.max_connections,
                'utilization': round((len(self.active_connections) / self.max_connections) * 100, 2)
            }

class LeastConnectionsLoadBalancer:
    def __init__(self, servers_config: List[Dict]):
        """
        Initialize with server configuration
        servers_config: [{'name': 'Server-1', 'url': 'http://...', 'max_connections': 50}, ...]
        """
        self.servers: List[LeastConnectionsServer] = []
        self.lock = threading.Lock()
        
        for config in servers_config:
            server = LeastConnectionsServer(
                name=config['name'],
                url=config['url'],
                max_connections=config.get('max_connections', 100)
            )
            self.servers.append(server)
    
    def get_server_with_least_connections(self) -> Optional[LeastConnectionsServer]:
        """Find server with least active connections"""
        with self.lock:
            if not self.servers:
                return None
            
            # Filter servers that can accept new connections
            available_servers = [s for s in self.servers if s.can_accept_connection()]
            
            if not available_servers:
                return None
            
            # Return server with least connections
            return min(available_servers, key=lambda s: s.get_connection_count())
    
    def assign_connection(self, connection_id: str, client_info: str = "") -> Optional[LeastConnectionsServer]:
        """Assign a new connection to the server with least connections"""
        server = self.get_server_with_least_connections()
        
        if server and server.add_connection(connection_id, client_info):
            return server
        
        return None
    
    def release_connection(self, connection_id: str) -> bool:
        """Release a connection from any server"""
        for server in self.servers:
            if server.remove_connection(connection_id):
                return True
        return False
    
    def get_load_distribution(self) -> List[Dict]:
        """Get current load distribution across all servers"""
        return [server.get_connection_details() for server in self.servers]
    
    def get_total_connections(self) -> int:
        """Get total active connections across all servers"""
        return sum(server.get_connection_count() for server in self.servers)

# Example usage
if __name__ == "__main__":
    # Create servers with different capacities
    servers_config = [
        {'name': 'Server-A', 'url': 'http://192.168.1.10:8080', 'max_connections': 10},
        {'name': 'Server-B', 'url': 'http://192.168.1.11:8080', 'max_connections': 15},
        {'name': 'Server-C', 'url': 'http://192.168.1.12:8080', 'max_connections': 12}
    ]
    
    lb = LeastConnectionsLoadBalancer(servers_config)
    
    print("=== Least Connections Load Balancer Demo ===")
    print("Simulating connections with varying durations\n")
    
    # Simulate connections
    connections = []
    
    # Add connections gradually
    for i in range(25):
        connection_id = f"conn_{i+1}"
        client_info = f"client_{i+1}"
        
        server = lb.assign_connection(connection_id, client_info)
        
        if server:
            connections.append((connection_id, server.name))
            print(f"Connection {connection_id} → {server.name} (Active: {server.get_connection_count()})")
        else:
            print(f"Connection {connection_id} → REJECTED (All servers full)")
        
        # Show load distribution every 5 connections
        if (i + 1) % 5 == 0:
            print("\n--- Load Distribution ---")
            for server_info in lb.get_load_distribution():
                print(f"{server_info['server']}: {server_info['active_connections']}/{server_info['max_connections']} "
                      f"({server_info['utilization']}% utilized)")
            print()
        
        # Simulate some connections finishing
        if i > 10 and i % 3 == 0 and connections:
            # Remove oldest connection
            old_conn_id, old_server = connections.pop(0)
            lb.release_connection(old_conn_id)
            print(f"Connection {old_conn_id} finished from {old_server}")
    
    print("\n=== Final Load Distribution ===")
    for server_info in lb.get_load_distribution():
        print(f"{server_info['server']}:")
        print(f"  Active: {server_info['active_connections']}/{server_info['max_connections']}")
        print(f"  Utilization: {server_info['utilization']}%")
        print(f"  Total Processed: {server_info['total_processed']}")
