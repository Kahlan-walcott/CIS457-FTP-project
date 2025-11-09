from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import sys, random 


'''Sends out FTP commands, parses for multilines of code'''
def ftp_command(s, cmd):
  print(f"Sending command {cmd}")
  buff = bytearray(512)
  s.sendall((cmd + "\r\n").encode())
  # TODO: Fix this part to parse multiline responses
  
  # Loop until end of lines
  while True:
    print('Start loop for multiline output')
    # print output and number or bytes
    nbytes = s.recv_into(buff)
    print(f"{nbytes} bytes: {buff.decode()}")
    # Test if line starts with 3 digit code
    try:
      three_digit_code = int(buff.decode()[0:3])
      print('THREE DIGIT CODE', three_digit_code)
      # if line starts with three digit code check for '-'
      if buff.decode()[4] != '-':
        # exit loop
        print('END LOOP')
        return three_digit_code
      else:
        continue
    # No 3 digit code, continue loop
    except:
      print('CONTINUE LOOP')
      continue

''' open TCP socket and connect to server '''
def open_server(server):
  buffer = bytearray(512)
  # command_sock = socket(AF_INET, SOCK_STREAM)
  # command_sock.connect((server, 21))
  try:
    command_sock = socket(AF_INET, SOCK_STREAM)
    command_sock.connect((server, 21))
  # Error handling: unknown FTP server
  except:
    print("Unknown server.")
    new_connect = str(input("Open connection -> "))
    new_connect = new_connect.split(' ')
    print(new_connect)
    return open_server(new_connect[1])
  
  # print(command_sock, 'Type', type(command_sock))
  len = command_sock.recv_into(buffer)
  print(f"Server response {len} bytes: {buffer.decode()}")
  #  prompt user input for username
  username = input("Enter username > ")
  user(str(username), command_sock)
  return command_sock

''' enter user id for server '''
def user(username, command_sock):
  user_check = ftp_command(command_sock, 'USER ' + username)
  if user_check == 331:
    pas = input("Enter password > ")
    password(str(pas), command_sock)

''' enter password for server '''
# enter password for server
def password(password, command_sock):
  pass_check = ftp_command(command_sock, 'PASS ' + password)
  # loop in case of wrong username or password (status code 530)
  if pass_check >= 530:
    print("Invalid username or password.")
    username2 = input("Enter username > ")
    user(username2, command_sock)
    if username2 == 'close':
      close(command_sock)

''' Show list of remote files user: dir or ls server: LIST '''
def list_out(command_sock):
  # create new socket
  new_sock = new_data_socket(command_sock)
  ftp_command(command_sock, 'TYPE A')
  ls_check = ftp_command(command_sock, 'LIST')

  # threading read_data with secondary response message
  if ls_check == 125 or ls_check == 150:
    threading([read_data, [new_sock, None]], [secondary_response, [command_sock]])

  elif ls_check >= 500:
    print('Command not recognized')
  elif ls_check >= 400 and ls_check < 500:
    print('Connection error')
  
''' Change current directory on the remote host User: cd Server: CWD '''
def cd(command_sock, directory):
  cd_check = ftp_command(command_sock, 'CWD ' + str(directory))
  # error message for when directory isn't there or available to enter
  if cd_check >= 550:
    print("That directory is not available.")
    
''' Download file xxxxx from the remote host User: get Server: RETR '''
def get(command_sock, file_path_name):
  # Create new socket
  new_sock = new_data_socket(command_sock)
  ftp_command(command_sock, 'TYPE I')
  get_check = ftp_command(command_sock, 'RETR ' + file_path_name)

  # threading read_data and secondary response message
  if get_check == 125 or get_check == 150:
    threading([read_data, [new_sock, file_path_name]], [secondary_response, [command_sock]])

  # downloading non-existent remote file 
  if get_check >= 500:
    print("File not found.")
    file_in = input("Enter command > ")
    get(command_sock, file_in)
    if file_in == 'close':
      close(command_sock)


''' Upload file yyyyy to the remote host User: put Server: STOR '''
def put(command_sock, file_path_name):
  # Open file to translate into a binary file (new_file)
  rfile = open(file_path_name, "rb")  # Open for reading as a binary file
  new_file = ('BIN' + str(file_path_name))
  wbin = open(new_file, "wb")  # Open for writing as a binary file
  
  # Read contents of old file into binary file
  buff = rfile.read()     # read all bytes from rfile into buf
  wbin.write(buff)           # write from buff to new_file
  print('NEW_FILE', new_file)
  print('FW', wbin)
  # close files
  rfile.close()
  wbin.close()

  # Create new socket
  new_sock = new_data_socket(command_sock)
  ftp_command(command_sock, 'TYPE I')
  put_check = ftp_command(command_sock, 'STOR ' + new_file)
 # secondary response message
  if put_check == 125 or put_check == 150:
    secondary_response(command_sock)

  # Error checking
  if put_check >= 450: 
    print("The file you are trying to upload is nonexistent.")
    
''' terminate the current FTP session, but keep your program running User: close Server: QUIT '''
def close(command_sock):
  ftp_command(command_sock, 'QUIT')

