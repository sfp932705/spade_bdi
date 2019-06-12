contador(0).

+incrementar(Inc)[source(S)]: .substring("master@localhost",S,R) 
 <- 
  .print("increasing");
  ?contador(X);
  .print(X);
  -+contador(X+Inc).

+decrementar(Dec)[source(S)]: .substring("master@localhost",S,R) 
 <- 
  .print("decreasing");
  ?contador(X);
  .print(X);
  -+contador(X-Dec).

-incrementar(Inc)[source(S)]: .substring("master@localhost",S,R) 
 <-
  .print("DELETING incrementar BELIEF from an untell message").

-decrementar(Dec)[source(S)]: .substring("master@localhost",S,R) 
 <-
  .print("DELETING decrementar BELIEF from an untell message").
