from browser import document, html, window

import editormodel, editormatrices, linearalgebra, editorhistory

import re

model = editormodel.model

PARSER_DEBUG = False

def log(msg):
  if not PARSER_DEBUG:
    return
  print(msg)

def onExpressionModelUpdate():
  expression = model["expression"]
  intermediateEquations = []
  recursiveParser(expression, False, intermediateEquations, "ANSA")
  print(intermediateEquations)

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
  editorhistory.addHistoryItem(element.value)
  #element.value = ""
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
  "exponent" : "([A-Z]+)\^([-+]?\d*\.?\d+|\d+)",
  "multiply_matrix": "([A-Z]+\*[A-Z]+)",
  "multiply_scalar_matrix": "([-+]?\d*\.?\d+|\d+)\*([A-Z]+)",
  "multiply_matrix_scalar": "([A-Z]+)\*([-+]?\d*\.?\d+|\d+)",
  "hadamard_product": "([A-Z]+)[☉]([A-Z]+)",
  "cross_product": "([A-Z]+)[x]([A-Z]+)",
  "dot_product": "([A-Z]+)[·]([A-Z]+)",
  "add_subtract_matrix": "([A-Z]+)[-+]([A-Z]+)",
  "function_expression": "([a-z]+)\(([A-Z]+)\)",
  "parentheses_expression": "\(([A-Za-z-+*☉·^]+)\)"
}

# Note that the order of operations for this parser is as follows:
"""
1. Exponentiation
2. Matrix-matrix multiplication
3. Scalar-matrix multiplication
4. Hadamard product
5. Cross product
6. Dot product
7. Addition/subtraction
8. Functions
"""

