#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>

#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 8005
#define BUFFER_SIZE 1024

int connect_to_server() {
    int client_socket;
    struct sockaddr_in server_address;
    char buffer[BUFFER_SIZE] = {0};

    if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("Erro no cliente");
        exit(EXIT_FAILURE);
    }

    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(SERVER_PORT);

    if (inet_pton(AF_INET, SERVER_IP, &server_address.sin_addr) <= 0)
    {
        perror("Erro no endereço");
        exit(EXIT_FAILURE);
    }

    if (connect(client_socket, (struct sockaddr *)&server_address, sizeof(server_address)) < 0)
    {
        perror("Erro na conexão");
        exit(EXIT_FAILURE);
    }

    printf("Server conectado no ip: %s e na porta %d\n", SERVER_IP, SERVER_PORT);

    return client_socket;
}

void close_connection(int client_socket) {
    close(client_socket);
}

void send_numbers(int client_socket) {
    char buffer[BUFFER_SIZE] = {0};
    while (1)
    {
        int num1, num2;

        printf("Insira dois números inteiros: ");
        scanf("%d %d", &num1, &num2);

        snprintf(buffer, sizeof(buffer), "%d %d", num1, num2);
        send(client_socket, buffer, strlen(buffer), 0);

        memset(buffer, 0, sizeof(buffer));
    }
}

int main()
{
    int client_socket = connect_to_server();
    send_numbers(client_socket);
    close_connection(client_socket);

    return 0;
}
