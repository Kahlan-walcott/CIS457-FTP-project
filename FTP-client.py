from socket import socket, AF_INET, SOCK_STREAM
# FTP_SERVER = "ftp.cs.brown.edu"
FTP_SERVER = 'test.rebex.net'

buffer = bytearray(512)

def ftp_command(s, cmd):
  print(f"Sending command {cmd}")
  buff = bytearray(512)
  s.sendall((cmd + "\r\n").encode())
  # TODO: Fix this part to parse multiline responses
  # i is the exit condition (when ### + ' ')
  i = 1
  # Loop until end of lines
  while i == 1:
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
        i = 0
        print('END LOOP')
    # No 3 digit code, continue loop
    except TypeError:
      print('CONTINUE LOOP')
      continue
  # nbytes = s.recv_into(buff)
  # print(f"{nbytes} bytes: {buff.decode()}")
  
command_sock = socket(AF_INET, SOCK_STREAM)
command_sock.connect((FTP_SERVER, 21))
my_ip, my_port = command_sock.getsockname()
len = command_sock.recv_into(buffer)
print(f"Server response {len} bytes: {buffer.decode()}")

# ftp_command(command_sock, "USER anonymous")
# ftp_command(command_sock, "QUIT")
ftp_command(command_sock, "USER demo")
ftp_command(command_sock, "PASS password")


# Show list of remote files user: dir server: LIST
def list_out ():
  pass

# Change current directory on the remote host User: cd Server: CWD
def move():
  pass

# Download file xxxxx from the remote host User: get Server: RETR
def get(file):
  pass

# Upload file yyyyy to the remote host User: put Server: STOR
def put(file):
  pass

# terminate the current FTP session, but keep your program running User: quit or close Server: QUIT
def end():
  pass


if __name__ == '__main__':
  commands = input("Enter command > ")
  commands.split()
  if commands[1] == "put":
    pass
  