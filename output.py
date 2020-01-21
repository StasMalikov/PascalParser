arr1 = [0, 0, 0]
var1 = 0
i = 1
while i < 4:
    arr1[i-1] = int(input())
    i = i + 1

j = 1
while j < 4:
    var1 = var1 + arr1[j-1]
    j = j + 1

print( var1)
