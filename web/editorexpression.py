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

def expressionInputAction(event):
  element = event.target
  model["expression"] = element.value
  onExpressionModelUpdate();

def initExpression(parentNode):
  input = html.INPUT(id="expression-input")
  parentNode <= input
  input.bind("blur", expressionInputAction)