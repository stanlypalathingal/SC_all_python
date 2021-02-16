import socket
#socket(family,protocol), In my case family is ipv6 and protocl is tcp
def subscribeStatus():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((socket.gethostname(),9006))
    message=s.recv(16)
    #print(message.decode("utf-8"))
    return message.decode("utf-8")
        # s.listen(5)
