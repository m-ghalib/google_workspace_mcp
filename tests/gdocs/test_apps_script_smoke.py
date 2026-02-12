"""
Smoke test: verify Apps Script Execution API round-trip works.

Tests the full pipeline: Python → Execution API → DocumentApp → result
against a known sample document (Job Offer Findings, smallest at 154KB).

Usage:
    op run -- uv run --env-file .env python tests/gdocs/test_apps_script_smoke.py
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from auth.credential_store import get_credential_store
from auth.google_auth import get_credentials
from googleapiclient.discovery import build

# Known sample document (smallest, 154KB)
SAMPLE_DOC_ID = "18TO5z2CcVIOXtoRbR-KammEvNRSDDZnn6sWqEty5jtA"
EXPECTED_TITLE = "Job Offer Findings"

# REST API sample for comparison
SAMPLE_JSON_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../gdocs/docs/docs_api/samples/sample_job_offer_findings.json",
)


def get_script_service(user_email: str):
    """Build authenticated Apps Script service.

    Scopes must match the script's appsscript.json manifest:
    - documents: for DocumentApp.openById()
    - script.external_request: for UrlFetchApp (image insertion)
    """
    scopes = [
        "https://www.googleapis.com/auth/documents",
        "https://www.googleapis.com/auth/script.external_request",
    ]
    credentials = get_credentials(
        user_google_email=user_email,
        required_scopes=scopes,
        client_secrets_path=os.getenv("GOOGLE_CLIENT_SECRETS_PATH"),
    )
    if not credentials or not credentials.valid:
        raise RuntimeError(
            f"No valid credentials for {user_email}. "
            "Run an MCP tool first to complete OAuth flow."
        )
    return build("script", "v1", credentials=credentials)


def call_apps_script(service, function_name: str, parameters: list = None) -> dict:
    """Call an Apps Script function and return the result."""
    script_id = os.getenv("APPS_SCRIPT_ID")
    if not script_id:
        raise RuntimeError("APPS_SCRIPT_ID not set in environment")

    body = {"function": function_name, "devMode": True}
    if parameters:
        body["parameters"] = parameters

    t0 = time.time()
    response = service.scripts().run(scriptId=script_id, body=body).execute()
    elapsed = time.time() - t0

    if "error" in response:
        error = response["error"]
        details = error.get("details", [{}])
        msg = details[0].get("errorMessage", error.get("message", "Unknown"))
        raise RuntimeError(f"Apps Script error: {msg}")

    result = response.get("response", {}).get("result")
    print(f"  [{function_name}] {elapsed:.2f}s")
    return result


def run_tests():
    # Auto-discover user email from credential store (single-user mode)
    user_email = os.getenv("GOOGLE_USER_EMAIL")
    if not user_email:
        store = get_credential_store()
        users = store.list_users()
        if not users:
            print("ERROR: No stored credentials found. Run an MCP tool first to complete OAuth.")
            sys.exit(1)
        user_email = users[0]
        print(f"Auto-discovered user: {user_email}")

    print(f"Using email: {user_email}")
    print(f"Script ID:   {os.getenv('APPS_SCRIPT_ID', 'NOT SET')}")
    print()

    service = get_script_service(user_email)
    passed = 0
    failed = 0

    # ── Test 1: getDocContent ──────────────────────────────────
    print("Test 1: getDocContent (basic read)")
    try:
        result = call_apps_script(
            service, "getDocContent", [SAMPLE_DOC_ID, {}]
        )
        assert result is not None, "Got None result"
        assert result["title"] == EXPECTED_TITLE, (
            f"Title mismatch: {result['title']} != {EXPECTED_TITLE}"
        )
        assert result["documentId"] == SAMPLE_DOC_ID
        assert len(result["content"]) > 0, "Empty content"
        print(f"  PASS — title='{result['title']}', content={len(result['content'])} chars")
        passed += 1
    except Exception as e:
        print(f"  FAIL — {e}")
        failed += 1

    # ── Test 2: getDocContent with structure ───────────────────
    print("Test 2: getDocContent (with structure)")
    try:
        result = call_apps_script(
            service, "getDocContent", [SAMPLE_DOC_ID, {"includeStructure": True}]
        )
        assert "structure" in result, "Missing 'structure' key"
        assert len(result["structure"]) > 0, "Empty structure"
        elem_types = set(e["type"] for e in result["structure"])
        print(f"  PASS — {len(result['structure'])} elements, types: {elem_types}")
        passed += 1
    except Exception as e:
        print(f"  FAIL — {e}")
        failed += 1

    # ── Test 3: getDocumentStructure ──────────────────────────
    print("Test 3: getDocumentStructure (detailed tree)")
    try:
        result = call_apps_script(
            service, "getDocumentStructure", [SAMPLE_DOC_ID]
        )
        assert result["title"] == EXPECTED_TITLE
        assert result["totalElements"] > 0
        assert result["statistics"]["paragraphs"] >= 0
        assert result["statistics"]["tables"] >= 0
        print(
            f"  PASS — {result['totalElements']} elements, "
            f"{result['statistics']['tables']} tables, "
            f"{len(result.get('tables', []))} table previews"
        )
        passed += 1
    except Exception as e:
        print(f"  FAIL — {e}")
        failed += 1

    # ── Test 4: Cross-validate against REST API sample ────────
    print("Test 4: Cross-validate title with REST API sample")
    try:
        with open(SAMPLE_JSON_PATH) as f:
            rest_sample = json.load(f)
        rest_title = rest_sample["title"]
        apps_result = call_apps_script(
            service, "getDocContent", [SAMPLE_DOC_ID, {}]
        )
        assert apps_result["title"] == rest_title, (
            f"Title mismatch: Apps Script='{apps_result['title']}' vs REST='{rest_title}'"
        )
        print(f"  PASS — Both APIs return title='{rest_title}'")
        passed += 1
    except FileNotFoundError:
        print(f"  SKIP — Sample JSON not found at {SAMPLE_JSON_PATH}")
    except Exception as e:
        print(f"  FAIL — {e}")
        failed += 1

    # ── Summary ───────────────────────────────────────────────
    print()
    print(f"Results: {passed} passed, {failed} failed")
    if failed > 0:
        sys.exit(1)
    print("Apps Script Execution API is working correctly.")


if __name__ == "__main__":
    run_tests()
