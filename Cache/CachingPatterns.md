## Caching Patterns

Different caching patterns balance **data freshness**, **consistency**, and **performance** in various ways. Below are four common patterns, detailed with prose examples.

### 1. Cache-Aside (Lazy Loading)
**How it works**  
1. Application attempts to read from cache.  
2. On **cache hit**, return cached value immediately.  
3. On **cache miss**, read from the primary store (e.g., database), populate the cache with the result, then return it.

**When to use**  
- Read-heavy workloads where only a subset of data is “hot.”  
- When cache stores unpredictable, on-demand data.

**Pros**  
- Simple to implement.  
- Cache only holds data that is actually used.

**Cons**  
- First access pays full database latency.  
- Potential “cache stampede” if many clients miss simultaneously.

**Example**  
An e-commerce site caches popular product details. When a user views a product for the first time, the system fetches it from the database, caches it, and serves it. Subsequent views are fast cache hits.

---

### 2. Read-Through / Write-Through
**How it works**  
- **Read-Through**: Application reads from cache proxy. On miss, the cache proxy loads from the primary store, caches it, and returns it.  
- **Write-Through**: Application writes go to the cache proxy, which synchronously writes both to cache and to the primary store.

**When to use**  
- Applications requiring **strong consistency** between cache and store.  
- When you want to **hide caching logic** from application code.

**Pros**  
- Cache always reflects the data store.  
- Simplifies application logic around cache.

**Cons**  
- Increased write latency (every write hits both cache and store).  
- Cache throughput limited by database write capacity.

**Example**  
A banking system uses write-through caching for account balances: every deposit operation updates both the cache and the database before acknowledging success, ensuring no stale reads.

---

### 3. Write-Back (Write-Behind)
**How it works**  
1. Application writes only to the cache.  
2. Cache acknowledges immediately to the client.  
3. Cache asynchronously flushes writes to the primary store in batches or at intervals.

**When to use**  
- Use cases demanding **ultra-low write latency** (e.g., real-time leaderboards).  
- Systems that can tolerate slight delays in persisting data.

**Pros**  
- Minimal write latency; client isn’t blocked by database writes.  
- Batch writes can improve store throughput.

**Cons**  
- Risk of data loss if cache crashes before flush.  
- Primary store lags behind cache state temporarily.

**Example**  
A gaming leaderboard writes score updates to an in-memory cache instantly. Every few seconds, the cache flushes batches of score updates to the database, smoothing write load.

---

### 4. Refresh-Ahead
**How it works**  
- A background process monitors cache entry TTLs.  
- Before an entry expires (e.g., when only 10% of TTL remains), it proactively reloads fresh data from the primary store and updates the cache.

**When to use**  
- High-traffic data that must remain in cache to avoid latency spikes.  
- Preventing “thundering herd” on cache expiry under peak load.

**Pros**  
- Almost zero chance of cache misses for hot entries.  
- Smooth request latency even when cache entries expire.

**Cons**  
- Additional background load on primary store.  
- Complexity of TTL monitoring and refresh scheduling.

**Example**  
A news website keeps top-trending articles in cache with 1-hour TTL. A scheduler refreshes those articles every 50 minutes, ensuring continuous in-cache delivery during traffic surges.

---

**Choosing the right pattern**  
- **Cache-Aside** for simple, on-demand hot data.  
- **Read-Through/Write-Through** for strong consistency with transparent caching.  
- **Write-Back** for write-latency-sensitive workloads willing to accept eventual persistence.  
- **Refresh-Ahead** for mission-critical hot data that must never expire under load.

Combine patterns when needed (e.g., cache-aside reads + write-through writes) to tailor caching behavior to your application’s consistency, latency, and throughput requirements.
