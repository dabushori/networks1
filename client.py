import socket
import sys

linesep = '\n'

# parsing the arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# a function to get the url from the server
# addr = (ip, port), url = string of url


def getInfoFromServer(addr, url):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(url.encode(), addr)
    data, address = s.recvfrom(1024)
    s.close()
    return data.decode()


while True:
    # getting the user's input
    url = input('Enter a url: ').strip(' ' + linesep)
    info = getInfoFromServer((serverIP, serverPort), url)
    # printing only the ip address of the url (the server's answer format is <url>,<ip>,<ttl>)
    print(info.split(',')[1])
