# Enums

All enumeration types in Google Apps Script Document API compared with REST API equivalents.

## Attribute

Master list of all formatting attributes. Used with `setAttributes()`/`getAttributes()` methods.

**Usage:** `DocumentApp.Attribute.BOLD`, `DocumentApp.Attribute.FONT_SIZE`, etc.

| Value | Description | REST API Equivalent |
|-------|-------------|---------------------|
| `BACKGROUND_COLOR` | Background color (Paragraph, Table, Document) | `TextStyle.backgroundColor` / `TableCellStyle.backgroundColor` / `ParagraphStyle.shading.backgroundColor` / `DocumentStyle.background.color` |
| `BOLD` | Font weight (bold/normal) | `TextStyle.bold` |
| `BORDER_COLOR` | Border color for table elements | `TableCellStyle.border{Top,Bottom,Left,Right}.color` / `ParagraphStyle.border{Top,Bottom,Left,Right,Between}.color` |
| `BORDER_WIDTH` | Border width in points | `TableCellStyle.border{Top,Bottom,Left,Right}.width` / `ParagraphStyle.border{Top,Bottom,Left,Right,Between}.width` |
| `CODE` | Code contents for equation elements | `Equation.suggestedInsertionIds` (suggestion tracking only) |
| `FONT_FAMILY` | Font family name | `TextStyle.weightedFontFamily.fontFamily` |
| `FONT_SIZE` | Font size in points | `TextStyle.fontSize.magnitude` |
| `FOREGROUND_COLOR` | Text color | `TextStyle.foregroundColor.color` |
| `HEADING` | Paragraph heading type | `ParagraphStyle.namedStyleType` |
| `HEIGHT` | Image height | `InlineObjectProperties.embeddedObject.size.height.magnitude` |
| `HORIZONTAL_ALIGNMENT` | Paragraph horizontal alignment | `ParagraphStyle.alignment` |
| `INDENT_END` | End indentation in points | `ParagraphStyle.indentEnd.magnitude` |
| `INDENT_FIRST_LINE` | First line indentation in points | `ParagraphStyle.indentFirstLine.magnitude` |
| `INDENT_START` | Start indentation in points | `ParagraphStyle.indentStart.magnitude` |
| `ITALIC` | Italic styling | `TextStyle.italic` |
| `GLYPH_TYPE` | List item glyph type | `Bullet.glyph.glyphType` |
| `LEFT_TO_RIGHT` | Text direction | `ParagraphStyle.direction` (enum: LEFT_TO_RIGHT / RIGHT_TO_LEFT) |
| `LINE_SPACING` | Line spacing multiplier | `ParagraphStyle.lineSpacing` |
| `LINK_URL` | Hyperlink URL | `TextStyle.link.url` |
| `LIST_ID` | List identifier | `Paragraph.bullet.listId` |
| `MARGIN_BOTTOM` | Bottom margin (document/paragraph) | `DocumentStyle.marginBottom.magnitude` / `ParagraphStyle.spaceBelow.magnitude` |
| `MARGIN_LEFT` | Left margin (document/paragraph) | `DocumentStyle.marginLeft.magnitude` |
| `MARGIN_RIGHT` | Right margin (document/paragraph) | `DocumentStyle.marginRight.magnitude` |
| `MARGIN_TOP` | Top margin (document/paragraph) | `DocumentStyle.marginTop.magnitude` / `ParagraphStyle.spaceAbove.magnitude` |
| `NESTING_LEVEL` | List item nesting depth | `Paragraph.bullet.nestingLevel` |
| `MINIMUM_HEIGHT` | Minimum row height (tables) | `TableRowStyle.minHeight.magnitude` |
| `PADDING_BOTTOM` | Bottom padding (table cells) | `TableCellStyle.paddingBottom.magnitude` |
| `PADDING_LEFT` | Left padding (table cells) | `TableCellStyle.paddingLeft.magnitude` |
| `PADDING_RIGHT` | Right padding (table cells) | `TableCellStyle.paddingRight.magnitude` |
| `PADDING_TOP` | Top padding (table cells) | `TableCellStyle.paddingTop.magnitude` |
| `PAGE_HEIGHT` | Page height in points | `DocumentStyle.pageSize.height.magnitude` |
| `PAGE_WIDTH` | Page width in points | `DocumentStyle.pageSize.width.magnitude` |
| `SPACING_AFTER` | Bottom spacing (paragraphs) | `ParagraphStyle.spaceBelow.magnitude` |
| `SPACING_BEFORE` | Top spacing (paragraphs) | `ParagraphStyle.spaceAbove.magnitude` |
| `STRIKETHROUGH` | Strikethrough text effect | `TextStyle.strikethrough` |
| `UNDERLINE` | Underline text effect | `TextStyle.underline` |
| `VERTICAL_ALIGNMENT` | Vertical alignment (table cells) | `TableCellStyle.contentAlignment` |
| `WIDTH` | Width (table cells/images) | `TableColumnProperties.width.magnitude` / `InlineObjectProperties.embeddedObject.size.width.magnitude` |

