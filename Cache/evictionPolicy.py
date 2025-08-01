"""
Cache eviction policies implementations in Python:
- Least Recently Used (LRU)
- Least Frequently Used (LFU)
- First In, First Out (FIFO)
- Random Replacement
"""

import collections
import random
import time

# 1. Least Recently Used (LRU)
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = collections.OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None
        # Move key to end to mark as recently used
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def put(self, key, value):
        if key in self.cache:
            # Remove old
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            # Evict least recently used (first item)
            self.cache.popitem(last=False)
        # Insert item as most recently used
        self.cache[key] = value


# 2. Least Frequently Used (LFU)
class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.values = {}                 # key -> value
        self.freq = {}                   # key -> freq count
        self.freq_list = collections.defaultdict(collections.OrderedDict)
        self.min_freq = 0

    def _update_freq(self, key):
        f = self.freq[key]
        # Remove from current freq list
        self.freq_list[f].pop(key)
        if not self.freq_list[f] and f == self.min_freq:
            self.min_freq += 1
        # Increment freq
        self.freq[key] += 1
        f_new = f + 1
        self.freq_list[f_new][key] = True

    def get(self, key):
        if key not in self.values:
            return None
        self._update_freq(key)
        return self.values[key]

    def put(self, key, value):
        if self.capacity <= 0:
            return
        if key in self.values:
            self.values[key] = value
            self._update_freq(key)
            return
        if len(self.values) >= self.capacity:
            # Evict least frequently used key
            k_evict, _ = self.freq_list[self.min_freq].popitem(last=False)
            self.values.pop(k_evict)
            self.freq.pop(k_evict)
        # Insert new key
        self.values[key] = value
        self.freq[key] = 1
        self.min_freq = 1
        self.freq_list[1][key] = True


# 3. First In, First Out (FIFO)
class FIFOCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = collections.deque()
        self.cache = {}

    def get(self, key):
        return self.cache.get(key, None)

    def put(self, key, value):
        if key in self.cache:
            self.cache[key] = value
            return
        if len(self.queue) >= self.capacity:
            # Evict oldest inserted key
            oldest = self.queue.popleft()
            self.cache.pop(oldest, None)
        # Insert new key
        self.queue.append(key)
        self.cache[key] = value


# 4. Random Replacement
class RandomCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}

    def get(self, key):
        return self.cache.get(key, None)

    def put(self, key, value):
        if key in self.cache:
            self.cache[key] = value
            return
        if len(self.cache) >= self.capacity:
            # Evict a random key
            k_evict = random.choice(list(self.cache.keys()))
            self.cache.pop(k_evict)
        self.cache[key] = value


# Example usage:
if __name__ == "__main__":
    # LRU
    lru = LRUCache(2)
    lru.put('a', 1)
    lru.put('b', 2)
    print(lru.get('a'))  # 1
    lru.put('c', 3)      # evicts 'b'
    print(lru.get('b'))  # None

    # LFU
    lfu = LFUCache(2)
    lfu.put('x', 10)
    lfu.put('y', 20)
    print(lfu.get('x'))  # 10
    lfu.put('z', 30)     # evicts 'y' (freq=1, oldest), 'x' freq=2
    print(lfu.get('y'))  # None

    # FIFO
    fifo = FIFOCache(2)
    fifo.put('p', 'P')
    fifo.put('q', 'Q')
    fifo.put('r', 'R')   # evicts 'p'
    print(fifo.get('p')) # None

    # Random
    rnd = RandomCache(2)
    rnd.put('m', 100)
    rnd.put('n', 200)
    rnd.put('o', 300) 
    print(rnd.get('m'), rnd.get('n'), rnd.get('o'))
