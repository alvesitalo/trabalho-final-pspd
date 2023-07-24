# Projeto de Pesquisa

## Integrantes

Daniel Barcelos Moreira - 170101711 <br>
Thiago Mesquita - 180138545 <br>
Italo Alves Guimarães - 180113666 <br>

## Como Rodar

- Acesse o cluster chococino
```
ssh -p 13508 <usuário>@chococino.naquadah.com.br
```

Clone o repositório
```
git clone https://github.com/alvesitalo/trabalho-final-pspd
```

Compile o código openmp/mpi
```
mpicc -o openmpi openmpi.c -fopenmp
```

Rode o servidor e o cliente
```
python3 server.py
gcc client.c -o client
./client
```

Insira os valores de powmin e powmax