**Notes:**
- Apps Script's `Attribute` enum consolidates text, paragraph, table, and document properties into a single namespace
- REST API separates these into distinct style objects (`TextStyle`, `ParagraphStyle`, `TableCellStyle`, `DocumentStyle`)
- Some Apps Script attributes map to multiple REST API fields depending on context (e.g., `BACKGROUND_COLOR`)

---

## ElementType

Type discriminator for document elements.

**Usage:** `element.getType() === DocumentApp.ElementType.PARAGRAPH`

| Value | Description | REST API Equivalent |
|-------|-------------|---------------------|
| `BODY_SECTION` | Document body | `Body` resource |
| `COMMENT_SECTION` | Comment thread | ❌ (Comments managed via separate API) |
| `DATE` | Date element | `ParagraphElement.person.personProperties` (partially) |
| `EQUATION` | Mathematical equation | `ParagraphElement.equation` |
| `EQUATION_FUNCTION` | Equation function | `Equation` (nested structure) |
| `EQUATION_FUNCTION_ARGUMENT_SEPARATOR` | Equation argument separator | `Equation` (nested structure) |
| `EQUATION_SYMBOL` | Equation symbol | `Equation` (nested structure) |
| `RICH_LINK` | Rich link (smart chip) | `ParagraphElement.richLink` |
| `FOOTER_SECTION` | Footer section | `Footer` resource |
| `FOOTNOTE` | Footnote reference | `ParagraphElement.footnoteReference` |
| `FOOTNOTE_SECTION` | Footnote content section | `Footnote` resource |
| `HEADER_SECTION` | Header section | `Header` resource |
| `HORIZONTAL_RULE` | Horizontal line | `ParagraphElement.horizontalRule` |
| `INLINE_DRAWING` | Inline drawing | `ParagraphElement.inlineObjectElement` (drawing type) |
| `INLINE_IMAGE` | Inline image | `ParagraphElement.inlineObjectElement` (image type) |
| `LIST_ITEM` | List item paragraph | `Paragraph` with `bullet` field |
| `PAGE_BREAK` | Page break | `ParagraphElement.pageBreak` |
| `PARAGRAPH` | Standard paragraph | `Paragraph` resource |
| `PERSON` | Person chip (smart chip) | `ParagraphElement.person` |
| `TABLE` | Table | `Table` resource |
| `TABLE_CELL` | Table cell | `TableCell` resource |
| `TABLE_OF_CONTENTS` | Table of contents | `TableOfContents` resource |
| `TABLE_ROW` | Table row | `TableRow` resource |
| `TEXT` | Text run | `ParagraphElement.textRun` |
| `UNSUPPORTED` | Unsupported element | ❌ (API evolves, some features not scriptable) |

**Notes:**
- Apps Script uses a flat enum; REST API uses union types in `StructuralElement` and `ParagraphElement`
- REST API distinguishes between structural elements (Paragraph, Table, SectionBreak) and inline elements (TextRun, InlineObjectElement, etc.)
- Comments in REST API are managed via a separate Comments API, not as document elements

