from browser import document, html, window

import editormodel, editormatrices, linearalgebra

import re

model = editormodel.model

def onExpressionModelUpdate():
  expression = model["expression"]
  intermediateEquations = []
  recursiveParser(expression, False, intermediateEquations, "ANSA")

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
  intermediateEquations = []
  return recursiveParser(expression, True, intermediateEquations, "ANSA")

# Recursive Parser
# 
# Uses the Basic Parser for single and dual operators evaluation
#
# For complex expressions that the Basic Parser cannot directly handle:
# - Uses intermediate ANSA ANSB ANSC... variables to progressively calculate the expression
#   in the proper sequence wrt to parentheses and operation priority (^ over * over +-)
#
# Example 1: expression "rref(A+B+(C+D*A))"
# rref(A+B+(C+D*A))
# rref(A+B+(C+ANSA)) with ANSA=D*A expression sent to basic parser
# rref(A+B+ANSB) with ANSB=C+ANSA
# rref(ANSC+ANSB) with ANSC=A+B
# rref(ANSD) wwith ANSD=ANSC+ANSB
# and basic parser can handle this and assign to ANS
#
# Example 2: expression "A+B*D*E+F*G+I"
#
# A+B*D*E+F*G+I
# A+ANSA*E+F*G+I with ANSA=B*D expression sent to basic parser 
# A+ANSB+F*G+I with ANSB=ANSA*E
# A+ANSB+ANSC+I with ANSC=F*G
# ANSD+ANSC+I with ANSD=A+ANSB
# ANSE+I with ANSE=ANSD+ANSC
# and basic parser can handle this and assign to ANS
#
# Example 3: expression "(((VARIABLENAME)))"
# (((VARIABLENAME)))
# ((VARIABLENAME))
# (VARIABLENAME)
# VARIABLENAME
# and basic parser can handle this and assign to ANS
#
# Example 4: expression "A^2+B^3*C^4"
# A^2+B^3*C^4
# ANSA+B^3*C^4 with ANSA=A^4 expression sent to basic parser
# ANSA+ANSB*C^4 with ANSB=B^3
# ANSA+ANSB*ANSC with ANSC=C^4
# ANSA+ANSD with ANSD=ANSB*ANSC
# and basic parser can handle this and assign to ANS
#
# Example 5: expression "A*(B+C)"
# A*(B+C)
# A*(ANSA) with ANSA=B+C
# A*ANSA
# and basic parser can handle this and assign to ANS

recursive_regex = {
  "exponent" : "([A-Z]+\^[-+]?\d*\.?\d+|\d+)"
}

def recursiveParser(expression, freeFlight, parentExpressions, nextAnsVariable):
  result = parser(expression, freeFlight)
  if result:
    return result
  # priorities
  # regex for VARA^number - can be handled by basic parser
  # regex for VARA*VARB and then other multiplications we support - can be handled by basic parser
  # regex for ([any character except '(' and at least one non alpha character]+)
  #   the above regex captures sub-expression within a proper set of parentheses. It can be recursively handled by recursiveParser
  # regex for [beginning of expression or non alpha character]([alpha characters])
  #   the above regex captures a set of parentheses that wraps up a variable name, not prefixing a single operator such as TRACE RREF etc.
  #   it's intended to simply remove that unecessary set of parentheses - see Example 5. above
  r = re.search(recursive_regex["exponent"], expression)
  if r and r.group(1):
    subExpression = f"{nextAnsVariable}={r.group(1)}"
    result = parser(subExpression, freeFlight)
    if not result:
      return False
    newExpression = expression[:r.span(1)[0]] + nextAnsVariable + expression[r.span(1)[1]:]
    nextAnsVariable=nextAns(nextAnsVariable)
    parentExpressions.append(expression)
    return recursiveParser(newExpression, freeFlight, parentExpressions, nextAnsVariable)
    # todo replace group(1) into expression with nextAnsVariable
    # then call recursively ourselves with the new expression and the next nextAnsVariable
  
  return False

# Example: A^2+B^2
# ANSA+B^2

def nextAns(variable):
  last = variable[len(variable)-1]
  nextLetter = chr(ord(last)+1)
  return variable[:len(variable)-1] + nextLetter
# Basic Parser below


regular_expressions = {
  "assignment_exp": "^([A-Z]+)=(.+)",
  "implicit_exp": "(.+)",
  "dual_exp": "^([A-Z]+)([+-☉·x])([A-Z]+)$",
  "single_exp": "^([a-z]+)\(([A-Z]+)\)",
  "multiply_exp": "^([A-Z]+|[-+]?\d*\.?\d+|\d+)\*([A-Z]+|[-+]?\d*\.?\d+|\d+)",
  "exponent_exp": "^([A-Z]+)\^([-+]?\d*\.?\d+|\d+)$"
}

# [-+]?\d*\.?\d+|\d+ is the regex for a float (like 2.5)

