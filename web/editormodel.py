model = {
    "commands" : [
      { "command" : "+", "expression" : "+", "tooltip" : "Add 2 matrices. Example: A=B+C", "operation_type" : "dual"},
      { "command" : "-", "expression" : "-",  "tooltip" : "Subtract 2 matrices. Example: A=B-C", "operation_type" : "dual"},
      { "command" : "*", "expression" : "*",  "tooltip" : "Multiply 2 matrices. Example: A=B*C", "operation_type" : "dual"},
      { "command" : "^", "expression" : "^", "tooltip" : "Raise a matrix to the power of an exponent. Example: A=B^2", "operation_type" : "dual"},
      { "command" : "x", "expression" : "x",  "tooltip" : "Cross product of 2 vectors. Example: A=BxC", "operation_type" : "dual"},
      { "command" : "·", "expression" : "·",  "tooltip" : "Dot product of 2 vectors. Example: A=B·C", "operation_type" : "dual"},
      { "command" : "☉", "expression" : "☉",  "tooltip" : "Hadamard product of 2 matrices. Example: A=B☉C", "operation_type" : "dual"},
      { "command" : "rref", "expression" : "rref()",  "tooltip" : "Reduce Row Echelon Form. Example: A=rref(B)", "operation_type" : "single"},
      { "command" : "det", "expression" : "det()", "tooltip" : "Evaluates the determinant of a square matrix. Example: A=det(B)", "operation_type" : "single"},
      { "command" : "trace", "expression" : "trace()", "tooltip" : "Evaluates the trace of a square matrix. Example: A=trace(B)", "operation_type" : "single"},
      { "command" : "transpose", "expression" : "transpose()", "tooltip" : "Swaps the rows and collumns of a matrix. Example: A=transpose(B)", "operation_type" : "single"}
    ],
    "matrices" : {
        "ANS" : { "name" : "ANS", "rows" : 3, "cols" : 3, "matrix" : [[0,0,0],[0,0,0],[0,0,0]] },
        "A" : { "name" : "A", "rows" : 3, "cols" : 3, "matrix" : [[0,0,0],[0,0,0],[0,0,0]] },
        "B" : { "name" : "B", "rows" : 3, "cols" : 3, "matrix" : [[0,0,0],[0,0,0],[0,0,0]] },
        "C" : { "name" : "C", "rows" : 3, "cols" : 3, "matrix" : [[0,0,0],[0,0,0],[0,0,0]] },
        "D" : { "name" : "D", "rows" : 3, "cols" : 3, "matrix" : [[0,0,0],[0,0,0],[0,0,0]] }
    },
    "expression" : "",
    "history" : [],
    "equation_solver" : {
      "equations" : [],
      "solutions" : {}
    }
}