---

## FontFamily

Font family names. **DEPRECATED** — use string names with `setFontFamily(string)` instead.

**Usage:** `text.setFontFamily("Arial")` (preferred) or `DocumentApp.FontFamily.ARIAL` (legacy)

| Value | Description | REST API Equivalent |
|-------|-------------|---------------------|
| `AMARANTH` | Amaranth font | `TextStyle.weightedFontFamily.fontFamily: "Amaranth"` |
| `ARIAL` | Arial font | `TextStyle.weightedFontFamily.fontFamily: "Arial"` |
| `ARIAL_BLACK` | Arial Black font | `TextStyle.weightedFontFamily.fontFamily: "Arial Black"` |
| `ARIAL_NARROW` | Arial Narrow font | `TextStyle.weightedFontFamily.fontFamily: "Arial Narrow"` |
| `ARVO` | Arvo font | `TextStyle.weightedFontFamily.fontFamily: "Arvo"` |
| `CALIBRI` | Calibri font | `TextStyle.weightedFontFamily.fontFamily: "Calibri"` |
| `CAMBRIA` | Cambria font | `TextStyle.weightedFontFamily.fontFamily: "Cambria"` |
| `COMIC_SANS_MS` | Comic Sans MS font | `TextStyle.weightedFontFamily.fontFamily: "Comic Sans MS"` |
| `CONSOLAS` | Consolas font | `TextStyle.weightedFontFamily.fontFamily: "Consolas"` |
| `CORSIVA` | Corsiva font | `TextStyle.weightedFontFamily.fontFamily: "Corsiva"` |
| `COURIER_NEW` | Courier New font | `TextStyle.weightedFontFamily.fontFamily: "Courier New"` |
| `DANCING_SCRIPT` | Dancing Script font | `TextStyle.weightedFontFamily.fontFamily: "Dancing Script"` |
| `DROID_SANS` | Droid Sans font | `TextStyle.weightedFontFamily.fontFamily: "Droid Sans"` |
| `DROID_SERIF` | Droid Serif font | `TextStyle.weightedFontFamily.fontFamily: "Droid Serif"` |
| `GARAMOND` | Garamond font | `TextStyle.weightedFontFamily.fontFamily: "Garamond"` |
| `GEORGIA` | Georgia font | `TextStyle.weightedFontFamily.fontFamily: "Georgia"` |
| `GLORIA_HALLELUJAH` | Gloria Hallelujah font | `TextStyle.weightedFontFamily.fontFamily: "Gloria Hallelujah"` |
| `GREAT_VIBES` | Great Vibes font | `TextStyle.weightedFontFamily.fontFamily: "Great Vibes"` |
| `LOBSTER` | Lobster font | `TextStyle.weightedFontFamily.fontFamily: "Lobster"` |
| `MERRIWEATHER` | Merriweather font | `TextStyle.weightedFontFamily.fontFamily: "Merriweather"` |
| `PACIFICO` | Pacifico font | `TextStyle.weightedFontFamily.fontFamily: "Pacifico"` |
| `PHILOSOPHER` | Philosopher font | `TextStyle.weightedFontFamily.fontFamily: "Philosopher"` |
| `POIRET_ONE` | Poiret One font | `TextStyle.weightedFontFamily.fontFamily: "Poiret One"` |
| `QUATTROCENTO` | Quattrocento font | `TextStyle.weightedFontFamily.fontFamily: "Quattrocento"` |
| `ROBOTO` | Roboto font | `TextStyle.weightedFontFamily.fontFamily: "Roboto"` |
| `SHADOWS_INTO_LIGHT` | Shadows Into Light font | `TextStyle.weightedFontFamily.fontFamily: "Shadows Into Light"` |
| `SYNCOPATE` | Syncopate font | `TextStyle.weightedFontFamily.fontFamily: "Syncopate"` |
| `TAHOMA` | Tahoma font | `TextStyle.weightedFontFamily.fontFamily: "Tahoma"` |
| `TIMES_NEW_ROMAN` | Times New Roman font | `TextStyle.weightedFontFamily.fontFamily: "Times New Roman"` |
| `TREBUCHET_MS` | Trebuchet MS font | `TextStyle.weightedFontFamily.fontFamily: "Trebuchet MS"` |
| `UBUNTU` | Ubuntu font | `TextStyle.weightedFontFamily.fontFamily: "Ubuntu"` |
| `VERDANA` | Verdana font | `TextStyle.weightedFontFamily.fontFamily: "Verdana"` |

