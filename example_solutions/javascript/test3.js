ans=(v,r)=>{for(;r--;){let n=v.slice(1)+"_",R=1,L=v[0]
v=""
for(c of n){if(c!=L)v+=R+L,R=0,L=c
++R}}return v}