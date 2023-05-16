let ans=f=>{for(let P=require('fs').readFileSync(f,'utf8').split("\n"),S=[],p=()=>S.pop(),c=[0,0],d=5,q=x=>S.push(~~x);;c=[(79+C+d%3)%80,~~(L-1+c[1]+d/3)%L]){var Z,L=P[c[1]],C=c[0],O=C<L.length?L[C]:' ',I="+-*/%`\\:$!@_|".indexOf(O)
if(I+1){Z=p()
if(I==6)f=p(),q(Z),q(f)
if(I<6)q(eval(p()+(I-5?O:'>')+Z))}if(+O||O=='0')q(+O)
d={'<':3,'>':5,'^':1,'v':7,'_':Z?3:5,'|':Z?1:7}[O]||d
if(O==':')q(Z),q(Z)
if(O=='!')q(!Z)
if(O=='@')return Z
L=P.length}}