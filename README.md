# sleep_test

Cloud Run Background Processing with Cloud Storage Trigger (Up to 60 minutes)

## Overview

This project demonstrates how to build an **event-driven Cloud Run service** that handles **Cloud Storage upload events** and performs **long-running background processing (up to 60 minutes)**.
Because Cloud Functions (Gen1 & Gen2) only support a max timeout of 540 seconds (9 minutes), this solution uses **Cloud Run + Eventarc** with a **non-blocking background thread**.

## Architecture

1. A file is uploaded to a Cloud Storage bucket.
2. Eventarc triggers a Cloud Run service via an HTTP POST request.
3. The Cloud Run service:
   - Immediately returns `204 No Content` to avoid retries.
   - Launches a background thread to process the file (sleep simulation: 1min, 10min, or 60min).

## Project Structure

```
cloudrun/
 ├── main.py
 ├── requirements.txt
 └── Dockerfile 
```

## Example Event Handling Logic

```python
if name.startswith("sleep_1min"):
    sleep_time = 60
elif name.startswith("sleep_10min"):
    sleep_time = 600
elif name.startswith("sleep_60min"):
    sleep_time = 3600
```

## Deployment Steps

1. Build and deploy the Cloud Run service:

```
gcloud run deploy sleep-handler \
  --source . \
  --region asia-northeast1 \
  --memory 512Mi \
  --timeout 3600 \
  --no-allow-unauthenticated
```

2. Create an Eventarc trigger for Cloud Storage events:

```
gcloud eventarc triggers create storage-upload-trigger \
  --location=asia-northeast1 \
  --destination-run-service=sleep-handler \
  --destination-run-region=asia-northeast1 \
  --event-filters="type=google.cloud.storage.object.v1.finalized" \
  --event-filters="bucket=YOUR_BUCKET_NAME" \
  --service-account=$(gcloud projects describe $(gcloud config get-value project) --format="value(projectNumber)")-compute@developer.gserviceaccount.com
```

## Test

1. Upload a test file:

```
gcloud run services logs read sleep-handler --region=asia-northeast1
```

2. Check Logs

```
gcloud run services logs read sleep-handler --region=asia-northeast1

```

## Notes

- Eventarc requires an immediate HTTP 2xx response, otherwise it will retry.
- The actual processing is done in a background thread to ensure fast HTTP response.
- For critical workloads, consider using Cloud Tasks for guaranteed long-running async jobs.

