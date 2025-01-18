from browser import document, html, window

import editormodel, editormatrices, linearalgebra

import re

model = editormodel.model

def onExpressionModelUpdate():
  expression = model["expression"]
  parser(expression)

#  if expression == "A=RREF(B)":
#    B = model["matrices"]["B"]["matrix"]
#    M1 = linearalgebra.Matrix.from_2d_list(B)
#    temp_matrix = linearalgebra.Op.reducedRowEchelonForm(M1)
#    model["matrices"]["A"]["matrix"] = temp_matrix.give_2d_list()

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


# Parser below


regular_expressions = {
  "assignment_exp": "^([A-Z])=(.+)",
  "dual_exp": "^([A-Z])([+-☉·⨯])([A-Z])"
}

def parser(expression):
  expression = expression.replace(" ", "")
  r = re.search(regular_expressions["assignment_exp"], expression)
  if r and r.group(1) and r.group(2):
    parserAssignmentExpression(r.group(1), r.group(2))
  

def parserAssignmentExpression(variable, implicitExpression):
  print(variable)
  print(implicitExpression)
  # dual expression ?
  r = re.search(regular_expressions["dual_exp"], implicitExpression)
  if r and r.group(1) and r.group(2) and r.group(3):
    result = parserDualExpression(r.group(1), r.group(2), r.group(3))
    modelMatrixResult = model["matrices"][variable]
    modelMatrixResult["matrix"] = result
  # or single expression ?

def parserDualExpression(leftVariable, dualOperator, rightVariable):
  lm = model["matrices"][leftVariable]["matrix"]
  leftMatrix = linearalgebra.Matrix.from_2d_list(lm)
  rm = model["matrices"][rightVariable]["matrix"]
  rightMatrix = linearalgebra.Matrix.from_2d_list(rm)
  if dualOperator == "+":
    result = leftMatrix + rightMatrix
  elif dualOperator == "-":
    result = leftMatrix - rightMatrix

  return result.give_2d_list()