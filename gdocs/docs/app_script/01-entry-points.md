# Entry Points — DocumentApp & Document Classes

This document compares Google Apps Script's `DocumentApp` (static entry point) and `Document` (instance class) against the Google Docs REST API.

---

## DocumentApp (Static Entry Point)

The `DocumentApp` class provides static factory methods for creating and accessing documents. It serves as the entry point for all document operations in Apps Script.

### Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `create(name)` | Document | Creates and returns a new document with the specified name | `documents.create` (POST /documents) |
| `getActiveDocument()` | Document | Returns the document to which the script is container-bound | ❌ No equivalent (container-bound scripts only) |
| `getUi()` | Ui | Returns the document's UI environment for adding menus, dialogs, and sidebars | ❌ No equivalent (UI scripting only) |
| `openById(id)` | Document | Returns the document with the specified ID | `documents.get` (GET /documents/{documentId}) |
| `openByUrl(url)` | Document | Opens and returns the document with the specified URL | `documents.get` (extract ID from URL, then GET) |

**Notes:**
- `getActiveDocument()` and `getUi()` only work with container-bound scripts running in the context of an open document
- `openById()` and `openByUrl()` allow accessing any document the script has permissions for

---

## Document (Instance Class)

The `Document` class represents an open document instance with methods for reading and modifying content, metadata, and permissions.

### Document Management

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getId()` | String | Retrieves the document's unique identifier | `Document.documentId` field |
| `getName()` | String | Retrieves the title of the document | `Document.title` field |
| `setName(name)` | Document | Sets the document title | `batchUpdate` → `UpdateDocumentStyleRequest` (partial) |
| `getUrl()` | String | Retrieves the URL to access the document | ❌ No equivalent (construct from ID) |
| `getLanguage()` | String | Gets the document's language code | `Document.documentStyle.defaultLanguage` field |
| `setLanguage(languageCode)` | Document | Sets the document's language code | `batchUpdate` → `UpdateDocumentStyleRequest` |
| `getSupportedLanguageCodes()` | String[] | Gets all supported language codes for Google Docs | ❌ No equivalent |

### Tab Management

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getActiveTab()` | Tab | Accesses the user's currently active tab | ❌ No equivalent (UI state only) |
| `setActiveTab(tabId)` | void | Sets the user's selected tab to the specified ID | ❌ No equivalent (UI state only) |
| `getTab(tabId)` | Tab | Gets a tab with the specified ID | `Document.tabs[]` array (filter by `tabId`) |
| `getTabs()` | Tab[] | Gets all unnested tabs in the document | `Document.tabs[]` array |

### Content Access

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getBody()` | Body | Retrieves the first tab's body or active tab's body | `Document.tabs[].documentTab.body` or legacy `Document.body` |
| `getHeader()` | HeaderSection \| null | Retrieves the first/active tab's header section | `Document.headers` map (keyed by header ID) |
| `getFooter()` | FooterSection \| null | Retrieves the first/active tab's footer section | `Document.footers` map (keyed by footer ID) |
| `addHeader()` | HeaderSection | Adds a header section if none exists | `batchUpdate` → `CreateHeaderRequest` |
| `addFooter()` | FooterSection | Adds a footer section if none exists | `batchUpdate` → `CreateFooterRequest` |

### Editor/Viewer Management

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `addEditor(emailAddress)` | Document | Adds a user as an editor | Drive API → `permissions.create` with `role=writer` |
| `addEditor(user)` | Document | Adds a user as an editor | Drive API → `permissions.create` with `role=writer` |
| `addEditors(emailAddresses)` | Document | Adds multiple users as editors | Drive API → multiple `permissions.create` calls |
| `removeEditor(emailAddress)` | Document | Removes a user from editor list | Drive API → `permissions.delete` |
| `removeEditor(user)` | Document | Removes a user from editor list | Drive API → `permissions.delete` |
| `getEditors()` | User[] | Gets all document editors | Drive API → `permissions.list` with `role=writer` |
| `addViewer(emailAddress)` | Document | Adds a user as a viewer | Drive API → `permissions.create` with `role=reader` |
| `addViewer(user)` | Document | Adds a user as a viewer | Drive API → `permissions.create` with `role=reader` |
| `addViewers(emailAddresses)` | Document | Adds multiple users as viewers | Drive API → multiple `permissions.create` calls |
| `removeViewer(emailAddress)` | Document | Removes a user from viewer list | Drive API → `permissions.delete` |
| `removeViewer(user)` | Document | Removes a user from viewer list | Drive API → `permissions.delete` |
| `getViewers()` | User[] | Gets all document viewers and commenters | Drive API → `permissions.list` with `role=reader` |

**Notes:**
- All permission management operations are handled by the Drive API, not the Docs API
- Apps Script abstracts this complexity with convenience methods on the Document class

### Bookmark Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `addBookmark(position)` | Bookmark | Adds a bookmark at the given position | `batchUpdate` → `CreateNamedRangeRequest` with bookmark semantics |
| `getBookmark(id)` | Bookmark \| null | Gets a bookmark with the specified ID | `Document.namedRanges` map (filter by ID) |
| `getBookmarks()` | Bookmark[] | Gets all bookmarks in the first/active tab | `Document.namedRanges` map (filter for bookmarks) |

### Range & Selection Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `newRange()` | RangeBuilder | Creates a builder for constructing Range objects | ❌ No equivalent (client-side range construction) |
| `newPosition(element, offset)` | Position | Creates a position reference relative to an element | ❌ No equivalent (client-side position construction) |
| `getSelection()` | Range \| null | Gets the user's selection in the active tab | ❌ No equivalent (UI state only) |
| `setSelection(range)` | Document | Sets the user's selection to the given range | ❌ No equivalent (UI state only) |
| `getCursor()` | Position \| null | Gets the user's cursor in the active tab | ❌ No equivalent (UI state only) |
| `setCursor(position)` | Document | Sets the user's cursor to the specified position | ❌ No equivalent (UI state only) |

**Notes:**
- Range and selection methods are UI-driven and only work in container-bound scripts
- The REST API has no concept of user selection or cursor position

### Named Range Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `addNamedRange(name, range)` | NamedRange | Adds a named range with an associated ID | `batchUpdate` → `CreateNamedRangeRequest` |
| `getNamedRangeById(id)` | NamedRange \| null | Gets a named range with the specified ID | `Document.namedRanges` map (filter by ID) |
| `getNamedRanges()` | NamedRange[] | Gets all named ranges in the first/active tab | `Document.namedRanges` map (all entries) |
| `getNamedRanges(name)` | NamedRange[] | Gets all named ranges matching the given name | `Document.namedRanges[name]` array |

### Footnote Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getFootnotes()` | Footnote[] \| null | Retrieves all footnote elements in the first/active tab | `Document.footnotes` map (all entries) |

