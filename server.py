import socket
import sys
from datetime import *

linesep = '\n'

# parsing the arguments
myPort = int(sys.argv[1])
parentIP = sys.argv[2]
parentPort = int(sys.argv[3])
ipsFileName = sys.argv[4]

# a function to get the url from another server
# addr = (ip, port), url = string of url


def getInfoFromServer(addr, url):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(url.encode(), addr)
    data, addr = s.recvfrom(1024)
    s.close()
    return data.decode()


# creating the server socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', myPort))

while True:
    # recieving input from client
    data, addr = s.recvfrom(1024)
    url = data.decode()

    # removing urls that their ttl passed
    ips = open(ipsFileName, 'r')
    lines = ips.readlines()
    ips.close()
    goodLines = []
    for line in lines:
        if len(line.split(',')) == 4:
            line = line.strip(' ' + linesep)
            FMT = '%H:%M:%S'
            ttl = str(line.split(',')[3]).strip(' ' + linesep)
            cTime = datetime.now().strftime(FMT)
            tDelta = datetime.strptime(
                cTime, FMT) - datetime.strptime(ttl, FMT)
            if len(line.split(',')) == 4 and timedelta.total_seconds(tDelta) <= int(line.split(',')[2]):
                goodLines.append(line)
        elif len(line.split(',')) == 3:
            goodLines.append(line)

    # writing the good lines (ips that their ttl didn't pass)
    ipsIn = open(ipsFileName, 'w')
    for goodLine in goodLines:
        ipsIn.write(goodLine.strip(' ' + linesep) + linesep)
    ipsIn.close()

    info = None
    ips = open(ipsFileName, 'r')
    lines = ips.readlines()
    ips.close()

    # finding the url in the ips file
    for line in lines:
        if url == str(line.split(',')[0]):
            if len(line.split(',')) == 4:
                info = ''
                for sub in line.split(',')[0:3]:
                    info = info + sub + ','
                info = info.strip(',')
            else:
                info = line

    # if the data wasn't found, ask the father server
    if info == None and parentIP != '-1' and parentPort != -1:
        info = getInfoFromServer((parentIP, parentPort), url)
        FMT = '%H:%M:%S'
        cTime = datetime.now().strftime(FMT)
        # add the time that the data was learned to the data
        toSave = info.strip(' ' + linesep) + ',' + cTime
        ipsIn = open(ipsFileName, 'a')
        # learn the father's amswer
        ipsIn.write(toSave)
        ipsIn.close()

    # send the answer back to the client
    if info != None:
        s.sendto(info.encode(), addr)
