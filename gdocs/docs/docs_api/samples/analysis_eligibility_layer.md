# Feature Analysis: Copy of Eligibility Layer and Shadow Test - Q1 2026

## Summary
- Document size: 997,473 bytes (974.1 KB)
- Total structural elements: 192
- Number of tabs: 4 (Product Brief, Requirements/Scope, Options Considered, FAQs)
- Key finding: This document demonstrates **multi-tab structure** with diverse table dimensions (up to 10x8), explicit cell styling with custom border colors and padding, merged cells, and **weightedFontFamily** usage showing font weight specifications beyond just font name.

## Element Inventory
| Element Type | Count | Notable Details |
|---|---|---|
| paragraph | 182 | Includes headings and normal text |
| table | 6 | Ranges from 1x2 to 10x8 dimensions |
| sectionBreak | 4 | CONTINUOUS type with LEFT_TO_RIGHT direction |
| pageBreak | 0 | None found |
| inlineObjectElement | 0 | No images |
| footnotes | 0 | None found |
| suggestions | 0 | No tracked changes |

## New/Unique Features (not in existing sample)

### 1. Multiple Tabs with Distinct Content Areas

This document uses **4 tabs** to organize content into logical sections, unlike the baseline single-tab document.

```json
{
  "tabs": [
    {
      "tabProperties": {
        "tabId": "t.0",
        "title": "Product Brief - The Why",
        "index": 0
      }
    },
    {
      "tabProperties": {
        "tabId": "t.ker7bo1h35gv",
        "title": "Requirements/Scope - The How",
        "index": 1
      }
    }
  ]
}
```

> Each tab has a unique `tabId` (some generated, some default), a human-readable `title`, and a zero-indexed `index`. Content is scoped to each tab under `documentTab.body.content`.

### 2. Weighted Font Family with Explicit Weight

Instead of just specifying a font name, this document uses `weightedFontFamily` with an explicit `weight` property.

```json
{
  "textRun": {
    "content": "\n",
    "textStyle": {
      "weightedFontFamily": {
        "fontFamily": "Calibri",
        "weight": 400
      },
      "fontSize": {}
    }
  }
}
```

> The `weight` field allows precise font weight specification (100-900 scale). A `weight` of 400 is normal, 700 is bold. This is more granular than the boolean `bold` property. Note the `fontSize: {}` is a sparse field meaning "use inherited font size."

### 3. Heading IDs with Custom Line Spacing

Paragraphs include `headingId` for linking/navigation and custom `lineSpacing` values.

```json
{
  "paragraphStyle": {
    "headingId": "h.cwncbzfs8bbz",
    "namedStyleType": "HEADING_2",
    "lineSpacing": 107.916664,
    "direction": "LEFT_TO_RIGHT",
    "spacingMode": "NEVER_COLLAPSE",
    "spaceAbove": {
      "unit": "PT"
    },
    "spaceBelow": {
      "unit": "PT"
    },
    "avoidWidowAndOrphan": false
  }
}
```

> `headingId` enables deep linking to specific sections. `lineSpacing` of 107.916664 represents ~108% line height. The sparse fields `spaceAbove` and `spaceBelow` with only `"unit": "PT"` mean **zero spacing** (no `magnitude` = 0).

### 4. Merged Cells with Explicit Border Styling

Tables contain merged cells spanning multiple columns, with detailed border color and padding specifications.

```json
{
  "tableCellStyle": {
    "rowSpan": 1,
    "columnSpan": 2,
    "backgroundColor": {},
    "borderLeft": {
      "color": {
        "color": {
          "rgbColor": {
            "red": 0.6431373,
            "green": 0.7607843,
            "blue": 0.95686275
          }
        }
      },
      "width": {
        "magnitude": 1,
        "unit": "PT"
      },
      "dashStyle": "SOLID"
    },
    "borderRight": {
      "color": {
        "color": {
          "rgbColor": {
            "red": 0.6431373,
            "green": 0.7607843,
            "blue": 0.95686275
          }
        }
      },
      "width": {
        "magnitude": 1,
        "unit": "PT"
      },
      "dashStyle": "SOLID"
    },
    "borderTop": {
      "color": {
        "color": {
          "rgbColor": {
            "red": 0.6431373,
            "green": 0.7607843,
            "blue": 0.95686275
          }
        }
      },
      "width": {
        "magnitude": 1,
        "unit": "PT"
      },
      "dashStyle": "SOLID"
    },
    "borderBottom": {
      "color": {
        "color": {
          "rgbColor": {
            "red": 0.6431373,
            "green": 0.7607843,
            "blue": 0.95686275
          }
        }
      },
      "width": {
        "magnitude": 1,
        "unit": "PT"
      },
      "dashStyle": "SOLID"
    },
    "paddingLeft": {
      "magnitude": 5,
      "unit": "PT"
    },
    "paddingRight": {
      "magnitude": 5,
      "unit": "PT"
    },
    "paddingTop": {
      "magnitude": 5,
      "unit": "PT"
    },
    "paddingBottom": {
      "magnitude": 5,
      "unit": "PT"
    },
    "contentAlignment": "TOP"
  }
}
```

