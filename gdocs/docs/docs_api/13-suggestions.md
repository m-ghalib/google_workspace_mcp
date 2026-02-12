# Suggestion Types

Types used for tracking suggested changes (Google Docs "Suggesting" mode).

## Overview

Most content types support suggestion tracking via:
- `suggestedInsertionIds[]` — suggestion IDs proposing this element was inserted
- `suggestedDeletionIds[]` — suggestion IDs proposing this element be deleted
- `suggested*Changes` maps — proposed modifications to properties, keyed by suggestion ID

---

## SuggestedTextStyle

A suggested modification to text formatting.

| Field | Type | Description |
|-------|------|-------------|
| `textStyle` | [`TextStyle`](./05-styles.md#textstyle) | The proposed text style values. |
| `textStyleSuggestionState` | [`TextStyleSuggestionState`](#textstylesuggestionstate) | Mask of which fields were changed. |

---

## TextStyleSuggestionState

Indicates which `TextStyle` fields have suggested changes.

| Field | Type | Description |
|-------|------|-------------|
| `boldSuggested` | boolean | Bold was changed. |
| `italicSuggested` | boolean | Italic was changed. |
| `underlineSuggested` | boolean | Underline was changed. |
| `strikethroughSuggested` | boolean | Strikethrough was changed. |
| `smallCapsSuggested` | boolean | Small caps was changed. |
| `backgroundColorSuggested` | boolean | Background color was changed. |
| `foregroundColorSuggested` | boolean | Foreground color was changed. |
| `fontSizeSuggested` | boolean | Font size was changed. |
| `weightedFontFamilySuggested` | boolean | Font family was changed. |
| `baselineOffsetSuggested` | boolean | Baseline offset was changed. |
| `linkSuggested` | boolean | Link was changed. |

---

## SuggestedParagraphStyle

A suggested modification to paragraph formatting.

| Field | Type | Description |
|-------|------|-------------|
| `paragraphStyle` | [`ParagraphStyle`](./05-styles.md#paragraphstyle) | The proposed paragraph style values. |
| `paragraphStyleSuggestionState` | [`ParagraphStyleSuggestionState`](#paragraphstylesuggestionstate) | Mask of changed fields. |

---

## ParagraphStyleSuggestionState

Indicates which `ParagraphStyle` fields have suggested changes.

| Field | Type | Description |
|-------|------|-------------|
| `headingIdSuggested` | boolean | |
| `namedStyleTypeSuggested` | boolean | |
| `alignmentSuggested` | boolean | |
| `lineSpacingSuggested` | boolean | |
| `directionSuggested` | boolean | |
| `spacingModeSuggested` | boolean | |
| `spaceAboveSuggested` | boolean | |
| `spaceBelowSuggested` | boolean | |
| `borderBetweenSuggested` | boolean | |
| `borderTopSuggested` | boolean | |
| `borderBottomSuggested` | boolean | |
| `borderLeftSuggested` | boolean | |
| `borderRightSuggested` | boolean | |
| `indentFirstLineSuggested` | boolean | |
| `indentStartSuggested` | boolean | |
| `indentEndSuggested` | boolean | |
| `keepLinesTogetherSuggested` | boolean | |
| `keepWithNextSuggested` | boolean | |
| `avoidWidowAndOrphanSuggested` | boolean | |
| `shadingSuggestionState` | `ShadingSuggestionState` | |
| `pageBreakBeforeSuggested` | boolean | |

---

## SuggestedBullet

A suggested modification to bullet formatting.

| Field | Type | Description |
|-------|------|-------------|
| `bullet` | [`Bullet`](./07-lists-named-ranges.md#bullet) | The proposed bullet config. |
| `bulletSuggestionState` | [`BulletSuggestionState`](#bulletsuggestionstate) | Mask of changed fields. |

---

## BulletSuggestionState

Indicates which `Bullet` fields have suggested changes.

| Field | Type | Description |
|-------|------|-------------|
| `listIdSuggested` | boolean | List ID was changed. |
| `nestingLevelSuggested` | boolean | Nesting level was changed. |
| `textStyleSuggestionState` | [`TextStyleSuggestionState`](#textstylesuggestionstate) | Text style changes. |

---

## SuggestedListProperties

A suggested modification to list properties.

| Field | Type | Description |
|-------|------|-------------|
| `listProperties` | [`ListProperties`](./07-lists-named-ranges.md#listproperties) | Modified configuration. |
| `listPropertiesSuggestionState` | [`ListPropertiesSuggestionState`](#listpropertiessuggestionstate) | Changed fields mask. |

---

## ListPropertiesSuggestionState

| Field | Type | Description |
|-------|------|-------------|
| `nestingLevelsSuggestionStates[]` | [`NestingLevelSuggestionState`](#nestinglevelsuggestionstate) | Per-level change indicators. |

---

## NestingLevelSuggestionState

Indicates which `NestingLevel` fields have suggested changes.

| Field | Type | Description |
|-------|------|-------------|
| `bulletAlignmentSuggested` | boolean | |
| `formatSuggested` | boolean | |
| `glyphFormatSuggested` | boolean | |
| `glyphSymbolSuggested` | boolean | |
| `glyphTypeSuggested` | boolean | |
| `indentFirstLineSuggested` | boolean | |
| `indentStartSuggested` | boolean | |
| `startNumberSuggested` | boolean | |
| `textStyleSuggestionState` | [`TextStyleSuggestionState`](#textstylesuggestionstate) | |

---

## SuggestedDocumentStyle

| Field | Type | Description |
|-------|------|-------------|
| `documentStyle` | [`DocumentStyle`](./05-styles.md#documentstyle) | Proposed document style. |
| `documentStyleSuggestionState` | `DocumentStyleSuggestionState` | Changed fields mask. |

---

## SuggestedNamedStyles

| Field | Type | Description |
|-------|------|-------------|
| `namedStyles` | [`NamedStyles`](./05-styles.md#namedstyles) | Proposed named styles. |
| `namedStylesSuggestionState` | `NamedStylesSuggestionState` | Changed fields mask. |

---

## Object Suggestion States

### EmbeddedObjectSuggestionState

| Field | Type | Description |
|-------|------|-------------|
| `embeddedDrawingPropertiesSuggestionState` | `EmbeddedDrawingPropertiesSuggestionState` | Drawing changes. |
| `embeddedObjectBorderSuggestionState` | [`EmbeddedObjectBorderSuggestionState`](#embeddedobjectbordersuggestionstate) | Border changes. |
| `imagePropertiesSuggestionState` | [`ImagePropertiesSuggestionState`](#imagepropertiessuggestionstate) | Image changes. |
| `linkedContentReferenceSuggestionState` | `LinkedContentReferenceSuggestionState` | Link changes. |
| `titleSuggested` | boolean | |
| `descriptionSuggested` | boolean | |

### EmbeddedObjectBorderSuggestionState

| Field | Type | Description |
|-------|------|-------------|
| `colorSuggested` | boolean | |
| `dashStyleSuggested` | boolean | |
| `propertyStateSuggested` | boolean | |
| `widthSuggested` | boolean | |

### ImagePropertiesSuggestionState

| Field | Type | Description |
|-------|------|-------------|
| `angleSuggested` | boolean | |
| `brightnessSuggested` | boolean | |
| `contentUriSuggested` | boolean | |
| `contrastSuggested` | boolean | |
| `cropPropertiesSuggestionState` | [`CropPropertiesSuggestionState`](#croppropertiessuggestionstate) | |
| `originalHeightSuggested` | boolean | |
| `originalWidthSuggested` | boolean | |
| `transparencySuggested` | boolean | |

### CropPropertiesSuggestionState

| Field | Type | Description |
|-------|------|-------------|
| `offsetTopSuggested` | boolean | |
| `offsetBottomSuggested` | boolean | |
| `offsetLeftSuggested` | boolean | |
| `offsetRightSuggested` | boolean | |

### PositionedObjectPositioningSuggestionState

| Field | Type | Description |
|-------|------|-------------|
| `layoutSuggested` | boolean | |
| `leftOffsetSuggested` | boolean | |
| `topOffsetSuggested` | boolean | |
