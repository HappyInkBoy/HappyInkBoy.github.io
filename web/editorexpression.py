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

def isValidExpression(expression):
  # Change this later
  r = re.search(regular_expressions["assignment_exp"], expression)
  if r and r.group(1) and r.group(2):
    return True
  r = re.search(regular_expressions["implicit_exp"], expression)
  if r and r.group(1):
    return True
  return True

# Parser below


regular_expressions = {
  "assignment_exp": "^([A-Z])=(.+)",
  "implicit_exp": "(.+)",
  "dual_exp": "^([A-Z])([+-☉·⨯])([A-Z])",
  "single_exp": "^([A-Z]+)\(([A-Z])\)"
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
    
    r = re.search(regular_expressions["implicit_exp"], expression)
    if r and r.group(1):
      print("valid implicit expression")
      parserImplicitExpression(r.group(1))
      clearError()
      return   

  except Exception as err:
    print("ok2")
    print(str(err))
    setError(str(err))

  

def parserAssignmentExpression(variable, implicitExpression):
  print(variable)
  print(implicitExpression)

  r = re.search(regular_expressions["single_exp"], implicitExpression)
  if r and r.group(1) and r.group(2):
    result = parserSingleExpression(r.group(1), r.group(2))
    modelMatrixResult = model["matrices"][variable]
    modelMatrixResult["matrix"] = result

  r = re.search(regular_expressions["dual_exp"], implicitExpression)
  if r and r.group(1) and r.group(2) and r.group(3):
    result = parserDualExpression(r.group(1), r.group(2), r.group(3))
    modelMatrixResult = model["matrices"][variable]
    modelMatrixResult["matrix"] = result

def parserImplicitExpression(implicitExpression):
  r = re.search(regular_expressions["single_exp"], implicitExpression)
  if r and r.group(1) and r.group(2):
    result = parserSingleExpression(r.group(1), r.group(2))
    modelMatrixResult = model["matrices"]["ANS"]
    modelMatrixResult["matrix"] = result

  r = re.search(regular_expressions["dual_exp"], implicitExpression)
  if r and r.group(1) and r.group(2) and r.group(3):
    result = parserDualExpression(r.group(1), r.group(2), r.group(3))
    modelMatrixResult = model["matrices"]["ANS"]
    modelMatrixResult["matrix"] = result

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
      raise Exception("Dot product can only be performed on column vectors")
    leftVector = leftMatrix.vector_list[0]
    rightVector = rightMatrix.vector_list[0]
    scalar_result = linearalgebra.Op.dotProduct(leftVector,rightVector)
    result = linearalgebra.Matrix.from_2d_list([[scalar_result]])
  elif dualOperator == "⨯":
    if len(leftMatrix.vector_list) > 1 or len(rightMatrix.vector_list) > 1:
      raise Exception("Cross product can only be performed on column vectors")
    leftVector = leftMatrix.vector_list[0]
    rightVector = rightMatrix.vector_list[0]
    vector_result = linearalgebra.Op.crossProduct(leftVector,rightVector)
    result = linearalgebra.Matrix([vector_result])
  return result.give_2d_list()

def parserSingleExpression(function, variable):
  variable_list = list(model["matrices"][variable]["matrix"])
  variable_matrix = linearalgebra.Matrix.from_2d_list(variable_list)
  if function == "RREF":
    result = linearalgebra.Op.reducedRowEchelonForm(variable_matrix)
  elif function == "DET":
    scalar_result = linearalgebra.Op.determinant(variable_matrix)
    result = linearalgebra.Matrix.from_2d_list([[scalar_result]])
  elif function == "TRACE":
    scalar_result = linearalgebra.Op.trace(variable_matrix)
    result = linearalgebra.Matrix.from_2d_list([[scalar_result]])
  elif function == "TRANSPOSE":
    result = variable_matrix.transpose()

  return result.give_2d_list()