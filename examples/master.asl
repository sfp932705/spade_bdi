!start.

+!start 
 <-
  -start;
  !obj2.

+!obj2: tipo(inc) 
 <- 
  .send("slave_1@localhost", tell, incrementar(2));
  .send("slave_2@localhost", tell, incrementar(5));
  .wait(2000);
  !obj2.

+!obj2: tipo(dec) 
 <- 
  .send("slave_1@localhost", tell, decrementar(2));
  .send("slave_2@localhost", tell, decrementar(5));
  .wait(2000);
  !obj2.

+!obj2: not tipo(_)
 <-
  .print("Finishing");
  .send("slave_1@localhost", untell, incrementar(2));
  .send("slave_2@localhost", untell, incrementar(5));
  .send("slave_1@localhost", untell, decrementar(2));
  .send("slave_2@localhost", untell, decrementar(5)).