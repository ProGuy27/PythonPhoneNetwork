# PythonPhoneNetwork
This is a simulation of a phone network using python

you have the ability to create switch boards and add phone numbers to them. 
You can also start and end calls between existing phone numbers. This uses a recursive pathfinding algorithm to verify a path between 2 phone numbers

Here is a list of the commands you can use inside of this program: 
command list: 
switch-add [area code] - adds a new switchboard with area code [area code]
switch-connect [area code 1] [area code 2] - connects two switch boards if the area codes entered correspond with two real switch boards
phone-add [area code]-[phone number part 1]-[phone number part 2] - adds a phone number to the desired switchboard. example: phone-add 301-746-5729 adds 
the number 746-5729 to the switch board 301
network-save [filename with file extension] - saves the current network to the desired file
network-load [file name with file extension] - loads the network present on the desired file
start call [phone number 1] [phone number 2] - starts a call between the two phone numbers
end-call [phone number] - if the specified phone number is in a call, end the call. 
display - displays all information about the phone network, like all current switchboards with their connections and phone numbers, as well as which of their phone
numbers are in use
