from datetime import date
R=range
ans=lambda s,e:sum(date(y,m,13).weekday()==4for y in R(s,e+1)for m in R(1,13))