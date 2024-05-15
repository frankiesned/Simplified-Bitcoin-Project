from prettytable import PrettyTable
import sys
import json

from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)


def pay1Opt(val):
    if val == 'A':
        opt = input("Who will be payee 1 (B, C, D): ")
        while(opt != 'B' and opt != 'C' and opt != 'D'):
            opt = input("Invalid payee! Who will be payee 1 (B, C, D): ")
    elif val == 'B':
        opt = input("Who will be payee 1 (A, C, D): ")
        while(opt != 'A' and opt != 'C' and opt != 'D'):
            opt = input("Invalid payee! Who will be payee 1 (A, C, D): ")
    elif val == 'C':
        opt = input("Who will be payee 1 (A, B, D): ")
        while(opt != 'A' and opt != 'B' and opt != 'D'):
            opt = input("Invalid payee! Who will be payee 1 (A, B, D): ")
    elif val == 'D':
        opt = input("Who will be payee 1 (A, B, C): ")
        while(opt != 'A' and opt != 'B' and opt != 'C'):
            opt = input("Invalid payee! Who will be payee 1 (A, B, C): ")

    return opt


def pay2Opt(val, val2):
    if val == 'A' and val2 == 'B':
        opt = input("Who will be payee 2 (C, D): ")
        while(opt != 'C' and opt != 'D'):
            opt = input("Invalid payee! Who will be payee 2 (C, D): ")

    elif val == 'A' and val2 == 'C' or val == 'C' and val2 == 'A':
        opt = input("Who will be payee 2 (B, D): ")
        while(opt != 'B' and opt != 'D'):
            opt = input("Invalid payee! Who will be payee 2 (B, D): ")

    elif val == 'A' and val2 == 'D':
        opt = input("Who will be payee 2 (B, C): ")
        while(opt != 'B' and opt != 'C'):
            opt = input("Invalid payee! Who will be payee 2 (B, C): ")

    elif val == 'B' and val2 == 'C':
        opt = input("Who will be payee 2 (A, D): ")
        while(opt != 'A' and opt != 'D'):
            opt = input("Invalid payee! Who will be payee 2 (A, D): ")

    elif val == 'B' and val2 == 'D':
        opt = input("Who will be payee 2 (A, C): ")
        while(opt != 'A' and opt != 'C'):
            opt = input("Invalid payee! Who will be payee 2 (A, C): ")

    elif val == 'C' and val2 == 'D':
        opt = input("Who will be payee 2 (C, D): ")
        while(opt != 'C' and opt != 'D'):
            opt = input("Invalid payee! Who will be payee 2 (C, D): ")

    return opt

#table used to display in format
table = PrettyTable()
table.field_names = ["User Payer", "TX #", "Status", "Payee 1", "Payee 2"]

#authenticating user
flag = 1
while(flag == 1):
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    auth = {
        "enter": "X",
        "user": username,
        "pass": password
    }

    authJson = json.dumps(auth)

    clientSocket.sendto(authJson.encode(),(serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    response = modifiedMessage.decode()

    #response here will be a dictonary with balance and tx
    response = json.loads(response)
    
    #response will be the balance
    #else it will be -1 if couldnt find the user in server
    authFlag = 1
    if(response.get("balance") == -1):  
        print("Not Authenticated.")
        while(authFlag == 1):
            print("1: Enter the username and password again.")
            print("2: Quit the program")
            var = input("Choose an option: ")

            if(var == '1'):
                authFlag = 0
            elif(var == '2'):
                clientSocket.close()
                sys.exit()
            else:
                print("Option must be 1 or 2.")
    else:
        print("\nAuthenticated")
        flag = 0

#user is authenticated

#store users current balance
userBalance = response.get("balance")
userID = response.get("ID")
print("Here is your balance: ", userBalance)

#store users confirmed TXs into a list
txList = {

}

txList.update(response.get("tx_data"))
for x in txList:
    table.add_row([txList[x]["payer"], x, txList[x]["status"], txList[x]["payee1"], txList[x]["payee2"]])

print(table) #print list

update = 0
flag = 1
while(flag == 1):

    print("\n1: Make a transaction.")
    print("2: Fetch and display list of transactions.")
    print("3: Quit the program.")

    flag = input("Choose an option: ")
    match flag:
        case '1':
            tx = {}
            id = {}

            id["status"] = 1
            id["payer"] = username      
            id["numTrans"] = input('Enter amount to transfer: ')
            
            id["payee1"] = pay1Opt(username)
            
            
            id["numRec1"] = input("Enter the amount to be payed to the first payee: ")
    
            while(int(id["numTrans"]) < int(id["numRec1"])):
                 val = "Too much, amount has to be under " + id["numTrans"] + ": "
                 id["numRec1"] = input(val)
            
            if(id["numTrans"] != id["numRec1"]):
                id["payee2"] = pay2Opt(id["payer"], id["payee1"])
                num = int(id["numTrans"]) - int(id["numRec1"])
                id["numRec2"] = str(num)
                print("Payee will receive", id["numRec2"])
            else:
                id["payee2"] = "none"
                id["numRec2"] = 0
            tx[userID] = id
            add = {
                "add" : "C",
                "cur_ID" : userID
            }
            add["addTx"] = tx
            addJson = json.dumps(add)
            clientSocket.sendto(addJson.encode(),(serverName, serverPort))
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            response = modifiedMessage.decode()
            response = json.loads(response)

            userID = str(userID)

            userBalance = response["balance"]

            if(response[userID]["status"] == 3):
                print("TX rejected, insufficient balance.")
                print("Here's your balance:",userBalance)
            else:
                print("\nTX accepted, sufficient balance.")
                print("Here's your new balance:",userBalance)
                update = 1

        case '2':
            disp = {
                "fetch" : "Z",
                "name" : username
            }
            dispJson = json.dumps(disp)
            clientSocket.sendto(dispJson.encode(),(serverName, serverPort))
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            response = modifiedMessage.decode()
            response = json.loads(response)
            fetchTx = {

            }
            if(update == 1):
                for x in response["txdata"]:
                    if(userID == x):
                        table.add_row([response["txdata"][x]["payer"], x, response["txdata"][x]["status"], response["txdata"][x]["payee1"], response["txdata"][x]["payee2"]])

            update = 0
            print("\nHere is your balance: ", userBalance)
            print(table)
        case '3':
            clientSocket.close()
            sys.exit()
        case _:
            print("Invalid choice")
    
    flag = 1    

    
    