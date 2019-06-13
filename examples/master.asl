!start.

+!start 
 <-
  -start;
  !obj2.

+!obj2: tipo(inc) 
 <-
  ?slave1(X);
  ?slave2(Y);
  .send(X, tell, incrementar(2));
  .send(Y, tell, incrementar(5));
  .wait(2000);
  !obj2.

+!obj2: tipo(dec) 
 <-
  ?slave1(X);
  ?slave2(Y);
  .send(X, tell, decrementar(2));
  .send(Y, tell, decrementar(5));
  .wait(2000);
  !obj2.

+!obj2: not tipo(_)
 <-
  ?slave1(X);
  ?slave2(Y);
  .print("Finishing");
  .send(X, untell, incrementar(2));
  .send(Y, untell, incrementar(5));
  .send(X, untell, decrementar(2));
  .send(Y, untell, decrementar(5)).
