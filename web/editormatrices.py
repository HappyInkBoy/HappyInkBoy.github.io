from browser import document, html, window

import editormodel

model = editormodel.model

def initMatrices(parentNode, matricesModel):
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
  element = event.target
  laData = eval(element.parent.attrs["laData"])
  name = laData["name"]
  row = laData["row"]
  col = laData["col"]
  model["matrices"][name]["matrix"][row][col] = float(element.value)
  onMatrixModelUpdate(name)

def matrixEditAction(event):
  element = event.target
  laData = eval(element.attrs["laData"])
  name = laData["name"]
  row = laData["row"]
  col = laData["col"]
  element.clear()
  input = html.INPUT()
  input.class_name = "matrix"
  element <= input
  input.bind("blur", matrixEditInputCloseAction)


def onMatrixModelUpdate(name):
    matrixModel = model["matrices"][name]
    parentNode = document[name]
    parentNode.clear()
    matrixValueEditor = html.TABLE()
    matrix = matrixModel["matrix"]
    for rowIndex, rowValue in enumerate(matrix):
        rowNode = html.TR()
        for colIndex, colValue in enumerate(rowValue):
            colNode = html.TD(colValue)
            colNode.attrs["laData"] = {
                "name" : name,
                "row" : rowIndex,
                "col" : colIndex
            }
            colNode.bind("click", matrixEditAction)
            rowNode <= colNode
        matrixValueEditor <= rowNode
    parentNode <= matrixValueEditor  

def initMatrix(parentNode, name):
    matrixEditor = html.TABLE()
    row1 = html.TR()
    row1 <= html.TD(name)
    tdPlusOrMinus = html.TD()
    initMatrixPlusMinus(tdPlusOrMinus, name, "cols")
    row1 <= tdPlusOrMinus
    matrixEditor <= row1
    row2 = html.TR()
    tdPlusOrMinus = html.TD()
    initMatrixPlusMinus(tdPlusOrMinus, name, "rows")
    row2 <= tdPlusOrMinus
    m = html.TD(id=name)
    row2 <= m
    matrixEditor <= row2
    parentNode <= matrixEditor
    onMatrixModelUpdate(name)
   
