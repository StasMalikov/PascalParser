data = '''
program myprog;
var 
    a,b,c,d : integer;
    i : Boolean;

function notcoprime(M,N: integer): Boolean;

begin
    a := 1;
    b := -2;
    c := a / b;
    d := a - b;

    if c > d
    then i:= true
    else i:= false;

end;
'''