import requests
import os
import sys

# Base URL for the FOSSA API
FOSSA_API = "https://app.fossa.com/api"

# The SBOM file to upload (must exist in the same directory as the script)
SBOM_FILE = "file.spdx"

# Your FOSSA API token (should be set in your environment)
FOSSA_TOKEN = os.getenv("FOSSA_TOKEN")

# Project details — customize these for each upload
PACKAGE_SPEC = "chelsea-sbom-test-2025"  # Arbitrary project/package name in FOSSA
REVISION = "test-1"                      # Can be a commit SHA, version number, etc.

# Exit early if token is missing
if not FOSSA_TOKEN:
    print("Error: FOSSA_TOKEN environment variable not set.")
    sys.exit(1)

# STEP 1: Request a signed URL for uploading the SBOM file
try:
    signed_url_resp = requests.get(
        f"{FOSSA_API}/components/signed_url",
        headers={"Authorization": f"Bearer {FOSSA_TOKEN}"},
        params={
            "packageSpec": PACKAGE_SPEC,
            "revision": REVISION,
            "fileType": "sbom"
        }
    )
except Exception as e:
    print("Error requesting signed URL:", e)
    sys.exit(1)

# Optional: Show full response (for debugging)
print("DEBUG: Response from signed_url:", signed_url_resp.text)

# Ensure the request succeeded
if signed_url_resp.status_code != 200:
    print("Failed to get signed URL:", signed_url_resp.status_code, signed_url_resp.text)
    sys.exit(1)

# Extract the signed S3 upload URL from the response
signed_url = signed_url_resp.json().get("signedUrl")
if not signed_url:
    print("Error: Signed URL not found in response.")
    sys.exit(1)

# STEP 2: Upload the SBOM file to the signed URL
try:
    with open(SBOM_FILE, 'rb') as f:
        upload_resp = requests.put(
            signed_url,
            headers={"Content-Type": "application/octet-stream"},
            data=f
        )
except FileNotFoundError:
    print(f"Error: Could not find the SBOM file: {SBOM_FILE}")
    sys.exit(1)
except Exception as e:
    print("Error uploading SBOM:", e)
    sys.exit(1)

# Ensure the upload was successful
if upload_resp.status_code != 200:
    print("Failed to upload SBOM:", upload_resp.status_code, upload_resp.text)
    sys.exit(1)

# STEP 3: Trigger a build in FOSSA to process the uploaded SBOM
build_payload = {
    "selectedTeams": [],  # Leave empty unless you want to assign to specific teams
    "archives": [
        {
            "packageSpec": PACKAGE_SPEC,
            "revision": REVISION,
            "fileType": "sbom"
        }
    ]
}

try:
    build_resp = requests.post(
        f"{FOSSA_API}/components/build?fileType=sbom",
        headers={
            "Authorization": f"Bearer {FOSSA_TOKEN}",
            "Content-Type": "application/json"
        },
        json=build_payload
    )
except Exception as e:
    print("Error triggering FOSSA build:", e)
    sys.exit(1)

# Confirm the build was triggered
if build_resp.status_code != 201:
    print("Failed to trigger build:", build_resp.status_code, build_resp.text)
    sys.exit(1)

# ✅ Success!
print("SBOM uploaded and build triggered successfully.")
