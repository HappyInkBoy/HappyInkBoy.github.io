model = {
    "commands" : [
      { "command" : "+", "expression" : "+", "tooltip" : "Add 2 matrices. Example: A=B+C"},
      { "command" : "-", "expression" : "-",  "tooltip" : "Subtract 2 matrices. Example: A=B-C"},
      { "command" : "*", "expression" : "*",  "tooltip" : "Multiply 2 matrices. Example: A=B*C"},
      { "command" : "^", "expression" : "^", "tooltip" : "Raise a matrix to the power of an exponent. Example: A=B^2"},
      { "command" : "⨯", "expression" : "⨯",  "tooltip" : "Cross product of 2 vectors. Example: A=B⨯C"},
      { "command" : "·", "expression" : "·",  "tooltip" : "Dot product of 2 vectors. Example: A=B·C"},
      { "command" : "☉", "expression" : "☉",  "tooltip" : "Hadamard product of 2 matrices. Example: A=B☉C"},
      { "command" : "RREF", "expression" : "RREF()",  "tooltip" : "Reduce Row Echelon Form. Example: A=RREF(B)"},
      { "command" : "DET", "expression" : "DET()", "tooltip" : "Evaluates the determinant of a square matrix. Example: A=DET(B)"},
      { "command" : "TRACE", "expression" : "TRACE()", "tooltip" : "Evaluates the trace of a square matrix. Example: A=TRACE(B)"},
      { "command" : "TRANSPOSE", "expression" : "TRANSPOSE()", "tooltip" : "Swaps the rows and collumns of a matrix. Example: A=TRANSPOSE(B)"}
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