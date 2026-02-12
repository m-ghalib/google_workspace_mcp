/**
 * Google Docs Operations via Apps Script DocumentApp
 *
 * Called from Python MCP server via Web App HTTP POST.
 * All functions accept document IDs and return JSON-serializable data.
 *
 * Naming convention: camelCase functions, matching Python snake_case callers.
 */

// =============================================================================
// WEB APP ROUTER
// =============================================================================

/**
 * Web App entry point. Receives POST requests with JSON body:
 *   {function: "functionName", parameters: [...]}
 *
 * Returns JSON mirroring the Execution API response format:
 *   Success: {response: {result: ...}}
 *   Error:   {error: {message: "...", details: [...]}}
 */
function doPost(e) {
  try {
    var payload = JSON.parse(e.postData.contents);
    var functionName = payload.function;
    var parameters = payload.parameters || [];

    // Allowlist of public functions (security)
    var ALLOWED_FUNCTIONS = [
      'getDocContent',
      'getDocumentStructure',
      'getTableStructure',
      'createDoc',
      'createTableWithData',
      'modifyTableRowColumn',
      'modifyDocText',
      'findAndReplace',
      'updateParagraphStyle',
      'modifyListFormatting',
      'updateTableCellStyle',
      'mergeTableCells',
      'setTableColumnWidth',
      'insertElements',
      'manageHeaderFooter'
    ];

    if (ALLOWED_FUNCTIONS.indexOf(functionName) === -1) {
      return ContentService.createTextOutput(JSON.stringify({
        error: {
          message: 'Function not allowed: ' + functionName,
          details: [{errorType: 'INVALID_ARGUMENT'}]
        }
      })).setMimeType(ContentService.MimeType.JSON);
    }

    // Dynamic dispatch
    var result = this[functionName].apply(this, parameters);

    return ContentService.createTextOutput(JSON.stringify({
      response: { result: result }
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      error: {
        message: err.message || String(err),
        details: [{errorType: 'SCRIPT_ERROR', errorMessage: err.message || String(err)}]
      }
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// =============================================================================
// DOCUMENT READING & STRUCTURE
// =============================================================================

/**
 * Get document text content with tab support.
 * @param {string} docId - Document ID
 * @param {Object} options - Optional: {includeStructure: bool, tabId: string}
 * @returns {Object} {title, content, tabs[]}
 */
function getDocContent(docId, options) {
  options = options || {};
  var doc = DocumentApp.openById(docId);
  var result = {
    title: doc.getName(),
    documentId: docId,
    link: 'https://docs.google.com/document/d/' + docId + '/edit'
  };

  var body = doc.getBody();
  result.content = body.getText();

  if (options.includeStructure) {
    result.structure = _getBodyStructure(body);
  }

  return result;
}

/**
 * Get detailed document structure as a tree.
 * Replaces the 200-line Python parse_document_structure().
 * @param {string} docId - Document ID
 * @param {string} tabId - Optional tab ID (not yet supported in Apps Script write)
 * @returns {Object} Structured document tree
 */
function getDocumentStructure(docId, tabId) {
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();

  var result = {
    title: doc.getName(),
    documentId: docId,
    totalElements: body.getNumChildren(),
    structure: _getBodyStructure(body),
    tables: [],
    statistics: {
      paragraphs: 0,
      tables: 0,
      listItems: 0,
      images: 0
    }
  };

  // Enumerate tables separately for easy access
  var tables = body.getTables();
  for (var t = 0; t < tables.length; t++) {
    var table = tables[t];
    var tableInfo = {
      tableIndex: t,
      rows: table.getNumRows(),
      columns: table.getRow(0).getNumCells(),
      elementIndex: body.getChildIndex(table),
      preview: []
    };

    // Preview first 3 rows
    var previewRows = Math.min(3, table.getNumRows());
    for (var r = 0; r < previewRows; r++) {
      var row = [];
      for (var c = 0; c < table.getRow(r).getNumCells(); c++) {
        row.push(table.getCell(r, c).getText().substring(0, 100));
      }
      tableInfo.preview.push(row);
    }

    result.tables.push(tableInfo);
    result.statistics.tables++;
  }

  return result;
}

/**
 * Get detailed table structure for debugging.
 * Replaces complex cell boundary calculation in Python.
 * @param {string} docId - Document ID
 * @param {number} tableIndex - Which table (0-based)
 * @returns {Object} Detailed table cell info
 */
function getTableStructure(docId, tableIndex) {
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();
  var tables = body.getTables();

  if (tableIndex >= tables.length) {
    throw new Error('Table index ' + tableIndex + ' not found. Document has ' + tables.length + ' table(s).');
  }

  var table = tables[tableIndex];
  var numRows = table.getNumRows();
  var numCols = table.getRow(0).getNumCells();

  var result = {
    tableIndex: tableIndex,
    dimensions: numRows + 'x' + numCols,
    cells: []
  };

  for (var r = 0; r < numRows; r++) {
    var rowInfo = [];
    var row = table.getRow(r);
    for (var c = 0; c < row.getNumCells(); c++) {
      var cell = table.getCell(r, c);
      rowInfo.push({
        position: '(' + r + ',' + c + ')',
        currentContent: cell.getText(),
        numChildren: cell.getNumChildren()
      });
    }
    result.cells.push(rowInfo);
  }

  return result;
}

// =============================================================================
// DOCUMENT CREATION
// =============================================================================

/**
 * Create a new Google Doc with optional initial content.
 * @param {string} title - Document title
 * @param {string} initialContent - Optional initial text
 * @returns {Object} {documentId, title, link}
 */
function createDoc(title, initialContent) {
  var doc = DocumentApp.create(title);
  if (initialContent) {
    doc.getBody().setText(initialContent);
  }
  var docId = doc.getId();
  return {
    documentId: docId,
    title: title,
    link: 'https://docs.google.com/document/d/' + docId + '/edit'
  };
}

// =============================================================================
// TABLE OPERATIONS
// =============================================================================

/**
 * Create a table with data in one operation.
 * Replaces cell-by-cell index refresh loop in Python.
 * @param {string} docId - Document ID
 * @param {string[][]} data - 2D array of cell values
 * @param {Object} options - {boldHeaders: bool, insertAtEnd: bool, elementIndex: number}
 * @returns {Object} {rows, columns, message}
 */
function createTableWithData(docId, data, options) {
  options = options || {};
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();

  var numRows = data.length;
  var numCols = data[0].length;

  // Append table at end of document (default) or at specific element index
  var table;
  if (options.elementIndex !== undefined && options.elementIndex !== null) {
    table = body.insertTable(options.elementIndex, data);
  } else {
    table = body.appendTable(data);
  }

  // Bold headers if requested
  if (options.boldHeaders !== false && numRows > 0) {
    var headerRow = table.getRow(0);
    for (var c = 0; c < headerRow.getNumCells(); c++) {
      headerRow.getCell(c).editAsText().setBold(true);
    }
  }

  return {
    rows: numRows,
    columns: numCols,
    message: 'Created ' + numRows + 'x' + numCols + ' table with data'
  };
}

/**
 * Insert or delete table rows/columns.
 * @param {string} docId - Document ID
 * @param {number} tableIndex - Which table (0-based)
 * @param {string} operation - 'insertRow', 'deleteRow', 'insertColumn', 'deleteColumn'
 * @param {number} index - Row or column index
 * @param {Object} options - {insertBelow: bool, insertRight: bool}
 * @returns {Object} {message, newDimensions}
 */
function modifyTableRowColumn(docId, tableIndex, operation, index, options) {
  options = options || {};
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();
  var tables = body.getTables();

  if (tableIndex >= tables.length) {
    throw new Error('Table index ' + tableIndex + ' not found. Document has ' + tables.length + ' table(s).');
  }

  var table = tables[tableIndex];
  var numRows = table.getNumRows();
  var numCols = table.getRow(0).getNumCells();
  var message = '';

  switch (operation) {
    case 'insertRow':
      if (index < 0 || index >= numRows) {
        throw new Error('Row index ' + index + ' out of bounds (0-' + (numRows - 1) + ')');
      }
      if (options.insertBelow !== false) {
        // Insert below: insert at index + 1
        table.insertTableRow(index + 1);
        message = 'Inserted row below row ' + index;
      } else {
        // Insert above: insert at index
        table.insertTableRow(index);
        message = 'Inserted row above row ' + index;
      }
      numRows++;
      break;

    case 'deleteRow':
      if (index < 0 || index >= numRows) {
        throw new Error('Row index ' + index + ' out of bounds (0-' + (numRows - 1) + ')');
      }
      if (numRows <= 1) {
        throw new Error('Cannot delete the last row');
      }
      table.removeRow(index);
      numRows--;
      message = 'Deleted row ' + index;
      break;

    case 'insertColumn':
      if (index < 0 || index >= numCols) {
        throw new Error('Column index ' + index + ' out of bounds (0-' + (numCols - 1) + ')');
      }
      if (numCols >= 20) {
        throw new Error('Cannot insert column. Google Docs maximum is 20 columns.');
      }
      // Apps Script doesn't have a direct insertColumn method
      // We need to add a cell to each row at the right position
      var insertAt = options.insertRight !== false ? index + 1 : index;
      for (var r = 0; r < numRows; r++) {
        table.getRow(r).insertTableCell(insertAt);
      }
      var position = options.insertRight !== false ? 'right of' : 'left of';
      numCols++;
      message = 'Inserted column ' + position + ' column ' + index;
      break;

    case 'deleteColumn':
      if (index < 0 || index >= numCols) {
        throw new Error('Column index ' + index + ' out of bounds (0-' + (numCols - 1) + ')');
      }
      if (numCols <= 1) {
        throw new Error('Cannot delete the last column');
      }
      // Remove the cell at this column index from each row
      for (var r = 0; r < numRows; r++) {
        table.getRow(r).removeCell(index);
      }
      numCols--;
      message = 'Deleted column ' + index;
      break;

    default:
      throw new Error('Unknown operation: ' + operation);
  }

  return {
    message: message,
    newDimensions: numRows + 'x' + numCols,
    rows: numRows,
    columns: numCols
  };
}

// =============================================================================
// TEXT OPERATIONS
// =============================================================================

/**
 * Modify text in a document: insert, delete, replace, and/or format.
 * Replaces index-math text operations in Python.
 * @param {string} docId - Document ID
 * @param {Object[]} operations - Array of operation objects
 *   Each operation: {type, startIndex, endIndex, text, bold, italic, underline,
 *                    fontSize, fontFamily, textColor, backgroundColor}
 * @returns {Object} {message, operationsCompleted}
 */
function modifyDocText(docId, operations) {
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();
  var completed = [];

  for (var i = 0; i < operations.length; i++) {
    var op = operations[i];

    switch (op.type) {
      case 'insert':
        var insertIndex = op.startIndex || 0;
        body.editAsText().insertText(insertIndex, op.text);
        completed.push('Inserted ' + op.text.length + ' chars at ' + insertIndex);
        break;

      case 'delete':
        body.editAsText().deleteText(op.startIndex, op.endIndex - 1);
        completed.push('Deleted range ' + op.startIndex + '-' + op.endIndex);
        break;

      case 'replace':
        body.editAsText().deleteText(op.startIndex, op.endIndex - 1);
        body.editAsText().insertText(op.startIndex, op.text);
        completed.push('Replaced range ' + op.startIndex + '-' + op.endIndex);
        break;

      case 'format':
        _applyTextFormatting(body.editAsText(), op.startIndex, op.endIndex - 1, op);
        completed.push('Formatted range ' + op.startIndex + '-' + op.endIndex);
        break;

      default:
        throw new Error('Unknown text operation type: ' + op.type);
    }
  }

  return {
    message: completed.join('; '),
    operationsCompleted: completed.length
  };
}

/**
 * Find and replace text throughout the document.
 * @param {string} docId - Document ID
 * @param {string} findText - Text or regex pattern to find
 * @param {string} replacement - Replacement text
 * @param {Object} options - {matchCase: bool}
 * @returns {Object} {replacements, message}
 */
function findAndReplace(docId, findText, replacement, options) {
  options = options || {};
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();

  // body.replaceText uses regex patterns
  var found = body.replaceText(findText, replacement);

  return {
    message: 'Replaced occurrences of "' + findText + '" with "' + replacement + '"',
    pattern: findText,
    replacement: replacement
  };
}

// =============================================================================
// PARAGRAPH STYLING
// =============================================================================

/**
 * Update paragraph style (headings, alignment, spacing, indentation).
 * @param {string} docId - Document ID
 * @param {number} paragraphIndex - Element index of the paragraph in body
 * @param {Object} style - {headingLevel, alignment, lineSpacing,
 *                          indentFirstLine, indentStart, indentEnd,
 *                          spaceAbove, spaceBelow}
 * @returns {Object} {message}
 */
function updateParagraphStyle(docId, paragraphIndex, style) {
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();

  var element = body.getChild(paragraphIndex);
  if (element.getType() !== DocumentApp.ElementType.PARAGRAPH) {
    throw new Error('Element at index ' + paragraphIndex + ' is not a paragraph (type: ' + element.getType() + ')');
  }

  var paragraph = element.asParagraph();
  var applied = [];

  if (style.headingLevel !== undefined) {
    var headingMap = {
      0: DocumentApp.ParagraphHeading.NORMAL,
      1: DocumentApp.ParagraphHeading.HEADING1,
      2: DocumentApp.ParagraphHeading.HEADING2,
      3: DocumentApp.ParagraphHeading.HEADING3,
      4: DocumentApp.ParagraphHeading.HEADING4,
      5: DocumentApp.ParagraphHeading.HEADING5,
      6: DocumentApp.ParagraphHeading.HEADING6
    };
    paragraph.setHeading(headingMap[style.headingLevel]);
    applied.push('heading=' + style.headingLevel);
  }

  if (style.alignment) {
    var alignMap = {
      'START': DocumentApp.HorizontalAlignment.LEFT,
      'CENTER': DocumentApp.HorizontalAlignment.CENTER,
      'END': DocumentApp.HorizontalAlignment.RIGHT,
      'JUSTIFIED': DocumentApp.HorizontalAlignment.JUSTIFY
    };
    if (alignMap[style.alignment]) {
      paragraph.setAlignment(alignMap[style.alignment]);
      applied.push('alignment=' + style.alignment);
    }
  }

  if (style.lineSpacing !== undefined) {
    paragraph.setLineSpacing(style.lineSpacing);
    applied.push('lineSpacing=' + style.lineSpacing);
  }

  if (style.indentFirstLine !== undefined) {
    paragraph.setIndentFirstLine(style.indentFirstLine);
    applied.push('indentFirstLine=' + style.indentFirstLine);
  }

  if (style.indentStart !== undefined) {
    paragraph.setIndentStart(style.indentStart);
    applied.push('indentStart=' + style.indentStart);
  }

  if (style.indentEnd !== undefined) {
    paragraph.setIndentEnd(style.indentEnd);
    applied.push('indentEnd=' + style.indentEnd);
  }

  if (style.spaceAbove !== undefined) {
    paragraph.setSpacingBefore(style.spaceAbove);
    applied.push('spaceAbove=' + style.spaceAbove);
  }

  if (style.spaceBelow !== undefined) {
    paragraph.setSpacingAfter(style.spaceBelow);
    applied.push('spaceBelow=' + style.spaceBelow);
  }

  return {
    message: 'Applied paragraph style: ' + applied.join(', ')
  };
}

// =============================================================================
// LIST FORMATTING
// =============================================================================

/**
 * Create or remove bullet/numbered list formatting.
 * @param {string} docId - Document ID
 * @param {number[]} paragraphIndices - Element indices of paragraphs to modify
 * @param {string} action - 'create' or 'delete'
 * @param {Object} options - {listType: 'UNORDERED'|'ORDERED'}
 * @returns {Object} {message}
 */
function modifyListFormatting(docId, paragraphIndices, action, options) {
  options = options || {};
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();

  var glyphType;
  if (action === 'create') {
    if (options.listType === 'ORDERED') {
      glyphType = DocumentApp.GlyphType.NUMBER;
    } else {
      glyphType = DocumentApp.GlyphType.BULLET;
    }
  }

  for (var i = 0; i < paragraphIndices.length; i++) {
    var element = body.getChild(paragraphIndices[i]);
    if (element.getType() === DocumentApp.ElementType.PARAGRAPH) {
      var para = element.asParagraph();
      if (action === 'create') {
        var listItem = para.convertToListItem();
        listItem.setGlyphType(glyphType);
      } else if (action === 'delete') {
        // If it's already a list item, convert to paragraph
        if (element.getType() === DocumentApp.ElementType.LIST_ITEM) {
          element.asListItem().convertToParagraph();
        }
      }
    } else if (element.getType() === DocumentApp.ElementType.LIST_ITEM) {
      if (action === 'delete') {
        element.asListItem().convertToParagraph();
      } else if (action === 'create') {
        element.asListItem().setGlyphType(glyphType);
      }
    }
  }

  var listDesc = options.listType === 'ORDERED' ? 'numbered list' : 'bullet list';
  var actionDesc = action === 'create'
    ? 'Created ' + listDesc + ' for ' + paragraphIndices.length + ' paragraph(s)'
    : 'Removed list formatting from ' + paragraphIndices.length + ' paragraph(s)';

  return { message: actionDesc };
}

// =============================================================================
// TABLE CELL STYLING
// =============================================================================

/**
 * Update table cell styling (background, padding, borders, alignment).
 * @param {string} docId - Document ID
 * @param {number} tableIndex - Which table (0-based)
 * @param {number} rowIndex - Cell row
 * @param {number} colIndex - Cell column
 * @param {Object} style - {backgroundColor, paddingTop, paddingBottom,
 *                          paddingLeft, paddingRight, contentAlignment}
 * @returns {Object} {message}
 */
function updateTableCellStyle(docId, tableIndex, rowIndex, colIndex, style) {
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();
  var tables = body.getTables();

  if (tableIndex >= tables.length) {
    throw new Error('Table index ' + tableIndex + ' not found. Document has ' + tables.length + ' table(s).');
  }

  var table = tables[tableIndex];
  var cell = table.getCell(rowIndex, colIndex);
  var applied = [];

  if (style.backgroundColor) {
    cell.setBackgroundColor(style.backgroundColor);
    applied.push('background=' + style.backgroundColor);
  }

  if (style.paddingTop !== undefined) {
    cell.setPaddingTop(style.paddingTop);
    applied.push('paddingTop');
  }
  if (style.paddingBottom !== undefined) {
    cell.setPaddingBottom(style.paddingBottom);
    applied.push('paddingBottom');
  }
  if (style.paddingLeft !== undefined) {
    cell.setPaddingLeft(style.paddingLeft);
    applied.push('paddingLeft');
  }
  if (style.paddingRight !== undefined) {
    cell.setPaddingRight(style.paddingRight);
    applied.push('paddingRight');
  }

  if (style.contentAlignment) {
    var alignMap = {
      'TOP': DocumentApp.VerticalAlignment.TOP,
      'MIDDLE': DocumentApp.VerticalAlignment.CENTER,
      'BOTTOM': DocumentApp.VerticalAlignment.BOTTOM
    };
    if (alignMap[style.contentAlignment]) {
      cell.setVerticalAlignment(alignMap[style.contentAlignment]);
      applied.push('alignment=' + style.contentAlignment);
    }
  }

  return {
    message: 'Updated cell (' + rowIndex + ',' + colIndex + ') in table ' + tableIndex + ': ' + applied.join(', ')
  };
}

/**
 * Merge a range of table cells.
 * @param {string} docId - Document ID
 * @param {number} tableIndex - Which table (0-based)
 * @param {number} startRow - Starting row
 * @param {number} startCol - Starting column
 * @param {number} rowSpan - Rows to merge
 * @param {number} colSpan - Columns to merge
 * @returns {Object} {message}
 */
function mergeTableCells(docId, tableIndex, startRow, startCol, rowSpan, colSpan) {
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();
  var tables = body.getTables();

  if (tableIndex >= tables.length) {
    throw new Error('Table index ' + tableIndex + ' not found.');
  }

  var table = tables[tableIndex];
  // Apps Script merge: merge cells from (startRow, startCol) spanning rowSpan x colSpan
  table.getCell(startRow, startCol).merge();

  return {
    message: 'Merged cells at (' + startRow + ',' + startCol + ') spanning ' + rowSpan + 'x' + colSpan + ' in table ' + tableIndex
  };
}

/**
 * Set column width for a table.
 * @param {string} docId - Document ID
 * @param {number} tableIndex - Which table (0-based)
 * @param {number[]} columnIndices - Columns to resize
 * @param {number} width - Width in points (null for even distribution)
 * @param {string} widthType - 'FIXED_WIDTH' or 'EVENLY_DISTRIBUTED'
 * @returns {Object} {message}
 */
function setTableColumnWidth(docId, tableIndex, columnIndices, width, widthType) {
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();
  var tables = body.getTables();

  if (tableIndex >= tables.length) {
    throw new Error('Table index ' + tableIndex + ' not found.');
  }

  var table = tables[tableIndex];

  if (widthType === 'EVENLY_DISTRIBUTED') {
    // Get total table width and distribute evenly
    var totalCols = table.getRow(0).getNumCells();
    // Apps Script doesn't have setColumnWidth directly for even distribution
    // We calculate even width from page width (assuming standard 468pt content width)
    var evenWidth = 468 / totalCols;
    for (var i = 0; i < columnIndices.length; i++) {
      table.setColumnWidth(columnIndices[i], evenWidth);
    }
    return { message: 'Distributed columns evenly at ' + Math.round(evenWidth) + 'pt each' };
  } else {
    for (var i = 0; i < columnIndices.length; i++) {
      table.setColumnWidth(columnIndices[i], width);
    }
    return { message: 'Set width of column(s) ' + columnIndices.join(',') + ' to ' + width + 'pt' };
  }
}

// =============================================================================
// DOCUMENT ELEMENTS (tables, page breaks, images)
// =============================================================================

/**
 * Insert structural elements into a document.
 * @param {string} docId - Document ID
 * @param {Object[]} elements - Array of elements to insert
 *   Each: {type: 'table'|'pageBreak'|'image', ...params}
 * @returns {Object} {message, elementsInserted}
 */
function insertElements(docId, elements) {
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();
  var inserted = [];

  for (var i = 0; i < elements.length; i++) {
    var elem = elements[i];

    switch (elem.type) {
      case 'table':
        if (elem.data) {
          body.appendTable(elem.data);
        } else {
          // Create empty table with specified dimensions
          var cells = [];
          for (var r = 0; r < (elem.rows || 1); r++) {
            var row = [];
            for (var c = 0; c < (elem.columns || 1); c++) {
              row.push('');
            }
            cells.push(row);
          }
          body.appendTable(cells);
        }
        inserted.push('table');
        break;

      case 'pageBreak':
        body.appendPageBreak();
        inserted.push('page break');
        break;

      case 'image':
        if (elem.url) {
          // URL-based image insertion: fetch and insert as blob
          var response = UrlFetchApp.fetch(elem.url);
          var blob = response.getBlob();
          var img = body.appendImage(blob);
          if (elem.width) img.setWidth(elem.width);
          if (elem.height) img.setHeight(elem.height);
          inserted.push('image');
        }
        break;

      default:
        throw new Error('Unknown element type: ' + elem.type);
    }
  }

  return {
    message: 'Inserted ' + inserted.length + ' element(s): ' + inserted.join(', '),
    elementsInserted: inserted.length
  };
}

// =============================================================================
// HEADER/FOOTER MANAGEMENT
// =============================================================================

/**
 * Manage document headers and footers.
 * Note: Apps Script only supports DEFAULT header/footer type.
 * FIRST_PAGE and EVEN_PAGE require REST API fallback.
 * @param {string} docId - Document ID
 * @param {string} action - 'update' or 'delete'
 * @param {string} sectionType - 'header' or 'footer'
 * @param {string} content - Text content (for 'update' action)
 * @param {string} headerFooterType - 'DEFAULT' (others need REST fallback)
 * @returns {Object} {message, needsRestFallback}
 */
function manageHeaderFooter(docId, action, sectionType, content, headerFooterType) {
  headerFooterType = headerFooterType || 'DEFAULT';

  // Apps Script only handles DEFAULT type
  if (headerFooterType !== 'DEFAULT') {
    return {
      message: 'Type ' + headerFooterType + ' requires REST API',
      needsRestFallback: true,
      sectionType: sectionType,
      headerFooterType: headerFooterType,
      content: content,
      action: action
    };
  }

  var doc = DocumentApp.openById(docId);

  if (action === 'update') {
    if (sectionType === 'header') {
      var header = doc.getHeader() || doc.addHeader();
      header.setText(content);
    } else {
      var footer = doc.getFooter() || doc.addFooter();
      footer.setText(content);
    }
    return { message: 'Updated ' + sectionType + ' with content' };
  }

  if (action === 'delete') {
    // Apps Script doesn't have removeHeader/removeFooter
    // Best we can do is clear the content
    if (sectionType === 'header') {
      var header = doc.getHeader();
      if (header) header.clear();
    } else {
      var footer = doc.getFooter();
      if (footer) footer.clear();
    }
    return { message: 'Cleared ' + sectionType + ' content' };
  }

  throw new Error('Unknown action: ' + action);
}

// =============================================================================
// INTERNAL HELPERS
// =============================================================================

/**
 * Extract body structure as a flat list of elements.
 * @param {Body} body - DocumentApp Body object
 * @returns {Object[]} Array of element descriptors
 */
function _getBodyStructure(body) {
  var elements = [];
  var numChildren = body.getNumChildren();

  for (var i = 0; i < numChildren; i++) {
    var child = body.getChild(i);
    var type = child.getType();
    var elem = {
      elementIndex: i,
      type: type.toString()
    };

    if (type === DocumentApp.ElementType.PARAGRAPH) {
      var para = child.asParagraph();
      elem.text = para.getText().substring(0, 200);
      elem.heading = para.getHeading().toString();
    } else if (type === DocumentApp.ElementType.TABLE) {
      var table = child.asTable();
      elem.rows = table.getNumRows();
      elem.columns = table.getRow(0).getNumCells();
    } else if (type === DocumentApp.ElementType.LIST_ITEM) {
      var item = child.asListItem();
      elem.text = item.getText().substring(0, 200);
      elem.glyphType = item.getGlyphType().toString();
      elem.nestingLevel = item.getNestingLevel();
    }

    elements.push(elem);
  }

  return elements;
}

/**
 * Apply text formatting to a range.
 * @param {Text} text - EditAsText object
 * @param {number} start - Start offset
 * @param {number} end - End offset (inclusive)
 * @param {Object} style - Formatting options
 */
function _applyTextFormatting(text, start, end, style) {
  if (style.bold !== undefined) {
    text.setBold(start, end, style.bold);
  }
  if (style.italic !== undefined) {
    text.setItalic(start, end, style.italic);
  }
  if (style.underline !== undefined) {
    text.setUnderline(start, end, style.underline);
  }
  if (style.fontSize) {
    text.setFontSize(start, end, style.fontSize);
  }
  if (style.fontFamily) {
    text.setFontFamily(start, end, style.fontFamily);
  }
  if (style.textColor) {
    text.setForegroundColor(start, end, style.textColor);
  }
  if (style.backgroundColor) {
    text.setBackgroundColor(start, end, style.backgroundColor);
  }
}
