from browser import document, html, window

import editormodel, editorexpression

model = editormodel.model

def commandAction(event):
  element = event.target
  if "laData" not in element.attrs:
    print("wrong element to hook commandAction")
    print(element)
    return
  editorexpression.enterCommand(element.attrs["laData"])
  return

def initCommands(parentNode):
  commandsTable = html.TABLE(id="targetbubble1")
  row = html.TR()
  for cmd in model["commands"]:
    td = html.TD(id="operation"+str(model["commands"].index(cmd)))
    td.classList.add("command")
    td.classList.add(cmd["operation_type"])
    td <= cmd["command"]
    td.title = cmd["tooltip"]
    td.attrs["laData"] = cmd["expression"]
    td.bind("click", commandAction)
    row <= td
  commandsTable <= row
  parentNode <= commandsTable