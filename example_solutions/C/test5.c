#define g(x,y);while(0<=x&x<7&0<=y&y<6?d[x][y]==c:0)++
long ans(*s,*e){for(int d[7][6]={},c=1,t=1;s<e;++s){int j=0,E=*s,L=1,R=1,Q=-2,*D=d[E];if(D[5])break;for(;D[j];++j)g(E,j-L)L;for(D[j]=c;++Q<3;){if(L+R>4)return c*t;L=R=1
g(E-L,j-Q*L)L
g(E+R,j+Q*R)R;}c=-c;t++;}return 0;}