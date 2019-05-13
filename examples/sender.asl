!start.

+!start <-
    .print("sending a message ...");
    .send("ReceiverAgent@localhost", achieve, hello("Hello World!"));
    .print("sent a message").