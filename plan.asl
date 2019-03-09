!start.

+!start <-
    +car(rojo);
    .a_function(3,W);
    .print("w =", W);
    literal_function(rojo,Y);
    .print("Y =", Y);
    .custom_action(8);
    .print("sending individual message ...");
    .send("BDIAgent@localhost", achieve, hello(15));
    .print("sent a message").
    +truck(azul).

+car(amarillo) 
 <- .print("El carro es amarillo.").

+!hello(Msg)[source(Sender)] <-
  .print("got a message from", Sender, "saying", Msg).

 