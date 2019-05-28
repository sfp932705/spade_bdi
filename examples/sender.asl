!start.

+!start <-
    .print("sending a message ...");
    .send("BDIReceiverAgent@localhost", achieve, hello("Hello World!"));
    .print("sent a message").