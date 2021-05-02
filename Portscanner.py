#--------------------------------IMPORTS----------------------------
import socket
import threading
from queue import Queue

target = '127.0.0.1' #Target IP Address
queue = Queue() #Creates An Empty Queue
open_ports = [] #List For All Open Ports


def portscan(port): #Function For Port Scanning, That Takes A Port As A Parameter
    try: #Try Statement For Error Raising
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates A Socket
        sock.connect((target, port)) #Connects The Socket To The Target IP Via Specified Port
        return True #Connection Successfully
    except:
        return False #Connection Failure

def fill_queue(portlist): #Function For Filling The Queue, That Takes The portlist List As An Parameter
    for port in portlist: #For Loop To Iterate Over The portlist List
        queue.put(port) #Adds Each Port To The Queue

def worker(): #Function For The Threading Of The Port Scanner
    while not queue.empty(): #While Loop To Check If The Queue Isn't Empty
        port = queue.get() #Queue's The Next Port To Be Scanned
        if portscan(port): #If Statement To Check If The Port Returns True (Is Open)
            print("Port {} is open!".format(port)) #Message For Open Port
            open_ports.append(port) #Adds Port To The open_ports Lists

portlist = range(1, 1024) #Specifies To Scan All Ports Between And Including 1 - 1024
fill_queue(portlist) #Calls The fill_queue Function With The portlist List As An Argument

thread_list = [] #List For Our Threads

for t in range(1000): #For Loop To Iterate Over The Amount of Threads Specified (1000)
    thread = threading.Thread(target=worker) #Creates Thread
    thread_list.append(thread) #Adds Thread To The thread_list List

for thread in thread_list: #For Loop To Iterate Over Each Thread In The thread_list List
    thread.start() #Starts Thread

for thread in thread_list: #Iterates Over Each Thread In The thread_list List
    thread.join() #Waits Until Current Thread Is Complete Then Executes Another Thread

print("Open ports are: ", open_ports)