def recursiveParser(expression, freeFlight, intermediateExpressions, nextAnsVariable):
  """
  Takes a complex expression, identifies sub-expression and passes them to the basic parser.
  Sub-expressions are then replaced with variables and this repeats until there is only one expression left.
  Args:
    expression (str): The user's math expression
    freeFlight (bool): True if there are no problems with the expression. False is otherwise.
    intermediateExpressions (list): List that records every expression and sub-expression
    nextAnsVariable (str): The name of a variable used to calculate intermediate steps
  Returns:
    result (bool): True if expression is valid. False if otherwise
  """
  log("recursive parser")
  log(expression)
  log(nextAnsVariable)
  intermediateExpressions.append(expression)
  result = parser(expression, freeFlight)
  if result:
    log("basic parser is happy, done")
    return result
  # priorities
  # regex for VARA^number - can be handled by basic parser
  # regex for VARA*VARB and then other multiplications we support - can be handled by basic parser
  # regex for ([any character except '(' and at least one non alpha character]+)
  #   the above regex captures sub-expression within a proper set of parentheses. It can be recursively handled by recursiveParser
  # regex for [beginning of expression or non alpha character]([alpha characters])
  #   the above regex captures a set of parentheses that wraps up a variable name, not prefixing a single operator such as TRACE RREF etc.
  #   it's intended to simply remove that unecessary set of parentheses - see Example 5. above
  
  log("search regex exponent")
  r = re.search(recursive_regex["exponent"], expression)
  if r and r.group(1) and r.group(2):
    log("regex exponent")
    log(r.group(0))
    log(r.group(1))
    subExpression = f"{nextAnsVariable}={r.group(0)}"
    result = parser(subExpression, freeFlight)
    if not result:
      return False
    intermediateExpressions.append(subExpression)
    newExpression = expression[:r.span(0)[0]] + nextAnsVariable + expression[r.span(0)[1]:]
    nextAnsVariable=nextAns(nextAnsVariable)
    return recursiveParser(newExpression, freeFlight, intermediateExpressions, nextAnsVariable)

  log("search regex multiply_matrix")
  r = re.search(recursive_regex["multiply_matrix"], expression)
  if r and r.group(1):
    log("regex in multiply matrices")
    log(r.group(1))
    subExpression = f"{nextAnsVariable}={r.group(1)}"
    result = parser(subExpression, freeFlight)
    if not result:
      return False
    intermediateExpressions.append(subExpression)
    newExpression = expression[:r.span(1)[0]] + nextAnsVariable + expression[r.span(1)[1]:]
    nextAnsVariable=nextAns(nextAnsVariable)
    return recursiveParser(newExpression, freeFlight, intermediateExpressions, nextAnsVariable)

  log("search regex multiply_scalar-matrix")
  r = re.search(recursive_regex["multiply_scalar_matrix"], expression)
  if r and r.group(1) and r.group(2):
    log("regex multiply scalar-matrix")
    log(r.group(0))
    log(r.group(1))
    log(r.group(2))
    subExpression = f"{nextAnsVariable}={r.group(0)}"
    result = parser(subExpression, freeFlight)
    if not result:
      return False
    intermediateExpressions.append(subExpression)
    newExpression = expression[:r.span(0)[0]]
    # this handles this case: A-2*B = A+ANSA with ANSA=-2*B.
    # otherwise we get the erroneous AANSA
    # This code is not used the the matrix_scalar because that one does not consume the operator in front of the leading term
    if len(newExpression) > 0 and (r.group(1)[0] == "+" or r.group(1)[0] == "-"):
      newExpression += "+"
    newExpression += nextAnsVariable + expression[r.span(0)[1]:]
    nextAnsVariable=nextAns(nextAnsVariable)
    return recursiveParser(newExpression, freeFlight, intermediateExpressions, nextAnsVariable)
  
  log("search regex multiply_matrix-scalar")
  r = re.search(recursive_regex["multiply_matrix_scalar"], expression)
  if r and r.group(1) and r.group(2):
    log("regex in multiply matrix-scalar")
    log(r.group(0))
    log(r.group(1))
    log(r.group(2))
    subExpression = f"{nextAnsVariable}={r.group(0)}"
    result = parser(subExpression, freeFlight)
    if not result:
      return False
    intermediateExpressions.append(subExpression)
    newExpression = expression[:r.span(0)[0]] + nextAnsVariable + expression[r.span(0)[1]:]
    nextAnsVariable=nextAns(nextAnsVariable)
    return recursiveParser(newExpression, freeFlight, intermediateExpressions, nextAnsVariable)

  log("search regex hadamard product")
  r = re.search(recursive_regex["hadamard_product"], expression)
  if r and r.group(1) and r.group(2):
    log(r.group(0))
    log(r.group(1))
    log(r.group(2))
    log("regex in matrix hadamard product")
    subExpression = f"{nextAnsVariable}={r.group(0)}"
    result = parser(subExpression, freeFlight)
    if not result:
      return False
    intermediateExpressions.append(subExpression)
    newExpression = expression[:r.span(0)[0]] + nextAnsVariable + expression[r.span(0)[1]:]
    nextAnsVariable=nextAns(nextAnsVariable)
    return recursiveParser(newExpression, freeFlight, intermediateExpressions, nextAnsVariable)

  log("search regex cross product")
  r = re.search(recursive_regex["cross_product"], expression)
  if r and r.group(1) and r.group(2):
    log(r.group(0))
    log(r.group(1))
    log(r.group(2))
    log("regex in matrix cross product")
    subExpression = f"{nextAnsVariable}={r.group(0)}"
    result = parser(subExpression, freeFlight)
    if not result:
      return False
    intermediateExpressions.append(subExpression)
    newExpression = expression[:r.span(0)[0]] + nextAnsVariable + expression[r.span(0)[1]:]
    nextAnsVariable=nextAns(nextAnsVariable)
    return recursiveParser(newExpression, freeFlight, intermediateExpressions, nextAnsVariable)

  log("search regex dot product")
  r = re.search(recursive_regex["dot_product"], expression)
  if r and r.group(1) and r.group(2):
    log(r.group(0))
    log(r.group(1))
    log(r.group(2))
    log("regex in matrix dot product")
    subExpression = f"{nextAnsVariable}={r.group(0)}"
    result = parser(subExpression, freeFlight)
    if not result:
      return False
    intermediateExpressions.append(subExpression)
    newExpression = expression[:r.span(0)[0]] + nextAnsVariable + expression[r.span(0)[1]:]
    nextAnsVariable=nextAns(nextAnsVariable)
    return recursiveParser(newExpression, freeFlight, intermediateExpressions, nextAnsVariable)

  log("search regex add/subtract")
  r = re.search(recursive_regex["add_subtract_matrix"], expression)
  if r and r.group(1) and r.group(2):
    log(r.group(0))
    log(r.group(1))
    log(r.group(2))
    log("regex in matrix addition/subtraction")
    subExpression = f"{nextAnsVariable}={r.group(0)}"
    result = parser(subExpression, freeFlight)
    if not result:
      return False
    intermediateExpressions.append(subExpression)
    newExpression = expression[:r.span(0)[0]] + nextAnsVariable + expression[r.span(0)[1]:]
    nextAnsVariable=nextAns(nextAnsVariable)
    return recursiveParser(newExpression, freeFlight, intermediateExpressions, nextAnsVariable)

  log("search regex function expressions")
  r = re.search(recursive_regex["function_expression"], expression)
  if r and r.group(1) and r.group(2):
    log(r.group(0))
    log(r.group(1))
    log(r.group(2))
    log("regex in matrix functions")
    subExpression = f"{nextAnsVariable}={r.group(0)}"
    result = parser(subExpression, freeFlight)
    if not result:
      return False
    intermediateExpressions.append(subExpression)
    newExpression = expression[:r.span(0)[0]] + nextAnsVariable + expression[r.span(0)[1]:]
    nextAnsVariable=nextAns(nextAnsVariable)
    return recursiveParser(newExpression, freeFlight, intermediateExpressions, nextAnsVariable)

  log("search regex parentheses expression")
  r = re.search(recursive_regex["parentheses_expression"], expression)
  if r and r.group(1):
    log(r.group(0))
    log(r.group(1))
    log("regex in parentheses expression")
    subExpression = f"{nextAnsVariable}={r.group(1)}"
    nextNextAns = nextAns(nextAnsVariable)
    result = recursiveParser(subExpression, freeFlight, intermediateExpressions, nextNextAns)
    if not result:
      return False
    newExpression = expression[:r.span(1)[0]-1] + nextAnsVariable + expression[r.span(1)[1]+1:]
    nextAnsVariable=nextAns(nextAnsVariable)
    return recursiveParser(newExpression, freeFlight, intermediateExpressions, nextAnsVariable)

  return False

