data = '''
program myprog;
var 
    d : integer;
    i : Boolean;
    
begin
    a := 1;
    b := -2;
    c := a / b;
    d := a - b;

    if c > d
    then i := true
    else i := false;
end;
'''