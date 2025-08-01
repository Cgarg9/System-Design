# Cache Eviction Policies

Eviction policies determine which entries are removed when a cache reaches capacity. Four common strategies are described below, with conceptual examples.

---

## 1. Least Recently Used (LRU)

**Definition:**  
Evict the entry that has gone the longest without being accessed.

**When to use:**  
Access patterns where recent data is more likely to be reused (e.g., user sessions, UI caching).

**Pros:**  
- Balances recency; adapts to changing “hot” data.  

**Cons:**  
- Requires tracking access order (e.g., via a linked list or timestamp).

**Example:**  
A web application caches user profile pages. If user A’s page is accessed, it moves to the “most recently used” position. When capacity is reached and a new profile is cached, the least-recently accessed profile is evicted.

---

## 2. Least Frequently Used (LFU)

**Definition:**  
Evict the entry with the lowest access frequency (number of hits).

**When to use:**  
Workloads where consistently popular items should remain cached, even if not recently accessed (e.g., product catalogs, trending items).

**Pros:**  
- Retains persistently popular items.  

**Cons:**  
- Requires per-entry hit counters; may evict items that spike briefly.

**Example:**  
An online store caches product details. Each time a product is viewed, its counter increments. When the cache is full, the product with the lowest view count is evicted, ensuring best-sellers stay cached.

---

## 3. First In, First Out (FIFO)

**Definition:**  
Evict entries in the same order they were inserted, regardless of access pattern.

**When to use:**  
Simple scenarios where insertion order correlates with obsolescence (e.g., time-based logs, streaming windows).

**Pros:**  
- Easy to implement with a queue.  

**Cons:**  
- Doesn’t account for access frequency or recency; may evict hot items.

**Example:**  
An analytics pipeline caches the last N ingestion events. As new events arrive, the oldest event in the cache is removed, maintaining a sliding window of the most recent N events.

---

## 4. Random Replacement

**Definition:**  
Evict a randomly chosen entry when space is needed.

**When to use:**  
Systems where simple eviction with minimal overhead is preferred, and access patterns are uniform or unpredictable.

**Pros:**  
- Extremely low overhead; no bookkeeping required.  
- Avoids pathological cases that foil LRU or LFU.

**Cons:**  
- May evict frequently accessed items by chance.

**Example:**  
A CDN edge server caches static assets. To keep the cache simple and fast, it randomly evicts cached objects when full, trading off some hit ratio for minimal management cost.

---

**Choosing an eviction policy** depends on your application’s access patterns and performance priorities:

- **LRU** for recency-driven workloads  
- **LFU** for frequency-driven workloads  
- **FIFO** for simple, order-based scenarios  
- **Random** for minimal overhead and uniform access patterns  
