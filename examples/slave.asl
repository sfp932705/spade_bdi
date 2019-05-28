contador(0).

+incrementar(Inc) <- 
  .print("increasing");
  ?contador(X);
  -+contador(X+1);
  -incrementar(_).

+decrementar(Dec) <- 
  .print("decreasing");
  ?contador(X);
  -+contador(X-1);
  -decrementar(_).
