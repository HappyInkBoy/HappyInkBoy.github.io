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
  colE = html.TD()
  row <= colA
  row <= colB
  row <= colC
  row <= colD
  row <= colE
  matricesTable <= row
  parentNode <= matricesTable
  initMatrix(colA, "A")
  initMatrix(colB, "B")
  initMatrix(colC, "C")
  initMatrix(colD, "D")
  initMatrix(colE, "ANS")

def addMatrix(parentNode, variable):
  if variable in model["matrices"]:
    print("error - adding matrix "+variable+" which already exists")
    return
  model["matrices"][variable] = { "name" : variable, "rows" : 3, "cols" : 3, "matrix" : [[0,0,0],[0,0,0],[0,0,0]] }
  matricesTable = html.TABLE()
  row = html.TR()
  col = html.TD()
  row <= col
  matricesTable <= row
  parentNode <= matricesTable
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
  if event.type == "keyup" and event.key != "Enter":
     return
  element = event.target # the input field
  # Blur callback is processed asynchronously so that the click
  # callback hits the target element the user intended to
  # Use case: edit a cell, then click on its right neighbour
  # first cell's blur callback is fired first. Then click callback
  # for its right neighbour is triggered as user intended
  timer.set_timeout(matrixEditInputCloseDelayedUpdate, 200, element)

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

def matrixEditAction(event):
  element = event.target
  
  if "laData" not in element.attrs:
     print("wrong element to hook matrixEditAction")
     print(element)
     return
  laData = eval(element.attrs["laData"])
  name = laData["name"]
  row = laData["row"]
  col = laData["col"]
  element.clear()
  input = html.INPUT()
  input.class_name = "matrix"
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
              colNode = html.TD()
              colNode.attrs["laData"] = {
                  "name" : name,
                  "row" : rowIndex,
                  "col" : colIndex
              }
              colNode.bind("click", matrixEditAction)
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