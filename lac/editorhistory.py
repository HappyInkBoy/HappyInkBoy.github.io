from browser import document, html, window

import editormodel, editorexpression

model = editormodel.model

showHistory = True

def addHistoryItem(expression):
  model["history"].insert(0,expression)
  if len(model["history"]) > 5:
    del model["history"][5]
  updateHistory(document["history"])
  return

def toggleHistory(event):
  global showHistory
  showHistory = not showHistory
  updateHistory(document["history"])

def updateHistory(parentNode):
  parentNode.clear()
  historyTable = html.TABLE(id="history_table")
  rowHeader = html.TR()
  tdHeader = html.TD()
  tdHeader <= "History"
  rowHeader <= tdHeader
  historyTable <= rowHeader
  if showHistory:
    for expression in model["history"]:
      row = html.TR()
      td = html.TD()
      td.classList.add("history_item")
      td <= expression
      row <= td
      historyTable <= row
  parentNode <= historyTable
  tdHeader.bind("click", toggleHistory)