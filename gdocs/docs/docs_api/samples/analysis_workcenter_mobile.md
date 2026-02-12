# Feature Analysis: Copy of Workcenter Mobile Spec Requirements

## Summary
- **Document size**: 14 MB (336,724 lines)
- **Total paragraphs**: 4,324
- **Total tables**: 102
- **Key finding**: This large multi-tab specification document demonstrates advanced Google Docs features including `person` chips (59 occurrences), embedded images (157 inline objects), hierarchical tab structure with nested child tabs, table headers, and 2-level nested bullet lists. It contains far more complex table structures and organizational hierarchy than the existing baseline sample.

## Element Inventory
| Element Type | Count | Notable Details |
|---|---|---|
| Paragraphs | 4,324 | Mix of headings (HEADING_1-3), normal text, and bulleted content |
| Tables | 102 | Multi-row/column structures with table headers (14 tables), fixed column widths |
| Bullet Lists | 537+ | Standard bullet glyphs (●, ○, ■) with 2-level nesting |
| Inline Object Elements | 157 | Embedded images with contentUri, size, margins, cropProperties |
| Person Elements | 59 | @-mention chips with name, email, personId |
| Tabs | 3+ | Multiple tabs including "Original RFP for work", "Completed" with nested child tabs |
| Links | Many | Hyperlinks with underlined blue text style |
| Named Styles | 8 | HEADING_1-6, TITLE, SUBTITLE, NORMAL_TEXT |

## New/Unique Features (not in existing sample)

### 1. Person Chips (@-mentions)
The document uses `person` elements to tag team members in tables and text. Each person has a unique `personId` and displays name/email.

```json
{
  "startIndex": 194,
  "endIndex": 195,
  "person": {
    "personId": "kix.xeznx9jz258t",
    "textStyle": {},
    "personProperties": {
      "name": "Vaidy Raghavan",
      "email": "vaidy.raghavan@xometry.com"
    }
  }
}
```

> Person chips are rendered as single-character elements in the content stream but carry full name/email metadata. Multiple person chips can appear consecutively in table cells to list team members.

