"""Fetch sample Google Docs and save raw API responses for documentation."""

import asyncio
import json
import re
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from auth.google_auth import get_authenticated_google_service
from auth.scopes import DOCS_READONLY_SCOPE

DOCS = {
    "13s5gHpPQmUOmkLHAYW78GoI07lT86zgbrgi3n9aF2Jw": "sample_document.json",
    "1u73oEpxyxRhc0ZZOrr9NSqnJeBu1OX_DP2Ag1HeXfsk": None,  # derive from title
    "1JFRW2hcjues_DiWueXTmmvmP4f4pvgyLp-8KRQXqlxQ": None,
    "18TO5z2CcVIOXtoRbR-KammEvNRSDDZnn6sWqEty5jtA": None,
}
USER_EMAIL = "momin.ghalib@xometry.com"
SAMPLES_DIR = Path(__file__).parent


def slugify(title: str) -> str:
    """Convert doc title to a filename-safe slug."""
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = slug.strip("_")
    return f"sample_{slug}.json"


async def main():
    service, _ = await get_authenticated_google_service(
        service_name="docs",
        version="v1",
        tool_name="extract_api_samples",
        user_google_email=USER_EMAIL,
        required_scopes=[DOCS_READONLY_SCOPE],
    )

    for doc_id, filename in DOCS.items():
        doc = await asyncio.to_thread(
            service.documents()
            .get(documentId=doc_id, includeTabsContent=True)
            .execute
        )

        if filename is None:
            filename = slugify(doc.get("title", doc_id))

        out_path = SAMPLES_DIR / filename
        out_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False))
        raw_size = len(json.dumps(doc))
        print(f"Saved {raw_size:,} bytes → {out_path.name}")

    service.close()
    print(f"\nDone. {len(DOCS)} documents saved to {SAMPLES_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
