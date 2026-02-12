"""Smoke test: verify Apps Script Execution API round-trip works."""

import asyncio
import json
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from auth.google_auth import get_authenticated_google_service
from auth.scopes import DOCS_WRITE_SCOPE, SCRIPT_PROJECTS_SCOPE, SCRIPT_EXTERNAL_REQUEST_SCOPE
from gdocs.apps_script_client import run_apps_script

# Use the smallest sample doc (job offer findings, 154KB)
DOC_ID = "1JFRW2hcjues_DiWueXTmmvmP4f4pvgyLp-8KRQXqlxQ"
USER_EMAIL = "momin.ghalib@xometry.com"


async def main():
    # Build the script service (not docs service)
    service, _ = await get_authenticated_google_service(
        service_name="script",
        version="v1",
        tool_name="smoke_test_apps_script",
        user_google_email=USER_EMAIL,
        required_scopes=[SCRIPT_PROJECTS_SCOPE, SCRIPT_EXTERNAL_REQUEST_SCOPE, DOCS_WRITE_SCOPE],
    )

    # --- Test 1: getDocContent (basic read) ---
    print("\n[Test 1] getDocContent...")
    t0 = time.perf_counter()
    result = await run_apps_script(service, "getDocContent", [DOC_ID])
    elapsed = time.perf_counter() - t0
    print(f"  Title: {result['title']}")
    print(f"  Content length: {len(result.get('content', ''))} chars")
    print(f"  Latency: {elapsed:.2f}s")

    # --- Test 2: getDocumentStructure (structure parsing) ---
    print("\n[Test 2] getDocumentStructure...")
    t0 = time.perf_counter()
    result = await run_apps_script(service, "getDocumentStructure", [DOC_ID])
    elapsed = time.perf_counter() - t0
    stats = result.get("statistics", {})
    print(f"  Total elements: {result.get('totalElements', 0)}")
    print(f"  Tables: {stats.get('tables', 0)}")
    print(f"  Table details:")
    for t in result.get("tables", []):
        preview_row = t["preview"][0] if t.get("preview") else []
        print(f"    Table {t['tableIndex']}: {t['rows']}x{t['columns']} — headers: {preview_row}")
    print(f"  Latency: {elapsed:.2f}s")

    # --- Test 3: getDocContent with structure (combined) ---
    print("\n[Test 3] getDocContent + includeStructure...")
    t0 = time.perf_counter()
    result = await run_apps_script(service, "getDocContent", [DOC_ID, {"includeStructure": True}])
    elapsed = time.perf_counter() - t0
    structure = result.get("structure", [])
    headings = [e for e in structure if e.get("heading", "").startswith("HEADING")]
    print(f"  Structure elements: {len(structure)}")
    print(f"  Headings found: {len(headings)}")
    for h in headings[:5]:
        print(f"    {h['heading']}: {h['text'][:80]}")
    print(f"  Latency: {elapsed:.2f}s")

    print("\n--- All tests passed ---")


if __name__ == "__main__":
    asyncio.run(main())
