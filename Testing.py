v = [0,1,80,2,3,4,5,6,7,8,9,12,13,14,15]

#variables

foundID = False
cont = 0
n=0
i=1
#while i<len(v):
 # for j in range(0, len(v)):
  #  if v[j]==n:
   #     n = n+1 
    #    break
  #else:
   # i+=1
while i<len(v):
    for j in range(0, len(v)):
        if v[j]==n:
            n = n+1 
            break
    else:
        i+=1
print(n)
