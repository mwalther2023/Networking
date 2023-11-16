For the server.py file in order to compile and run it you will need to be on a linux or mac machine due to the windows complications with sys.stdin and sockets</br>
To run simply use the following command:</br>
<b>*$ python3 server.py [server name/IP] [port]*</b>

This will begin the server startup on the specified location.</br>
Once a connection is made the server will wait for a user connection.</br>
After recieving the initial message with the necessary parameters the server can now forward valid messages to the desired room or client.</br>
When a client disconnects they will be removed from the list to be read, write, or check exceptions.</br>

To exit the user can use ctrl+c to initiate a keyboard kill of the server in which it will send the shutdown message to all connected clients forcing their disconnect.