**Notes:**
- This enum is deprecated in Apps Script; use string names instead
- REST API always uses string font names, never enums
- REST API also supports font weight (100–900) via `weightedFontFamily.weight`

---

## GlyphType

Bullet/list marker types.

**Usage:** `listItem.setGlyphType(DocumentApp.GlyphType.BULLET)`

| Value | Description | REST API Equivalent |
|-------|-------------|---------------------|
| `BULLET` | Circular filled bullet (default) | `Bullet.glyph.glyphType: "BULLET"` |
| `HOLLOW_BULLET` | Hollow circular bullet | ❌ (must use custom glyph) |
| `SQUARE_BULLET` | Square bullet | ❌ (must use custom glyph or preset) |
| `NUMBER` | Numbered list (1, 2, 3) | `Bullet.glyph.glyphType: "NUMBERED"` |
| `LATIN_UPPER` | Uppercase Latin letters (A, B, C) | `Bullet.glyph.glyphType: "ALPHA_UPPER"` |
| `LATIN_LOWER` | Lowercase Latin letters (a, b, c) | `Bullet.glyph.glyphType: "ALPHA_LOWER"` |
| `ROMAN_UPPER` | Uppercase Roman numerals (I, II, III) | `Bullet.glyph.glyphType: "ROMAN_UPPER"` |
| `ROMAN_LOWER` | Lowercase Roman numerals (i, ii, iii) | `Bullet.glyph.glyphType: "ROMAN_LOWER"` |

**Notes:**
- REST API has fewer `GlyphType` values but supports `BulletGlyphPreset` for complex nested styles
- REST API also supports `customGlyphSymbol` for arbitrary Unicode bullet characters
- Apps Script has more explicit bullet shape options (HOLLOW_BULLET, SQUARE_BULLET) not directly mapped to REST API enums

**REST API additions:**
- `Bullet.glyph.glyphType: "GLYPH_TYPE_UNSPECIFIED"` — unspecified
- `BulletGlyphPreset` enum — pre-configured multi-level bullet styles (BULLET_DISC_CIRCLE_SQUARE, NUMBERED_DECIMAL_ALPHA_ROMAN, etc.)

---

## HorizontalAlignment

Paragraph horizontal alignment.

**Usage:** `paragraph.setAlignment(DocumentApp.HorizontalAlignment.CENTER)`

| Value | Description | REST API Equivalent |
|-------|-------------|---------------------|
| `LEFT` | Left-aligned | `ParagraphStyle.alignment: "START"` (in LTR text) |
| `CENTER` | Center-aligned | `ParagraphStyle.alignment: "CENTER"` |
| `RIGHT` | Right-aligned | `ParagraphStyle.alignment: "END"` (in LTR text) |
| `JUSTIFY` | Justified (full-width) | `ParagraphStyle.alignment: "JUSTIFIED"` |

**Notes:**
- REST API uses direction-agnostic values: `START` (left in LTR, right in RTL) and `END` (right in LTR, left in RTL)
- Apps Script uses absolute directions (LEFT, RIGHT) regardless of text direction
- REST API also has `ALIGNMENT_UNSPECIFIED` for inherited alignment

---

## ParagraphHeading

Paragraph heading/style types.

**Usage:** `paragraph.setHeading(DocumentApp.ParagraphHeading.HEADING_1)`

