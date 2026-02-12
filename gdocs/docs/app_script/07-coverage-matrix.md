# Coverage Matrix — Apps Script vs. Google Docs REST API

This document provides an operation-level comparison between Google Apps Script's DocumentApp and the Google Docs REST API v1, using the REST API as the golden standard for high-fidelity document operations.

---

## Method Coverage by Class

| Apps Script Class | Methods | REST API Coverage | Notes |
|-------------------|--------:|:-----------------:|-------|
| DocumentApp | 5 | 3/5 (60%) | 2 UI-only methods |
| Document | 45 | 32/45 (71%) | 13 UI/container-bound methods |
| Body | 48 | 48/48 (100%) | Full coverage via batchUpdate |
| Paragraph | 51 | 51/51 (100%) | Full coverage via batchUpdate |
| ListItem | 57 | 57/57 (100%) | Full coverage via batchUpdate |
| Table | 17 | 17/17 (100%) | Full coverage via batchUpdate |
| TableRow | 39 | 39/39 (100%) | Full coverage via batchUpdate |
| TableCell | 64 | 64/64 (100%) | Full coverage via batchUpdate |
| Text | 73 | 73/73 (100%) | Full coverage via batchUpdate |
| InlineImage | 21 | 21/21 (100%) | Full coverage |
| PositionedImage | 11 | 11/11 (100%) | Full coverage |
| InlineDrawing | 13 | 13/13 (100%) | Full coverage |
| HorizontalRule | 9 | 9/9 (100%) | Full coverage |
| PageBreak | 9 | 9/9 (100%) | Full coverage |
| HeaderSection | ~40 | ~40/40 (100%) | Full coverage |
| FooterSection | ~40 | ~40/40 (100%) | Full coverage |
| Footnote | ~10 | ~10/10 (100%) | Full coverage |
| FootnoteSection | ~40 | ~40/40 (100%) | Full coverage |
| Range/RangeBuilder | ~15 | Different paradigm | Element-based vs index-based |
| Bookmark | ~5 | ~5/5 (100%) | Different addressing |
| NamedRange | ~5 | ~5/5 (100%) | Different addressing |
| Tab | 6 | Read-only | No tab creation/deletion in Apps Script |
| DocumentTab | 15 | Read-only | Content access mirrors Document class |
| TableOfContents | ~23 | ~23/23 (100%) | Full ContainerElement methods |
| Person | ~12 | Read-only | Can read but not insert smart chips |
| Date | ~13 | Read-only | Can read but not insert date chips |
| RichLink | ~13 | Read-only | Can read but not insert rich links |
| Equation | ~25 | Apps Script advantage | Full tree structure (REST API is opaque) |
| EquationFunction | ~26 | Apps Script advantage | Nested function access (REST API: none) |
| EquationFunctionArgumentSeparator | ~10 | Apps Script advantage | Argument boundary access (REST API: none) |
| EquationSymbol | ~11 | Apps Script advantage | Symbol code access (REST API: none) |
| ContainerElement | ~36 | Paradigm difference | Abstract base — no REST API equivalent |
| **TOTALS** | **~820** | **~710/820 (87%)** | |

> The ~13% of Apps Script methods without REST API equivalents include UI-state/container-bound operations (cursor, selection, active tab, active document, save/close), read-only smart chip access, read-only tab access, and Apps Script's unique equation tree traversal capabilities.

---

## REST API Batch Update Operations → Apps Script

The REST API has **37 batchUpdate request types**. Here is how each maps to Apps Script:

### Text Operations (4/4 = 100%)

| REST API Request | Apps Script Equivalent | Fidelity |
|------------------|----------------------|----------|
| `InsertTextRequest` | `Text.insertText()`, `Body.appendParagraph()`, etc. | ✅ Full |
| `DeleteContentRangeRequest` | `Text.deleteText()`, `Element.removeFromParent()` | ✅ Full |
| `ReplaceAllTextRequest` | `Body.replaceText()`, `Text.replaceText()` | ✅ Full |
| `ReplaceNamedRangeContentRequest` | Get NamedRange → manipulate elements | ⚠️ Manual |