# Example: A^2+B^2
# ANSA+B^2

def nextAns(variable):
  last = variable[len(variable)-1]
  if last == "Z":
    nextLetter = "AA"
  else:
    nextLetter = chr(ord(last)+1)
  return variable[:len(variable)-1] + nextLetter
# Basic Parser below


regular_expressions = {
  "assignment_exp": "^([A-Z]+)=(.+)",
  "implicit_exp": "(.+)",
  "dual_exp": "^([A-Z]+)([+-☉·x])([A-Z]+)$",
  "single_exp": "^([a-z]+)\(([A-Z]+)\)",
  "multiply_exp": "^([A-Z]+|[-+]?\d*\.?\d+|\d+)\*([A-Z]+|[-+]?\d*\.?\d+|\d+)$",
  "exponent_exp": "^([A-Z]+)\^([-+]?\d*\.?\d+|\d+)$"
}

# [-+]?\d*\.?\d+|\d+ is the regex for a float (like 2.5)

# if freeFlight is True, evaluate expression without modifying the model
# this is used to evaluate the expression the user is entering before they are done
# if parser returns False, the expression is invalid or incomplete.
#
# if freeFlight is False, evaluate expression and put result in the model
def parser(expression, freeFlight):
  """
  Takes an expression and identifies whether it is assigning a value to another matrix, or if it implicitly assigns value to the answer matrix
  Args:
    expression (str): The user's math expression
    freeFlight (bool): True if there are no problems with the expression. False is otherwise.
  Returns:
    (bool): True if there are no problems with the expression. False is otherwise.
  """
  log("basic parser")
  log(expression)
  try:
    expression = expression.replace(" ", "")
    r = re.search(regular_expressions["assignment_exp"], expression)
    if r and r.group(1) and r.group(2):
      log("valid assignment expression")
      parserAssignmentExpression(r.group(1), r.group(2), freeFlight)
      clearError()
      return True
    
    r = re.search(regular_expressions["implicit_exp"], expression)
    if r and r.group(1):
      log("valid implicit expression")
      parserImplicitExpression(r.group(1), freeFlight)
      clearError()
      return True  
    return False

  except Exception as err:
    log("ahh error...")
    log(str(err))
    setError(str(err))
    return False

# return True if variable can be updated / created
# return False otherwise.
# Example: always True for ANSX variables, they are needed to compute intermediate steps in complex expressions
# Example: for user variables and ANS, this is controlled by the freeFlight flag (which is True for type ahead check, and False when user presses ENTER
# and expect the user variables to be reflecting the output of their expression
def canModifyVariable(variable, freeFlight):
  if editormatrices.isHidden(variable):
    return True
  return not freeFlight

