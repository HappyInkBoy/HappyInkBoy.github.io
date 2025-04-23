from browser import document, html, window, timer

import editormodel

model = editormodel.model

def initMatrices(parentNode):
  matricesTable = html.TABLE()
  row = html.TR()

  colRowsCols = html.TD()
  colRowsCols.class_name = "matrix_top_cell"
  rowsColsTable = html.TABLE()
  rct1 = html.TR()
  rct1 <= html.TD("Rows:")
  rct2 = html.TR()
  rct2 <= html.TD("Cols:")
  rowsColsTable <= rct1
  rowsColsTable <= rct2
  colRowsCols <= rowsColsTable
  row <= colRowsCols 

  colA = html.TD()
  colA.class_name = "matrix_top_cell"
  colB = html.TD()
  colB.class_name = "matrix_top_cell"
  colC = html.TD()
  colC.class_name = "matrix_top_cell"
  colD = html.TD()
  colD.class_name = "matrix_top_cell"
  colANS = html.TD(id="parent_ans")
  colANS.class_name = "matrix_top_cell"
  row <= colA
  row <= colB
  row <= colC
  row <= colD
  row <= colANS
  matricesTable <= row
  parentNode <= matricesTable
  initMatrix(colA, "A")
  initMatrix(colB, "B")
  initMatrix(colC, "C")
  initMatrix(colD, "D")
  initMatrix(colANS, "ANS")

def isHidden(variableName):
  return variableName.startswith("ANS") and variableName != "ANS"

def addMatrix(parentNode, variable):
  if variable in model["matrices"]:
    print("error - adding matrix "+variable+" which already exists")
    return
  model["matrices"][variable] = { "name" : variable, "rows" : 3, "cols" : 3, "matrix" : [[0,0,0],[0,0,0],[0,0,0]] }
  row = parentNode.select_one("table tr")
  col = html.TD()
  col.class_name = "matrix_top_cell"

  beforeNode = document["parent_ans"]
  if not isHidden(variable):
    row.insertBefore(col, beforeNode)

  initMatrix(col, variable)
  return model["matrices"][variable]

def plusMinusAction(event):
  element = event.target
  laData = eval(element.attrs["laData"])
  name = laData["name"]
  matrixModel = model["matrices"][name]
  matrixModel[laData["rowsOrCols"]] += 1 if laData["operation"] == "plus" else -1
  if matrixModel[laData["rowsOrCols"]] == 0:
     matrixModel[laData["rowsOrCols"]] = 1
     return
  oldMatrix = matrixModel["matrix"]
  # The old matrix is merged into the new one
  matrixModel["matrix"] = [[0 for col in range(matrixModel["cols"])] for row in range(matrixModel["rows"])]
  for rowIndex, row in enumerate(oldMatrix):
    for colIndex, col in enumerate(row):
      value = row[colIndex]
      if rowIndex < len(matrixModel["matrix"]) and colIndex < len(matrixModel["matrix"][0]):
        matrixModel["matrix"][rowIndex][colIndex] = value
  onMatrixModelUpdate(laData["name"])

def initMatrixPlusMinus(parentNode, name, rowsOrCols):
    parentNode.classList.add("matrix_resizer_parent")
    minus = html.DIV("-")
    minus.classList.add(rowsOrCols)
    minus.classList.add("minus")
    minus.classList.add("matrix_resizer")
    plus = html.DIV("+")
    plus.classList.add(rowsOrCols)
    plus.classList.add("plus")
    plus.classList.add("matrix_resizer")
    
    minus.attrs["laData"] = {
        "name" : name,
        "rowsOrCols" : rowsOrCols,
        "operation" : "minus"
    }
    plus.attrs["laData"] = {
        "name" : name,
        "rowsOrCols" : rowsOrCols,
        "operation" : "plus"
    }
    parentNode <= minus
    parentNode <= plus
    minus.bind("click", plusMinusAction)
    plus.bind("click", plusMinusAction)

