!start.

+!start <-
    +car(rojo);
    //.a_function(3,W);
    //.print("w =", W);
    //literal_function(rojo,Y);
    //.print("Y =", Y);
    //.custom_action(8);
    .print("sending individual message ...");
    .send("RECEIVERBDIAgent@localhost", achieve, hello(15));
    .print("sent a message").
    +truck(azul).

+car(Color) 
 <- .print("El carro es ",Color).


 