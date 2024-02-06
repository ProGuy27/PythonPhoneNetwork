"""
This program is to simulate a phone network. 
It has a number of different functions
It can create a switch board, add phone numbers to it, and connect switch boards
you can also start and end calls between phone numbers on different switchboards
using the network load and network save commands, you can save the network to a seperate file, as well as load from a seperate file

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

"""

SEPARATOR = '|'
HYPHEN = "-"
QUIT = 'quit'
SWITCH_CONNECT = 'switch-connect'
SWITCH_ADD = 'switch-add'
PHONE_ADD = 'phone-add'
NETWORK_SAVE = 'network-save'
NETWORK_LOAD = 'network-load'
START_CALL = 'start-call'
END_CALL = 'end-call'
DISPLAY = 'display'

def add_brd(arcode, netlist):
    """
    add_brd()
    param arcode: an area code, an int
    param netlist: a 1d list representing all of the switch board in the network. 1 board per index in the list
    if the area code does not exist in the network, add it. if it does, dont
    """
    exist = False
    for i in range(len(netlist)):
        if netlist[i]['area'] == arcode:
            print('that area code is already in use')
            exist = True
    if not exist:
        netlist.append({'area':arcode, 'nums':[], 'connections':[], 'calls':[]})

def connect(arOne, arTwo, netlist):
    """
    connect()
    param arOne: first area code
    param arTwo: second area code
    param netlist: the network list
    if the two area codes exist in the network, draw a trunk line between them
    this can be seen by the connections sublist within the dictionary. 
    i forgot to mention, a switchboard is represented by a dictionary. 
    this is its format: 
    {'area': areacode, 'nums': [123, 456, ...], 'connections': [301, 879, 166, ...], 'calls': ['301-842-3790 to 443-567-8932', '122-765-6566 to 216-298-1089', ...]}
    basically, if the two area codes exist, they will add themselves onto each other connections list 
    """
    exist = 0 # this variable is to increment if the area code exists within the network
    arOneIndex = -1
    arTwoIndex = -1
    for i in range(len(netlist)):
        if netlist[i]['area'] == arOne or netlist[i]['area'] == arTwo:
            exist += 1
            if netlist[i]['area'] == arOne: # this block of code is to save the index at where it found that area code
                arOneIndex = i
            else: 
                arTwoIndex = i

    if exist == 2: # if the exists variable is two, or in other words, if both area codes exist in this network
        if arTwo not in netlist[arOneIndex]['connections']:
            netlist[arOneIndex]['connections'].append(netlist[arTwoIndex]['area'])
        else: 
            print("these two lines are boards are already connected")
            return
        if arOne not in netlist[arTwoIndex]['connections']:
            netlist[arTwoIndex]['connections'].append(netlist[arOneIndex]['area'])
        else: 
            print("these two lines are boards are already connected")
            return
    else: 
        print("one of the selected area codes does not exist")
        return

def add_phn(number, netlist):
    """
    add_phn()
    param number: a phone number in the format of areacode-numPart1-numPart2
    param area: an area code. might or might not exist in the network, gotta check
    param netlist: the network list
    this method checks if the area exists in the network. if it does, add the phone number to that areacode board
    """
    exist = False
    index = -1
    number = number.split(HYPHEN) # split the phone number on the hyphen
    area = int(number[0])

    for i in range(len(netlist)):
        if netlist[i]['area'] == area:
            exist = True
            index = i
    if exist:
        if number[1]+number[2] not in netlist[index]['nums']:
            netlist[index]['nums'].append(number[1]+number[2])
        else: 
            print('that number is already in use')
    else: 
        print("area code doesnt exist")


def format_num(areacode, num):
    """
    given an area code and the other two parts of a number, 
    puts the number into format of areacode-num1-num2
    example: 
    8791661 at 301 would return 301-879-1661
    """
    return str(areacode) + HYPHEN + num[0:3] + HYPHEN + num[3:]

def num_strip(num):
    # given a number, strips it of its area code and returns it in the format of this: '301-445-8730' --> '4458730'
    temp = num.split(HYPHEN)
    return temp[1]+temp[2]

def find_board(num, netlist):
    """ this is a very useful function. given a number it returns the index on the netlist of its switchboard """
    areacode = int(num.split(HYPHEN)[0])

    # locates index of switchboard
    for i in range(len(netlist)):
        if netlist[i]['area'] == areacode:
            return i
        
    return -1 # area code no exist

