# TextTorrent
A simple torrenting application.

## Tutorial
To use the application, the tracker needs to be run first. The tracker keeps track of the files each peer has.
Start any number of peers to connect to the tracker. It is adviced to use docker or something similar in order not to run into errors when running multiple instances of peer.py. When a peer connects, all the local files of the peer are listed by the tracker. To download or see which files are available, simply type "ls". You will then see a list. Write the corresponding index number for the file you want to download. Repeat as many times as you wish for different files. Once you're done write 'close' to close the connection.

## Commands

`ls` - displays available files

`close` - closes the connection

