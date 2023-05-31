def ans(p):
 d=[6*[0]for _ in range(7)];c=t=1;g=lambda x,y:0<=x<7and-1<y<6and d[x][y]==c
 for e in p:
  if d[e][5]:break
  j=d[e].index(0);d[e][j]=c;L=R=1
  while g(e,j-L):L+=1
  for Q in(-1,0,1,2):
   if L+R>4:return c*t
   L=R=1
   while g(e-L,j-Q*L):L+=1
   while g(e+R,j+Q*R):R+=1
  c=-c;t+=1
 return 0