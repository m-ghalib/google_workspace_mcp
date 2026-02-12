# Document Resource

The root resource representing a Google Docs document.

## Document

| Field | Type | Description |
|-------|------|-------------|
| `documentId` | string | Output only. Unique document identifier. |
| `title` | string | The document title. |
| `tabs[]` | [`Tab`](./08-tabs.md) | Document tabs (populated when `includeTabsContent=true`). |
| `revisionId` | string | Output only. Opaque revision identifier for optimistic concurrency. |
| `suggestionsViewMode` | enum [`SuggestionsViewMode`](./11-enums.md#suggestionsviewmode) | Output only. Current suggestions rendering mode. |
| `body` | [`Body`](./03-structural-elements.md#body) | Output only. Main document content (legacy; use `tabs` instead). |
| `headers` | map<string, [`Header`](./03-structural-elements.md#header)> | Output only. Headers keyed by header ID. |
| `footers` | map<string, [`Footer`](./03-structural-elements.md#footer)> | Output only. Footers keyed by footer ID. |
| `footnotes` | map<string, [`Footnote`](./03-structural-elements.md#footnote)> | Output only. Footnotes keyed by footnote ID. |
| `documentStyle` | [`DocumentStyle`](./05-styles.md#documentstyle) | Output only. Document-wide style settings. |
| `namedStyles` | [`NamedStyles`](./05-styles.md#namedstyles) | Output only. Named style definitions. |
| `lists` | map<string, [`List`](./07-lists-named-ranges.md#list)> | Output only. List definitions keyed by list ID. |
| `namedRanges` | map<string, [`NamedRanges`](./07-lists-named-ranges.md#namedranges)> | Output only. Named ranges keyed by name. |
| `inlineObjects` | map<string, [`InlineObject`](./06-objects.md#inlineobject)> | Output only. Inline objects keyed by object ID. |
| `positionedObjects` | map<string, [`PositionedObject`](./06-objects.md#positionedobject)> | Output only. Positioned objects keyed by object ID. |

### Sample Response

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
        "body": { "content": [ "... 273 structural elements ..." ] },
        "documentStyle": { "pageSize": { "height": { "magnitude": 792, "unit": "PT" }, "width": { "magnitude": 612, "unit": "PT" } } },
        "namedStyles": { "styles": [ "... 9 named styles ..." ] }
      }
    }
  ]
}
```

### Notes

- When `includeTabsContent=true` on `documents.get`, content is in `tabs[].documentTab` and the legacy fields (`body`, `headers`, etc.) are empty.
- When `includeTabsContent=false` (default), the first tab's content populates the legacy fields.
