# Enum Types

All enumeration types used across the Google Docs API.

## SuggestionsViewMode

How suggestions are rendered in the document.

| Value | Description |
|-------|-------------|
| `DEFAULT_FOR_CURRENT_ACCESS` | Default based on user's access level. |
| `SUGGESTIONS_INLINE` | All suggestions shown inline. |
| `PREVIEW_SUGGESTIONS_ACCEPTED` | Document rendered with all suggestions accepted. |
| `PREVIEW_WITHOUT_SUGGESTIONS` | Document rendered with all suggestions rejected. |

---

## NamedStyleType

Predefined paragraph/text style identifiers.

| Value | Description |
|-------|-------------|
| `NAMED_STYLE_TYPE_UNSPECIFIED` | Unspecified. |
| `NORMAL_TEXT` | Normal body text. |
| `TITLE` | Title style. |
| `SUBTITLE` | Subtitle style. |
| `HEADING_1` | Heading level 1. |
| `HEADING_2` | Heading level 2. |
| `HEADING_3` | Heading level 3. |
| `HEADING_4` | Heading level 4. |
| `HEADING_5` | Heading level 5. |
| `HEADING_6` | Heading level 6. |

---

## Alignment

Paragraph text alignment.

| Value | Description |
|-------|-------------|
| `ALIGNMENT_UNSPECIFIED` | Inherited from parent. |
| `START` | Left-aligned (LTR) or right-aligned (RTL). |
| `CENTER` | Centered. |
| `END` | Right-aligned (LTR) or left-aligned (RTL). |
| `JUSTIFIED` | Justified. |

---

## ContentDirection

Text direction.

| Value | Description |
|-------|-------------|
| `CONTENT_DIRECTION_UNSPECIFIED` | Unspecified. |
| `LEFT_TO_RIGHT` | Left-to-right text flow. |
| `RIGHT_TO_LEFT` | Right-to-left text flow. |

---

## SpacingMode

How paragraph spacing is handled.

| Value | Description |
|-------|-------------|
| `SPACING_MODE_UNSPECIFIED` | Inherited. |
| `NEVER_COLLAPSE` | Spacing always rendered. |
| `COLLAPSE_LISTS` | Spacing skipped between list items. |

---

## BaselineOffset

Vertical text offset.

| Value | Description |
|-------|-------------|
| `BASELINE_OFFSET_UNSPECIFIED` | Inherited from parent. |
| `NONE` | No offset. |
| `SUPERSCRIPT` | Offset upwards (superscript). |
| `SUBSCRIPT` | Offset downwards (subscript). |

---

## DashStyle

Border and line dash patterns.

| Value | Description |
|-------|-------------|
| `DASH_STYLE_UNSPECIFIED` | Unspecified. |
| `SOLID` | Solid line (default). |
| `DOT` | Dotted line. |
| `DASH` | Dashed line. |

---

## Unit

Measurement unit for dimensions.

| Value | Description |
|-------|-------------|
| `UNIT_UNSPECIFIED` | Unknown. |
| `PT` | Point (1/72 inch). |

---

## AutoTextType

Dynamic text field type.

| Value | Description |
|-------|-------------|
| `TYPE_UNSPECIFIED` | Unspecified. |
| `PAGE_NUMBER` | Current page number. |
| `PAGE_COUNT` | Total page count. |

---

## TabStopAlignment

Alignment at a tab stop position.

| Value | Description |
|-------|-------------|
| `TAB_STOP_ALIGNMENT_UNSPECIFIED` | Unspecified. |
| `START` | Left-aligned (default). |
| `CENTER` | Center-aligned. |
| `END` | Right-aligned. |

---

## BulletAlignment

Horizontal bullet positioning.

| Value | Description |
|-------|-------------|
| `BULLET_ALIGNMENT_UNSPECIFIED` | Unspecified. |
| `START` | Aligned to line start. |
| `CENTER` | Centered. |
| `END` | Aligned to line end. |

---

## GlyphType

Bullet symbol category.

| Value | Description |
|-------|-------------|
| `GLYPH_TYPE_UNSPECIFIED` | Unspecified. |
| `BULLET` | Standard bullet point. |
| `NUMBERED` | Numbered list. |
| `ROMAN_LOWER` | Lowercase Roman numerals (i, ii, iii). |
| `ROMAN_UPPER` | Uppercase Roman numerals (I, II, III). |
| `ALPHA_LOWER` | Lowercase letters (a, b, c). |
| `ALPHA_UPPER` | Uppercase letters (A, B, C). |

---

## BulletGlyphPreset

Preset bullet styles for `CreateParagraphBulletsRequest`.

