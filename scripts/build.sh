#!/bin/bash
set -euo pipefail

# --- Configuration ---
if [ ! -f .env ]; then
  echo "❌ ERROR: .env file not found. Copy .env.example to .env and fill in the values."
  exit 1
fi

source .env

IMAGE="docker.io/${DOCKER_USERNAME}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"

echo "🏗️  Building image for linux/amd64..."
docker build --platform linux/amd64 -t "${IMAGE}" .

echo "🚀 Pushing image to Docker Hub..."
docker push "${IMAGE}"

echo "✅ Build and push complete: ${IMAGE}"