def roundMatrix(matrix_list):
  """
  This is just a function to round any float value in the matrix
  Args:
    matrix_list (2d list)
  Returns:
    rounded_list (2d list)
  """
  if not isinstance(matrix_list, list):
    raise TypeError("roundMatrix() can only accept a 2d list as an argument")

  rounded_list = []
  for sublist in matrix_list:
    rounded_sublist = []
    for element in sublist:
      rounded_sublist.append(round(element,3))
    rounded_list.append(rounded_sublist)

  return rounded_list

def parserAssignmentExpression(variable, implicitExpression, freeFlight):
  """
  Identifies what operation/function is used in the expression by using regular expressions
  A specific matrix is modified based on the result of the calculation from the user's expression
  Args:
    variable (str): Represents the id of a matrix
    implicitExpression (str): The expression containing an operation/function
    freeFlight (bool): True if there are no problems with the expression. False is otherwise.
  Returns:
    None
  """
  r = re.search("^([A-Z]+)$", implicitExpression)
  if r and r.group(1):
    result = list(model["matrices"][implicitExpression]["matrix"])
    result = roundMatrix(result)
    if canModifyVariable(variable, freeFlight): 
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
    result = roundMatrix(result)
    if canModifyVariable(variable, freeFlight):
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
    result = roundMatrix(result)
    if canModifyVariable(variable, freeFlight): 
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
    result = roundMatrix(result)
    if canModifyVariable(variable, freeFlight): 
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
    result = roundMatrix(result)
    if canModifyVariable(variable, freeFlight):
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
  """
  Identifies what operation/function is used in the expression by using regular expressions
  The answer matrix is modified based on the result of the calculation from the user's expression
  Args:
    implicitExpression (str): The expression containing an operation/function
    freeFlight (bool): True if there are no problems with the expression. False is otherwise.
  Returns:
    None
  """
  r = re.search("^([A-Z]+)$", implicitExpression)
  if r and r.group(1):
    result = list(model["matrices"][implicitExpression]["matrix"])
    result = roundMatrix(result)
    modelMatrixResult = model["matrices"]["ANS"]
    if canModifyVariable("ANS", freeFlight):
      modelMatrixResult["matrix"] = result
      modelMatrixResult["rows"] = len(result)
      modelMatrixResult["cols"] = len(result[0])
    return

  r = re.search(regular_expressions["single_exp"], implicitExpression)
  if r and r.group(1) and r.group(2):
    result = parserSingleExpression(r.group(1), r.group(2))
    result = roundMatrix(result)
    modelMatrixResult = model["matrices"]["ANS"]
    if canModifyVariable("ANS", freeFlight):
      modelMatrixResult["matrix"] = result
      modelMatrixResult["rows"] = len(result)
      modelMatrixResult["cols"] = len(result[0])
    return
  
  r = re.search(regular_expressions["exponent_exp"], implicitExpression)
  if r and r.group(1) and r.group(2):
    result = parserExponentExpression(r.group(1), r.group(2))
    result = roundMatrix(result)
    modelMatrixResult = model["matrices"]["ANS"]
    if canModifyVariable("ANS", freeFlight): 
      modelMatrixResult["matrix"] = result
      modelMatrixResult["rows"] = len(result)
      modelMatrixResult["cols"] = len(result[0])
    return

  r = re.search(regular_expressions["multiply_exp"], implicitExpression)
  if r and r.group(1) and r.group(2):
    result = parserMultiplyExpression(r.group(1), r.group(2))
    result = roundMatrix(result)
    modelMatrixResult = model["matrices"]["ANS"]
    if canModifyVariable("ANS", freeFlight):
      modelMatrixResult["matrix"] = result
      modelMatrixResult["rows"] = len(result)
      modelMatrixResult["cols"] = len(result[0])
    return

  r = re.search(regular_expressions["dual_exp"], implicitExpression)
  if r and r.group(1) and r.group(2) and r.group(3):
    result = parserDualExpression(r.group(1), r.group(2), r.group(3))
    result = roundMatrix(result)
    modelMatrixResult = model["matrices"]["ANS"]
    if canModifyVariable("ANS", freeFlight):
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
    log(leftMatrix)
    log(rightMatrix)
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
  log(result)
  return result.give_2d_list()