### Style Operations (6/8 = 75%)

| REST API Request | Apps Script Equivalent | Fidelity |
|------------------|----------------------|----------|
| `UpdateTextStyleRequest` | `Text.setBold()`, `setItalic()`, `setFontSize()`, etc. | ⚠️ Partial — missing small caps, font weight |
| `UpdateParagraphStyleRequest` | `Paragraph.setAlignment()`, `setSpacingBefore()`, etc. | ⚠️ Partial — missing borders, shading, keep-together, widow/orphan |
| `UpdateDocumentStyleRequest` | `Body.setPageHeight()`, `setMarginTop()`, etc. | ⚠️ Partial — missing background color, header/footer margins, pageless mode |
| `UpdateSectionStyleRequest` | ❌ No equivalent | ❌ None |
| `UpdateTableCellStyleRequest` | `TableCell.setPaddingTop()`, `setBackgroundColor()`, etc. | ⚠️ Partial — missing border control |
| `UpdateTableColumnPropertiesRequest` | `Table.setColumnWidth()` | ✅ Full |
| `UpdateTableRowStyleRequest` | ❌ No equivalent | ❌ None |
| `PinTableHeaderRowsRequest` | ❌ No equivalent | ❌ None |

### List Operations (2/2 = 100%)

| REST API Request | Apps Script Equivalent | Fidelity |
|------------------|----------------------|----------|
| `CreateParagraphBulletsRequest` | `ListItem.setGlyphType()` | ⚠️ Partial — missing bullet presets |
| `DeleteParagraphBulletsRequest` | `ListItem.removeFromParent()` + re-add as Paragraph | ⚠️ Manual |

### Named Style Operations (1/1 = 100%)

| REST API Request | Apps Script Equivalent | Fidelity |
|------------------|----------------------|----------|
| `UpdateNamedStyleRequest` | No direct equivalent; can set heading on paragraphs | ⚠️ Partial |

### Insert Operations (6/6 = 100%)

| REST API Request | Apps Script Equivalent | Fidelity |
|------------------|----------------------|----------|
| `InsertInlineImageRequest` | `Body.insertImage()`, `Paragraph.insertInlineImage()` | ✅ Full |
| `InsertTableRequest` | `Body.insertTable()` | ✅ Full |
| `InsertTableRowRequest` | `Table.insertTableRow()` | ✅ Full |
| `InsertTableColumnRequest` | ❌ No direct method | ⚠️ Manual (add cells per row) |
| `InsertPageBreakRequest` | `Body.appendPageBreak()` | ✅ Full |
| `InsertSectionBreakRequest` | ❌ No equivalent | ❌ None |

### Delete Operations (5/7 = 71%)

| REST API Request | Apps Script Equivalent | Fidelity |
|------------------|----------------------|----------|
| `DeleteTableRowRequest` | `Table.removeRow()` | ✅ Full |
| `DeleteTableColumnRequest` | ❌ No direct method | ⚠️ Manual |
| `DeletePositionedObjectRequest` | `PositionedImage.removeFromParent()` | ✅ Full |
| `DeleteHeaderRequest` | `HeaderSection.removeFromParent()` | ✅ Full |
| `DeleteFooterRequest` | `FooterSection.removeFromParent()` | ✅ Full |
| `DeleteNamedRangeRequest` | `NamedRange.remove()` | ✅ Full |
| `DeleteContentRangeRequest` | Multiple element-level methods | ✅ Full |

### Create Operations (4/4 = 100%)

| REST API Request | Apps Script Equivalent | Fidelity |
|------------------|----------------------|----------|
| `CreateHeaderRequest` | `Document.addHeader()` | ✅ Full |
| `CreateFooterRequest` | `Document.addFooter()` | ✅ Full |
| `CreateNamedRangeRequest` | `Document.addNamedRange()` | ✅ Full |
| `CreateFootnoteRequest` | `Body.appendParagraph()` + footnote methods | ⚠️ Manual |

