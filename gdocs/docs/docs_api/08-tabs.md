# Tabs

Multi-tab document support (introduced to support tabbed document structure).

## Tab

A document tab containing content and metadata.

| Field | Type | Description |
|-------|------|-------------|
| `tabProperties` | [`TabProperties`](#tabproperties) | Tab metadata. |
| `childTabs[]` | [`Tab`](#tab) | Nested child tabs. |
| `documentTab` | [`DocumentTab`](#documenttab) | The tab's content. |

### Sample Response

```json
{
  "tabProperties": {
    "tabId": "t.0",
    "title": "Partner Management Roles and Responsibilities",
    "index": 0
  },
  "documentTab": {
    "body": {
      "content": [ "... 273 structural elements ..." ]
    },
    "documentStyle": {
      "pageSize": {
        "height": { "magnitude": 792, "unit": "PT" },
        "width": { "magnitude": 612, "unit": "PT" }
      },
      "marginTop": { "magnitude": 72, "unit": "PT" },
      "documentFormat": { "documentMode": "PAGELESS" }
    },
    "namedStyles": {
      "styles": [ "... 9 named styles (NORMAL_TEXT, TITLE, HEADING_1–6, SUBTITLE) ..." ]
    }
  }
}
```

> With `includeTabsContent=true`, each tab's `documentTab` mirrors the root Document structure. This 2-tab document has tab IDs `t.0` and `t.cham5uds7eg4`.

### Sample Response — Hierarchical Tabs with Child Tabs

```json
{
  "tabProperties": {
    "tabId": "t.dfdw4zha1oav",
    "title": "Completed",
    "index": 2
  },
  "childTabs": [
    {
      "tabProperties": {
        "tabId": "t.7vtku6ypfk3c",
        "title": "Round 1: Main Navigation",
        "parentTabId": "t.dfdw4zha1oav",
        "index": 0,
        "nestingLevel": 1
      },
      "documentTab": {
        "body": {
          "content": [
            {
              "endIndex": 1,
              "sectionBreak": {
                "sectionStyle": {
                  "columnSeparatorStyle": "NONE",
                  "contentDirection": "LEFT_TO_RIGHT",
                  "sectionType": "CONTINUOUS"
                }
              }
            }
          ]
        }
      }
    }
  ]
}
```

> A parent tab ("Completed") with a nested child tab. Child tabs include `parentTabId` linking back to the parent and `nestingLevel: 1` indicating one level deep. Each child tab has its own independent `documentTab` with body content. This enables outline-style document organization (e.g., grouping completed feature specs under a parent tab).

---

## TabProperties

Configuration metadata for a document tab.

| Field | Type | Description |
|-------|------|-------------|
| `tabId` | string | Immutable. Unique tab identifier. |
| `title` | string | User-visible tab name. |
| `parentTabId` | string | Optional. ID of parent tab (empty for root-level). |
| `index` | integer | Zero-based position within parent. |
| `nestingLevel` | integer | Output only. Depth in tab hierarchy. |
| `iconEmoji` | string | Optional. Unicode emoji displayed with tab name. |

### Sample Response — Multi-Tab Document

```json
[
  { "tabId": "t.0", "title": "Product Brief - The Why", "index": 0 },
  { "tabId": "t.ker7bo1h35gv", "title": "Requirements/Scope - The How", "index": 1 },
  { "tabId": "t.zhnysc1ong96", "title": "Readout", "index": 0 },
  { "tabId": "t.oy9qgwojx2u", "title": "Appendix", "index": 1 }
]
```

> Tab IDs use two formats: `t.0` for the default first tab, and `t.<hash>` for subsequent tabs. Tab titles are user-editable strings. The `index` is zero-based within the parent (or within root-level tabs if no parent).

---

## DocumentTab

The content container for a tab. Mirrors the top-level Document structure.

| Field | Type | Description |
|-------|------|-------------|
| `body` | [`Body`](./03-structural-elements.md#body) | Main content. |
| `headers` | map<string, [`Header`](./03-structural-elements.md#header)> | Headers keyed by ID. |
| `footers` | map<string, [`Footer`](./03-structural-elements.md#footer)> | Footers keyed by ID. |
| `footnotes` | map<string, [`Footnote`](./03-structural-elements.md#footnote)> | Footnotes keyed by ID. |
| `documentStyle` | [`DocumentStyle`](./05-styles.md#documentstyle) | Document-wide style. |
| `namedStyles` | [`NamedStyles`](./05-styles.md#namedstyles) | Named style definitions. |
| `lists` | map<string, [`List`](./07-lists-named-ranges.md#list)> | Lists keyed by ID. |
| `namedRanges` | map<string, [`NamedRanges`](./07-lists-named-ranges.md#namedranges)> | Named ranges keyed by name. |
| `inlineObjects` | map<string, [`InlineObject`](./06-objects.md#inlineobject)> | Inline objects keyed by ID. |
| `positionedObjects` | map<string, [`PositionedObject`](./06-objects.md#positionedobject)> | Positioned objects keyed by ID. |

---

## TabsCriteria

Criteria for filtering operations to specific tabs.

| Field | Type | Description |
|-------|------|-------------|
| `tabIds[]` | string | IDs of tabs to target. Empty means all tabs. |
