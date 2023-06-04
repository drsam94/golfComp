def ans(f):
 P=open(f).read().split('\n');S=[];p=lambda:len(S)and S.pop();m=n=J=0;d=5
 while 64-J:
  O=P[n][m:];O=O and O[0]or" ";Z=O in'\\:$!@`_|'and p();Q=Z==0;d={60:3,62:5,94:1,118:7,95:[3,5][Q],124:[1,7][Q]}.get(J:=ord(O),d);n=(n+d//3-1)%len(P);m=(m+d%3-1)%80;S+=[Z,Z]*(58==J)+[Q]*(33==J)+[J-48]*(47<J<58)
  if O in'+-*/%`':a=p();S+=[int(eval(f"{p()}{O if J-96else'>'}{a}"))]
  if 92==J:S+=[Z,p()]
 return Z