### Merge Operations (2/2 = 100%)

| REST API Request | Apps Script Equivalent | Fidelity |
|------------------|----------------------|----------|
| `MergeTableCellsRequest` | `Table.getCell().merge()` | ✅ Full |
| `UnmergeTableCellsRequest` | ❌ No direct equivalent | ❌ None |

### Positioned Object Operations (1/1 = 100%)

| REST API Request | Apps Script Equivalent | Fidelity |
|------------------|----------------------|----------|
| `InsertPositionedObjectRequest` (private) | `Paragraph.addPositionedImage()` | ✅ Full |

### Tab Operations (0/2 = 0%)

| REST API Request | Apps Script Equivalent | Fidelity |
|------------------|----------------------|----------|
| `CreateTabRequest` | ❌ No equivalent | ❌ None |
| `DeleteTabRequest` | ❌ No equivalent | ❌ None |

---

## Summary: batchUpdate Coverage

| Category | Total Requests | ✅ Full | ⚠️ Partial/Manual | ❌ None |
|----------|---------------:|--------:|-------------------:|--------:|
| Text Operations | 4 | 3 | 1 | 0 |
| Style Operations | 8 | 1 | 4 | 3 |
| List Operations | 2 | 0 | 2 | 0 |
| Named Style Ops | 1 | 0 | 1 | 0 |
| Insert Operations | 6 | 4 | 1 | 1 |
| Delete Operations | 7 | 5 | 1 | 1 |
| Create Operations | 4 | 3 | 1 | 0 |
| Merge Operations | 2 | 1 | 0 | 1 |
| Positioned Objects | 1 | 1 | 0 | 0 |
| Tab Operations | 2 | 0 | 0 | 2 |
| **TOTAL** | **37** | **18 (49%)** | **11 (30%)** | **8 (21%)** |

### Interpretation

- **49%** of REST API operations have **full-fidelity** Apps Script equivalents
- **30%** have **partial or manual** equivalents (achievable but with workarounds or missing sub-features)
- **21%** have **no Apps Script equivalent** at all

Combined: **~79%** of REST API operations are achievable through Apps Script (49% full + 30% partial), while **~21%** are impossible.

---

## Feature-Level Gap Analysis

### Features ONLY in REST API (not achievable via Apps Script)

| Feature | REST API Mechanism | Impact |
|---------|-------------------|--------|
| **Suggestion system** | `suggestedInsertionIds`, `suggestedDeletionIds`, `suggested*Changes` | Cannot create, accept, or reject tracked changes |
| **Smart chips (Person)** | `ParagraphElement.person` | Can read via Apps Script; cannot insert via either API |
| **Smart chips (RichLink)** | `ParagraphElement.richLink` | Can read via Apps Script; cannot insert via either API |
| **Smart chips (Date)** | `ParagraphElement.dateElement` (inferred) | Can read via Apps Script; cannot insert via either API |
| **Small caps** | `TextStyle.smallCaps` | Cannot render small capitals |
| **Explicit font weight** | `TextStyle.weightedFontFamily.weight` (100-900) | Cannot set arbitrary font weights |
| **Paragraph borders** | `ParagraphStyle.border{Top,Bottom,Left,Right,Between}` | Cannot add borders to paragraphs |
| **Paragraph shading** | `ParagraphStyle.shading.backgroundColor` | Cannot set paragraph background (distinct from text highlight) |
| **Keep lines together** | `ParagraphStyle.keepLinesTogether` | Cannot prevent paragraph from splitting across pages |
| **Keep with next** | `ParagraphStyle.keepWithNext` | Cannot keep paragraph on same page as next |
| **Widow/orphan control** | `ParagraphStyle.avoidWidowAndOrphan` | Cannot control orphan/widow lines |
| **Page break before** | `ParagraphStyle.pageBreakBefore` | Cannot force page break before paragraph |
| **Tab stops** | `ParagraphStyle.tabStops[]` | Cannot set custom tab positions |
| **Section breaks** | `InsertSectionBreakRequest` | Cannot insert section breaks |
| **Section styling** | `UpdateSectionStyleRequest` | Cannot modify section properties |
| **Table row styling** | `UpdateTableRowStyleRequest` | Cannot set row height or header rows |
| **Table cell borders** | `TableCellStyle.border{Top,Bottom,Left,Right}` | Cannot control individual cell borders |
| **Table header pinning** | `PinTableHeaderRowsRequest` | Cannot pin table headers for print |
| **Unmerge cells** | `UnmergeTableCellsRequest` | Cannot unmerge previously merged cells |
| **Tab management** | `CreateTabRequest`, `DeleteTabRequest` | Apps Script has Tab and DocumentTab classes for reading tab structure; cannot create or delete tabs via either API |
| **Document background** | `DocumentStyle.background.color` | Cannot set page background color |
| **Pageless mode** | `DocumentStyle.documentFormat.documentMode` | Cannot toggle pageless layout |
| **Field masks** | `fields` parameter on all Update requests | Cannot do sparse partial updates |
| **Write control** | `WriteControl.requiredRevisionId` | Cannot do optimistic concurrent editing |

