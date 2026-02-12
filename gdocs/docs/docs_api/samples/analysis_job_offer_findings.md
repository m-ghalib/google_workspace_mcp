# Feature Analysis: Job Offer Findings

## Summary
- Document size: 157,806 bytes (~154KB)
- Total structural elements: 67 across 2 tabs (56 in "Readout" tab, 11 in "Appendix" tab)
- Key finding: This document showcases rich inline content (6 embedded images across tabs) and demonstrates the multi-tab structure with named tabs, providing a solid example of how tabbed documents organize content. While person and date elements are also in the baseline, this doc shows them in a business analytics context.

## Element Inventory
| Element Type | Count | Notable Details |
|---|---|---|
| paragraph | 64 | Mix of TITLE, HEADING_2, and NORMAL_TEXT styles |
| sectionBreak | 2 | One per tab |
| table | 1 | 2×2 table with centered alignment and fixed column widths |
| person | 1+ | Inline person mentions with email and display name |
| dateElement | 2+ | Smart date objects with timestamp and formatted display text |
| inlineObjectElement | 6 | 4 images in tab 1, 2 images in tab 2 (appendix) |

## New/Unique Features (not in existing sample)

### More Extensive Inline Objects (Images)
This document contains 6 embedded images across two tabs (4 in main tab, 2 in appendix), compared to just 1 in the baseline. Images are stored in `inlineObjects` dictionary at the tab level, not the document root level.