def identify_board(areacode, netlist):
    """ given an area code, returns the index of its switchboard on the network """
    for i in range(len(netlist)):
        if netlist[i]['area'] == areacode:
            return i
    return -1
#def in_board(num, netlist):
    
def is_conn(num1area, num2area, checked, netlist):

    """
    this function is to determine, given two switchboard areacodes, if a path exists between the two of them
    
    """

    i_one = identify_board(num1area,netlist) # the find board method, given a number, returns the index of the switchboard it is on within the network netlist

    if num1area == num2area: # if the switchboard of num1 = the switchboard of num2, they most definitely have a path, so return true
        return True
    else:
        checked.append(num1area) # num1 and 2 arent on the same board yet, so make sure we record that the current board of num1 is checked
        for connection in netlist[i_one]['connections']: # loop though the connections of the board num1 is on
            if connection not in checked: 
                
                # extract the number and put it in the correct format
                connection_board = identify_board(connection, netlist)
                sample_area = netlist[connection_board]['area']
                
                if is_conn(connection, num2area, checked, netlist): # recursive call
                    return True
    return False # all else has failed, so that means there is no path connecting the two nums 

def in_call(num1, netlist):
    """
    given that num1 exists on a proper area code, seeks to find if num1 is in a call or not. true if in call, false if not 
    """
    for board in netlist:
        for call in board['calls']:
            if num1 in call:
                return True
    return False

def start_call(num_one, num_two, netlist):
    """
    this function is to start a call between two numbers if and only if: 
    1. the area codes of the numbers exist
    2. the numbers exist on the desired area code
    3. there exists a path connecting their switchboards
    4. they are not already in a call

    """
    # do the area codes exist 
    num1area = netlist[find_board(num_one,netlist)]['area']
    num2area = netlist[find_board(num_two,netlist)]['area']

    num1 = num_strip(num_one)
    num2 = num_strip(num_two)

    if find_board(num_one, netlist) == -1 or find_board(num_two, netlist) == -1:
        print('that area code does not exist')
        return
    elif num1 not in netlist[find_board(num_one,netlist)]['nums'] or num2 not in netlist[find_board(num_two,netlist)]['nums']:
        print('one or both of the input numbers is not in use')
        return 
    elif not is_conn(num1area,num2area,[],netlist): 
        print('unable to make a call between these two numbers (not connection)')
        return
    elif in_call(num_one, netlist) or in_call(num_two, netlist):
        print('one or both of these numbers are currently in a call')
        return
    else: 
        """
        we now know that: 
        1. the area codes of nums 1 and 2 exist
        2. these numbers exist within those switchboards
        3. there exists a path connecting those switchboards
        4. they arent in a call
        now we can start a call
        """
        call = num_one + ' to ' + num_two

        netlist[find_board(num_one,netlist)]['calls'].append(call)
        netlist[find_board(num_two,netlist)]['calls'].append(call)

def end_call(num, netlist):
    """
    this function, given a number that may or may not exist, has end the call if it is in a call
    """
    if find_board(num,netlist) == -1: 
        print('this numbers area code doesnt exist')
        return
    elif num_strip(num) not in netlist[find_board(num,netlist)]['nums']:
        print('this number is not in use')
        return
    else: 
        """
        at this point, we know that the input number exists. we just have to check if its in a call or not
        if it is, end it. if its not, dont 
        """
        for board in netlist:
            for c in range(len(board['calls'])):
                if num in board['calls'][c]:
                    board['calls'].remove(board['calls'][c])

def display(netlist):
    """
    this is the display function
    """
    for board in netlist: # for every board in the network
        print('switchboard with area code:', board['area']) # print out its area code
        print('\ttrunk lines are:', end = ' ') 
        for connection in board['connections']: # print out its trunk lines by area code
            print(str(connection) + ', ', end = '')
        print()
        print('\tlocal phone numbers are:', end = ' ')
        for number in board['nums']: # print out its local numbers, and dont forget to denotate whether that number is in a call or not 
            print(number, end = '')
            if in_call(format_num(board['area'],number), netlist):
                print(' is in use, ', end = '')
            else: 
                print(' is not in use, ', end = '')
        print()

