model = {
    "commands" : [
      { "command" : "+", "expression" : "+", "tooltip" : "Add 2 matrices. Example: A=B+C"},
      { "command" : "-", "expression" : "-",  "tooltip" : "Subtract 2 matrices. Example: A=B-C"},
      { "command" : "*", "expression" : "*",  "tooltip" : "Multiply 2 matrices. Example: A=B*C"},
      { "command" : "RREF", "expression" : "RREF()",  "tooltip" : "Reduce Row Echelon Form. Example: A=RREF(B)"}
    ],
    "matrices" : {
        "A" : { "name" : "A", "rows" : 3, "cols" : 3, "matrix" : [[0,0,0],[0,0,0],[0,0,0]] },
        "B" : { "name" : "B", "rows" : 3, "cols" : 3, "matrix" : [[0,0,0],[0,0,0],[0,0,0]] },
        "C" : { "name" : "C", "rows" : 3, "cols" : 3, "matrix" : [[0,0,0],[0,0,0],[0,0,0]] },
        "D" : { "name" : "D", "rows" : 3, "cols" : 3, "matrix" : [[0,0,0],[0,0,0],[0,0,0]] },
        "ANS" : { "name" : "ANS", "rows" : 3, "cols" : 3, "matrix" : [[0,0,0],[0,0,0],[0,0,0]] }
    },
    "expression" : "",
    "history" : {}
}