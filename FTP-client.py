from socket import socket, AF_INET, SOCK_STREAM
# FTP_SERVER = 'test.rebex.net'

buffer = bytearray(512)
code = int(000)

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
        break
      # print('CODE', three_digit_code)
      # if three_digit_code == 221:
      #   break
      else:
        continue
    # No 3 digit code, continue loop
    except:
      # if code == 221:
      #   print("In except block")
      #   break
      print('CONTINUE LOOP')
      continue

# ftp_command(command_sock, "USER demo")
# ftp_command(command_sock, "PASS password")
# ftp_command(command_sock, 'LIST')

# ftp_command(command_sock, 'USER ftp')
# ftp_command(command_sock, 'USER mail@example.com')

# open TCP socket and connect to server
def open(server):
  command_sock = socket(AF_INET, SOCK_STREAM)
  command_sock.connect((server, 21))
  my_ip, my_port = command_sock.getsockname()
  len = command_sock.recv_into(buffer)
  print(f"Server response {len} bytes: {buffer.decode()}")
  # TODO: prompt user input for username or password when required
  username = input("Enter username > ")
  user(str(username), command_sock)
  pas = input("Enter password > ")
  password(str(pas), command_sock)
  return command_sock

# enter user id for server
def user(username, command_sock):
  ftp_command(command_sock, 'USER ' + username)

# enter password for server
def password(password, command_sock):
  ftp_command(command_sock, 'PASS ' + password)

# Show list of remote files user: dir or ls server: LIST
def list_out(command_sock):
  ftp_command(command_sock, 'LIST')
  # TODO: account for secondary response message

# Change current directory on the remote host User: cd Server: CWD
def cd(command_sock, directory):
  ftp_command(command_sock, 'CWD ' + directory)

# Download file xxxxx from the remote host User: get Server: RETR
def get(command_sock, file_path_name):
  ftp_command(command_sock, 'RETR ' + file_path_name)
  # TODO: account for secondary response message


# Upload file yyyyy to the remote host User: put Server: STOR
def put(command_sock, file_path_name):
  ftp_command(command_sock, 'STOR ' + file_path_name)
  # TODO: account for secondary response message

# terminate the current FTP session, but keep your program running User: close Server: QUIT
def close(command_sock):
  ftp_command(command_sock, 'QUIT')

# terminate both FTP session and program User: quit Server: QUIT
def quit(command_sock):
  ftp_command(command_sock, 'QUIT')


if __name__ == '__main__':
  command_lst = ['dir', 'ls', 'cd', "put", "get", "quit", "close"]
  server = input("Enter server name > ")
  command_sock = open(server)
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
      # causes an infinite loop (how to find out if the connection has already been severed - no infinite loop) 221
      # print("The code" ,three_digit_code)
      # if three_digit_code == 221:
      quit(command_sock)
      print("Program closing.")
      # break
      # if three_digit_code != 221:
      # quit(command_sock)
      break

    if inputs[0] == "close":
      close(command_sock)
