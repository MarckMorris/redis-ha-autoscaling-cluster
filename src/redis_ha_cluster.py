# -*- coding: utf-8 -*-
"""
Redis High-Availability Cluster - Simplified Demo
"""

import redis
import time
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RedisClusterDemo:
    def __init__(self):
        self.master = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.slaves = [
            redis.Redis(host='localhost', port=6380, decode_responses=True),
            redis.Redis(host='localhost', port=6381, decode_responses=True)
        ]
        
    def check_health(self):
        """Check cluster health"""
        print("\n" + "=" * 80)
        print(f"REDIS HA CLUSTER STATUS - {datetime.now()}")
        print("=" * 80)
        
        # Check master
        try:
            self.master.ping()
            info = self.master.info()
            print(f"\nMASTER (port 6379): HEALTHY")
            print(f"  Connected clients: {info.get('connected_clients', 0)}")
            print(f"  Used memory: {info.get('used_memory_human', '0')}")
            print(f"  Total commands: {info.get('total_commands_processed', 0):,}")
            print(f"  Connected slaves: {info.get('connected_slaves', 0)}")
        except Exception as e:
            print(f"\nMASTER (port 6379): DOWN - {e}")
        
        # Check slaves
        for i, slave in enumerate(self.slaves, 1):
            try:
                slave.ping()
                print(f"\nSLAVE {i} (port {6379+i}): HEALTHY")
            except Exception as e:
                print(f"\nSLAVE {i} (port {6379+i}): DOWN - {e}")
        
        print("=" * 80)
    
    def simulate_load(self):
        """Simulate operations"""
        try:
            for i in range(100):
                self.master.set(f"key_{i}", f"value_{i}")
                self.master.get(f"key_{i}")
            logger.info("Executed 200 operations (100 SET + 100 GET)")
        except Exception as e:
            logger.error(f"Load simulation failed: {e}")
    
    def run(self):
        print("\n" + "=" * 80)
        print("Redis HA Cluster - DEMO")
        print("=" * 80)
        
        for i in range(6):
            self.check_health()
            self.simulate_load()
            time.sleep(10)
        
        print("\nDEMO COMPLETE!")


if __name__ == "__main__":
    demo = RedisClusterDemo()
    demo.run()
