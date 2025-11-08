from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import sys, random 

# FTP_SERVER = 'test.rebex.net'

# buffer = bytearray(512)

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
    # buff = bytearray(nbytes)
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

# ftp_command(command_sock, "USER demo")
# ftp_command(command_sock, "PASS password")

# open TCP socket and connect to server
def open(server):
  buffer = bytearray(512)
  command_sock = socket(AF_INET, SOCK_STREAM)
  command_sock.connect((server, 21))
  # my_ip, my_port = command_sock.getsockname()
  # print('MY_IP AND MY_PORT', my_ip, my_port)
  len = command_sock.recv_into(buffer)
  print(f"Server response {len} bytes: {buffer.decode()}")
  # TODO: prompt user input for username
  username = input("Enter username > ")
  user(str(username), command_sock)
  return command_sock

# enter user id for server
def user(username, command_sock):
  user_check = ftp_command(command_sock, 'USER ' + username)
  if user_check == 331:
    pas = input("Enter password > ")
    password(str(pas), command_sock)


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

# Show list of remote files user: dir or ls server: LIST
def list_out(command_sock):
  # ls_check = ftp_command(command_sock, 'LIST')
  # TODO: account for secondary response message
  # read data here
  stuff = new_data_socket(command_sock)
  print(stuff)
  ls_check = ftp_command(command_sock, 'NLST')

  # I couldn't get the command back so this is commented out
  # close(command_sock)
  if ls_check == 125 or ls_check == 150:
    print(f"{stuff}, {ls_check}")
  # if ls_check == 226 or ls_check == 250:
  new_data_socket(command_sock)

# Change current directory on the remote host User: cd Server: CWD
def cd(command_sock, directory):
  ftp_command(command_sock, 'CWD ' + str(directory))

# Download file xxxxx from the remote host User: get Server: RETR
def get(command_sock, file_path_name):
  # get_check = ftp_command(command_sock, 'RETR ' + file_path_name)
  new_data_socket(command_sock)
  # TODO: account for secondary response message
  # if get_check == 125 or get_check == 150:
  # if ls_check == 226 or ls_check == 250:


# Upload file yyyyy to the remote host User: put Server: STOR
def put(command_sock, file_path_name):
  # put_check = ftp_command(command_sock, 'STOR ' + file_path_name)
  new_data_socket(command_sock)
  # fw = open("somefile", "wb")
  # fw.write(buff_w)
  # TODO: account for secondary response message
  # if put_check == 125 or put_check == 150:
  # if ls_check == 226 or ls_check == 250:


# terminate the current FTP session, but keep your program running User: close Server: QUIT
def close(command_sock):
  ftp_command(command_sock, 'QUIT')

# terminate both FTP session and program User: quit Server: QUIT
def quit(command_sock):
  ftp_command(command_sock, 'QUIT')
  sys.exit(0)

# open new data socket
def new_data_socket(old_command_sock):
  my_ip, my_port = old_command_sock.getsockname()
  my_ip = my_ip.replace('.', ',')
  # generate random # 1024 - 65535
  ran_port = random.randint(1024,65535)
  # get values for ran_port = x * 256 + y
  x = ran_port//256
  y = ran_port % 256
  port_comm = ftp_command(command_sock, f"PORT {my_ip},{x},{y}")
  
  # Use the "receptionist" to accept incoming connections
  data_receptioninst = socket(AF_INET, SOCK_STREAM)
  data_receptioninst.bind(("0.0.0.0", ran_port))
  data_receptioninst.listen(1)         # max number of pending request

  # Use the "data_socket" to perform the actual byte transfer
  data_socket = data_receptioninst.accept()
  # nbytes = old_command_sock.recv_into(buff)
  # # buff = bytearray(nbytes)
  # print(f"{nbytes} bytes: {buff.decode()}")
  return data_receptioninst


if __name__ == '__main__':
  command_lst = ['dir', 'ls', 'cd', "put", "get", "quit", "close", "open"]
  first = str(input("Open connection -> "))
  first = first.split(' ')
  print(first)
  while first[0] != 'open' or len(first) <= 1:
    print(first, len(first))
    print('Error - cannot run command')
    first = input('Open connection -> ')
  command_sock = open(first[1])
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
      command_sock.close()
      if closes == 0:
        quit(command_sock)
      print("Program closing.")
      break

    if inputs[0] == "close":
      closes = 1
      command_sock.close()
      close(command_sock)
      # server = input("Enter server name > ")
      # command_sock = open(server)

    if inputs[0] == 'open':
      command_sock = open(first[1])

# ftp.dlptest.com	
# username dlpuser
#password rNrKYTX9g7z3RgJRmxWuGHbeu
