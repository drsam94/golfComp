def ans(f):
 P=open(f).read().splitlines();S=[];p=lambda:len(S)and S.pop();c=[0,0];d=5
 while O:=P[c[1]][c[0]]:
  if O in'_|':O='<>^v'[(p()==0)+2*(O=='|')]
  if O in'+-*/%`':a=p();S+=[eval(f"{p()}{ {'`':'>','/':'//'}.get(O,O)}{a}")]
  d={'<':3,'>':5,'^':1,'v':7}.get(O,d);Z=O in'\\:$!@'and p();X=(c[1]+d//3-1)%len(P);c=[(c[0]+d%3-1)%len(P[X]),X];S+=[Z,Z]*(':'==O)+[Z==0]*('!'==O)+[ord(O)-48]*('/'<O<':')
  if'\\'==O:S+=[Z,p()]
  if'@'==O:return Z