ans=(v,r)=>{for(;r--;){n='',R=L=0
for(c of v+"_"){if(c!=L)n+=L?R+L:'',R=0,L=c
++R}v=n}return n}