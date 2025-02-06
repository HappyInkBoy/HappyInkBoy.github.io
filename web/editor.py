from browser import document, html, window

import editormodel, editorcommands, editormatrices, editorexpression, equationsolver

window.model = editormodel.model

editor = html.TABLE()
editor <= html.TR(html.TD(html.DIV(id="commands")))
editor <= html.TR(html.TD(html.DIV(id="matrices")))
editor <= html.TR(html.TD(html.DIV(id="expression")))
editor <= html.TR(html.TD(html.DIV(id="error")))
editor <= html.TR(html.TD(html.DIV(id="history")))
document <= editor

document["commands"] <= "Commands"
document["matrices"] <= "Matrices"
document["expression"] <= "Expression"
document["history"] <= "History"

editorcommands.initCommands(document["commands"])
editormatrices.initMatrices(document["matrices"])
editorexpression.initExpression(document["expression"])

#equationsolver.parseEquation("2x+1y+3z=2")
#equationsolver.convertToMatrix(["1x-2z=0", "5x+2y-1z=0", "-1x+4y+2z=5", "2x-3y+4z=-10"])
result_list = equationsolver.convertToMatrix(["1x-2z=0", "5x+2y-1z=0", "-1x+4y+2z=5"])
equationsolver.solution(result_list[0],result_list[1])
result_list = equationsolver.convertToMatrix(["1x-2z=0", "5x+2y-1z=0", "2x-4z=5"])
equationsolver.solution(result_list[0],result_list[1])