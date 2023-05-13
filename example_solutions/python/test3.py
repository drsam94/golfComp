def ans(v,r):
 while r:
  n='';R=1;L=v[0]
  for c in v[1:]+'_':X=c!=L;n+=X*(str(R)+L);R+=1-R*X;L=c
  v=n;r-=1
 return v