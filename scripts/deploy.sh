#!/bin/bash
set -euo pipefail

# --- Configuration ---
if [ ! -f .env ]; then
  echo "❌ ERROR: .env file not found. Copy .env.example to .env and fill in the values."
  exit 1
fi

source .env

# Default to public image unless --custom flag is passed
MODE=${1:-""}
IMAGE="docker.io/${PUBLIC_IMAGE_URI}"

if [ "$MODE" == "--custom" ]; then
    IMAGE="docker.io/${DOCKER_USERNAME}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
    echo "📦 Using CUSTOM image: ${IMAGE}"
else
    echo "📦 Using pre-built PUBLIC image: ${IMAGE}"
fi

echo "⚙️  Enabling required GCP APIs..."
gcloud services enable run.googleapis.com aiplatform.googleapis.com \
  --project="${GCP_PROJECT_ID}"

echo "🚢 Deploying ${CLOUD_RUN_SERVICE_NAME} to Cloud Run..."
gcloud run deploy "${CLOUD_RUN_SERVICE_NAME}" \
  --image "${IMAGE}" \
  --project "${GCP_PROJECT_ID}" \
  --region "${LOCATION}" \
  --allow-unauthenticated \
  --set-env-vars "GCP_PROJECT_ID=${GCP_PROJECT_ID},LOCATION=${LOCATION},MODEL_ID=${MODEL_ID},RULES_FILE=${RULES_FILE}"

echo "🔍 Fetching Cloud Run service account..."
SA=$(gcloud run services describe "${CLOUD_RUN_SERVICE_NAME}" \
  --project "${GCP_PROJECT_ID}" \
  --region "${LOCATION}" \
  --format "value(spec.template.spec.serviceAccountName)")

echo "🔐 Granting roles/aiplatform.user to ${SA}..."
gcloud projects add-iam-policy-binding "${GCP_PROJECT_ID}" \
  --member "serviceAccount:${SA}" \
  --role "roles/aiplatform.user" \
  --condition=None

echo "✅ Deployment complete!"
URL=$(gcloud run services describe "${CLOUD_RUN_SERVICE_NAME}" \
  --project "${GCP_PROJECT_ID}" \
  --region "${LOCATION}" \
  --format "value(status.url)")

echo "🔗 Service URL: ${URL}"
echo "📝 Test with:"
echo "curl -X POST ${URL}/v1/review -H 'Content-Type: application/json' -d '{\"content\": \"Store admin password in plaintext config file.\"}'"
