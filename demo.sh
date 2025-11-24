#!/bin/bash
echo "Starting Redis HA Cluster Demo..."
docker-compose up -d
sleep 10
pip install redis
python src/redis_ha_cluster.py
