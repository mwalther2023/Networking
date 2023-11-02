For the client.py file in order to compile and run it you will need to be on a linux or mac machine due to the windows complications with sys.stdin and sockets
To run simply use the following command:
$ python3 client.py [server name/IP] [port]

This will begin the client startup on the specified server.
Once a connection is made the client will prompt the user for a Name and chat room targets.
After sending the initial message with these parameters the user can now type "msg" to begin the process of sending a message to either directly to a user or generally to a chat room which is specified by the user's input.
To send a direct message this is shown through the following inputs by the user:
$ msg
$ [@user_name]
$ [message contents]
For a chat room message:
$ msg
$ [#chat_room]
$ [message contents]

To exit the user can use ctrl+c to initiate a keyboard kill of the program or type "exit" after a message sequence prompt was completed.