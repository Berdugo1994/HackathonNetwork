# HackathonNetwork
Intro to Nets 2020 Hackathon Assignment - Keyboard Spamming Battle Royale
Our objective is to write a client-server application which will implement a fast-paced Keyboard
Spamming game. The players in this game are randomly divided into two teams, which have ten
seconds to mash as many keys on the keyboard as possible.
Each team in the course will write both a client application and a server application, and
everybody’s clients and servers are expected to work together with full compatibility.
These target was fully accomplished with remote control on ssh linux server.
Based on UDP, TCP protocols, includes UDP Broadcasting, TCP connection and multithread Design pattern.
Do you think you are typing faster than us ? Lets battle !!!

on the left side you can see the server interface, and on the right the client.
The project done by Sarit Hollander and me.
![Server Client run](https://i.ibb.co/ZSqBcvK/client-server.png)



**
To connect to remote : you must login to your VPN ,
have a file named 'config' on C:\Users\#yourName"\.ssh
with the next lines :
        Host *remoteName*
        Hostname *IPAdress of remote*
        Port *SELECT-PORT*
        User *type*

then on the cmd : ssh *remoteName*
enter password if needed
cd to your path.
then :"python3 Server.py/Client.py"

