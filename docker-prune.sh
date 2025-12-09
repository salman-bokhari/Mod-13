#!/bin/bash
set -e

echo "Stopping all running containers..."
docker ps -q | xargs -r docker stop

echo "Removing all containers, networks, images, and volumes..."
docker system prune -af

echo "Starting fresh Postgres container..."
docker run --name mod13-postgres \
  -e POSTGRES_USER=testuser \
  -e POSTGRES_PASSWORD=testpass \
  -e POSTGRES_DB=testdb \
  -p 5432:5432 \
  -d postgres:15

echo "Done! Postgres container 'mod13-postgres' is running on port 5432."