| Value | Description | REST API Equivalent |
|-------|-------------|---------------------|
| `NORMAL` | Normal body text | `ParagraphStyle.namedStyleType: "NORMAL_TEXT"` |
| `HEADING1` | Heading level 1 (highest) | `ParagraphStyle.namedStyleType: "HEADING_1"` |
| `HEADING2` | Heading level 2 | `ParagraphStyle.namedStyleType: "HEADING_2"` |
| `HEADING3` | Heading level 3 | `ParagraphStyle.namedStyleType: "HEADING_3"` |
| `HEADING4` | Heading level 4 | `ParagraphStyle.namedStyleType: "HEADING_4"` |
| `HEADING5` | Heading level 5 | `ParagraphStyle.namedStyleType: "HEADING_5"` |
| `HEADING6` | Heading level 6 (lowest) | `ParagraphStyle.namedStyleType: "HEADING_6"` |
| `TITLE` | Title style | `ParagraphStyle.namedStyleType: "TITLE"` |
| `SUBTITLE` | Subtitle style | `ParagraphStyle.namedStyleType: "SUBTITLE"` |

**Notes:**
- Direct mapping between Apps Script and REST API, but naming differs (HEADING1 → HEADING_1)
- REST API also has `NAMED_STYLE_TYPE_UNSPECIFIED` for unspecified/inherited style
- REST API's `ParagraphStyle.headingId` is a read-only identifier for cross-referencing (no Apps Script equivalent)

---

## PositionedLayout

Text wrapping behavior for positioned images.

**Usage:** `positionedImage.setLayout(DocumentApp.PositionedLayout.WRAP_TEXT)`

| Value | Description | REST API Equivalent |
|-------|-------------|---------------------|
| `ABOVE_TEXT` | Image positioned above text (overlays) | `PositionedObjectLayout: "IN_FRONT_OF_TEXT"` |
| `BREAK_BOTH` | Image breaks text on left and right | `PositionedObjectLayout: "BREAK_LEFT_RIGHT"` |
| `BREAK_LEFT` | Image breaks text on left | `PositionedObjectLayout: "BREAK_LEFT"` |
| `BREAK_RIGHT` | Image breaks text on right | `PositionedObjectLayout: "BREAK_RIGHT"` |
| `WRAP_TEXT` | Text wraps around image | `PositionedObjectLayout: "WRAP_TEXT"` |

**Notes:**
- REST API also has `BEHIND_TEXT` (image behind text) — no Apps Script equivalent
- REST API has `POSITIONED_OBJECT_LAYOUT_UNSPECIFIED` for unspecified layout

---

## TextAlignment

Vertical text offset (superscript/subscript).

**Usage:** `text.setTextAlignment(DocumentApp.TextAlignment.SUPERSCRIPT)`

| Value | Description | REST API Equivalent |
|-------|-------------|---------------------|
| `NORMAL` | Normal baseline | `TextStyle.baselineOffset: "NONE"` |
| `SUPERSCRIPT` | Raised text (exponents) | `TextStyle.baselineOffset: "SUPERSCRIPT"` |
| `SUBSCRIPT` | Lowered text (subscripts) | `TextStyle.baselineOffset: "SUBSCRIPT"` |

**Notes:**
- Apps Script name is misleading — this is NOT horizontal alignment, it's baseline offset
- REST API has clearer naming: `BaselineOffset` enum
- REST API also has `BASELINE_OFFSET_UNSPECIFIED` for inherited offset

---

## VerticalAlignment

Vertical content alignment within table cells.

**Usage:** `tableCell.setVerticalAlignment(DocumentApp.VerticalAlignment.TOP)`

| Value | Description | REST API Equivalent |
|-------|-------------|---------------------|
| `BOTTOM` | Bottom-aligned | `TableCellStyle.contentAlignment: "BOTTOM"` |
| `CENTER` | Center-aligned | `TableCellStyle.contentAlignment: "MIDDLE"` |
| `TOP` | Top-aligned | `TableCellStyle.contentAlignment: "TOP"` |

