def ans(s,e):
 r=w=d=m=0;y=1900
 while y<=e:r+=(w==4)*(d==12)*(y>=s);w=-~w%7;d=-~d%(31-(m in(3,5,8,10))+(m==1)*((y%4<1)*((y%25>0)|(y%16<1))-3));m+=1>d;m%=12;y+=m+d<1
 return r