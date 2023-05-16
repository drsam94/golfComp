let ans=f=>{for(let P=require('fs').readFileSync(f,'utf8').split("\n"),S=[],p=x=>S.pop(),c=[0,0],d=5;q=x=>S.push(~~x);c=[(79+C+d%3)%80,~~(Z-1+c[1]+d/3)%Z]){var Z=P[c[1]],C=c[0],O=C<Z.length?Z[C]:' ',I="<>^v_|\\:!@$+-*/%`".indexOf(O)
Z=I>3?p():0
I==6?q(Z,f=p())+q(f):I>10?q(eval(p()+(I-16?O:'>')+Z)):I==7?q(Z)+q(Z):I==8?q(!Z):(+O||O=='0')?q(+O):0
d=[3,5,1,7,Z?3:5,Z?1:7][I]||d
if(I==9)return Z
Z=P.length}}