from prettytable import PrettyTable
import json

from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ('The server is ready to receive')

#username/password : balance
users = {
    "A": 10,
    "A_ID": 100,

    "B": 10,
    "B_ID": 200,

    "C": 10,
    "C_ID": 300,

    "D": 10,
    "D_ID": 400,
}


txA = {
    
}

txB ={
    
}

txC = {

}

txD = {

}


def fetch_txData(user):
    hist = {

    }
    if(user == 'A'):
        hist["txdata"] = txA
    elif(user == 'B'):
        hist["txdata"] = txB
    elif(user == 'C'):
        hist["txdata"] = txC
    else:
        hist["txdata"] = txD

    histJson = json.dumps(hist)
    print("TX Fetched Successfully\n")
    return histJson


def updateTx(user, tx):
    if(user == 'A'):
        txA.update(tx)
    elif(user == 'B'):
        txB.update(tx)
    elif(user == 'C'):
        txC.update(tx)
    else:
        txD.update(tx)

def add_txData(clientTx): 

    userID = str(clientTx.get("cur_ID"))
    #data in ID
    newtx = {

    }

    newtx.update(clientTx["addTx"])

    user = newtx[userID]["payer"]
    print("Attenmpting to add new TX: \n")
    print(newtx)
    add = {

    }

    if(users.get(user) >= int(newtx[userID]["numTrans"])):
        print("TX Accepted\n")
        newtx[userID]["status"] = 2
        print('New TX :')
        print(newtx)

        users[newtx[userID]["payee1"]] = users.get(newtx[userID]["payee1"]) + int(newtx[userID]["numRec1"])
        updateTx(newtx[userID]["payee1"], newtx)
        if(newtx[userID]["payee2"] != 'none'):
            users[newtx[userID]["payee2"]] = users.get(newtx[userID]["payee2"]) + int(newtx[userID]["numRec2"])
            updateTx(newtx[userID]["payee2"], newtx)


        if(user == 'A'):   
            txA.update(newtx)
            users['A'] = users.get(user) - int(newtx[userID]["numTrans"])
            users['A_ID'] = users.get('A_ID') + 1

        elif(user =='B'): 
            txB.update(newtx)
            users['B'] = users.get(user) - int(newtx[userID]["numTrans"])
            users['B_ID'] = users.get('B_ID') + 1

        elif(user == 'C'): 
            txC.update(newtx)
            users['C'] = users.get(user) - int(newtx[userID]["numTrans"])
            users['C_ID'] = users.get('C_ID') + 1

        elif(user == 'D'): 
            txD.update(newtx)
            users['D'] = users.get(user) - int(newtx[userID]["numTrans"])
            users['D_ID'] = users.get('D_ID') + 1

    else:
        print("TX Rejected, not enough balance\n")
        newtx[userID]["status"] = 3
    
    add.update({"balance": users.get(user)})
    add.update(newtx)
    addJson = json.dumps(add)
    return addJson

    

#function used to identify user 
def authenticate_user(user, password):

    auth = { #hold the balance and tx history

    }

    if(user == 'A' and password == 'A'):
        print("User Authenticated\n")
        auth.update({"balance": users.get('A')})
        auth.update({"ID": users.get('A_ID')})
        auth["tx_data"] = txA
    elif(user == 'B' and password == 'B'):
        print("User Authenticated\n")
        auth.update({"balance": users.get('B')})
        auth.update({"ID": users.get('B_ID')})
        auth["tx_data"] = txB
    elif(user == 'C' and password == 'C'):
        print("User Authenticated\n")
        auth.update({"balance": users.get('C')})
        auth.update({"ID": users.get('C_ID')})
        auth["tx_data"] = txC
    elif(user == 'D' and password == 'D'):
        print("User Authenticated\n")
        auth.update({"balance": users.get('D')})
        auth.update({"ID": users.get('D_ID')})
        auth["tx_data"] = txD
    else:
        print("User Not Authenticated")
        auth.update({"balance": -1})
    
    authJson = json.dumps(auth)
    return authJson

#Function will be used to identify the message sent by the client 
#Once the server identifies the message sent by the client,
#It will send back the appropriate response 
def identify_message(temp_message): 
    temp_message = json.loads(temp_message)
    if(temp_message.get('enter') == 'X'):
        print("New Message received from client!\n")
        print("Authenticating user\n")
        return authenticate_user(temp_message.get('user'), temp_message.get('pass'))
    elif(temp_message.get('fetch') == 'Z'):
        print("New Message received from client!\n")
        print("Fetching TX\n")
        return fetch_txData(temp_message.get('name')) 
    elif(temp_message.get('add') == 'C'):
        print("New Message received from client!\n")
        print("Adding TX\n")
        return add_txData(temp_message)

    

while 1: 
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode()
    client_message = identify_message(modifiedMessage)
    serverSocket.sendto(client_message.encode(), clientAddress)
    print("Message sent back to client!\n")