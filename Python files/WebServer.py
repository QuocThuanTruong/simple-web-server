import socket
import time
import threading
import re

"""
Simple HTTP Web Server.
"""
class WebServer:
    HTTP_PORT = 80
    DEFAULT_BACKLOG = 5

    """
    Init webserver with default port is 80.
    @params
        port    port of server.
    """
    def __init__(self, port = HTTP_PORT):
        self._host = socket.gethostname() 
        self._addr = socket.gethostbyname(self._host)
        self._port =  port
        self._server_directory = 'D:\\Nam2\\HKII\\MMT\\ThucHanh\\Socketio\\Web-Server\\HTML files'              #Current dir stored server files

    """
    Create socket server using IPv4 and TCP.
    """
    def create(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #Create server socket

        try:
            self._server_socket.bind((self._host, self._port))                          #Binding host and port

            print("\nServer infomation:")
            print(f"\tHost name: {self._host}")
            print(f"\tIP address: {self._addr}")
            print(f"\tPort: {self._port}\n")
        except Exception as e:
            print(f"Failed to bind server on port {self._port}.")
            print(e)
            self.shutdown()

        self._listen()                                                                  #Listen to connection

    """
    Shut down the server.
    """
    def shutdown(self):
        self._server_socket.shutdown(socket.SHUT_WR)

    """
    Listen to client's connection.
    """
    def _listen(self):
        self._server_socket.listen(self.DEFAULT_BACKLOG)

        #Create inf loop connection
        while True:
            (client_socket, client_addr) = self._server_socket.accept()
            print(f"Connection from {client_addr} has been established.")
            threading.Thread(target = self._handle_client_request, args = (client_socket, client_addr)).start()

    """
    Get client request and handle, reponse it.
    @params
        client_socket   client that server accepted.
        client_addr     address of client (IP, port).
    """
    def _handle_client_request(self, client_socket, client_addr):
        DEFAULT_USERNAME = "admin"
        DEFAULT_PASSWORD = "admin"
        PACKET_SIZE = 4096

        data = client_socket.recv(PACKET_SIZE).decode()                                 #Receive data from client_socket

        #Not exist data -> end func _handle_client_request
        if not data:
            return

        #Split data to get file_requested
        method_request = data.split(' ')[0]

        if method_request == "GET":
            file_requested = data.split(' ')[1]
            file_requested = file_requested.split('?')[0]                               #Ignore ?xxx if have

            if file_requested == '/':
                file_requested = "/index.html" 
        elif method_request == "POST":
            #Implements here
            pass
                    
        #Open file_requested to get data_response and create response_header
        try:
            if method_request == "GET":
                file_response_client = open(self._server_directory + file_requested, 'rb')
                data_response = file_response_client.read()
                response_header = self._create_response_header(200)
            elif method_request == "POST":
                #Implements here
                pass

        except:
            file_response_client = open(self._server_directory + "/404.html", 'rb')
            data_response = file_response_client.read()
            response_header = self._create_response_header(404) 

        finally:
            file_response_client.close()
        
        #Send response to client include header + data
        response_to_client = response_header.encode()
        response_to_client += data_response

        client_socket.send(response_to_client)

        #Close connection
        client_socket.close()

    """
    Create HTTP general header - applying to both requests and responses (no relation to data).
    Supported response code: 200, 301, 404
    @params
        response_code   HTTP response code in header
    """
    def _create_response_header(self, response_code):
        SERVER_NAME = 'Python.Webserver'
        HTTP_200_HEADER = 'HTTP/1.1 200 OK\r\n'
        HTTP_301_HEADER = 'HTTP/1.1 301 Moved Permanently\r\n'
        HTTP_404_HEADER = 'HTTP/1.1 404 Not Found\r\n'

        #Append header 
        header = ''
        if response_code == 200:
            header += HTTP_200_HEADER
        elif response_code == 301:
            header += HTTP_301_HEADER
        elif response_code == 404:
            header += HTTP_404_HEADER
        
        #Format time stamp: dWeek, dMonth month year hh:MM:ss 
        cur_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += f"Date: {cur_time}\r\n"
        header += f"Server: {SERVER_NAME}\r\n"
        header += "Connection: close\r\n\n"
        
        return header

if __name__ == "__main__":
    web_server = WebServer(80)
    web_server.create()
