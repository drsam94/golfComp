#define p (S-s?*--S:0)
#define P*S++
#define I(x);if(O==*#x)
#define M(x)I(x)P=p x a
struct FILE;long ans(char*f){int a=0,b,T=90,s[T],*S=s,c=0,d=5;char C[2700]={},O;for(f=fopen(f,"r");fgets(&C[a],T,f);a+=T);for(;;c=(89+c%T+d%3)%T+T*((29+c/T+d/3)%30)){O=C[c];a=strchr(",.+0&a]%",O+1)?p:0;I(\\)b=p,P=a,P=b;M(+)M(-)M(*)M(%)M(/)I(`)P=p>a;I(_)O=2*!p+60;I(|)O="^v"[!p]I(<)d=3;I(>)d=5;I(^)d=1;I(v)d=7;if(O>47&O<58)P=O-48;I(:)*S=p,P=P;I(!)P=!p;I(@)return p;}}