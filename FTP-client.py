from socket import socket, AF_INET, SOCK_STREAM
# FTP_SERVER = "ftp.cs.brown.edu"
FTP_SERVER = 'test.rebex.net'
# FTP_SERVER = 'ftp.scene.org'

buffer = bytearray(512)

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
      else:
        continue
    # No 3 digit code, continue loop
    except:
      print('CONTINUE LOOP')
      continue
  
command_sock = socket(AF_INET, SOCK_STREAM)
command_sock.connect((FTP_SERVER, 21))
my_ip, my_port = command_sock.getsockname()
# len = command_sock.recv_into(buffer)
# print(f"Server response {len} bytes: {buffer.decode()}")

# ftp_command(command_sock, "USER anonymous")
# ftp_command(command_sock, "QUIT")
ftp_command(command_sock, "USER demo")
ftp_command(command_sock, "PASS password")
# ftp_command(command_sock, 'USER ftp')
# ftp_command(command_sock, 'USER mail@example.com')

# open TCP socket and connect to server
def open(server):
  pass
  # command_sock = socket(AF_INET, SOCK_STREAM)
  # command_sock.connect((FTP_SERVER, 21))
  # my_ip, my_port = command_sock.getsockname()
  # len = command_sock.recv_into(buffer)
  # print(f"Server response {len} bytes: {buffer.decode()}")

# enter user id for server
def user(username):
  pass

# enter password for server
def password(password):
  pass

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
  pass
  # commands = input("Enter thing > ")
  