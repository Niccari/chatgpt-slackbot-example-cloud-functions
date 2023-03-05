#!/bin/sh

source .env.production

echo "**These environment variables will be set. proceed? (y/N)**"
echo "- PROJECT_ID: $PROJECT_ID"
echo "- REGION: $REGION"
echo "- FUNCTIONS_URL: $FUNCTIONS_URL"
echo "- OIDC_TOKEN_SERVICE_ACCOUNT: $OIDC_TOKEN_SERVICE_ACCOUNT"
read input 

if [ $input = 'y' ] ; then
    echo "start deploying..."
else
    echo "aborted."
    exit 1
fi

gcloud functions deploy chatgpt-slackbot \
  --gen2 \
  --entry-point chatgpt_slackbot \
  --project=${PROJECT_ID} \
  --region=${REGION} \
  --runtime=python311 \
  --set-env-vars PROJECT_ID=${PROJECT_ID},REGION=${REGION},FUNCTIONS_URL=${FUNCTIONS_URL},OIDC_TOKEN_SERVICE_ACCOUNT=${OIDC_TOKEN_SERVICE_ACCOUNT} \
  --set-secrets OPENAI_API_KEY=openai_api_key:latest,SLACK_BOT_TOKEN=slack_bot_token:latest,SLACK_SIGNING_SECRET=slack_signing_secret:latest,ORGANIZATION_ID=organization_id:latest \
  --trigger-http \
  --allow-unauthenticated \
  --timeout 120
