from browser import document, html, window

import editormodel, editormatrices, linearalgebra

model = editormodel.model

def onExpressionModelUpdate():
  expression = model["expression"]
  if expression == "A=B+C":
    B = model["matrices"]["B"]
    C = model["matrices"]["C"]

    A = model["matrices"]["A"]
    A["rows"] = B["rows"]
    A["cols"] = B["cols"]
    A["matrix"] = [[0 for row in range(A["rows"])] for col in range(A["cols"])]
    for row in range(A["rows"]):
      for col in range(A["cols"]):
        A["matrix"][row][col] = B["matrix"][row][col] + C["matrix"][row][col]
  if expression == "A=RREF(B)":
    B = model["matrices"]["B"]["matrix"]
    M1 = linearalgebra.Matrix.from_2d_list(B)
    temp_matrix = linearalgebra.Op.reducedRowEchelonForm(M1)
    model["matrices"]["A"]["matrix"] = temp_matrix.give_2d_list()

  editormatrices.onMatrixModelUpdate("A")

def isValidExpression(expression):
  return expression == "A=B+C" or expression == "A=RREF(B)"

def expressionInputAction(event):
  element = event.target
  if event.type == "keyup" and event.key != "Enter":
     element.class_name = "valid" if isValidExpression(element.value) else "invalid"
     return
  model["expression"] = element.value
  element.value = ""
  onExpressionModelUpdate()

def enterCommand(commandName):
  input = document["expression-input"]
  input.value += commandName

def initExpression(parentNode):
  input = html.INPUT(id="expression-input")
  parentNode <= input
  input.bind("keyup", expressionInputAction)