**Notes:**
- Apps Script uses `CENTER`, REST API uses `MIDDLE` for the same concept
- REST API also has `CONTENT_ALIGNMENT_UNSPECIFIED` and `CONTENT_ALIGNMENT_UNSUPPORTED` for edge cases

---

## REST API Only Enums

The following enums exist in the REST API but have no Apps Script equivalent:

### SuggestionsViewMode

How suggestions are rendered in document responses.

| Value | Description |
|-------|-------------|
| `DEFAULT_FOR_CURRENT_ACCESS` | Default based on user's access level |
| `SUGGESTIONS_INLINE` | All suggestions shown inline |
| `PREVIEW_SUGGESTIONS_ACCEPTED` | Document rendered with all suggestions accepted |
| `PREVIEW_WITHOUT_SUGGESTIONS` | Document rendered with all suggestions rejected |

**Apps Script equivalent:** ❌ None — Apps Script has no suggestion system

---

### ContentDirection

Text flow direction.

| Value | Description |
|-------|-------------|
| `CONTENT_DIRECTION_UNSPECIFIED` | Unspecified (inherited) |
| `LEFT_TO_RIGHT` | Left-to-right text flow |
| `RIGHT_TO_LEFT` | Right-to-left text flow |

**Apps Script equivalent:** `Paragraph.setLeftToRight(boolean)` — boolean instead of enum

---

### SpacingMode

How paragraph spacing is handled in lists.

| Value | Description |
|-------|-------------|
| `SPACING_MODE_UNSPECIFIED` | Inherited from parent |
| `NEVER_COLLAPSE` | Spacing always rendered |
| `COLLAPSE_LISTS` | Spacing skipped between list items |

**Apps Script equivalent:** ❌ None — spacing always rendered

---

### DashStyle

Border/line dash patterns.

| Value | Description |
|-------|-------------|
| `DASH_STYLE_UNSPECIFIED` | Unspecified |
| `SOLID` | Solid line (default) |
| `DOT` | Dotted line |
| `DASH` | Dashed line |

**Apps Script equivalent:** ❌ None — borders not exposed in Apps Script

---

### Unit

Measurement unit for dimensions.

| Value | Description |
|-------|-------------|
| `UNIT_UNSPECIFIED` | Unknown |
| `PT` | Point (1/72 inch) |

**Apps Script equivalent:** ❌ None — Apps Script uses raw numbers (always points)

---

### AutoTextType

Dynamic text field types (page numbers, etc.).

| Value | Description |
|-------|-------------|
| `TYPE_UNSPECIFIED` | Unspecified |
| `PAGE_NUMBER` | Current page number |
| `PAGE_COUNT` | Total page count |

**Apps Script equivalent:** ❌ None — no API for inserting auto-text fields

---

### TabStopAlignment

Alignment at tab stop positions.

| Value | Description |
|-------|-------------|
| `TAB_STOP_ALIGNMENT_UNSPECIFIED` | Unspecified |
| `START` | Left-aligned (default) |
| `CENTER` | Center-aligned |
| `END` | Right-aligned |

**Apps Script equivalent:** ❌ None — tab stops not exposed in Apps Script

---

### BulletAlignment

Horizontal bullet positioning.

| Value | Description |
|-------|-------------|
| `BULLET_ALIGNMENT_UNSPECIFIED` | Unspecified |
| `START` | Aligned to line start |
| `CENTER` | Centered |
| `END` | Aligned to line end |

**Apps Script equivalent:** ❌ None — bullet alignment not exposed in Apps Script

---

### BulletGlyphPreset

Pre-configured multi-level bullet styles.