# if freeFlight is True, evaluate expression without modifying the model
# this is used to evaluate the expression the user is entering before they are done
# if parser returns False, the expression is invalid or incomplete.
#
# if freeFlight is False, evaluate expression and put result in the model
def parser(expression, freeFlight):
  try:
    expression = expression.replace(" ", "")
    r = re.search(regular_expressions["assignment_exp"], expression)
    if r and r.group(1) and r.group(2):
      print("valid assignment expression")
      parserAssignmentExpression(r.group(1), r.group(2), freeFlight)
      clearError()
      return True
    
    r = re.search(regular_expressions["implicit_exp"], expression)
    if r and r.group(1):
      print("valid implicit expression")
      parserImplicitExpression(r.group(1), freeFlight)
      clearError()
      return True  
    return False

  except Exception as err:
    setError(str(err))
    return False

  

def parserAssignmentExpression(variable, implicitExpression, freeFlight):
  r = re.search("^([A-Z]+)$", implicitExpression)
  if r and r.group(1):
    result = model["matrices"][implicitExpression]["matrix"]
    if not freeFlight: 
      if variable in model["matrices"]:
        modelMatrixResult = model["matrices"][variable]
      else:
        modelMatrixResult = editormatrices.addMatrix(document["matrices"], variable)
      modelMatrixResult["matrix"] = result
      modelMatrixResult["rows"] = len(result)
      modelMatrixResult["cols"] = len(result[0])
    return

  r = re.search(regular_expressions["single_exp"], implicitExpression)
  if r and r.group(1) and r.group(2):
    result = parserSingleExpression(r.group(1), r.group(2))
    if not freeFlight: 
      if variable in model["matrices"]:
        modelMatrixResult = model["matrices"][variable]
      else:
        modelMatrixResult = editormatrices.addMatrix(document["matrices"], variable)
      modelMatrixResult["matrix"] = result
      modelMatrixResult["rows"] = len(result)
      modelMatrixResult["cols"] = len(result[0])
    return

  r = re.search(regular_expressions["exponent_exp"], implicitExpression)
  if r and r.group(1) and r.group(2):
    result = parserExponentExpression(r.group(1), r.group(2))
    if not freeFlight: 
      if variable in model["matrices"]:
        modelMatrixResult = model["matrices"][variable]
      else:
        modelMatrixResult = editormatrices.addMatrix(document["matrices"], variable)
      modelMatrixResult["matrix"] = result
      modelMatrixResult["rows"] = len(result)
      modelMatrixResult["cols"] = len(result[0])
    return

  r = re.search(regular_expressions["multiply_exp"], implicitExpression)
  if r and r.group(1) and r.group(2):
    result = parserMultiplyExpression(r.group(1), r.group(2))
    if not freeFlight: 
      if variable in model["matrices"]:
        modelMatrixResult = model["matrices"][variable]
      else:
        modelMatrixResult = editormatrices.addMatrix(document["matrices"], variable)
      modelMatrixResult["matrix"] = result
      modelMatrixResult["rows"] = len(result)
      modelMatrixResult["cols"] = len(result[0])
    return

  r = re.search(regular_expressions["dual_exp"], implicitExpression)
  if r and r.group(1) and r.group(2) and r.group(3):
    result = parserDualExpression(r.group(1), r.group(2), r.group(3))
    if not freeFlight:
      if variable in model["matrices"]:
        modelMatrixResult = model["matrices"][variable]
      else:
        modelMatrixResult = editormatrices.addMatrix(document["matrices"], variable)
      modelMatrixResult["matrix"] = result
      modelMatrixResult["rows"] = len(result)
      modelMatrixResult["cols"] = len(result[0])
    return

  raise Exception("Invalid Assignment Expression") 

