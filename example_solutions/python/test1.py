ans=lambda x:sum(y*(y%3*y%5<1)for y in range(x))