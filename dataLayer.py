import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 33))
s.listen()


def main_fun(client):
    while True:
        ch = client.recv(1024)  # receiving user choice
        ch = ch.decode('utf-8')  # decoding data
        if ch == "1":
            fileName = client.recv(1024)
            fileName = fileName.decode('utf-8')
            #no_of_bytes = client.recv(1024)  # receiving no of bytes of file data
            #no_of_bytes = no_of_bytes.decode("utf-8")
            file_data = client.recv(99000)  # receive data of file
            new_file_path = "Database/" + fileName  # new file path
            file_data = file_data.decode('utf-8')
            file_obj = open(new_file_path, 'w')  # create file and open it
            file_obj.write(file_data)  # write data in file
            file_obj.close()  # close file


        elif ch == "3":
            fileName = client.recv(1024)
            fileName = fileName.decode('utf-8')
            filePath = "Database/" + fileName
            fileObj = open(filePath, 'r')
            data = fileObj.read()
            client.send(bytes(str(len(data.encode('utf-8'))), 'utf-8'))
            client.send(bytes(data, 'utf-8'))


while True:
    clientSocket, address = s.accept()
    print(f"connected {address}")
    main_fun(clientSocket)