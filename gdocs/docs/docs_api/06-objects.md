# Objects & Positioning

Embedded and positioned objects within a document (images, drawings, charts).

## InlineObject

An object embedded inline with text.

| Field | Type | Description |
|-------|------|-------------|
| `objectId` | string | Output only. Unique object identifier. |
| `inlineObjectProperties` | [`InlineObjectProperties`](#inlineobjectproperties) | Object configuration. |
| `suggestedInlineObjectPropertiesChanges` | map<string, `SuggestedInlineObjectProperties`> | Suggested property changes. |
| `suggestedInsertionId` | string | Suggestion ID if this object was suggested. |
| `suggestedDeletionIds[]` | string | Suggestion IDs proposing deletion. |

---

## InlineObjectProperties

Properties for an inline object.

| Field | Type | Description |
|-------|------|-------------|
| `embeddedObject` | [`EmbeddedObject`](#embeddedobject) | The embedded content. |

### Sample Response — Embedded Image

```json
{
  "kix.16a2leki7wtf": {
    "objectId": "kix.16a2leki7wtf",
    "inlineObjectProperties": {
      "embeddedObject": {
        "imageProperties": {
          "contentUri": "https://lh7-rt.googleusercontent.com/docsz/AD_4nXfWTEcovHoiZ_IRjgxOSKFpas5i96OiAXY89i2JGjnDnI1JNS6ZetNiftarEi0D48ciKLwG9Mmgce-bITLgWoSkA3ap8yben6AgzAn-0VMLaSgFr3TMV3CxPyD7RsIsM57CW9SxhHZDKzbnLlhDogLeaxTm?key=ca7LIdFW1wY8kSYymF0-sA",
          "cropProperties": {}
        },
        "embeddedObjectBorder": {
          "color": { "color": { "rgbColor": {} } },
          "width": { "unit": "PT" },
          "dashStyle": "SOLID",
          "propertyState": "NOT_RENDERED"
        },
        "size": {
          "height": { "magnitude": 184, "unit": "PT" },
          "width": { "magnitude": 468, "unit": "PT" }
        },
        "marginTop": { "magnitude": 9, "unit": "PT" },
        "marginBottom": { "magnitude": 9, "unit": "PT" },
        "marginRight": { "magnitude": 9, "unit": "PT" },
        "marginLeft": { "magnitude": 9, "unit": "PT" }
      }
    }
  }
}
```

> An image from the tab-level `inlineObjects` dictionary (with `includeTabsContent=true`, inline objects are stored at `tabs[n].documentTab.inlineObjects`, not at the document root). The `propertyState: "NOT_RENDERED"` on the border means no visible border. Empty `cropProperties: {}` means no cropping. Empty `rgbColor: {}` in the border color means transparent/black default. Default 9PT margins on all sides.

---

## PositionedObject

An object with absolute positioning within a document.

| Field | Type | Description |
|-------|------|-------------|
| `objectId` | string | Output only. Unique object identifier. |
| `positionedObjectProperties` | [`PositionedObjectProperties`](#positionedobjectproperties) | Configuration and appearance. |
| `suggestedPositionedObjectPropertiesChanges` | map | Suggested property changes. |
| `suggestedInsertionId` | string | Suggestion ID if this object was suggested. |
| `suggestedDeletionIds[]` | string | Suggestion IDs proposing deletion. |

---

## PositionedObjectProperties

Configuration for a positioned object.

| Field | Type | Description |
|-------|------|-------------|
| `embeddedObject` | [`EmbeddedObject`](#embeddedobject) | The embedded content. |
| `positioning` | [`PositionedObjectPositioning`](#positionedobjectpositioning) | Layout and anchor settings. |

---

## PositionedObjectPositioning

Controls how a positioned object is anchored relative to text.

| Field | Type | Description |
|-------|------|-------------|
| `layout` | enum [`PositionedObjectLayout`](./11-enums.md#positionedobjectlayout) | Text wrapping mode. |
| `leftOffset` | [`Dimension`](./12-common-types.md#dimension) | Distance from left margin/anchor. |
| `topOffset` | [`Dimension`](./12-common-types.md#dimension) | Distance from top margin/anchor. |

---

## EmbeddedObject

The actual content embedded within an object. Union of specific object types.

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Descriptive title. |
| `description` | string | Detailed description. |
| `embeddedObjectBorder` | [`EmbeddedObjectBorder`](#embeddedobjectborder) | Border styling. |
| `embeddedDrawingProperties` | `EmbeddedDrawingProperties` | Drawing-specific config (currently empty). |
| `imageProperties` | [`ImageProperties`](#imageproperties) | Image-specific metadata. |
| `linkedContentReference` | [`LinkedContentReference`](#linkedcontentreference) | External content link. |
| `sheetsChartReference` | [`SheetsChartReference`](#sheetschartreference) | Embedded Sheets chart. |

---

## EmbeddedObjectBorder

Border styling for embedded objects.

| Field | Type | Description |
|-------|------|-------------|
| `color` | [`OptionalColor`](./12-common-types.md#optionalcolor) | Border color. |
| `width` | [`Dimension`](./12-common-types.md#dimension) | Border thickness. |
| `dashStyle` | enum [`DashStyle`](./11-enums.md#dashstyle) | Line pattern. |
| `propertyState` | enum [`PropertyState`](./11-enums.md#propertystate) | Whether border is rendered. |

---

## ImageProperties

Metadata and styling for embedded images.

| Field | Type | Description |
|-------|------|-------------|
| `contentUri` | string | URI where the image is hosted. |
| `brightness` | number | Brightness adjustment (-1.0 to 1.0). |
| `contrast` | number | Contrast adjustment (-1.0 to 1.0). |
| `transparency` | number | Opacity level (0.0 to 1.0). |
| `angle` | number | Clockwise rotation in degrees (0–360). |
| `cropProperties` | [`CropProperties`](#cropproperties) | Cropping settings. |
| `originalWidth` | [`Dimension`](./12-common-types.md#dimension) | Image width at 100% scale. |
| `originalHeight` | [`Dimension`](./12-common-types.md#dimension) | Image height at 100% scale. |
| `byteSize` | integer | Output only. File size in bytes. |

---

## CropProperties

Image cropping configuration. Values are proportional (0.0 to 1.0).

| Field | Type | Description |
|-------|------|-------------|
| `offsetTop` | number | Distance from top edge. |
| `offsetBottom` | number | Distance from bottom edge. |
| `offsetLeft` | number | Distance from left edge. |
| `offsetRight` | number | Distance from right edge. |

---

## LinkedContentReference

Reference to external content linked within an embedded object.

| Field | Type | Description |
|-------|------|-------------|
| `sheetsChartReference` | [`SheetsChartReference`](#sheetschartreference) | Reference to a Sheets chart. |

---

## SheetsChartReference

Identifies a specific chart from a Google Sheets document.

| Field | Type | Description |
|-------|------|-------------|
| `spreadsheetId` | string | The Sheets document ID. |
| `chartId` | integer | The specific chart identifier within the sheet. |

---

## Size

Dimensions with both width and height.

| Field | Type | Description |
|-------|------|-------------|
| `height` | [`Dimension`](./12-common-types.md#dimension) | Vertical measurement. |
| `width` | [`Dimension`](./12-common-types.md#dimension) | Horizontal measurement. |
