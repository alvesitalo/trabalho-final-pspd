import time
import sys
from pyspark import SparkContext

BUFFER_SIZE = 1024

def ind2d(i, j, tam):
    return i * (tam + 2) + j

def uma_vida(args):
    (tabul_in, tabul_out, tam, i) = args
    for j in range(1, tam + 1):
        vizviv = (tabul_in[ind2d(i - 1, j - 1, tam)] + tabul_in[ind2d(i - 1, j, tam)] +
                  tabul_in[ind2d(i - 1, j + 1, tam)] + tabul_in[ind2d(i, j - 1, tam)] +
                  tabul_in[ind2d(i, j + 1, tam)] + tabul_in[ind2d(i + 1, j - 1, tam)] +
                  tabul_in[ind2d(i + 1, j, tam)] + tabul_in[ind2d(i + 1, j + 1, tam)])

        if tabul_in[ind2d(i, j, tam)] and vizviv < 2:
            tabul_out[ind2d(i, j, tam)] = 0
        elif tabul_in[ind2d(i, j, tam)] and vizviv > 3:
            tabul_out[ind2d(i, j, tam)] = 0
        elif not tabul_in[ind2d(i, j, tam)] and vizviv == 3:
            tabul_out[ind2d(i, j, tam)] = 1
        else:
            tabul_out[ind2d(i, j, tam)] = tabul_in[ind2d(i, j, tam)]

def init_tabul(tam):
    tabul_in = [0] * (tam + 2) * (tam + 2)
    tabul_out = [0] * (tam + 2) * (tam + 2)
    tabul_in[ind2d(1, 2, tam)] = 1
    tabul_in[ind2d(2, 3, tam)] = 1
    tabul_in[ind2d(3, 1, tam)] = 1
    tabul_in[ind2d(3, 2, tam)] = 1
    tabul_in[ind2d(3, 3, tam)] = 1
    return tabul_in, tabul_out

def correto(tabul, tam):
    cnt = sum(tabul)
    return cnt == 5 and tabul[ind2d(tam - 2, tam - 1, tam)] and \
           tabul[ind2d(tam - 1, tam, tam)] and \
           tabul[ind2d(tam, tam - 2, tam)] and \
           tabul[ind2d(tam, tam - 1, tam)] and \
           tabul[ind2d(tam, tam, tam)]

def main():
    sc = SparkContext(appName="GameOfLife")
    if len(sys.argv) < 3:
        print("Falha nos argumentos")
        sys.exit(1)
        
    powmin = int(sys.argv[1])
    powmax = int(sys.argv[2])
    print(f"\nValores recebidos no Spark: {powmin} e {powmax}\n")

    for pow in range(powmin, powmax + 1):
        tam = 1 << pow

        t0 = time.time()
        tabul_in, tabul_out = init_tabul(tam)
        t1 = time.time()

        iterations = 2 * (tam - 3)
        for _ in range(iterations):
            broadcasted_tabul_in = sc.broadcast(tabul_in)
            rdd = sc.parallelize(range(1, tam + 1))
            rdd.foreach(lambda i: uma_vida((broadcasted_tabul_in.value, tabul_out, tam, i)))
            tabul_in, tabul_out = tabul_out, tabul_in

        t2 = time.time()

        is_correct = correto(tabul_in, tam)
        global_is_correct = sc.parallelize([is_correct]).reduce(lambda x, y: x and y)

        if sc.getConf().get('spark.driver.host') == 'localhost':
            if global_is_correct:
                print("**Ok, RESULTADO CORRETO**")
            else:
                print("**Nok, RESULTADO ERRADO**")

        t3 = time.time()

        print("----------------------RESULTADO---------------------------")
        print("tam=%d; tempos: init=%7.7f, comp=%7.7f, fim=%7.7f, tot=%7.7f" %
              (tam, t1 - t0, t2 - t1, t3 - t2, t3 - t0))
        print("\n")

    sc.stop()

if __name__ == "__main__":
    main()
