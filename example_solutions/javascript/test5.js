ans=p=>{var j=Array,c=t=L=R=1,d=[...j(7)].map(x=>j(6).fill(0)),g=(x,y)=>d[x]?.[y]==c
for(e of p){j=d[e].indexOf(0)
if(j<0)break
for(d[e][j]=c;g(e,j-L++););for(Q=-2;++Q<3;){if(L+R>5)return c*t
for(L=R=1;g(e-L,j-Q*L++););for(;g(e+R,j+Q*R);++R);}c=-c
t++}return 0}