### 2. Hierarchical Tab Structure with Child Tabs
The document uses a multi-level tab hierarchy with `childTabs` arrays and `nestingLevel` properties.

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
      }
    }
  ]
}
```

> The baseline sample has a single flat tab. This document demonstrates that tabs can be organized hierarchically using `parentTabId` and `nestingLevel`, creating an outline-style structure with 191+ nestingLevel references across the document.

### 3. Table Headers
The document uses `"tableHeader": true` on row styles to designate header rows (14 occurrences).

```json
{
  "startIndex": 548,
  "endIndex": 609,
  "tableCells": [
    {
      "startIndex": 549,
      "endIndex": 558,
      "content": [
        {
          "startIndex": 550,
          "endIndex": 558,
          "paragraph": {
            "elements": [
              {
                "startIndex": 550,
                "endIndex": 558,
                "textRun": {
                  "content": "Journey\n",
                  "textStyle": {
                    "bold": true
                  }
                }
              }
            ]
          }
        }
      ]
    }
  ],
  "tableRowStyle": {
    "minRowHeight": {
      "unit": "PT"
    },
    "tableHeader": true
  }
}
```

> Table headers are marked at the row level with `tableHeader: true`. Header cells typically use bold text for visual emphasis.

### 4. Large Multi-Column Tables with Fixed Widths
This document contains large tables (up to 14 rows x 6 columns) with explicit fixed-width column sizing.

```json
{
  "startIndex": 547,
  "endIndex": 6282,
  "table": {
    "rows": 14,
    "columns": 6,
    "tableStyle": {
      "tableColumnProperties": [
        {
          "widthType": "FIXED_WIDTH",
          "width": {
            "magnitude": 69.75,
            "unit": "PT"
          }
        },
        {
          "widthType": "FIXED_WIDTH",
          "width": {
            "magnitude": 131.25,
            "unit": "PT"
          }
        }
      ]
    }
  }
}
```

> The baseline sample uses 2-3 column tables. This document demonstrates 6-column tables spanning thousands of character positions (indices 547-6282) with per-column width specifications.

### 5. Inline Object Elements (Embedded Images)
The document contains 157 embedded images with `inlineObjectElement` references and full image metadata in the `inlineObjects` dictionary.

```json
{
  "startIndex": 8170,
  "endIndex": 8171,
  "inlineObjectElement": {
    "inlineObjectId": "kix.749oi8whobp5",
    "textStyle": {}
  }
}
```

And the corresponding inline object definition:

```json
"inlineObjects": {
  "kix.3dtsqzq6fap": {
    "objectId": "kix.3dtsqzq6fap",
    "inlineObjectProperties": {
      "embeddedObject": {
        "imageProperties": {
          "contentUri": "https://lh7-rt.googleusercontent.com/docsz/AD_4nXdJpY6e4r3blqG_-SFJrH5RHMuk76N2qFkSPoyYHJoMDFzUbSpqh0uhS1bXW__KGWZ5NuD76spdtoqXDeaMfxL2PZY3iByOYNLR0icfI62PrOLhhJ9_MTnhDkIzDP4csFEEDA89RZvZWCjANs5W5YEKY6ZF6E5Koe4WzQpOC7CfLsTXGw?key=-R3OkhEkMxp8YSWyM4uWBA",
          "cropProperties": {}
        },
        "embeddedObjectBorder": {
          "color": {
            "color": {
              "rgbColor": {}
            }
          },
          "width": {
            "unit": "PT"
          },
          "dashStyle": "SOLID",
          "propertyState": "NOT_RENDERED"
        },
        "size": {
          "height": {
            "magnitude": 24,
            "unit": "PT"
          },
          "width": {
            "magnitude": 60.75,
            "unit": "PT"
          }
        },
        "marginTop": {
          "magnitude": 9,
          "unit": "PT"
        },
        "marginBottom": {
          "magnitude": 9,
          "unit": "PT"
        },
        "marginRight": {
          "magnitude": 9,
          "unit": "PT"
        },
        "marginLeft": {
          "magnitude": 9,
          "unit": "PT"
        }
      }
    }
  }
}
```

> Inline object elements occupy a single character position in the content stream but reference detailed metadata in the tab's `inlineObjects` dictionary. Images include `contentUri` (Google CDN URL), explicit size dimensions, margins, border styles, and crop properties.

### 6. PAGELESS Document Mode
The document uses pageless mode, which affects layout and rendering.

```json
"documentStyle": {
  "background": {
    "color": {}
  },
  "pageNumberStart": 1,
  "marginTop": {
    "magnitude": 72,
    "unit": "PT"
  },
  "marginBottom": {
    "magnitude": 72,
    "unit": "PT"
  },
  "marginRight": {
    "magnitude": 72,
    "unit": "PT"
  },
  "marginLeft": {
    "magnitude": 72,
    "unit": "PT"
  },
  "pageSize": {
    "height": {
      "magnitude": 792,
      "unit": "PT"
    },
    "width": {
      "magnitude": 612,
      "unit": "PT"
    }
  },
  "marginHeader": {
    "magnitude": 36,
    "unit": "PT"
  },
  "marginFooter": {
    "magnitude": 36,
    "unit": "PT"
  },
  "useCustomHeaderFooterMargins": true,
  "documentFormat": {
    "documentMode": "PAGELESS"
  }
}
```

> The `documentMode: "PAGELESS"` setting indicates continuous scroll layout (like Google Docs' default view) rather than page-based layout. This is a per-tab setting that affects how margins and page breaks are handled.

### 7. 2-Level Nested Bullet Lists
The document uses list nesting with `nestingLevel: 1` to create sub-bullets.

```json
{
  "startIndex": 8100,
  "endIndex": 8126,
  "paragraph": {
    "elements": [
      {
        "startIndex": 8100,
        "endIndex": 8126,
        "textRun": {
          "content": "Tie in notifications here\n",
          "textStyle": {}
        }
      }
    ],
    "paragraphStyle": {
      "namedStyleType": "NORMAL_TEXT",
      "direction": "LEFT_TO_RIGHT",
      "indentFirstLine": {
        "magnitude": 54,
        "unit": "PT"
      },
      "indentStart": {
        "magnitude": 72,
        "unit": "PT"
      }
    },
    "bullet": {
      "listId": "kix.m6yi3wvzwcl5",
      "nestingLevel": 1,
      "textStyle": {}
    }
  }
}
```

And the corresponding list properties showing multiple nesting levels:

```json
"kix.m6yi3wvzwcl5": {
  "listProperties": {
    "nestingLevels": [
      {
        "bulletAlignment": "START",
        "glyphSymbol": "●",
        "glyphFormat": "%0",
        "indentFirstLine": {
          "magnitude": 18,
          "unit": "PT"
        },
        "indentStart": {
          "magnitude": 36,
          "unit": "PT"
        },
        "textStyle": {
          "underline": false
        },
        "startNumber": 1
      },
      {
        "bulletAlignment": "START",
        "glyphSymbol": "○",
        "glyphFormat": "%1",
        "indentFirstLine": {
          "magnitude": 54,
          "unit": "PT"
        },
        "indentStart": {
          "magnitude": 72,
          "unit": "PT"
        },
        "textStyle": {
          "underline": false
        },
        "startNumber": 1
      }
    ]
  }
}
```

> The baseline sample shows only flat bullet lists. This document demonstrates 2-level nesting (levels 0-1) with different glyph symbols at each level (● at level 0, ○ at level 1). The `nestingLevel` field on the bullet determines which level's formatting to use. Lists can support up to 9 nesting levels (0-8) as defined in the `nestingLevels` array.

## Style Diversity

The document uses the full standard set of named styles:
- **Headings**: HEADING_1 (20pt), HEADING_2 (16pt), HEADING_3 (14pt gray), HEADING_4-6 (12pt-11pt gray, HEADING_6 italic)
- **Title/Subtitle**: TITLE (26pt), SUBTITLE (15pt gray)
- **Normal text**: NORMAL_TEXT (11pt Arial, 115% line spacing)

Text styling includes:
- **Bold** text in table headers and emphasis
- **Underlined blue links** (RGB: 0.067, 0.333, 0.8) for URLs
- Standard paragraph spacing and indentation for bullets (18pt first line, 36pt start)

## Comparison to Baseline

The baseline sample (`sample_document.json`) contains:
- Simple 2-3 column tables without headers
- Flat bullet lists only (no nesting)
- Basic named styles (HEADING_1-3, NORMAL_TEXT)
- No person chips
- No inline images
- Single tab structure

This new sample adds:
- **Person chips** (team member @-mentions)
- **Hierarchical multi-tab structure** with child tabs
- **Table headers** (`tableHeader: true`)
- **Large multi-column tables** (6 columns, 14 rows)
- **Embedded images** with full metadata (contentUri, size, margins, borders)
- **Nested bullet lists** (2 levels with different glyphs)
- **Pageless document mode** configuration
- **Much larger scale** (14MB, 4,324 paragraphs vs. smaller baseline)

## Interesting Snippets

### Snippet 1: RACI Table with Person Chips

This table demonstrates person chips embedded in table cells to list team members.

```json
{
  "startIndex": 185,
  "endIndex": 302,
  "table": {
    "rows": 6,
    "columns": 2,
    "tableRows": [
      {
        "startIndex": 186,
        "endIndex": 198,
        "tableCells": [
          {
            "startIndex": 187,
            "endIndex": 193,
            "content": [
              {
                "startIndex": 188,
                "endIndex": 193,
                "paragraph": {
                  "elements": [
                    {
                      "startIndex": 188,
                      "endIndex": 193,
                      "textRun": {
                        "content": "Tech\n",
                        "textStyle": {}
                      }
                    }
                  ]
                }
              }
            ]
          },
          {
            "startIndex": 193,
            "endIndex": 198,
            "content": [
              {
                "startIndex": 194,
                "endIndex": 198,
                "paragraph": {
                  "elements": [
                    {
                      "startIndex": 194,
                      "endIndex": 195,
                      "person": {
                        "personId": "kix.xeznx9jz258t",
                        "textStyle": {},
                        "personProperties": {
                          "name": "Vaidy Raghavan",
                          "email": "vaidy.raghavan@xometry.com"
                        }
                      }
                    },
                    {
                      "startIndex": 195,
                      "endIndex": 196,
                      "person": {
                        "personId": "kix.od4jwzec3v2",
                        "textStyle": {},
                        "personProperties": {
                          "name": "Matthew Halbe",
                          "email": "mhalbe@xometry.com"
                        }
                      }
                    },
                    {
                      "startIndex": 196,
                      "endIndex": 197,
                      "person": {
                        "personId": "kix.s0ixrb2d3q0m",
                        "textStyle": {},
                        "personProperties": {
                          "name": "Aaron Johnson",
                          "email": "ajohnson@xometry.com"
                        }
                      }
                    },
                    {
                      "startIndex": 197,
                      "endIndex": 198,
                      "textRun": {
                        "content": "\n",
                        "textStyle": {}
                      }
                    }
                  ]
                }
              }
            ]
          }
        ]
      }
    ]
  }
}
```

### Snippet 2: Large Table with Header Row and Fixed Column Widths

```json
{
  "startIndex": 547,
  "endIndex": 6282,
  "table": {
    "rows": 14,
    "columns": 6,
    "tableRows": [
      {
        "startIndex": 548,
        "endIndex": 609,
        "tableCells": [
          {
            "startIndex": 549,
            "endIndex": 558,
            "content": [
              {
                "startIndex": 550,
                "endIndex": 558,
                "paragraph": {
                  "elements": [
                    {
                      "startIndex": 550,
                      "endIndex": 558,
                      "textRun": {
                        "content": "Journey\n",
                        "textStyle": {
                          "bold": true
                        }
                      }
                    }
                  ]
                }
              }
            ]
          },
          {
            "startIndex": 558,
            "endIndex": 571,
            "content": [
              {
                "startIndex": 559,
                "endIndex": 571,
                "paragraph": {
                  "elements": [
                    {
                      "startIndex": 559,
                      "endIndex": 571,
                      "textRun": {
                        "content": "Touchpoints\n",
                        "textStyle": {
                          "bold": true
                        }
                      }
                    }
                  ]
                }
              }
            ]
          }
        ],
        "tableRowStyle": {
          "minRowHeight": {
            "unit": "PT"
          },
          "tableHeader": true
        }
      }
    ],
    "tableStyle": {
      "tableColumnProperties": [
        {
          "widthType": "FIXED_WIDTH",
          "width": {
            "magnitude": 69.75,
            "unit": "PT"
          }
        },
        {
          "widthType": "FIXED_WIDTH",
          "width": {
            "magnitude": 131.25,
            "unit": "PT"
          }
        },
        {
          "widthType": "FIXED_WIDTH",
          "width": {
            "magnitude": 86.25,
            "unit": "PT"
          }
        }
      ]
    }
  }
}
```

### Snippet 3: Nested Bullet List (Level 1)

```json
{
  "startIndex": 8100,
  "endIndex": 8126,
  "paragraph": {
    "elements": [
      {
        "startIndex": 8100,
        "endIndex": 8126,
        "textRun": {
          "content": "Tie in notifications here\n",
          "textStyle": {}
        }
      }
    ],
    "paragraphStyle": {
      "namedStyleType": "NORMAL_TEXT",
      "direction": "LEFT_TO_RIGHT",
      "indentFirstLine": {
        "magnitude": 54,
        "unit": "PT"
      },
      "indentStart": {
        "magnitude": 72,
        "unit": "PT"
      }
    },
    "bullet": {
      "listId": "kix.m6yi3wvzwcl5",
      "nestingLevel": 1,
      "textStyle": {}
    }
  }
}
```

### Snippet 4: Hierarchical Tab Structure

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

### Snippet 5: Inline Object (Embedded Image) Reference

```json
{
  "startIndex": 8170,
  "endIndex": 8172,
  "paragraph": {
    "elements": [
      {
        "startIndex": 8170,
        "endIndex": 8171,
        "inlineObjectElement": {
          "inlineObjectId": "kix.749oi8whobp5",
          "textStyle": {}
        }
      },
      {
        "startIndex": 8171,
        "endIndex": 8172,
        "textRun": {
          "content": "\n",
          "textStyle": {}
        }
      }
    ],
    "paragraphStyle": {
      "namedStyleType": "NORMAL_TEXT",
      "direction": "LEFT_TO_RIGHT"
    }
  }
}
```

### Snippet 6: Inline Object Metadata (Image Properties)

```json
"inlineObjects": {
  "kix.1moalm5bc3xx": {
    "objectId": "kix.1moalm5bc3xx",
    "inlineObjectProperties": {
      "embeddedObject": {
        "imageProperties": {
          "contentUri": "https://lh7-rt.googleusercontent.com/docsz/AD_4nXdXUfOhFIDb1CE7YwgIGrqQradEJjCL-1TEQniuuTFF-1RZIrtfj1zKHMtxKlV9yB_hZzEcbat1NJ5QvUPT6OHR3SpY4bSCYFIZH-hg8FyR_llsKzmhuQgil53jlCydJHpTHLNnVo4ItiueD9ojWWP5N-s3hAczKICCG580LLgRuEsCBQ?key=-R3OkhEkMxp8YSWyM4uWBA",
          "cropProperties": {}
        },
        "embeddedObjectBorder": {
          "color": {
            "color": {
              "rgbColor": {}
            }
          },
          "width": {
            "unit": "PT"
          },
          "dashStyle": "SOLID",
          "propertyState": "NOT_RENDERED"
        },
        "size": {
          "height": {
            "magnitude": 192.7999188311688,
            "unit": "PT"
          },
          "width": {
            "magnitude": 351.375,
            "unit": "PT"
          }
        },
        "marginTop": {
          "magnitude": 9,
          "unit": "PT"
        },
        "marginBottom": {
          "magnitude": 9,
          "unit": "PT"
        },
        "marginRight": {
          "magnitude": 9,
          "unit": "PT"
        },
        "marginLeft": {
          "magnitude": 9,
          "unit": "PT"
        }
      }
    }
  }
}
```

### Snippet 7: Pageless Document Mode Configuration

```json
"documentStyle": {
  "background": {
    "color": {}
  },
  "pageNumberStart": 1,
  "marginTop": {
    "magnitude": 72,
    "unit": "PT"
  },
  "marginBottom": {
    "magnitude": 72,
    "unit": "PT"
  },
  "marginRight": {
    "magnitude": 72,
    "unit": "PT"
  },
  "marginLeft": {
    "magnitude": 72,
    "unit": "PT"
  },
  "pageSize": {
    "height": {
      "magnitude": 792,
      "unit": "PT"
    },
    "width": {
      "magnitude": 612,
      "unit": "PT"
    }
  },
  "marginHeader": {
    "magnitude": 36,
    "unit": "PT"
  },
  "marginFooter": {
    "magnitude": 36,
    "unit": "PT"
  },
  "useCustomHeaderFooterMargins": true,
  "documentFormat": {
    "documentMode": "PAGELESS"
  }
}
```

### Snippet 8: List Properties with Multiple Nesting Levels

```json
"kix.m6yi3wvzwcl5": {
  "listProperties": {
    "nestingLevels": [
      {
        "bulletAlignment": "START",
        "glyphSymbol": "●",
        "glyphFormat": "%0",
        "indentFirstLine": {
          "magnitude": 18,
          "unit": "PT"
        },
        "indentStart": {
          "magnitude": 36,
          "unit": "PT"
        },
        "textStyle": {
          "underline": false
        },
        "startNumber": 1
      },
      {
        "bulletAlignment": "START",
        "glyphSymbol": "○",
        "glyphFormat": "%1",
        "indentFirstLine": {
          "magnitude": 54,
          "unit": "PT"
        },
        "indentStart": {
          "magnitude": 72,
          "unit": "PT"
        },
        "textStyle": {
          "underline": false
        },
        "startNumber": 1
      },
      {
        "bulletAlignment": "START",
        "glyphSymbol": "■",
        "glyphFormat": "%2",
        "indentFirstLine": {
          "magnitude": 90,
          "unit": "PT"
        },
        "indentStart": {
          "magnitude": 108,
          "unit": "PT"
        },
        "textStyle": {
          "underline": false
        },
        "startNumber": 1
      }
    ]
  }
}
```
