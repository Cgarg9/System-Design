# Caching

Caching is a **technique that stores copies of frequently accessed data in a faster storage layer** so subsequent requests can be served more quickly. By reducing latency and alleviating load on backend systems, caching is essential for building high-performance, scalable applications.

---

## Why Caching Matters

- **Reduced Latency**: Serving data from a cache (e.g., in-memory) is orders of magnitude faster than hitting a database or remote service.  
- **Lower Backend Load**: Fewer requests reach origin servers, databases, or APIs—freeing them to handle other tasks.  
- **Cost Efficiency**: Less compute and I/O translates to lower infrastructure costs.  
- **Higher Throughput**: Caching increases requests-per-second capacity by offloading repeated work.

---

## Core Concepts

- **Cache Hit**: Requested data is found in cache → served immediately.  
- **Cache Miss**: Data absent in cache → fetched from source, then stored in cache.  
- **Eviction Policy**: Strategy to remove entries when cache is full or stale:
  - Least Recently Used (LRU)
  - Least Frequently Used (LFU)
  - First In, First Out (FIFO)
  - Random Replacement  
- **Invalidation**: Ensures cache consistency when underlying data changes. Common approaches:
  - Time-to-Live (TTL) expiration
  - Explicit deletion on updates (write-through or write-back)
  - Versioning or cache-busting keys  

---

## Caching Layers

| Layer                | Description                                                                                      |
|----------------------|--------------------------------------------------------------------------------------------------|
| **CPU Cache (L1/L2)**   | On-die SRAM for instructions/data closest to the CPU cores; lowest latency[41].                   |
| **In-Memory Cache**     | RAM-based key-value stores (Redis, Memcached) for application data, session state, query results[43]. |
| **Disk Cache**          | Local SSD/HDD caches large or infrequently updated data (OS page cache, browser cache)[41].         |
| **Distributed Cache**   | Multi-node cache clusters for horizontal scalability and fault tolerance (e.g., AWS ElastiCache)[42]. |
| **CDN Cache**           | Edge servers worldwide cache static and dynamic web assets (images, HTML, video chunks)[46].         |
| **Browser/HTTP Cache**  | Client-side caches responses per HTTP headers to avoid redundant network requests[41].               |

---

## Caching Patterns

1. **Cache-Aside (Lazy Loading)**  
   - Application checks cache; on miss, loads from source and populates cache.  
   - Simple, on-demand caching of hot data.

2. **Read-Through / Write-Through**  
   - Cache layer shields application: reads and writes go through cache, which syncs with the source.  
   - Ensures strong consistency at the cost of higher latency.

3. **Write-Back (Write-Behind)**  
   - Writes go to cache first; async background process flushes to source.  
   - Ultra-low write latency; risk of data loss if cache fails.

4. **Refresh-Ahead**  
   - Background process preemptively refreshes entries nearing expiration.  
   - Prevents cache stampedes and reduces miss spikes during peak traffic.

---

## When to Use Caching

- **Read-Heavy Workloads**: Data is requested far more often than updated.  
- **Expensive Computations**: Results of complex queries, image processing, or ML inference.  
- **Latency-Sensitive Features**: Real-time dashboards, personalized recommendations, search.  
- **Repeated Data**: Common lookup tables, configuration data, user session state.

---

## Best Practices

- Choose the **right eviction policy** based on access patterns.  
- Implement **cache invalidation** early to avoid stale data.  
- Monitor **cache hit ratio**; aim for ≥ 80% for cost-effective caching.  
- Combine multiple **cache layers** (e.g., in-memory + CDN) for optimal performance.  
- Use **consistent hashing** or **sharding** in distributed caches to balance load.

---

**Caching** is a cornerstone for building responsive, scalable systems. By selecting appropriate layers, patterns, and policies, you can dramatically improve performance while controlling cost and complexity.
