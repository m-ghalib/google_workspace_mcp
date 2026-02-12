# BatchUpdate Response Types

Each response in the `replies[]` array corresponds to the request at the same index. Requests that don't produce meaningful output return empty response objects.

## ReplaceAllTextResponse

Returned by `ReplaceAllTextRequest`.

| Field | Type | Description |
|-------|------|-------------|
| `occurrencesChanged` | integer | Number of text occurrences replaced. |

---

## CreateNamedRangeResponse

Returned by `CreateNamedRangeRequest`.

| Field | Type | Description |
|-------|------|-------------|
| `namedRangeId` | string | The ID of the created named range. |

---

## InsertInlineImageResponse

Returned by `InsertInlineImageRequest`.

| Field | Type | Description |
|-------|------|-------------|
| `objectId` | string | The ID of the created inline object. |

---

## InsertInlineSheetsChartResponse

Returned by `InsertInlineSheetsChartRequest`.

| Field | Type | Description |
|-------|------|-------------|
| `objectId` | string | The object ID of the inserted chart. |

---

## CreateHeaderResponse

Returned by `CreateHeaderRequest`.

| Field | Type | Description |
|-------|------|-------------|
| `headerId` | string | The ID of the created header. |

---

## CreateFooterResponse

Returned by `CreateFooterRequest`.

| Field | Type | Description |
|-------|------|-------------|
| `footerId` | string | The ID of the created footer. |

---

## CreateFootnoteResponse

Returned by `CreateFootnoteRequest`.

| Field | Type | Description |
|-------|------|-------------|
| `footnoteId` | string | The ID of the created footnote. |

---

## AddDocumentTabResponse

Returned by `AddDocumentTabRequest`.

| Field | Type | Description |
|-------|------|-------------|
| `tabProperties` | [`TabProperties`](./08-tabs.md#tabproperties) | Properties of the newly added tab. |
