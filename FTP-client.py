from socket import socket, AF_INET, SOCK_STREAM
FTP_SERVER = "ftp.cs.brown.edu"

buffer = bytearray(512)

def ftp_command(s, cmd):
  print(f"Sending command {cmd}")
  buff = bytearray(512)
  s.sendall((cmd + "\r\n").encode())
  # TODO: Fix this part to parse multiline responses
  nbytes = s.recv_into(buff)
  print(f"{nbytes} bytes: {buff.decode()}")
  
command_sock = socket(AF_INET, SOCK_STREAM)
command_sock.connect((FTP_SERVER, 21))
my_ip, my_port = command_sock.getsockname()
len = command_sock.recv_into(buffer)
print(f"Server response {len} bytes: {buffer.decode()}")

ftp_command(command_sock, "USER anonymous")
ftp_command(command_sock, "QUIT")


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
  commands = input("Enter thing > ")