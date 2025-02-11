from browser import document, html, window, timer

import editormodel

model = editormodel.model

def initMatrices(parentNode):
  matricesTable = html.TABLE()
  row = html.TR()
  colA = html.TD()
  colB = html.TD()
  colC = html.TD()
  colD = html.TD()
  colANS = html.TD(id="parent_ans")
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

def addMatrix(parentNode, variable):
  if variable in model["matrices"]:
    print("error - adding matrix "+variable+" which already exists")
    return
  model["matrices"][variable] = { "name" : variable, "rows" : 3, "cols" : 3, "matrix" : [[0,0,0],[0,0,0],[0,0,0]] }
  row = parentNode.select_one("table tr")
  col = html.TD()

  beforeNode = document["parent_ans"]
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
  matrixModel["matrix"] = [[0 for col in range(matrixModel["cols"])] for row in range(matrixModel["rows"])]
  onMatrixModelUpdate(laData["name"])

def initMatrixPlusMinus(parentNode, name, rowsOrCols):
    minus = html.DIV("-")
    plus = html.DIV("+")
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
    targetElement = document[f"{name}_{targetRow}_{targetCol}"]
    timer.set_timeout(matrixEditAction, 200, targetElement)
  
  if event.type == "keyup" and event.key == "ArrowRight":
    parent = element.parent # the td column that hosts the input field during the edit operation
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
    targetElement = document[f"{name}_{targetRow}_{targetCol}"]
    timer.set_timeout(matrixEditAction, 200, targetElement)

  # Blur callback is processed asynchronously so that the click
  # callback hits the target element the user intended to
  # Use case: edit a cell, then click on its right neighbour
  # first cell's blur callback is fired first. Then click callback
  # for its right neighbour is triggered as user intended
  timer.set_timeout(matrixEditInputCloseDelayedUpdate, 150, element)

def matrixEditInputCloseDelayedUpdate(element):
  parent = element.parent # the td column that hosts the input field during the edit operation
  laData = eval(parent.attrs["laData"])
  name = laData["name"]
  row = laData["row"]
  col = laData["col"]
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
  originalValue = element.innerHTML
  if originalValue == "0":
    originalValue = ""
  element.clear()
  input = html.INPUT()
  input.value = originalValue
  input.class_name = "matrix"
  input.attrs["navigationLeft"] = "cleared"
  input.attrs["navigationRight"] = "cleared"
  element <= input
  input.focus()
  input.bind("blur", matrixEditInputCloseAction)
  input.bind("keyup", matrixEditInputCloseAction)


def onMatrixModelUpdate(name):
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
              colNode.bind("click", matrixEditActionEvent)
              rowNode <= colNode
            colNode.innerHTML = colValue

def initMatrix(parentNode, name):
    matrixEditor = html.TABLE()
    row1 = html.TR()
    row1 <= html.TD(name)
    tdPlusOrMinus = html.TD()
    initMatrixPlusMinus(tdPlusOrMinus, name, "rows")
    row1 <= tdPlusOrMinus
    matrixEditor <= row1
    row2 = html.TR()
    tdPlusOrMinus = html.TD()
    initMatrixPlusMinus(tdPlusOrMinus, name, "cols")
    row2 <= tdPlusOrMinus
    m = html.TD(id=name)
    row2 <= m
    matrixEditor <= row2
    parentNode <= matrixEditor
    onMatrixModelUpdate(name)