import socket
import threading
from checkSum import checksum

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen()

file_Name_list={}


def connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 33))
    return s


def main_fun(client):
    ss = connection()
    f = "y"
    while f == "y":
        ch = client.recv(1024)  # receiving user choice
        ch = ch.decode('utf-8')  # decoding data
        ss.send(bytes(ch,'utf-8'))
        if ch == "1":
            fileName = client.recv(1024)
            fileName = fileName.decode('utf-8')
            if fileName in file_Name_list.keys():
                client.send(bytes("0",'utf-8'))  # sending signal that file already present
                check_sum = client.recv(1024)  # receiving check sum of file
                check_sum = check_sum.decode('utf-8')  # decoding data
                server_check_sum = file_Name_list.get(fileName)  # getting checksum of file present on datalayer
                if check_sum == server_check_sum:
                    client.send(bytes("0",'utf-8'))  # sending signal that file is already up-to-date
                else:
                    client.send(bytes("1", 'utf-8'))  # sending signal that file is not up to date
                    no_of_bytes = client.recv(1024)  # receiving no of bytes of file data
                    file_data = client.recv(int(no_of_bytes.decode('utf-8')))  # receive data of file


                    ss.send(bytes(fileName, 'utf-8'))
                    #ss.send(bytes(no_of_bytes.decode('utf-8'),'utf-8'))
                    ss.send(bytes(file_data.decode('utf-8'),'utf-8'))


                    file_data = file_data.decode('utf-8')
                    file_Name_list[fileName] = checksum(file_data.encode('utf-8'))


            else:
                client.send(bytes("1",'utf-8'))  # send that file does not exist
                no_of_bytes = client.recv(1024)  # receiving no of bytes of file data
                file_data = client.recv(int(no_of_bytes.decode('utf-8')))  # receive data of file

                ss.send(bytes(fileName, 'utf-8'))
                #ss.send(bytes(no_of_bytes.decode('utf-8'), 'utf-8'))
                ss.send(bytes(file_data.decode('utf-8'), 'utf-8'))


                file_data = file_data.decode('utf-8')
                file_Name_list[fileName] = checksum(file_data.encode('utf-8'))  # create a dictionary tuple whihc have file name and checksum

        elif ch == "2":
            data = file_Name_list.keys()
            string = ""
            j = 0
            for i in data:
                if j == 0:
                    string = i
                    j = j + 1
                else:
                    string = string + "," + i
            client.send(bytes(str(len(string.encode('utf-8'))), 'utf-8'))
            client.send(bytes(string, 'utf-8'))

        elif ch == "3":
            fileName = client.recv(1024)
            fileName = fileName.decode('utf-8')
            if fileName in file_Name_list.keys():
                ss.send(bytes(fileName, 'utf-8'))
                client.send(bytes("0", 'utf-8'))
                no_of_bytes = ss.recv(1024)  # receiving no of bytes of file data
                data = ss.recv(int(no_of_bytes.decode('utf-8')))  # receive data of file
                client.send(bytes(no_of_bytes.decode('utf-8'), 'utf-8'))
                client.send(bytes(data.decode('utf-8'), 'utf-8'))
            else:
                client.send(bytes("1", 'utf-8'))
        f = client.recv(1024)
        f = f.decode('utf-8')



i = 0
while True:
    clientSocket, address = s.accept()
    print(f"connected {address}")
    thread_name = "t" + str(i)
    t = threading.Thread(target=main_fun, args=(clientSocket,), name=thread_name)
    t.start()
    i = i + 1