def matrixEditInputCloseAction(event):
  if event.type == "keyup" and event.key != "Enter" and event.key != "ArrowRight" and event.key != "ArrowLeft" and event.key != "ArrowDown" and event.key != "ArrowUp":
    return
  element = event.target # the input field

  # If navigation key:
  # - get the element row and col
  # - compute the desired element row and col to enter edit
  # - set id on the td elements NAME_ROW_COL when they are created
  # - fetch the desired element by id
  # - invoke matrixEditAction(event) with a fake event (target to desired element)

  if event.type == "keyup" and event.key == "ArrowDown":
    parent = element.parent
    laData = eval(parent.attrs["laData"])
    name = laData["name"]
    row = laData["row"]
    col = laData["col"]
    targetRow = row + 1
    targetCol = col
    try:
      targetElement = document[f"{name}_{targetRow}_{targetCol}"]
    except KeyError:
      return # Navigating out of bounds
    timer.set_timeout(matrixEditAction, 200, targetElement)
  if event.type == "keyup" and event.key == "ArrowUp":
    parent = element.parent
    laData = eval(parent.attrs["laData"])
    name = laData["name"]
    row = laData["row"]
    col = laData["col"]
    targetRow = row - 1
    targetCol = col
    try:
      targetElement = document[f"{name}_{targetRow}_{targetCol}"]
    except KeyError:
      return # Navigating out of bounds
    timer.set_timeout(matrixEditAction, 200, targetElement)
  if event.type == "keyup" and event.key == "ArrowLeft":
    parent = element.parent # the td column that hosts the input field during the edit operation
    element.attrs["navigationRight"] = "cleared" # user moved left inside the input field, so this resets our logic for navigating to the next cell on the right
    if element.selectionStart > 0:
      element.attrs["navigationLeft"] = "cleared"
      return
    if element.selectionStart == 0 and len(element.value) != 0 and element.attrs.get("navigationLeft") == "cleared":
      element.attrs["navigationLeft"] = "active"
      return # In this case, the user's cursor is not at the end of the number
    element.attrs["navigationLeft"] = "cleared"
    laData = eval(parent.attrs["laData"])
    name = laData["name"]
    row = laData["row"]
    col = laData["col"]
    targetRow = row
    targetCol = col - 1
    try:
      targetElement = document[f"{name}_{targetRow}_{targetCol}"]
    except KeyError:
      try:
        colsCount = model["matrices"][name]["cols"]
        targetElement = document[f"{name}_{targetRow-1}_{colsCount-1}"]
      except KeyError:
        return
    timer.set_timeout(matrixEditAction, 200, targetElement)
  
  if event.type == "keyup" and event.key == "ArrowRight":
    parent = element.parent # the td column that hosts the input field during the edit operation
    element.attrs["navigationLeft"] = "cleared" # user moved right inside the input field, so this resets our logic for navigating to the previous cell on the left
    if element.selectionStart < len(element.value):
      element.attrs["navigationRight"] = "cleared"
      return
    if element.selectionStart == len(element.value) and len(element.value) != 0 and element.attrs.get("navigationRight") == "cleared":
      element.attrs["navigationRight"] = "active"
      return # In this case, the user's cursor is not at the end of the number
    element.attrs["navigationRight"] = "cleared"
    laData = eval(parent.attrs["laData"])
    name = laData["name"]
    row = laData["row"]
    col = laData["col"]
    targetRow = row
    targetCol = col + 1
    try:
      targetElement = document[f"{name}_{targetRow}_{targetCol}"]
    except KeyError:
      try:
        targetElement = document[f"{name}_{targetRow+1}_0"]
      except KeyError:
        return
    timer.set_timeout(matrixEditAction, 200, targetElement)

  # Blur callback is processed asynchronously so that the click
  # callback hits the target element the user intended to
  # Use case: edit a cell, then click on its right neighbour
  # first cell's blur callback is fired first. Then click callback
  # for its right neighbour is triggered as user intended
  timer.set_timeout(matrixEditInputCloseDelayedUpdate, 150, element)

def matrixEditInputCloseDelayedUpdate(element):
  parent = element.parent # the td column that hosts the input field during the edit operation
  if parent is None:
    # Skip when user presses arrow keys quickly before each edit timer gets a chance to be handled
    return
  laData = eval(parent.attrs["laData"])
  name = laData["name"]
  row = laData["row"]
  col = laData["col"]
  if element.value == "":
    element.value = "0"
  try:
    model["matrices"][name]["matrix"][row][col] = float(element.value)
  except Exception:
    pass # no new value
  element.unbind("blur", matrixEditInputCloseAction)
  element.unbind("keyup", matrixEditInputCloseAction)
  parent.clear()
  parent.innerHTML = model["matrices"][name]["matrix"][row][col]

