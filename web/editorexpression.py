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
  for key in model["matrices"]:
    editormatrices.onMatrixModelUpdate(key)

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

def setError(error):
  errorDiv = document['error']
  errorDiv.innerHTML = error

def clearError():
  errorDiv = document['error']
  errorDiv.innerHTML = ""

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
  try:
    expression = expression.replace(" ", "")
    r = re.search(regular_expressions["assignment_exp"], expression)
    if r and r.group(1) and r.group(2):
      print("valid assignment expression")
      parserAssignmentExpression(r.group(1), r.group(2))
      clearError()
      return
    
    r = re.search(regular_expressions["dual_exp"], expression)
    if r and r.group(1) and r.group(2) and r.group(3):
      result = parserDualExpression(r.group(1), r.group(2), r.group(3))
      modelMatrixResult = model["matrices"]["ANS"]
      modelMatrixResult["matrix"] = result
      clearError()
      return   

  except Exception as err:
    print("ok2")
    setError(str(err))

  

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
  lm = list(model["matrices"][leftVariable]["matrix"])
  leftMatrix = linearalgebra.Matrix.from_2d_list(lm)
  rm = list(model["matrices"][rightVariable]["matrix"])
  rightMatrix = linearalgebra.Matrix.from_2d_list(rm)
  if dualOperator == "+":
    result = leftMatrix + rightMatrix
  elif dualOperator == "-":
    result = leftMatrix - rightMatrix
  elif dualOperator == "☉":
    result = linearalgebra.Op.hadamardProduct(leftMatrix,rightMatrix)
  elif dualOperator == "·":
    if len(leftMatrix.vector_list) > 1 or len(rightMatrix.vector_list) > 1:
      print("ok")
      raise Exception("Dot product can only be performed on column vectors")
    leftVector = leftMatrix.vector_list[0]
    rightVector = rightMatrix.vector_list[0]
    scalar_result = linearalgebra.Op.dotProduct(leftVector,rightVector)
    result = linearalgebra.Matrix.from_2d_list([[scalar_result]])
  elif dualOperator == "⨯":
    leftVector = leftMatrix.vector_list[0]
    rightVector = rightMatrix.vector_list[0]
    vector_result = linearalgebra.Op.crossProduct(leftVector,rightVector)
    result = linearalgebra.Matrix([vector_result])

  return result.give_2d_list()