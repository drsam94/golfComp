long ans(s,e){long r=0;int w=0,d=0,m=0,y=1900;while(y<=e){r+=(w=++w%7)==5&d==12&y>=s;y+=!(d*=++d<30+(2773>>m&1)-(m==1)*(2-(y%4<1&(y%100||y%400<1))))&&!(m*=12>++m);}return r;}