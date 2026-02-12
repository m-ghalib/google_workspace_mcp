# Google Docs API v1 — Complete Reference

> Source: https://developers.google.com/workspace/docs/api/reference/rest/v1/documents

## API Overview

The Google Docs API provides programmatic access to Google Docs documents. It exposes a single resource (`documents`) with three methods, plus a rich set of batch update request types for document manipulation.

## Base URL

```
https://docs.googleapis.com/v1
```

## Documents

- [Methods](./01-methods.md) — `get`, `create`, `batchUpdate`
- [Document Resource Schema](./02-document-resource.md) — Full `Document` object hierarchy
- [Structural Elements](./03-structural-elements.md) — `Body`, `Paragraph`, `Table`, `SectionBreak`, etc.
- [Paragraph Elements](./04-paragraph-elements.md) — `TextRun`, `InlineObjectElement`, `Person`, `RichLink`, etc.
- [Styles & Formatting](./05-styles.md) — `TextStyle`, `ParagraphStyle`, `DocumentStyle`, `TableCellStyle`, etc.
- [Objects & Positioning](./06-objects.md) — `InlineObject`, `PositionedObject`, `EmbeddedObject`, images
- [Lists & Named Ranges](./07-lists-named-ranges.md) — `List`, `ListProperties`, `NestingLevel`, `NamedRange`
- [Tabs](./08-tabs.md) — `Tab`, `TabProperties`, `DocumentTab`
- [BatchUpdate Requests](./09-batch-update-requests.md) — All 37 request types
- [BatchUpdate Responses](./10-batch-update-responses.md) — All response types
- [Enums](./11-enums.md) — All enumeration types
- [Common Types](./12-common-types.md) — `Range`, `Location`, `Dimension`, `Color`, etc.
- [Suggestion Types](./13-suggestions.md) — Suggestion tracking types and states
- [Formatting Guide](./14-formatting-guide.md) — Practical patterns for paragraph editing, styles, lists, tables

## Authorization Scopes

| Scope | Access Level |
|-------|-------------|
| `https://www.googleapis.com/auth/documents` | Full read/write |
| `https://www.googleapis.com/auth/documents.readonly` | Read-only |
| `https://www.googleapis.com/auth/drive` | Full Drive access (includes Docs) |
| `https://www.googleapis.com/auth/drive.readonly` | Read-only Drive access |
| `https://www.googleapis.com/auth/drive.file` | Per-file access |