> `columnSpan: 2` indicates this cell merges across 2 columns. All four borders have custom light blue color (RGB: 0.64, 0.76, 0.96), 1PT width, and SOLID style. The empty `backgroundColor: {}` means **transparent** (explicitly no color, not inherited). Uniform 5PT padding on all sides.

### 5. Large Multi-Column Tables

The document includes a 10-row × 8-column table, significantly larger than the baseline sample.

```json
{
  "rows": 10,
  "columns": 8,
  "firstRow": {
    "startIndex": 3067,
    "endIndex": 3230,
    "cellCount": 8,
    "sampleCell": {
      "startIndex": 3068,
      "endIndex": 3091,
      "tableCellStyle": {
        "rowSpan": 1,
        "columnSpan": 1,
        "backgroundColor": {
          "color": {
            "rgbColor": {
              "red": 0.9372549,
              "green": 0.9372549,
              "blue": 0.9372549
            }
          }
        },
        "paddingLeft": {
          "magnitude": 5,
          "unit": "PT"
        },
        "paddingRight": {
          "magnitude": 5,
          "unit": "PT"
        },
        "paddingTop": {
          "magnitude": 5,
          "unit": "PT"
        },
        "paddingBottom": {
          "magnitude": 5,
          "unit": "PT"
        },
        "contentAlignment": "TOP"
      }
    }
  }
}
```

> This 10×8 table demonstrates handling of wide, multi-column data layouts. The sample cell shows a light gray background (RGB: 0.94, 0.94, 0.94) — unlike the merged cell's empty `backgroundColor: {}`, this one explicitly sets a gray color. Both use 5PT padding on all sides.

### 6. Hyperlinks with Heading References

Links include URL references to other Google Docs with specific heading anchors.

```json
{
  "textRun": {
    "content": "The Below Table is from an analysis into Q3 2025 Domestic, CNC, Default Grouping",
    "textStyle": {
      "link": {
        "url": "https://docs.google.com/document/d/1OBEMSd4OK3DFe6tbMoLvCOHnwN3VrazamyCAmPm4cBI/edit?tab=t.0#heading=h.g36twfkncjpg"
      },
      "underline": true,
      "foregroundColor": {
        "color": {
          "rgbColor": {
            "red": 0.06666667,
            "green": 0.33333334,
            "blue": 0.8
          }
        }
      }
    }
  }
}
```

> The URL includes `#heading=h.g36twfkncjpg` anchor for deep linking to a specific section. The link uses standard blue color (RGB: 0.07, 0.33, 0.8) and is underlined, following typical hyperlink styling conventions.

## Style Diversity

### Named Styles Used
- **NORMAL_TEXT**: 156 occurrences (majority of document)
- **HEADING_2**: 25 occurrences
- **HEADING_3**: 1 occurrence

> This document uses a flatter heading hierarchy than the baseline (which included HEADING_1, HEADING_2, HEADING_3). Most structure comes from HEADING_2 and tables.

### Font Families
- **Calibri**: 2 occurrences (document title styling)
- **Open Sans**: 2 occurrences (body text)

> Mix of system font (Calibri) and Google font (Open Sans), unlike baseline which likely uses default Docs fonts.

### Font Sizes
- 6 PT: 1 occurrence (very small, possibly for spacing)
- 10 PT: 26 occurrences
- 11 PT: 1 occurrence
- 12 PT: 1 occurrence
- 13 PT: 26 occurrences (most common body text)

> Tighter size range than typical documents. Predominant sizes are 10PT and 13PT.

### Colors Used (Foreground)
- Black: (0, 0, 0)
- Blue link color: (0.07, 0.33, 0.8)
- Dark blue/gray: (0.11, 0.13, 0.15)
- Medium blue: (0.18, 0.46, 0.71)
- Red: (1, 0, 0)

> 5 distinct colors, including brand/theme colors (medium blue for headings) and accent colors (red for emphasis).

### Text Decorations
- **bold**: 3 occurrences
- **underline**: 2 occurrences (likely links)
- **italic**: 1 occurrence

> Minimal text decoration usage, relying more on color and font size for visual hierarchy.

## Interesting Snippets