| Value | Description |
|-------|-------------|
| `BULLET_GLYPH_PRESET_UNSPECIFIED` | Unspecified |
| `BULLET_DISC_CIRCLE_SQUARE` | Disc > Circle > Square nesting |
| `BULLET_DIAMONDX_ARROW3D_SQUARE` | DiamondX > Arrow3D > Square nesting |
| `BULLET_CHECKBOX` | Checkbox bullets |
| `BULLET_ARROW_DIAMOND_DISC` | Arrow > Diamond > Disc nesting |
| `BULLET_STAR_CIRCLE_SQUARE` | Star > Circle > Square nesting |
| `BULLET_ARROW3D_CIRCLE_SQUARE` | Arrow3D > Circle > Square nesting |
| `BULLET_LEFTTRIANGLE_DIAMOND_DISC` | LeftTriangle > Diamond > Disc nesting |
| `BULLET_DIAMONDX_HOLLOWDIAMOND_SQUARE` | DiamondX > HollowDiamond > Square nesting |
| `BULLET_DIAMOND_CIRCLE_SQUARE` | Diamond > Circle > Square nesting |
| `NUMBERED_DECIMAL_ALPHA_ROMAN` | 1. > a. > i. nesting |
| `NUMBERED_DECIMAL_ALPHA_ROMAN_PARENS` | 1) > a) > i) nesting |
| `NUMBERED_DECIMAL_NESTED` | 1. > 1.1. > 1.1.1. nesting |
| `NUMBERED_UPPERALPHA_ALPHA_ROMAN` | A. > a. > i. nesting |
| `NUMBERED_UPPERROMAN_UPPERALPHA_DECIMAL` | I. > A. > 1. nesting |
| `NUMBERED_ZERODECIMAL_ALPHA_ROMAN` | 01. > a. > i. nesting |

**Apps Script equivalent:** ❌ None — must manually configure each nesting level with `setGlyphType()`

---

### SectionType

Section break types.

| Value | Description |
|-------|-------------|
| `SECTION_TYPE_UNSPECIFIED` | Unspecified |
| `CONTINUOUS` | New section starts immediately (no page break) |
| `NEXT_PAGE` | New section starts on next page |

**Apps Script equivalent:** ❌ None — section breaks not exposed in Apps Script

---

### ColumnSeparatorStyle

Visual dividers between columns.

| Value | Description |
|-------|-------------|
| `COLUMN_SEPARATOR_STYLE_UNSPECIFIED` | Unspecified |
| `NONE` | No divider |
| `BETWEEN_EACH_COLUMN` | Divider between each column pair |

**Apps Script equivalent:** ❌ None — multi-column layout not exposed in Apps Script

---

### WidthType

Column width measurement types.

| Value | Description |
|-------|-------------|
| `WIDTH_TYPE_UNSPECIFIED` | Unspecified |
| `EVENLY_DISTRIBUTED` | Columns share equal width |
| `FIXED_WIDTH` | Column has a fixed width |

**Apps Script equivalent:** ❌ None — table columns use fixed widths only

---

### PropertyState

Whether an optional property is rendered.

| Value | Description |
|-------|-------------|
| `PROPERTY_STATE_UNSPECIFIED` | Unspecified |
| `RENDERED` | Property is applied/visible |
| `NOT_RENDERED` | Property is not applied/hidden |

**Apps Script equivalent:** ❌ None — no API for conditional rendering

---

### HeaderFooterType

Header/footer types (currently only DEFAULT exists).

| Value | Description |
|-------|-------------|
| `HEADER_FOOTER_TYPE_UNSPECIFIED` | Unspecified |
| `DEFAULT` | Default header/footer |

**Apps Script equivalent:** Limited — `Document.addHeader()` / `addFooter()` exist but don't expose type selection

---

### ImageReplaceMethod

How replacement images are fitted.

| Value | Description |
|-------|-------------|
| `IMAGE_REPLACE_METHOD_UNSPECIFIED` | Unspecified |
| `CENTER_CROP` | Scales and centers the image to fill bounds, cropping excess |

**Apps Script equivalent:** ❌ None — image replacement not exposed in Apps Script

---

## Coverage Summary

### Apps Script Enums

