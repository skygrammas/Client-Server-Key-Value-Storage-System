# Client-Server-Key-Value-Storage-System

# Project Description

This project introduces the concept of client/server architecture and caching as discussed in class. Your task is to create a simple web and proxy server that stores and retrieves key-value pairs using socket programming interface. The server only permits commands such as GET PUT and DUMP in the request field followed by the key and value stored. GET returns the value of the key specified, PUT stores the key and a specified value on the server and DUMP lists all of the key value pairs contained in the server. When the client makes a GET request, this request is passed through the proxy server. If the server has made the same request using the same key, the key-value should be retrieved from the proxy server instead of the server. 

# Connecting to the Server via a Client
To establish a connection with the server:
Install  telnet . 
Ensure that your server/proxy server program is running. 
Open a terminal and connect to the client using the command  telnet <ip address> <port #>  

# Code
To help you get started, we have included partial implementations to a proxy server and server. You are to complete the implementation and ensure proper functionality. The places where you need to fill in code are marked with #TODO. Each place may require one or more lines of code. 

# Requirement Summary
Implement GET and PUT commands on the server 
Implement the DUMP command on the server
Implement a proxy server that forwards requests from the client to the server
Implement caching that returns the value of a GET command if it has been previously requested by the client
