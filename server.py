import socket
import threading
import subprocess

BUFFER_SIZE = 1024

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Servidor rodando na porta {self.port}")

            while True:
                client_socket, address = self.server_socket.accept()
                client_handler = ClientHandler(client_socket, address)
                client_handler.start()

        except KeyboardInterrupt:
            print("Servidor desligado")
        finally:
            self.server_socket.close()

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, address):
        super().__init__()
        self.client_socket = client_socket
        self.address = address

    def run(self):
        print(f"Cliente conectado, IP: {self.address[0]}, Porta: {self.address[1]}")
        while True:
            data = self.client_socket.recv(BUFFER_SIZE)
            if not data:
                print(f"Host desconectado, IP: {self.address[0]}, Porta: {self.address[1]}")
                break

            nums = [int(num) for num in data.decode().split()]
            powmin, powmax = nums[0], nums[1]
            print(f"Cliente {self.address[0]}:{self.address[1]} enviou: powmin={powmin}, powmax={powmax}")

            valueArgs = {'powmin': powmin, 'powmax': powmax}
            self.openmpi(valueArgs)
            self.spark(valueArgs)

            print("\nAguardando cliente\n")
            sum_result = powmin + powmax
            response = f"Soma: {sum_result}"
            self.client_socket.send(response.encode())

        self.client_socket.close()

    def openmpi(self, valueArgs):
        print("Rodando com OpenMP e MPI\n")
        comando = f"./openmpi {valueArgs['powmin']} {valueArgs['powmax']}"
        subprocess.call(comando, shell=True)

    def spark(self, valueArgs):
        print("Rodando com Spark\n")
        comando = f"python3 ./jogodavida.py {valueArgs['powmin']} {valueArgs['powmax']}"
        subprocess.call(comando, shell=True)

def main():
    server = Server("0.0.0.0", 8005)
    server.run()

if __name__ == "__main__":
    main()