9 enums total:
- ✅ `Attribute` — comprehensive formatting attribute list (38 values)
- ✅ `ElementType` — element type discriminator (24 values)
- ⚠️ `FontFamily` — **deprecated**, use strings instead (31 values)
- ✅ `GlyphType` — bullet/list marker types (8 values)
- ✅ `HorizontalAlignment` — paragraph alignment (4 values)
- ✅ `ParagraphHeading` — heading/style types (9 values)
- ✅ `PositionedLayout` — image text wrapping (5 values)
- ✅ `TextAlignment` — baseline offset (3 values)
- ✅ `VerticalAlignment` — table cell vertical alignment (3 values)

### REST API Enums

23 enums total:
- ✅ `Alignment` — paragraph horizontal alignment (5 values) — **Apps Script equivalent: HorizontalAlignment**
- ✅ `AutoTextType` — dynamic text fields (3 values) — ❌ **Apps Script: None**
- ✅ `BaselineOffset` — superscript/subscript (4 values) — **Apps Script equivalent: TextAlignment**
- ✅ `BulletAlignment` — bullet positioning (4 values) — ❌ **Apps Script: None**
- ✅ `BulletGlyphPreset` — pre-configured bullet styles (17 values) — ❌ **Apps Script: None**
- ✅ `ColumnSeparatorStyle` — multi-column dividers (3 values) — ❌ **Apps Script: None**
- ✅ `ContentAlignment` — table cell vertical alignment (5 values) — **Apps Script equivalent: VerticalAlignment**
- ✅ `ContentDirection` — text flow direction (3 values) — **Apps Script equivalent: boolean `setLeftToRight()`**
- ✅ `DashStyle` — border line patterns (4 values) — ❌ **Apps Script: None**
- ✅ `GlyphType` — bullet marker category (7 values) — **Apps Script equivalent: GlyphType** (8 values)
- ✅ `HeaderFooterType` — header/footer types (2 values) — ⚠️ **Apps Script: Limited API**
- ✅ `ImageReplaceMethod` — image fitting (2 values) — ❌ **Apps Script: None**
- ✅ `NamedStyleType` — predefined paragraph styles (9 values) — **Apps Script equivalent: ParagraphHeading**
- ✅ `PositionedObjectLayout` — image text wrapping (7 values) — **Apps Script equivalent: PositionedLayout** (5 values)
- ✅ `PropertyState` — conditional rendering (3 values) — ❌ **Apps Script: None**
- ✅ `SectionType` — section break types (3 values) — ❌ **Apps Script: None**
- ✅ `SpacingMode` — paragraph spacing in lists (3 values) — ❌ **Apps Script: None**
- ✅ `SuggestionsViewMode` — suggestion rendering (4 values) — ❌ **Apps Script: None**
- ✅ `TabStopAlignment` — tab stop alignment (4 values) — ❌ **Apps Script: None**
- ✅ `Unit` — measurement units (2 values) — ❌ **Apps Script: None** (always points)
- ✅ `WidthType` — column width types (3 values) — ❌ **Apps Script: None**

Additional enums not fully documented here:
- `DocumentFormat` (document format type)
- `DocumentMode` (PAGELESS, etc.)

### Key Differences

1. **Apps Script has `Attribute` enum, REST API doesn't** — Apps Script consolidates all formatting properties into a single enum for use with `setAttributes()`/`getAttributes()`; REST API uses separate typed objects
2. **REST API has 14 enums with no Apps Script equivalent** — mostly advanced layout features (borders, sections, spacing modes, suggestions, etc.)
3. **Naming conventions differ** — Apps Script uses `HEADING1`, REST API uses `HEADING_1`; Apps Script uses `CENTER` for cell alignment, REST API uses `MIDDLE`
4. **REST API enums are more granular** — separates concerns (alignment, direction, spacing mode) while Apps Script combines into fewer enums
5. **Suggestion system is REST API only** — `SuggestionsViewMode` and all suggestion-related fields have no Apps Script equivalent

### Coverage Ranking

1. **REST API**: 23+ enums covering all formatting, layout, and suggestion features
2. **Apps Script**: 9 enums (1 deprecated) covering common formatting tasks but missing advanced layout features

The REST API has significantly richer enum coverage, reflecting its more granular control over document formatting and layout.
