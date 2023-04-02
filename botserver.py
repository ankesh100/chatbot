import socket
import threading
import os
from string import punctuation

import chatbot
import utils

conf = utils.get_config()
toBool = lambda str: True if str == "True" else False
DEBUG_SERVER = toBool(conf["DEBUG"]["server"])

def session(connection):
    i = 0   # counter for how many times we have been round the loop
    startMessage = ""
    
    # initialize the connection to the database
    conf = utils.get_config()
    
    DBHOST = conf["MySQL"]["server"]
    DBUSER = conf["MySQL"]["dbuser"]
    DBNAME = conf["MySQL"]["dbname"]
    
    #print("Starting Bot...")
    # initialize the connection to the database
    #print("Connecting to database...")
    DBconnection = utils.db_connection(DBHOST, DBUSER, DBNAME)
    DBcursor =  DBconnection.cursor()
    DBconnectionID = utils.db_connectionID(DBcursor)
    #print("...connected")
    
    botSentence = 'Hello!'
    weight = 0
    
    trainMe = False
    botSentence = 'Hello!'
    startMessage = startMessage + ("")
    
    def receive(connection):
        
        if DEBUG_SERVER: print("PID {}, thread {} \n".format(pid, thread))
        received = connection.recv(1024)
        if not received:
            print("Closing connection {}".format(thread))
            #return False
            main()
        else:
            if DEBUG_SERVER: print("Received {}, echoing".format(received))
            return received
        
        
    
    while True:
        pid = os.getpid()
        thread = threading.current_thread()
        
        
        # pass received message to chatbot
        received = receive(connection)
        humanSentence = received.decode().strip()
        
        
        if humanSentence == '' or humanSentence.strip(punctuation).lower() == 'quit' or humanSentence.strip(punctuation).lower() == 'exit':
            break

        # Chatbot processing
        botSentence, weight, trainMe = chatbot.chat_flow(DBcursor, humanSentence, weight)
        
        if trainMe:
            send = "I'm sorry it's new for me just teach me what to reply next time?".encode()
            connection.send(send)
            previousSentence = humanSentence
            received = receive(connection)
            humanSentence = received.decode().strip()
                        
            if humanSentence != "skip":
                chatbot.train_me(previousSentence, humanSentence, DBcursor)
                botSentence = "Oh!!! okay i got it"
                #connection.send(send)
            else:
                botSentence = "Cloudy: OK, moving on..."
                #connection.send(send)
                trainMe = False

        DBconnection.commit()
        send = botSentence.encode()
                
        if i == 0:
            send = startMessage.encode() + send
        
        connection.send(send)
        
        i = i + 1

if __name__ == "__main__":
    print("Starting...")
    
    LISTEN_HOST = conf["Server"]["listen_host"]
    LISTEN_PORT = int(conf["Server"]["tcp_socket"])
    LISTEN_QUEUE = int(conf["Server"]["listen_queue"])
    
    # Set up the listening socket
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sckt.bind((LISTEN_HOST, LISTEN_PORT))
    sckt.listen(LISTEN_QUEUE)
    print("...socket set up")
    
    # Accept connections in a loop
    while True:
        print("Waiting for a connection")
        (connection, address) = sckt.accept()
        print("Connect Received" ,connection, address)
        
        threading.Thread(target = session, args=[connection]).start()
        t = threading.Thread(target = session, args=[connection])
        #t.setDaemon(True)  #set to Daemon status, allows CTRL-C to kill all threads
        t.start()
        #t.join()
    
    print("trying again")
    sckt.close()
    #sckt.wait()
    #main()
