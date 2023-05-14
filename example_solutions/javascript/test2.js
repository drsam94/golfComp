ans=(s,e)=>{for(var r=d=m=w=0,y=1900;y<=e;){r+=w==4&d==12&y>=s
w=++w%7
if(++d>29+(2773>>m&1)-(m==1)*(1+!(y%4<1&&(y%25|y%16<1))))d=++m-m
if(m==12)m=++y-y}return r}