''' terminate both FTP session and program User: quit Server: QUIT '''
def quit(command_sock):
  try:
    ftp_command(command_sock, 'QUIT')
    sys.exit(0)
  except:
    sys.exit(0)

''' open new data socket '''
def new_data_socket(old_command_sock):
  my_ip, my_port = old_command_sock.getsockname()
  my_ip = my_ip.replace('.', ',')
  # generate random # 1024 - 65535
  ran_port = random.randint(1024,65535)
  # get values for ran_port = x * 256 + y
  x = ran_port//256
  y = ran_port % 256
  ftp_command(command_sock, f"PORT {my_ip},{x},{y}")
  
  # Use the "receptionist" to accept incoming connections
  data_receptionist = socket(AF_INET, SOCK_STREAM)
  data_receptionist.bind(("0.0.0.0", ran_port))
  data_receptionist.listen(1)         # max number of pending request

  # Use the "data_socket" to perform the actual byte transfer
  data_socket = data_receptionist.accept()
  # make data_socket type socket.socket()
  data_socket = data_socket[0]
  return data_socket

''' Read output for secondary response message'''
def secondary_response(command_sock):
  buff = bytearray(512)
  while True:
    #print('Start loop for multiline output')
    # print output and number or bytes
    nbytes = command_sock.recv_into(buff)
    print(f"{nbytes} bytes: {buff.decode()}")
    # Test if line starts with 3 digit code
    try:
      three_digit_code = int(buff.decode()[0:3])
      print('THREE DIGIT CODE', three_digit_code)
      # if line starts with three digit code check for '-'
      if buff.decode()[4] != '-':
        # exit loop
        # print('END LOOP')
        return three_digit_code
      else:
        continue
    # No 3 digit code, continue loop
    except:
      print('CONTINUE LOOP')
      continue

''' prints incoming data'''
def read_data(data_sock, path=None):
  # max 512 bytes per buff
  buff = bytearray(512)
  if path != None:
    fw = open(str(path), "wb")  # Open for writing as a binary file
  nbytes = 512
  while nbytes >= 512:
    nbytes = data_sock.recv_into(buff)
    print(f"{nbytes} bytes: \n{buff.decode()}")
    if path != None:
      fw.write(buff)

  if path != None:
    print('FW')
    print(fw)
    fw.close()

  # else:
    # loop until no more bytes
  # nbytes = 512
  # while nbytes >= 512:
  #   nbytes = data_sock.recv_into(buff)
  #   print(f"{nbytes} bytes: \n{buff.decode()}")
  
  # close socket when done
  data_sock.close()


''' Read output for secondary response message'''
def secondary_response(command_sock):
  buff = bytearray(512)
  while True:
    #print('Start loop for multiline output')
    # print output and number or bytes
    nbytes = command_sock.recv_into(buff)
    print(f"{nbytes} bytes: {buff.decode()}")
    # Test if line starts with 3 digit code
    try:
      three_digit_code = int(buff.decode()[0:3])
      print('THREE DIGIT CODE', three_digit_code)
      # if line starts with three digit code check for '-'
      if buff.decode()[4] != '-':
        # exit loop
        # print('END LOOP')
        return three_digit_code
      else:
        continue
    # No 3 digit code, continue loop
    except:
      print('CONTINUE LOOP')
      continue

''' Threading for LIST, RETR, STOR, and read_data'''
def threading(funct1, funct2):
  # funct1 is read_data(new_sock)
  # funct2 is seocndary_response(command_sock)
  # print(f"FUNCT1: {funct1} \n")
  # print(f"FUNCT2: {funct2} \n")
  one = Thread(target=funct1[0], args=(funct1[1]))
  one.start()
  two = Thread(target=funct2[0], args=(funct2[1]))
  two.start()

  one.join()
  two.join()
  # print('ONE: FTP command', one)
  # print('TWO: read data', two)
  #return one

if __name__ == '__main__':
  command_lst = ['dir', 'ls', 'cd', "put", "get", "quit", "close", "open"]
  first = str(input("Open connection -> "))
  first = first.split(' ')
  print(first)
  while first[0] != 'open' or len(first) <= 1:
    print('Error - cannot run command')
    first = input('Open connection -> ')
    first = first.split(' ')
  command_sock = open_server(first[1])
  # To tell if the user typed close before before quit
  closes = 0
  # type open then name of server
  while True: 
    commands = input("Enter command > ")
    inputs = commands.split()
    print(inputs)

    if inputs[0] not in command_lst:
      commands = input("Please enter a valid command > ")
      inputs = commands.split()

    if inputs[0] == 'dir' or inputs[0] == 'ls':
      list_out(command_sock)

    if inputs[0] == 'cd':
      cd(command_sock, inputs[1])

    if inputs[0] == "put":
      put(command_sock, str(inputs[1]))

    if inputs[0] == "get":
      get(command_sock, inputs[1])

    if inputs[0] == "quit":
      quit(command_sock)
      command_sock.close()
      if closes == 0:
        quit(command_sock)
      print("Program closing.")
      break

    if inputs[0] == "close":
      closes = 1
      close(command_sock)
      server = input("Enter server name > ")
      command_sock = open(server)
     
    if inputs[0] == 'open':
      command_sock = open_server(first[1])