### Features ONLY in Apps Script (not in REST API)

| Feature | Apps Script Mechanism | Impact |
|---------|----------------------|--------|
| **UI state access** | `getSelection()`, `getCursor()`, `getActiveTab()` | Can read/write user's selection and cursor position |
| **Container-bound context** | `getActiveDocument()`, `getUi()` | Can access the document the script is attached to |
| **Text attribute indices** | `Text.getTextAttributeIndices()` | Can find formatting change boundaries |
| **Unified attribute system** | `Attribute` enum + `setAttributes()`/`getAttributes()` | Single API for all formatting types |
| **Method chaining** | All setter methods return the element | Fluent API for readability |
| **Direct blob access** | `getBlob()`, `getAs(contentType)` | Export without going through Drive API |
| **Equation tree access** | `Equation.getChild()`, `EquationFunction.getCode()`, `EquationSymbol.getCode()` | Can read full equation structure — REST API treats equations as opaque blobs |

---

## Verdict: Is Apps Script Enough?

### For Common Document Operations: YES (~80% coverage)

Apps Script handles the bread-and-butter of document manipulation well:
- Creating and editing text content
- Basic formatting (bold, italic, font, size, color, alignment)
- Tables (create, populate, style cells)
- Lists (create, nest, style)
- Images (insert, resize, position)
- Headers, footers, footnotes
- Find and replace
- Bookmarks and named ranges

### For High-Fidelity Document Control: NO (~21% gap)

The REST API is required when you need:
- **Tracked changes / suggestions** — the biggest gap; Apps Script has zero suggestion support
- **Advanced paragraph formatting** — borders, shading, page break control, widow/orphan
- **Modern smart chips** — @-mentions, rich links, dates
- **Precise table formatting** — cell borders, row height, header pinning
- **Document-level settings** — background color, pageless mode, section breaks
- **Concurrent editing safety** — revision-based write control

### Recommendation

| Use Case | Recommended API |
|----------|----------------|
| Simple document generation (reports, letters) | Apps Script |
| Bulk find-and-replace across documents | Apps Script |
| Template-based mail merge | Apps Script |
| Interactive document add-ons with UI | Apps Script |
| High-fidelity formatting control | REST API |
| Suggestion/review workflows | REST API |
| Smart chip insertion | REST API |
| Concurrent multi-user editing | REST API |
| Programmatic tab management | REST API |
| Cross-platform (non-Google) integration | REST API |
| **MCP server implementation** | **REST API** (needs precision + full feature access) |
