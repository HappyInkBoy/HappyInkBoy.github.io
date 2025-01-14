# To test locally

* open terminal
* go to <folder that contains this github repo>/web
* enter this command to start a local http server: `python3 -m http.server`
* open web browser to http://localhost:8000/calculator.html

# To publish

* push to github repo so it is available via github pages

# To consume as a user

Open web browser to https://happyinkboy.github.io/web/calculator.html

# Here are some valid expressions for the calculator:

* ANS = A + B
* A + B
* A*B
* RREF(A)
* B = RREF(A)

BNF
variable = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "K" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "ANS" ;
digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
number = [ "-" ], digit, {digit} ;


Valid expressions are represented below in the form of the EBNF (Extended Backus Naur Form): https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form

dual operator = "+" | "-" | "*" | "☉" | "·" | "⨯" ;
matrix digit operator = "^" ;
single operator = "RREF" | "DET" | "TRACE" | "TRANSPOSE" ;
assignement expression = variable, "=", implicit expression ;
implicit expression = dual expression | single expression ;
dual expression = variable, dual operator, variable ; 
single expression = single operator, "(", variable, ")" ;
matrix digit expression = variable, matrix digit operator, number ;

Note that:
☉ is U+2609
· is U+00B7
⨯ is U+2A2F

Below are strech goals
* A + B + C
* AB
* A(B+C)
