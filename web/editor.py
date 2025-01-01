from browser import document, html, window

import editormodel, editormatrices, editorexpression

window.model = editormodel.model

editor = html.TABLE()
editor <= html.TR(html.TD(html.DIV(id="commands")))
editor <= html.TR(html.TD(html.DIV(id="matrices")))
editor <= html.TR(html.TD(html.DIV(id="expression")))
editor <= html.TR(html.TD(html.DIV(id="history")))
document <= editor

document["commands"] <= "Commands"
document["matrices"] <= "Matrices"
document["expression"] <= "Expression"
document["history"] <= "History"

editormatrices.initMatrices(document["matrices"], editormodel.model["matrices"])
editorexpression.initExpression(document["expression"])