def shutdown(netlist):
    """
    param netlist: the network list
    this function, given the network list, is to reach into each switchboard and end all calls that are
    on going
    """
    for board in netlist:
        for call in board['calls']:
            board['calls'].remove(call)

def network_save(file_name, netlist):
    """
    param filename: the name of a file, including file extension (.txt, .sv, ...)
    param netlist: the netlist
    this function exports the data of the netlist over to a file indicated by the input
    """
    # first, shut down all calls by calling the shutdown method
    shutdown(netlist)

    # then, open up the file with the corresponding name 
    save_file = open(file_name, 'w') # open the file in write mode so it overwrites any previously saved data
    
    for board in netlist:
        for component in board:
            if component == 'area': # import area code
                save_file.write(str(board[component]) + SEPARATOR)
            elif component == 'nums': # import phone numbers 
                for number in range(len(board[component])):
                    if number == len(board[component])-1:
                        save_file.write(board[component][number] + SEPARATOR)
                    else: 
                        save_file.write(board[component][number] + ' ')
            elif component == 'connections': # import connections
                for connection in range(len(board[component])):
                    if connection == len(board[component])-1:
                        save_file.write(str(board[component][connection]))
                    else: 
                        save_file.write(str(board[component][connection]) + ' ')
        save_file.write('\n')
    save_file.close()

def wipe_net(netlist):
    """ this function is to wipe the netlist. it is a helper function for network_load() """
    while len(netlist) >= 1:
        netlist.remove(netlist[0])

def count(str, c):
    # in the string str, this function returns how many instances of c
    count = 0
    for l in str:
        if l == c:
            count += 1
    return count

def network_load(file_name, netlist):
    """
    from a file that exists, this function will load the data contained within it. 
    """
    save_file = open(file_name, 'r')

    wipe_net(netlist)
    display(netlist)

    for line in save_file: # add in the switchboards
        
        board_data = line.split('|')
        add_brd(int(board_data[0]),netlist)
    save_file.close()

    save_file = open(file_name, 'r')

    for l in save_file:
        if '\n' in l:
            l = l[0:len(l)-1]
        
        if count(l,'|') > 1: # if the current line has more than 1 divider,
            board_data = l.split('|')
            while '' in board_data: # remove any empty spaces
                board_data.remove('')

            if len(board_data) == 2: # there are no trunk lines, only numbers to add
                nums = board_data[1].split(' ') 

                for number in nums: # add the numbers
                    add_phn(format_num(int(board_data[0]), number), netlist)

            elif len(board_data) == 3: # there are trunk lines and numbers
                nums = board_data[1].split(' ') 

                for number in nums: # add the numbers
                    add_phn(format_num(int(board_data[0]), number), netlist)
                
                connections = board_data[2].split(' ')

                #added = [] # this list contains all of the added connections
                for connection in connections: # add the trunk lines
                    if not is_conn(int(board_data[0]), int(connection), [], netlist): 
                        # basically, if the two switchboards arent already connected, connect them
                        connect(int(board_data[0]), int(connection), netlist)

    print(f"network {file_name} loaded")  
    save_file.close()

if __name__ == '__main__':
    net = []
    s = ''

    while s != QUIT:
        #display(net)
        s = input('>>').strip().lower()
        instruction = s.split(' ')
        if len(instruction) == 3: # its a 2 parameter command
            if instruction[0] == SWITCH_CONNECT:
                # it is time to connect two switchboards 
                connect(int(instruction[1]), int(instruction[2]), net)
            elif instruction[0] == START_CALL:
                # it is time to make a call between two numbers
                start_call(instruction[1],instruction[2],net)
        elif len(instruction) == 2: # it is a one parameter command
            if instruction[0] == SWITCH_ADD:
                # it is time to add a switchboard
                add_brd(int(instruction[1]), net)
            elif instruction[0] == PHONE_ADD:
                # it is time to add a phone number
                add_phn(instruction[1],net)
            elif instruction[0] == END_CALL:
                # it is time to end a call
                end_call(instruction[1],net)
            elif instruction[0] == NETWORK_SAVE:
                # it is time to save the network
                network_save(instruction[1], net)
            elif instruction[0] == NETWORK_LOAD:
                # it is time to load a network
                network_load(instruction[1], net)
        else: 
            if instruction[0] == DISPLAY:
                # display the network
                display(net)