**Image structure example:**
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
            "magnitude": 184,
            "unit": "PT"
          },
          "width": {
            "magnitude": 468,
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

> Note: `inlineObjects` are stored at `tabs[n].documentTab.inlineObjects`, NOT at the document root level. Empty `rgbColor: {}` in border color means transparent/not rendered (see `propertyState: "NOT_RENDERED"`).

### Named Tabs Structure
Document has two explicitly named tabs: "Readout" (main content) and "Appendix" (supplementary data).

```json
{
  "tabs": [
    {
      "tabProperties": {
        "tabId": "t.zhnysc1ong96",
        "title": "Readout",
        "index": 0
      }
    },
    {
      "tabProperties": {
        "tabId": "t.oy9qgwojx2u",
        "title": "Appendix",
        "index": 1
      }
    }
  ]
}
```

### Person Element (Inline Mentions)
The document includes person mentions that render as chips with name and email.

```json
{
  "startIndex": 35,
  "endIndex": 36,
  "person": {
    "personId": "kix.w3y151lkmuc",
    "textStyle": {},
    "personProperties": {
      "name": "Trisha Schutter",
      "email": "patricia.schutter@xometry.com"
    }
  }
}
```

> Person elements occupy a single character position (note startIndex: 35, endIndex: 36) but render as interactive chips.

### Date Element (Smart Dates)
Smart date objects with timestamps and locale-aware formatting.

```json
{
  "startIndex": 864,
  "endIndex": 865,
  "dateElement": {
    "dateId": "kix.ufzz5692u4o",
    "textStyle": {},
    "dateElementProperties": {
      "timestamp": "2025-12-12T12:00:00Z",
      "locale": "en",
      "dateFormat": "DATE_FORMAT_MONTH_DAY_YEAR_ABBREVIATED",
      "timeFormat": "TIME_FORMAT_DISABLED",
      "displayText": "Dec 12, 2025"
    }
  }
}
```

> Date elements store both raw timestamp and formatted display text. Like person elements, they occupy a single character position. The `displayText` is what renders to users.

### Paragraph Spacing Properties
Explicit spacing before/after paragraphs using `spaceAbove` and `spaceBelow`.

```json
{
  "paragraphStyle": {
    "namedStyleType": "NORMAL_TEXT",
    "direction": "LEFT_TO_RIGHT",
    "spaceAbove": {
      "magnitude": 12,
      "unit": "PT"
    },
    "spaceBelow": {
      "magnitude": 12,
      "unit": "PT"
    }
  }
}
```

### Paragraph Indentation
First-line and start indentation for visual hierarchy.

```json
{
  "paragraphStyle": {
    "namedStyleType": "NORMAL_TEXT",
    "direction": "LEFT_TO_RIGHT",
    "indentFirstLine": {
      "magnitude": 144,
      "unit": "PT"
    },
    "indentStart": {
      "magnitude": 144,
      "unit": "PT"
    }
  }
}
```

## Style Diversity

### Text Styles Present
- **Bold**: Used for emphasis and labels (e.g., "Image 1:", "cautiously")
- **Italic**: Used extensively for image captions and emphasis
- **Bold + Italic**: Combined for caption labels
- **Underline**: Used for hyperlinks
- **Foreground colors**: Multiple RGB color specifications for text
- **Background colors**: Both white (#FFFFFF) and yellow highlight (#FFF2CC) backgrounds
- **Font sizes**: 11.5pt, 13pt
- **Link styling**: Blue underlined text with URL

### Paragraph Styles
- **Named styles**: TITLE, HEADING_2, NORMAL_TEXT
- **Alignment**: START (left), CENTER
- **Spacing**: 12pt above/below for body paragraphs
- **Indentation**: 144pt indents for nested content

### Table Features
- Fixed-width columns (266.25pt and 201.75pt)
- Cell padding: 5pt on all sides
- Row minimum height constraints
- Center-aligned text in all cells
- Content alignment set to TOP
- Empty `backgroundColor: {}` means transparent (inherits from parent)

## Interesting Snippets

### 1. Person Element in Context
```json
{
  "startIndex": 18,
  "endIndex": 37,
  "paragraph": {
    "elements": [
      {
        "startIndex": 18,
        "endIndex": 35,
        "textRun": {
          "content": "Product Analyst: ",
          "textStyle": {}
        }
      },
      {
        "startIndex": 35,
        "endIndex": 36,
        "person": {
          "personId": "kix.w3y151lkmuc",
          "textStyle": {},
          "personProperties": {
            "name": "Trisha Schutter",
            "email": "patricia.schutter@xometry.com"
          }
        }
      },
      {
        "startIndex": 36,
        "endIndex": 37,
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

### 2. Date Range with Mixed Styling
```json
{
  "startIndex": 826,
  "endIndex": 1054,
  "paragraph": {
    "elements": [
      {
        "startIndex": 826,
        "endIndex": 864,
        "textRun": {
          "content": "The timeline of this analysis is from ",
          "textStyle": {}
        }
      },
      {
        "startIndex": 864,
        "endIndex": 865,
        "dateElement": {
          "dateId": "kix.ufzz5692u4o",
          "textStyle": {},
          "dateElementProperties": {
            "timestamp": "2025-12-12T12:00:00Z",
            "locale": "en",
            "dateFormat": "DATE_FORMAT_MONTH_DAY_YEAR_ABBREVIATED",
            "timeFormat": "TIME_FORMAT_DISABLED",
            "displayText": "Dec 12, 2025"
          }
        }
      },
      {
        "startIndex": 865,
        "endIndex": 868,
        "textRun": {
          "content": " - ",
          "textStyle": {}
        }
      },
      {
        "startIndex": 868,
        "endIndex": 869,
        "dateElement": {
          "dateId": "kix.ur371wwxpc3t",
          "textStyle": {},
          "dateElementProperties": {
            "timestamp": "2026-01-20T12:00:00Z",
            "locale": "en",
            "dateFormat": "DATE_FORMAT_MONTH_DAY_YEAR_ABBREVIATED",
            "timeFormat": "TIME_FORMAT_DISABLED",
            "displayText": "Jan 20, 2026"
          }
        }
      },
      {
        "startIndex": 869,
        "endIndex": 911,
        "textRun": {
          "content": ". The data shown below should be received ",
          "textStyle": {}
        }
      },
      {
        "startIndex": 911,
        "endIndex": 921,
        "textRun": {
          "content": "cautiously",
          "textStyle": {
            "bold": true
          }
        }
      },
      {
        "startIndex": 921,
        "endIndex": 1054,
        "textRun": {
          "content": " as the timeframe involves heavy seasonality, with strong variations in both job volume and the number of partners on the job board.\n",
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

### 3. Inline Object Element (Image Embedding)
```json
{
  "startIndex": 2151,
  "endIndex": 2153,
  "paragraph": {
    "elements": [
      {
        "startIndex": 2151,
        "endIndex": 2152,
        "inlineObjectElement": {
          "inlineObjectId": "kix.lm9v2t8cj1u4",
          "textStyle": {
            "foregroundColor": {
              "color": {
                "rgbColor": {
                  "red": 0.11372549,
                  "green": 0.10980392,
                  "blue": 0.11372549
                }
              }
            },
            "fontSize": {
              "magnitude": 11.5,
              "unit": "PT"
            }
          }
        }
      },
      {
        "startIndex": 2152,
        "endIndex": 2153,
        "textRun": {
          "content": "\n",
          "textStyle": {
            "foregroundColor": {
              "color": {
                "rgbColor": {
                  "red": 0.11372549,
                  "green": 0.10980392,
                  "blue": 0.11372549
                }
              }
            },
            "fontSize": {
              "magnitude": 11.5,
              "unit": "PT"
            }
          }
        }
      }
    ],
    "paragraphStyle": {
      "namedStyleType": "NORMAL_TEXT",
      "direction": "LEFT_TO_RIGHT",
      "indentFirstLine": {
        "magnitude": 144,
        "unit": "PT"
      },
      "indentStart": {
        "magnitude": 144,
        "unit": "PT"
      }
    }
  }
}
```

### 4. Background Color (Yellow Highlight)
```json
{
  "startIndex": 737,
  "endIndex": 738,
  "textRun": {
    "content": "\n",
    "textStyle": {
      "backgroundColor": {
        "color": {
          "rgbColor": {
            "red": 1,
            "green": 0.9490196,
            "blue": 0.8
          }
        }
      }
    }
  }
}
```

### 5. Bold + Italic Caption Label
```json
{
  "startIndex": 2079,
  "endIndex": 2151,
  "paragraph": {
    "elements": [
      {
        "startIndex": 2079,
        "endIndex": 2087,
        "textRun": {
          "content": "Image 1:",
          "textStyle": {
            "bold": true,
            "italic": true
          }
        }
      },
      {
        "startIndex": 2087,
        "endIndex": 2151,
        "textRun": {
          "content": " The number of jobs offered at the event level for all partners\n",
          "textStyle": {
            "italic": true
          }
        }
      }
    ],
    "paragraphStyle": {
      "namedStyleType": "NORMAL_TEXT",
      "direction": "LEFT_TO_RIGHT",
      "indentFirstLine": {
        "unit": "PT"
      },
      "indentStart": {
        "unit": "PT"
      }
    }
  }
}
```

### 6. Hyperlink with Standard Link Styling
```json
{
  "startIndex": 38,
  "endIndex": 55,
  "paragraph": {
    "elements": [
      {
        "startIndex": 38,
        "endIndex": 54,
        "textRun": {
          "content": "Looker Dashboard",
          "textStyle": {
            "underline": true,
            "foregroundColor": {
              "color": {
                "rgbColor": {
                  "red": 0.06666667,
                  "green": 0.33333334,
                  "blue": 0.8
                }
              }
            },
            "link": {
              "url": "https://xometry.looker.com/dashboards/5367?Outsourcing+Group+Name=&Verified+Country=&Session+Start+Date=after+2025%2F09%2F07&Is+JCP+Certified%3F+%28Yes+%2F+No%29=&Is+AS9100+Certified%3F+%28Yes+%2F+No%29=&Accepted+Partner+Company+Name=&Is+CMMC+Level+2+Self+Certified+%28Yes+%2F+No%29=&Is+CMMC+Level+1+Certified+%28Yes+%2F+No%29="
            }
          }
        }
      },
      {
        "startIndex": 54,
        "endIndex": 55,
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

### 7. Table with Fixed Column Widths and Cell Styling
```json
{
  "startIndex": 3558,
  "endIndex": 3655,
  "table": {
    "rows": 2,
    "columns": 2,
    "tableRows": [
      {
        "startIndex": 3559,
        "endIndex": 3611,
        "tableCells": [
          {
            "startIndex": 3560,
            "endIndex": 3600,
            "content": [
              {
                "startIndex": 3561,
                "endIndex": 3599,
                "paragraph": {
                  "elements": [
                    {
                      "startIndex": 3561,
                      "endIndex": 3599,
                      "textRun": {
                        "content": "Number of Unique Partner-Offers shown\n",
                        "textStyle": {
                          "foregroundColor": {
                            "color": {
                              "rgbColor": {
                                "red": 0.11372549,
                                "green": 0.10980392,
                                "blue": 0.11372549
                              }
                            }
                          },
                          "fontSize": {
                            "magnitude": 11.5,
                            "unit": "PT"
                          }
                        }
                      }
                    }
                  ],
                  "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "alignment": "CENTER",
                    "direction": "LEFT_TO_RIGHT"
                  }
                }
              }
            ],
            "tableCellStyle": {
              "rowSpan": 1,
              "columnSpan": 1,
              "backgroundColor": {},
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
        ],
        "tableRowStyle": {
          "minRowHeight": {
            "magnitude": 22.60638427734375,
            "unit": "PT"
          }
        }
      }
    ],
    "tableStyle": {
      "tableColumnProperties": [
        {
          "widthType": "FIXED_WIDTH",
          "width": {
            "magnitude": 266.25,
            "unit": "PT"
          }
        },
        {
          "widthType": "FIXED_WIDTH",
          "width": {
            "magnitude": 201.75,
            "unit": "PT"
          }
        }
      ]
    }
  }
}
```

### 8. Center-Aligned Paragraph with Image
```json
{
  "startIndex": 2440,
  "endIndex": 2442,
  "paragraph": {
    "elements": [
      {
        "startIndex": 2440,
        "endIndex": 2441,
        "inlineObjectElement": {
          "inlineObjectId": "kix.gahyxfornoyn",
          "textStyle": {
            "foregroundColor": {
              "color": {
                "rgbColor": {
                  "red": 0.11372549,
                  "green": 0.10980392,
                  "blue": 0.11372549
                }
              }
            },
            "fontSize": {
              "magnitude": 11.5,
              "unit": "PT"
            }
          }
        }
      },
      {
        "startIndex": 2441,
        "endIndex": 2442,
        "textRun": {
          "content": "\n",
          "textStyle": {
            "foregroundColor": {
              "color": {
                "rgbColor": {
                  "red": 0.11372549,
                  "green": 0.10980392,
                  "blue": 0.11372549
                }
              }
            },
            "fontSize": {
              "magnitude": 11.5,
              "unit": "PT"
            }
          }
        }
      }
    ],
    "paragraphStyle": {
      "namedStyleType": "NORMAL_TEXT",
      "alignment": "CENTER",
      "direction": "LEFT_TO_RIGHT",
      "indentFirstLine": {
        "unit": "PT"
      },
      "indentStart": {
        "unit": "PT"
      }
    }
  }
}
```

> Note the sparse field representation: `indentFirstLine: { "unit": "PT" }` without a `magnitude` key means zero indent, not "inherit from style".

## Comparison to Baseline

**What's similar:**
- Both have person elements and date elements
- Both use tables with center alignment
- Both have hyperlinks with standard blue underline styling
- Both use HEADING_2 and NORMAL_TEXT styles
- Both have 2 tabs

**What's different/more diverse:**
- **More inline objects**: 6 images vs 1 in baseline
- **Richer text styling**: Background colors (both white and yellow highlight), more color variations
- **Different heading hierarchy**: Uses only HEADING_2 (focused doc), whereas baseline uses HEADING_1, HEADING_2, HEADING_3, and HEADING_5
- **More alignment variation**: Uses both START and CENTER alignment for paragraphs
- **Paragraph spacing**: Explicit spaceAbove/spaceBelow values
- **Indentation**: Heavy use of 144pt indents for visual nesting
- **Table simplicity**: Simpler 2×2 table vs baseline's more complex table with merged cells
- **Named tabs**: "Readout" and "Appendix" provide clear organizational structure

## Key Takeaways

1. **Multi-tab documents** use tab-level `inlineObjects` dictionaries, not root-level
2. **Sparse field representation** means `{}` or `{ "unit": "PT" }` without magnitude equals zero/transparent, not inherited
3. **Smart elements** (person, dateElement) occupy single character positions but render as interactive chips
4. **Image positioning** is controlled via paragraph alignment and indentation rather than floating positioning
5. **Color specification** uses floating-point RGB values (0.0-1.0 range), not 0-255 integers
6. **Table column widths** can be fixed with explicit PT values via `tableColumnProperties`
7. **Caption patterns** commonly use bold+italic for labels, italic for descriptions
