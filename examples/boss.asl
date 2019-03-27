!start.
type(dec).

+!start <-
    -start;
    !obj2.

+!obj2: type(inc) <- 
    .send("slave_1@localhost", tell, incrementar(0));
    .send("slave_2@localhost", tell, incrementar(0));
    .wait(2000);
    !obj2.

+!obj2: type(dec) <- 
    .send("slave_1@localhost", tell, decrementar(0));
    .send("slave_2@localhost", tell, decrementar(0));
    .wait(2000);
    !obj2.