def ans(f):
 P=open(f).read().splitlines();S=[];p=lambda:len(S)and S.pop();c=[0,0];d=5
 while 1:
  O=P[c[1]][c[0]]
  if O in'+-*/%`':a=p();S+=[eval(f"{p()}{ {'`':'>','/':'//'}.get(O,O)}{a}")]
  if'\\'==O:S+=[p(),p()]
  if O in'_|':O='<>^v'[(p()==0)+2*(O=='|')]
  d={'<':3,'>':5,'^':1,'v':7}.get(O,d)
  if'/'<O<':':S+=[int(O)]
  if':'==O:S+=[p()]*2
  if'$'==O:p()
  if'!'==O:S+=[p()==0]
  if'@'==O:return p()
  X=(c[1]+d//3-1)%len(P);c=[(c[0]+d%3-1)%len(P[X]),X]