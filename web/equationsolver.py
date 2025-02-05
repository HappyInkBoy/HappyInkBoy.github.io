import linearalgebra as la
import math
import re

def convertToMatrix(equations):
  """
  Args:
    equations (list): ["x+y-2z=0", "5x+2y-z=0", "-x+4y+2z=5", "2x-3y+4z=-10"]
  Returns:
    result (list[list]):
    [
    [1,1,-2,0],
    [5,2,-1,0],
    [-1,4,2,5],
    [2,-3,4,-10]
    ]
  """
  parsedEquations = []
  allVariables = {}
  for equation in equations:
    pe = parseEquation(equation)
    parsedEquations.append(pe)
    for variable in pe.keys():
      allVariables[variable] = variable
  

  allVariablesSortedList = list(allVariables.keys())
  allVariablesSortedList.sort()
  # todo build a list of all variables and make sure each parsedEquation has them all (eventually with
  # a zero coefficient)
  for var in allVariablesSortedList:
    for pe in parsedEquations:
      if var not in pe:
        pe[var] = 0


  result = []
  for pe in parsedEquations:
    variables = list(pe.keys())
    variables.sort()
    matrix_row = []
    for var in variables:
      matrix_row.append(pe[var])
    result.append(matrix_row)

  print(result)

  return result, allVariablesSortedList

def parseEquation(equation):
  """
  Returns:
    dictionary where keys are variables and values are coefficients and a special variable for result (the value of the equation)
    Example: "x+y-2z=0" returns { x : 1, y : 1, z : -2, result : 0}
  """
  variable = None
  coefficient = 0

  matches = re.findall("([-+]?\d*\.?\d+|\d+)([a-z])", equation)
  equation_value = equation.split("=")[1]

  result = {}

  for match in matches:
    result[match[1]] = float(match[0])
  # Add validations later
  result["zz_ans"] = float(equation_value)

  return result

def solution(equation_matrix_list, variable_list):

  equation_matrix = la.Matrix.from_2d_list(equation_matrix_list)

  if len(equation_matrix.vector_list) > len(equation_matrix.vector_list[0].components)+1:
    # If there are at least 2 more columns than rows
    raise Exception("Not enough equations to find a point of intersection")
  elif len(equation_matrix.vector_list[0].components) >= len(equation_matrix.vector_list):
    # If the number of rows is greater than or equal to the number of columns
    raise Exception("Too many equations are provided")

  rref_matrix = la.Op.reducedRowEchelonForm(equation_matrix)
  # Add validations later (by that I mean that if the user either puts in too many equations or too few equations, then the solving cannot work)

  solution_dictionary = {}

  for index, row in enumerate(rref_matrix.give_2d_list()):
    solution_dictionary[variable_list[index]] = row[len(row)-1]

  print(solution_dictionary)

  pass

# [-+]?\d*\.?\d+|\d+ is the regex for a float (like 2.5)
# [-+]?\d*\.?\d+|\d+[a-z] is the regex for a float times variable (like 2.5x)

# ["x+y-2z=0", "5x+2y-z=0", "-x+4y+2z=5", "2x-3y+4z=-10"]
# Note that the regular expression/parser needs to be updated to allow variables with an implicit 1 as its coefficient