def matrixEditActionEvent(event):
  matrixEditAction(event.target)

def matrixEditAction(element):
  if "laData" not in element.attrs:
    print("wrong element to hook matrixEditAction")
    print(element)
    return
  laData = eval(element.attrs["laData"])
  name = laData["name"]
  row = laData["row"]
  col = laData["col"]
  originalValue = element.textContent
  if originalValue == "0":
    originalValue = ""
  element.clear()
  input = html.INPUT()
  input.value = originalValue
  input.class_name = "matrix"
  input.attrs["navigationLeft"] = "cleared"
  input.attrs["navigationRight"] = "active"
  element <= input
  input.focus()
  input.bind("blur", matrixEditInputCloseAction)
  input.bind("keyup", matrixEditInputCloseAction)


def onMatrixModelUpdate(name):
    if isHidden(name):
      return
    mutable = name != "ANS"
    matrixModel = model["matrices"][name]
    parentNode = document[name]
    childNodes = parentNode.child_nodes
    reuseTable = len(childNodes) == 1
    if reuseTable:
      matrixValueEditor = childNodes[0]
    else:
      matrixValueEditor = html.TABLE()
      parentNode <= matrixValueEditor
    matrix = matrixModel["matrix"]
    htmlRows = matrixValueEditor.child_nodes

    # remove excess of row nodes (e.g. occurs when matrix shrank)
    while len(htmlRows) > len(matrix):
      node = htmlRows[len(htmlRows)-1]
      matrixValueEditor.removeChild(node)
      htmlRows = matrixValueEditor.child_nodes

    for rowIndex, rowValue in enumerate(matrix):
        if len(htmlRows) > rowIndex:
          rowNode = htmlRows[rowIndex]
        else:
          rowNode = html.TR()
          matrixValueEditor <= rowNode
        htmlCols = rowNode.child_nodes

        # remove excess of col nodes (e.g. occurs when matrix shrank)
        while len(htmlCols) > len(rowValue):
          node = htmlCols[len(htmlCols)-1]
          rowNode.removeChild(node)
          htmlCols = rowNode.child_nodes

        for colIndex, colValue in enumerate(rowValue):
            if len(htmlCols) > colIndex:
              colNode = htmlCols[colIndex]
            else:
              colNode = html.TD(id=f"{name}_{rowIndex}_{colIndex}")
              colNode.attrs["laData"] = {
                  "name" : name,
                  "row" : rowIndex,
                  "col" : colIndex
              }
              if mutable:
                colNode.bind("click", matrixEditActionEvent)
              rowNode <= colNode
            colNode.innerHTML = colValue

def initMatrix(parentNode, name):
    if isHidden(name):
      return
    mutable = name != "ANS"
    matrixEditor = html.TABLE()
    matrixEditor.class_name = "matrix_collapse"

    row1 = html.TR()
    tdPlusOrMinus = html.TD(id="targetbubble2"+name)
    if mutable:
      initMatrixPlusMinus(tdPlusOrMinus, name, "rows")
    else:
      tdPlusOrMinus <= html.BR()
      tdPlusOrMinus.class_name = "answer_padding"
    row1 <= tdPlusOrMinus
    matrixEditor <= row1

    row2 = html.TR()
    tdPlusOrMinus = html.TD()
    if mutable:
      initMatrixPlusMinus(tdPlusOrMinus, name, "cols")
    else:
      tdPlusOrMinus <= html.BR()
      tdPlusOrMinus.class_name = "answer_padding"
    row2 <= tdPlusOrMinus
    matrixEditor <= row2

    row3 = html.TR()
    row3.class_name = name + "_divide"
    row3 <= html.TD(name)
    matrixEditor <= row3

    row4 = html.TR()
    row4.class_name = name + "_divide"
    m = html.TD(id=name)
    row4 <= m
    matrixEditor <= row4
    parentNode <= matrixEditor
    onMatrixModelUpdate(name)