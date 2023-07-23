#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <mpi.h>

#define POWMIN 3
#define POWMAX 10

// Funções do Jogo da Vida
void UmaVida(int* tabulIn, int* tabulOut, int tam) {
    // Implementação da lógica do Jogo da Vida
}

void InitTabul(int* tabulIn, int* tabulOut, int tam) {
    // Implementação da inicialização do tabuleiro
}

int Correto(int* tabul, int tam) {
    // Implementação para verificar se o tabuleiro está correto
}

int main(int argc, char** argv) {
    int num_procs, rank;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    int pow, i, tam, *tabulIn, *tabulOut;
    char msg[9];
    double t0, t1, t2, t3;

    // para todos os tamanhos do tabuleiro
    for (pow = POWMIN; pow <= POWMAX; pow++) {
        tam = 1 << pow;

        // aloca e inicializa tabuleiros
        tabulIn = (int*)malloc((tam + 2) * (tam + 2) * sizeof(int));
        tabulOut = (int*)malloc((tam + 2) * (tam + 2) * sizeof(int));
        InitTabul(tabulIn, tabulOut, tam);

        t0 = MPI_Wtime();

        #pragma omp parallel for private(i) shared(tabulIn, tabulOut, tam) schedule(static)
        for (i = 0; i < 2 * (tam - 3); i++) {
            UmaVida(tabulIn, tabulOut, tam);
            UmaVida(tabulOut, tabulIn, tam);
        }

        t1 = MPI_Wtime();

        if (Correto(tabulIn, tam))
            printf("**Ok, RESULTADO CORRETO**\n");
        else
            printf("**Nok, RESULTADO ERRADO**\n");

        t2 = MPI_Wtime();

        printf("Processo %d; tam=%d; tempos: init=%7.7f, comp=%7.7f, fim=%7.7f, tot=%7.7f \n",
               rank, tam, t1 - t0, t2 - t1, t2 - t0);

        free(tabulIn);
        free(tabulOut);
    }

    MPI_Finalize();
    return 0;
}
