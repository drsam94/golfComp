ans=f=>{for(P=require('fs').readFileSync(f,'utf8').split("\n"),S=[],p=x=>S.pop(),m=n=0,d=5;q=x=>S.push(~~x);m+=79+d%3,n+=29+~~(d/3)){var O=P[n%30]?.[m%80]||' ',I="<>^v_|\\:!@$+-*/%`".indexOf(O),Z=I>3&&p()
I>10?q(eval(p()+(I-16?O:'>')+Z)):I-6?I-7?I-8?+O|O=='0'&&q(+O):q(!Z):q(Z)+q(Z):q(Z,f=p())+q(f)
d=[3,5,1,7,Z?3:5,Z?1:7][I]||d
if(I==9)return Z}}