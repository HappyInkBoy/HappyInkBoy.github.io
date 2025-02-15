from browser import document, html, window

import editormodel, editorcommands, editormatrices, editorexpression, equationsolver

window.model = editormodel.model

editor = html.TABLE()
editor.class_name = "outer editor"
editor <= html.TR(html.TD(html.DIV(id="commands")))
editor <= html.TR(html.TD(html.DIV(id="matrices")))
editor <= html.TR(html.TD(html.DIV(id="expression")))
editor <= html.TR(html.TD(html.DIV(id="error")))
editor <= html.TR(html.TD(html.DIV(id="history")))
document <= editor

solver = html.TABLE()
solver.class_name = "outer solver"
solver <= html.TR(html.TD(html.DIV(id="equation_solver")))
document <= solver

document["commands"] <= "Commands"
document["matrices"] <= "Matrices"
document["expression"] <= "Expression: "
document["history"] <= "History"
document["equation_solver"] <= "Equation Solver"

editorcommands.initCommands(document["commands"])
editormatrices.initMatrices(document["matrices"])
editorexpression.initExpression(document["expression"])
equationsolver.initEquations(document["equation_solver"])

#print(equationsolver.parseEquation("x+y-z=2"))
#equationsolver.convertToMatrix(["1x-2z=0", "5x+2y-1z=0", "-1x+4y+2z=5", "2x-3y+4z=-10"])
result_list = equationsolver.convertToMatrix(["x - y + z = 0", "5x+2y-z=0", "-x+4y+2z=5"])