### 1. Section Break Structure
```json
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
```
> Section breaks define page layout regions. `CONTINUOUS` means no column layout change. `columnSeparatorStyle: "NONE"` indicates single-column layout (no separator lines). These typically appear at tab boundaries.

### 2. Sparse Field Pattern: Empty Font Size
```json
{
  "textStyle": {
    "weightedFontFamily": {
      "fontFamily": "Calibri",
      "weight": 400
    },
    "fontSize": {}
  }
}
```
> An empty `fontSize: {}` object means "inherit from named style" — this is distinct from omitting the `fontSize` field entirely. The presence of the empty object signals "I checked and chose to inherit."

### 3. Sparse Field Pattern: Zero Spacing
```json
{
  "paragraphStyle": {
    "namedStyleType": "HEADING_2",
    "spaceAbove": {
      "unit": "PT"
    },
    "spaceBelow": {
      "unit": "PT"
    }
  }
}
```
> When `spaceAbove` or `spaceBelow` contains only `"unit": "PT"` without a `magnitude` field, this means **zero points of spacing**. This sparse representation saves bytes compared to `"magnitude": 0`.

### 4. Content Alignment in Table Cells
```json
{
  "tableCellStyle": {
    "contentAlignment": "TOP"
  }
}
```
> `contentAlignment: "TOP"` vertically aligns cell content to the top edge. Other values include "MIDDLE" and "BOTTOM". This is separate from horizontal text alignment within paragraphs.

### 5. Transparent Background vs. Explicit Color
```json
// Transparent (no background color)
{
  "tableCellStyle": {
    "backgroundColor": {}
  }
}

// Explicit gray background
{
  "tableCellStyle": {
    "backgroundColor": {
      "color": {
        "rgbColor": {
          "red": 0.9372549,
          "green": 0.9372549,
          "blue": 0.9372549
        }
      }
    }
  }
}
```
> The empty `backgroundColor: {}` means "transparent/no fill" — the cell inherits whatever is behind it (usually white). When a color is explicitly set with RGB values, it overrides any default. This distinction is critical for cell styling.

### 6. Border Styling with Custom Colors
```json
{
  "borderLeft": {
    "color": {
      "color": {
        "rgbColor": {
          "red": 0.6431373,
          "green": 0.7607843,
          "blue": 0.95686275
        }
      }
    },
    "width": {
      "magnitude": 1,
      "unit": "PT"
    },
    "dashStyle": "SOLID"
  }
}
```
> Each border (left, right, top, bottom) can have independent color, width, and style. `dashStyle` values include "SOLID", "DOTTED", "DASHED". The nested color structure allows for theme colors vs. explicit RGB.

## Comparison to Baseline Sample

### What's Similar
- Uses tables with merged cells
- Contains hyperlinks
- Uses named styles (HEADING_2, NORMAL_TEXT)
- Has section breaks
- Includes bold/underline text decorations

### What's Different/New
1. **Multi-tab structure** (4 tabs vs. 1)
2. **Weighted font families** with explicit weight values
3. **Larger tables** (10×8 vs. smaller in baseline)
4. **Custom border colors** on table cells (light blue theme)
5. **Explicit cell padding** values (5PT uniform)
6. **Heading IDs** for deep linking
7. **Custom line spacing** values (107.916664)
8. **Sparse field usage** for zero spacing (`spaceAbove: {"unit": "PT"}`)
9. **Font diversity** (Calibri + Open Sans vs. default fonts)
10. **Limited heading hierarchy** (mostly HEADING_2, one HEADING_3, no HEADING_1)

## Testing Recommendations

To ensure robust handling of this document's features, test:

1. **Multi-tab operations**: Verify content modifications work across all 4 tabs
2. **Large table navigation**: Ensure 10×8 table cell access and modification works correctly
3. **Merged cell handling**: Test reading/writing to cells with `columnSpan > 1`
4. **Border style preservation**: Verify custom border colors survive round-trip edits
5. **Heading ID references**: Ensure heading IDs remain stable after content edits
6. **Sparse field handling**: Confirm zero spacing (`{"unit": "PT"}`) is preserved vs. being interpreted as "inherit"
7. **Weighted font rendering**: Test that `weightedFontFamily` weights are respected
8. **Deep link generation**: Validate heading anchor URLs are correctly constructed

## Document Use Case

Based on the content and structure, this appears to be a **product requirements document (PRD)** or **technical design document** with:
- Product overview/rationale (Tab 1: "The Why")
- Technical specifications (Tab 2: "The How")
- Design alternatives (Tab 3: "Options Considered")
- FAQ/clarifications (Tab 4: "FAQs")

The multi-tab structure, large comparison tables (10×8), cross-document references, and structured heading IDs suggest this is a **collaborative planning document** used by product/engineering teams for decision-making and alignment.
