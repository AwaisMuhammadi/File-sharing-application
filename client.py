import socket
from pathlib import Path
from checkSum import checksum

def connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1234))
    return s


def main_fun():
    ss = connection()
    print("Welcome to Virtual Cloudly")
    print("1.Upload File\n2.List Available Files\n3.Download File\n4.Exit")

    f = "y"
    while f == "y":
        ch = input("Enter your choice:")
        ss.send(bytes(ch, "utf-8"))
        if ch == "1":
            filePath = input("Enter file path: ")
            if Path(filePath).is_file():  # F:/Semester 6/DC/SemProj/file.txt
                # extracting file name form path
                filePath_list = filePath.split('/')
                # send name of the file
                ss.send(bytes(filePath_list[-1],'utf-8'))
                # receive whether it exists or not
                check = ss.recv(1024)  # receive 0 if exist otherwise 1
                check = check.decode('utf-8')
                if check == "0":
                    fileObj = open(filePath, 'r')
                    data = fileObj.read()
                    check_sum = checksum(data.encode('utf-8'))
                    ss.send(bytes(check_sum,'utf-8'))
                    check_sum_match = ss.recv(1024)
                    check_sum_match = check_sum_match.decode('utf-8')
                    if check_sum_match == "0":
                        print("File is already up-to-date!")
                    elif check_sum_match == "1":
                        fileObj = open(filePath, 'r')
                        data = fileObj.read()
                        ss.send(bytes(str(len(data.encode('utf-8'))), 'utf-8'))
                        ss.send(bytes(data, 'utf-8'))
                        print("File updated successfully!")




                elif check == "1": # file does not exist so send complete file
                    fileObj = open(filePath, 'r')
                    data = fileObj.read()
                    ss.send(bytes(str(len(data.encode('utf-8'))), 'utf-8'))
                    ss.send(bytes(data, 'utf-8'))
                    print("File uploaded successfully!")
            else:
                print("Wrong Path. File does not exist!")
        elif ch == "2":
            no_of_bytes = ss.recv(1024)  # receiving no of bytes of list
            list_of_files = ss.recv(int(no_of_bytes.decode('utf-8')))  # receive list of available files
            list_of_files = list_of_files.decode('utf-8')
            list_of_files = list_of_files.split(',')
            print("Available files:")
            for item in list_of_files:
                print(item)
        elif ch == "3":
            fileName = input("Enter file name: ")
            ss.send(bytes(fileName,'utf-8'))  # send file name
            check = ss.recv(1024)
            check = check.decode('utf-8')
            if check == "0":  # file is available
                no_of_bytes = ss.recv(1024)  # receiving no of bytes of file data
                file_data = ss.recv(int(no_of_bytes.decode('utf-8')))  # receive data of file
                file_obj = open(fileName, 'wb')  # create file and open it
                file_obj.write(file_data)  # write data in file
                file_obj.close()  # close file
                print(fileName+" downloaded successfully")
            else:
                print("No such file exist on server!")

        elif ch == "4":
            print("Exiting...")
            exit()


        else:
            print("You have entered a wrong number!")

        f = input("Do you want to perform another task [y/n]:")
        ss.send(bytes(f, "utf-8"))



main_fun()