### Export & Save Methods

| Method | Return Type | Description | REST API Equivalent |
|--------|-------------|-------------|---------------------|
| `getBlob()` | Blob | Retrieves document contents as a blob | Drive API → `files.get` with `alt=media` |
| `getAs(contentType)` | Blob | Exports document as a blob of specified type (PDF, Markdown, etc.) | Drive API → `files.export` with `mimeType` |
| `saveAndClose()` | void | Saves the current document | ❌ No equivalent (REST API auto-saves all changes) |

**Notes:**
- Export methods route through the Drive API
- `saveAndClose()` is only needed in Apps Script; REST API changes are immediately persisted

---

## Coverage Summary

### Apps Script → REST API Mapping

| Category | Apps Script Methods | With REST API Equivalent | Without REST API Equivalent |
|----------|--------------------:|-------------------------:|----------------------------:|
| DocumentApp (Entry Points) | 5 | 3 | 2 |
| Document Management | 7 | 5 | 2 |
| Tab Management | 4 | 2 | 2 |
| Content Access | 5 | 5 | 0 |
| Permission Management | 12 | 12 | 0 |
| Bookmark Methods | 3 | 3 | 0 |
| Range & Selection | 6 | 0 | 6 |
| Named Range Methods | 4 | 4 | 0 |
| Footnote Methods | 1 | 1 | 0 |
| Export & Save | 3 | 2 | 1 |
| **TOTAL** | **50** | **37** | **13** |

### Apps Script Methods WITHOUT REST API Equivalents (13 total)

These are UI-driven operations or container-bound script features unavailable via REST API:

1. `DocumentApp.getActiveDocument()` — Container-bound script context
2. `DocumentApp.getUi()` — UI scripting
3. `Document.getUrl()` — Can construct from ID, not exposed as field
4. `Document.getSupportedLanguageCodes()` — Static reference data
5. `Document.getActiveTab()` — UI state
6. `Document.setActiveTab()` — UI state
7. `Document.newRange()` — Client-side builder pattern
8. `Document.newPosition()` — Client-side position construction
9. `Document.getSelection()` — UI state
10. `Document.setSelection()` — UI state
11. `Document.getCursor()` — UI state
12. `Document.setCursor()` — UI state
13. `Document.saveAndClose()` — Explicit save not needed in REST API

### REST API Operations WITHOUT Apps Script Equivalents

The REST API has **37 request types** in `batchUpdate` that cover content modification at a granular level. Apps Script exposes these through **element-level methods** on classes like `Body`, `Paragraph`, `Text`, etc., rather than providing direct equivalents on the `Document` class.

Examples of REST API operations not directly represented as `Document` methods:
- `InsertTextRequest` — Accessed via `Text.insertText()`
- `DeleteContentRangeRequest` — Accessed via `RangeElement.deleteContent()`
- `UpdateParagraphStyleRequest` — Accessed via `Paragraph.setAttributes()`
- `InsertTableRequest` — Accessed via `Body.insertTable()`

Apps Script uses **object-oriented mutation** (call methods on elements) while the REST API uses **declarative batch updates** (send JSON describing all changes). The mapping exists but at different abstraction levels.

---

## Key Differences

1. **Abstraction Level**
   - Apps Script: High-level OOP with methods on element objects
   - REST API: Low-level declarative batch operations

2. **Save Model**
   - Apps Script: Explicit `saveAndClose()` required
   - REST API: Changes are immediately persisted

3. **UI State**
   - Apps Script: Can read/write selections, cursors, active tabs
   - REST API: No access to UI state (headless operations only)

4. **Permission Management**
   - Apps Script: Built-in methods on Document class
   - REST API: Must use separate Drive API

5. **Export**
   - Apps Script: Built-in `getBlob()` and `getAs()` methods
   - REST API: Must use separate Drive API export endpoints

6. **Concurrency**
   - Apps Script: No explicit concurrency control
   - REST API: Provides `WriteControl` with revision IDs for optimistic locking
