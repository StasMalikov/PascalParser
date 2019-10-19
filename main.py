
data = '''
program coprimes;
var M,N: integer;

function notcoprime(M,N: integer): boolean;

var
    K, i, myint: integer;
    Res: Boolean;
begin
    myint:=6;
    Res := false;
    if N > M then K := M else K := N;
    for i := 2 to K do
    Res := Res or (N mod i = 0) and (M mod i = 0);
    notcoprime := Res;
end;
'''
