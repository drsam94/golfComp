sub ans{my($d,$a)=5,0;for my$y(1900..@_[1]){for my$m(0..11){$a++if($d%7==4&$y>=@_[0]);$d+=30+(2773>>$m&1);if($m==1){$d-=2;$d++if($y%4<1&($y%25>0|$y%16<1))}}}$a}