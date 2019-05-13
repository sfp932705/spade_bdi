contador(8).
tipo(dec).
!inicio.

+!inicio
<-
 .print("Iniciando....");
 !obj2.
 
 
 +!obj2: tipo(inc)
 <-
  .print("Incrementando");
  ?contador(X);
  -+contador(X+1);
  .wait(1000);
  !obj2.
  
  
+!obj2: tipo(dec)
<-
.print("Decrementando");
?contador(X);
-+contador(X-1);
.wait(1000);
!obj2.


+!obj2: not tipo(_)
<-
.print("Esperando");
  .wait(1000);
   !obj2.