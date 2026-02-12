# Methods — `documents`

## documents.get

Retrieves the latest version of a document.

```
GET https://docs.googleapis.com/v1/documents/{documentId}
```

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `documentId` | string | **Required.** The ID of the document to retrieve. |

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `suggestionsViewMode` | enum (`SuggestionsViewMode`) | Mode for rendering suggestions. Default: `DEFAULT_FOR_CURRENT_ACCESS`. |
| `includeTabsContent` | boolean | If `true`, populates `Document.tabs` instead of legacy `body` field. |

### Request Body

Empty.

### Response

Returns a [`Document`](./02-document-resource.md) resource.

#### Sample Response

```json
{
  "documentId": "13s5gHpPQmUOmkLHAYW78GoI07lT86zgbrgi3n9aF2Jw",
  "title": "Copy of Partner Management Roles and Responsibilities",
  "revisionId": "AONSffwgDYQhl-HDHASniZIWmv2Me23lKwgJ7ne...",
  "suggestionsViewMode": "SUGGESTIONS_INLINE",
  "tabs": [
    {
      "tabProperties": { "tabId": "t.0", "title": "Partner Management Roles and Responsibilities", "index": 0 },
      "documentTab": {
        "body": { "content": [ "..." ] },
        "documentStyle": { "..." : "..." },
        "namedStyles": { "styles": [ "..." ] }
      }
    },
    {
      "tabProperties": { "tabId": "t.cham5uds7eg4", "title": "Tab 2", "index": 1 },
      "documentTab": { "..." : "..." }
    }
  ]
}
```

> With `includeTabsContent=true`, the root-level `body`, `headers`, `footers`, etc. are empty — all content lives under `tabs[].documentTab`.

### Scopes

Requires one of:
- `documents` / `documents.readonly`
- `drive` / `drive.readonly` / `drive.file`

---

## documents.create

Creates a blank document with a given title.

```
POST https://docs.googleapis.com/v1/documents
```

### Request Body

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | The title of the new document. |

> All other fields in the request body (including content) are **ignored**.

### Response

Returns the newly created [`Document`](./02-document-resource.md) resource with all fields populated.

### Scopes

Requires one of: `documents`, `drive`, `drive.file`

---

## documents.batchUpdate

Applies one or more updates to a document atomically.

```
POST https://docs.googleapis.com/v1/documents/{documentId}:batchUpdate
```

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `documentId` | string | **Required.** The ID of the document to update. |

### Request Body

| Field | Type | Description |
|-------|------|-------------|
| `requests[]` | [`Request`](./09-batch-update-requests.md) | Array of update operations applied sequentially. |
| `writeControl` | `WriteControl` | Optional write control for concurrent editing. |

#### WriteControl

| Field | Type | Description |
|-------|------|-------------|
| `requiredRevisionId` | string | Revision ID the client is based on. Fails if stale. |
| `targetRevisionId` | string | Target revision ID. Optional alternative to `requiredRevisionId`. |

### Response Body

| Field | Type | Description |
|-------|------|-------------|
| `replies[]` | [`Response`](./10-batch-update-responses.md) | Responses for each request (same order). Empty responses for requests that don't produce output. |
| `writeControl` | `WriteControl` | Updated write control with new revision ID. |
| `documentId` | string | The document ID. |

### Scopes

Requires one of: `documents`, `drive`, `drive.file`