def parserImplicitExpression(implicitExpression, freeFlight):
  r = re.search("^([A-Z]+)$", implicitExpression)
  if r and r.group(1):
    result = model["matrices"][implicitExpression]["matrix"]
    modelMatrixResult = model["matrices"]["ANS"]
    if not freeFlight:
      modelMatrixResult["matrix"] = result
      modelMatrixResult["rows"] = len(result)
      modelMatrixResult["cols"] = len(result[0])
    return

  r = re.search(regular_expressions["single_exp"], implicitExpression)
  if r and r.group(1) and r.group(2):
    result = parserSingleExpression(r.group(1), r.group(2))
    modelMatrixResult = model["matrices"]["ANS"]
    if not freeFlight:
      modelMatrixResult["matrix"] = result
      modelMatrixResult["rows"] = len(result)
      modelMatrixResult["cols"] = len(result[0])
    return
  
  r = re.search(regular_expressions["exponent_exp"], implicitExpression)
  if r and r.group(1) and r.group(2):
    result = parserExponentExpression(r.group(1), r.group(2))
    modelMatrixResult = model["matrices"]["ANS"]
    if not freeFlight: 
      modelMatrixResult["matrix"] = result
      modelMatrixResult["rows"] = len(result)
      modelMatrixResult["cols"] = len(result[0])
    return

  r = re.search(regular_expressions["multiply_exp"], implicitExpression)
  if r and r.group(1) and r.group(2):
    result = parserMultiplyExpression(r.group(1), r.group(2))
    modelMatrixResult = model["matrices"]["ANS"]
    if not freeFlight:
      modelMatrixResult["matrix"] = result
      modelMatrixResult["rows"] = len(result)
      modelMatrixResult["cols"] = len(result[0])
    return

  r = re.search(regular_expressions["dual_exp"], implicitExpression)
  if r and r.group(1) and r.group(2) and r.group(3):
    result = parserDualExpression(r.group(1), r.group(2), r.group(3))
    modelMatrixResult = model["matrices"]["ANS"]
    if not freeFlight:
      modelMatrixResult["matrix"] = result
      modelMatrixResult["rows"] = len(result)
      modelMatrixResult["cols"] = len(result[0])
    return
  raise Exception("Invalid Expression") 

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
    print(leftMatrix)
    print(rightMatrix)
    result = linearalgebra.Op.hadamardProduct(leftMatrix,rightMatrix)
  elif dualOperator == "·":
    if len(leftMatrix.vector_list) > 1 or len(rightMatrix.vector_list) > 1:
      raise Exception("Dot product can only be performed on column vectors")
    leftVector = leftMatrix.vector_list[0]
    rightVector = rightMatrix.vector_list[0]
    scalar_result = linearalgebra.Op.dotProduct(leftVector,rightVector)
    result = linearalgebra.Matrix.from_2d_list([[scalar_result]])
  elif dualOperator == "x":
    if len(leftMatrix.vector_list) > 1 or len(rightMatrix.vector_list) > 1:
      raise Exception("Cross product can only be performed on column vectors")
    leftVector = leftMatrix.vector_list[0]
    rightVector = rightMatrix.vector_list[0]
    vector_result = linearalgebra.Op.crossProduct(leftVector,rightVector)
    result = linearalgebra.Matrix([vector_result])
  else:
    raise Exception("Unsupported expression: " + leftVariable + dualOperator + rightVariable)
  return result.give_2d_list()

def parserSingleExpression(function, variable):
  variable_list = list(model["matrices"][variable]["matrix"])
  variable_matrix = linearalgebra.Matrix.from_2d_list(variable_list)
  if function == "rref":
    result = linearalgebra.Op.reducedRowEchelonForm(variable_matrix)
  elif function == "det":
    scalar_result = linearalgebra.Op.determinant(variable_matrix)
    result = linearalgebra.Matrix.from_2d_list([[scalar_result]])
  elif function == "trace":
    scalar_result = linearalgebra.Op.trace(variable_matrix)
    result = linearalgebra.Matrix.from_2d_list([[scalar_result]])
  elif function == "transpose":
    result = variable_matrix.transpose()
  else:
    raise Exception("Unsupported function "+function)
  return result.give_2d_list()

def parserMultiplyExpression(leftVariable, rightVariable):

  if any(char.isdigit() for char in leftVariable):
    leftVariable = float(leftVariable)
  if any(char.isdigit() for char in rightVariable):
    rightVariable = float(rightVariable)

  if isinstance(leftVariable,str) and isinstance(rightVariable,str):
    left_list = list(model["matrices"][leftVariable]["matrix"])
    left_matrix = linearalgebra.Matrix.from_2d_list(left_list)
    right_list = list(model["matrices"][rightVariable]["matrix"])
    right_matrix = linearalgebra.Matrix.from_2d_list(right_list)
    result = left_matrix.matrixMultiply(right_matrix)
    if isinstance(result,linearalgebra.Vector):
      result = linearalgebra.Matrix([result])
  elif (isinstance(leftVariable,int) or isinstance(leftVariable,float)) and (isinstance(rightVariable,int) or isinstance(rightVariable,float)):
    scalar_result = leftVariable * rightVariable
    result = linearalgebra.Matrix.from_2d_list([[scalar_result]])
  elif (isinstance(leftVariable,int) or isinstance(leftVariable,float)) and isinstance(rightVariable,str):
    right_list = list(model["matrices"][rightVariable]["matrix"])
    right_matrix = linearalgebra.Matrix.from_2d_list(right_list)
    result = right_matrix.scalarMultiply(leftVariable)
  elif isinstance(leftVariable,str) and (isinstance(rightVariable,int) or isinstance(rightVariable,float)):
    left_list = list(model["matrices"][leftVariable]["matrix"])
    left_matrix = linearalgebra.Matrix.from_2d_list(left_list)
    result = left_matrix.scalarMultiply(rightVariable)

  return result.give_2d_list()

def parserExponentExpression(variable, exponent_string):
  variable_list = list(model["matrices"][variable]["matrix"])
  variable_matrix = linearalgebra.Matrix.from_2d_list(variable_list)

  try:
    exponent = int(exponent_string)
  except ValueError:
    raise Exception("This calculator does not support rational exponents for matrices")

  print(type(variable_matrix), type(exponent))
  result = variable_matrix**exponent
  print(result)
  return result.give_2d_list()