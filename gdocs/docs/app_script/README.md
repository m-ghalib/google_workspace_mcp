# Google Apps Script DocumentApp — Complete Reference

> Source: https://developers.google.com/apps-script/reference/document

## API Overview

The Google Apps Script DocumentApp API provides a DOM-like, object-oriented interface for creating and manipulating Google Docs. Unlike the REST API's 3-method + 37-batchUpdate design, Apps Script exposes **~500+ methods** across **35 classes** with tree-based navigation and in-place mutation.

### Architectural Comparison

| Aspect | Apps Script DocumentApp | Google Docs REST API |
|--------|------------------------|---------------------|
| **Access model** | DOM-like tree traversal | Flat index-based addressing |
| **Mutation model** | In-place method calls | Declarative batch requests |
| **Methods** | ~500+ across 35 classes | 3 methods + 37 batchUpdate types |
| **Addressing** | Element references (survive edits) | UTF-16 index positions (precise but fragile) |
| **Concurrency** | No explicit control | WriteControl with revision IDs |
| **Suggestions** | Not supported | Full suggestion tracking system |

## Documents

- [Entry Points](./01-entry-points.md) — `DocumentApp` (static factory) + `Document` (instance class)
- [Structural Elements](./02-structural-elements.md) — `Body`, `Paragraph`, `ListItem`, `Table`, `TableRow`, `TableCell`
- [Text & Inline Elements](./03-text-and-inline.md) — `Text`, `InlineImage`, `PositionedImage`, `InlineDrawing`, `HorizontalRule`, `PageBreak`
- [Styles & Formatting](./04-styles-formatting.md) — Formatting paradigm comparison (method-based vs. declarative)
- [Enums](./05-enums.md) — All 9 enum types with REST API mapping
- [Sections, Ranges & Bookmarks](./06-sections-ranges.md) — `HeaderSection`, `FooterSection`, `Footnote*`, `Range*`, `Position`, `Bookmark`, `NamedRange`
- [Coverage Matrix](./07-coverage-matrix.md) — Complete operation-level comparison with coverage percentages
- [Tabs & Table of Contents](./08-tabs-and-toc.md) — Tab, DocumentTab, TableOfContents
- [Smart Chips](./09-smart-chips.md) — Person, Date, RichLink (read-only access)
- [Equations](./10-equations.md) — Equation, EquationFunction, EquationFunctionArgumentSeparator, EquationSymbol
- [ContainerElement Base Class](./11-container-element.md) — Abstract base class (36 shared methods inherited by all container types)

## Coverage at a Glance

**35/35 classes documented (100% coverage)**. Apps Script covers ~75-80% of REST API operations for common document tasks, but has significant gaps in advanced formatting, layout control, and modern features.

### What Apps Script Does Well (full coverage)
- Text CRUD (insert, delete, replace, find)
- Basic formatting (bold, italic, underline, font, size, color)
- Structural manipulation (paragraphs, tables, lists, images)
- Headers, footers, footnotes
- Bookmarks and named ranges
- Document metadata and permissions (via Drive API)

### What Apps Script Cannot Do (REST API only)
- **Suggestion tracking** — create/accept/reject suggested changes
- **Smart chips** — Person, Date, RichLink are read-only (can read but not insert)
- **Advanced paragraph formatting** — borders, shading, keep-together, widow/orphan control
- **Small caps and explicit font weight** (100-900 scale)
- **Table cell borders** and row height constraints
- **Document background color** and pageless mode
- **Field masks** for sparse partial updates
- **Concurrent editing control** via revision IDs

### What Apps Script Does Better
- **Equation access** — Full tree traversal of equation structure (REST API is completely opaque)

## Authorization Scopes

| Scope | Access Level |
|-------|-------------|
| `https://www.googleapis.com/auth/documents` | Full read/write |
| `https://www.googleapis.com/auth/documents.readonly` | Read-only |
| `https://www.googleapis.com/auth/documents.currentonly` | Current document only (container-bound) |
| `https://www.googleapis.com/auth/script.container.ui` | UI access (menus, dialogs) |

## Corresponding REST API Reference

See [../docs_api/README.md](../docs_api/README.md) for the complete Google Docs REST API v1 reference used as the comparison baseline throughout this documentation.