| Value | Description |
|-------|-------------|
| `BULLET_GLYPH_PRESET_UNSPECIFIED` | Unspecified. |
| `BULLET_DISC_CIRCLE_SQUARE` | Disc > Circle > Square nesting. |
| `BULLET_DIAMONDX_ARROW3D_SQUARE` | DiamondX > Arrow3D > Square nesting. |
| `BULLET_CHECKBOX` | Checkbox bullets. |
| `BULLET_ARROW_DIAMOND_DISC` | Arrow > Diamond > Disc nesting. |
| `BULLET_STAR_CIRCLE_SQUARE` | Star > Circle > Square nesting. |
| `BULLET_ARROW3D_CIRCLE_SQUARE` | Arrow3D > Circle > Square nesting. |
| `BULLET_LEFTTRIANGLE_DIAMOND_DISC` | LeftTriangle > Diamond > Disc nesting. |
| `BULLET_DIAMONDX_HOLLOWDIAMOND_SQUARE` | DiamondX > HollowDiamond > Square nesting. |
| `BULLET_DIAMOND_CIRCLE_SQUARE` | Diamond > Circle > Square nesting. |
| `NUMBERED_DECIMAL_ALPHA_ROMAN` | 1. > a. > i. nesting. |
| `NUMBERED_DECIMAL_ALPHA_ROMAN_PARENS` | 1) > a) > i) nesting. |
| `NUMBERED_DECIMAL_NESTED` | 1. > 1.1. > 1.1.1. nesting. |
| `NUMBERED_UPPERALPHA_ALPHA_ROMAN` | A. > a. > i. nesting. |
| `NUMBERED_UPPERROMAN_UPPERALPHA_DECIMAL` | I. > A. > 1. nesting. |
| `NUMBERED_ZERODECIMAL_ALPHA_ROMAN` | 01. > a. > i. nesting. |

---

## SectionType

Section break type.

| Value | Description |
|-------|-------------|
| `SECTION_TYPE_UNSPECIFIED` | Unspecified. |
| `CONTINUOUS` | New section starts immediately (no page break). |
| `NEXT_PAGE` | New section starts on next page. |

---

## ColumnSeparatorStyle

Visual divider between columns.

| Value | Description |
|-------|-------------|
| `COLUMN_SEPARATOR_STYLE_UNSPECIFIED` | Unspecified. |
| `NONE` | No divider. |
| `BETWEEN_EACH_COLUMN` | Divider between each column pair. |

---

## WidthType

Column width measurement type.

| Value | Description |
|-------|-------------|
| `WIDTH_TYPE_UNSPECIFIED` | Unspecified. |
| `EVENLY_DISTRIBUTED` | Columns share equal width. |
| `FIXED_WIDTH` | Column has a fixed width. |

---

## ContentAlignment

Vertical content alignment within a table cell.

| Value | Description |
|-------|-------------|
| `CONTENT_ALIGNMENT_UNSPECIFIED` | Unspecified. |
| `CONTENT_ALIGNMENT_UNSUPPORTED` | Unsupported alignment. |
| `TOP` | Top-aligned. |
| `MIDDLE` | Middle-aligned. |
| `BOTTOM` | Bottom-aligned. |

---

## PropertyState

Whether an optional property is rendered.

| Value | Description |
|-------|-------------|
| `PROPERTY_STATE_UNSPECIFIED` | Unspecified. |
| `RENDERED` | Property is applied/visible. |
| `NOT_RENDERED` | Property is not applied/hidden. |

---

## PositionedObjectLayout

Text wrapping behavior around positioned objects.

| Value | Description |
|-------|-------------|
| `POSITIONED_OBJECT_LAYOUT_UNSPECIFIED` | Unspecified. |
| `WRAP_TEXT` | Text wraps around the object. |
| `BREAK_LEFT` | Object breaks text, occupies left side. |
| `BREAK_RIGHT` | Object breaks text, occupies right side. |
| `BREAK_LEFT_RIGHT` | Object breaks text, extends full width. |
| `IN_FRONT_OF_TEXT` | Object overlays text. |
| `BEHIND_TEXT` | Object appears behind text. |

---

## HeaderFooterType

Header/footer type.

| Value | Description |
|-------|-------------|
| `HEADER_FOOTER_TYPE_UNSPECIFIED` | Unspecified. |
| `DEFAULT` | Default header/footer. |

---

## ImageReplaceMethod

How a replacement image is fitted.

| Value | Description |
|-------|-------------|
| `IMAGE_REPLACE_METHOD_UNSPECIFIED` | Unspecified. |
| `CENTER_CROP` | Scales and centers the image to fill the original bounds, cropping excess. |
