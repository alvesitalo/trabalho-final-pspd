from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, when

def init_spark():
    return SparkSession.builder.appName("GameOfLifeSpark").getOrCreate()

def UmaVidaSpark(tabul, tam):
    # Create a DataFrame from the tabulIn array
    spark = init_spark()
    df = spark.createDataFrame(tabul, schema=["cell"])

    # Calculate the neighbors' sum for each cell
    df = df.withColumn("i", (col("cell") - 1) // tam + 1)
    df = df.withColumn("j", (col("cell") - 1) % tam + 1)

    neighbor_indices = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for di, dj in neighborindices:
        df = df.withColumn(f"neighbor{di}{dj}", col("cell") + di * tam + dj)

    df = df.withColumn("vizviv", sum(when(col(f"neighbor{di}_{dj}") > 0, 1).otherwise(0) for di, dj in neighbor_indices))

    # Apply the Game of Life rules using DataFrame operations
    df = df.withColumn(
        "tabulOut",
        when((col("cell") == 1) & (col("vizviv") < 2), 0)
        .when((col("cell") == 1) & (col("vizviv") > 3), 0)
        .when((col("cell") == 0) & (col("vizviv") == 3), 1)
        .otherwise(col("cell"))
    )

    # Convert the DataFrame back to a tabulOut array
    tabulOut = df.select("tabulOut").rdd.flatMap(lambda x: x).collect()
    return tabulOut

def main():
    POWMIN = 3
    POWMAX = 10

    for pow in range(POWMIN, POWMAX + 1):
        tam = 1 << pow

        # Allocate and initialize tabulIn and tabulOut arrays
        tabulIn = [0] * ((tam + 2) * (tam + 2))
        tabulOut = [0] * ((tam + 2) * (tam + 2))
        tabulIn[ind2d(1, 2)] = 1
        tabulIn[ind2d(2, 3)] = 1
        tabulIn[ind2d(3, 1)] = 1
        tabulIn[ind2d(3, 2)] = 1
        tabulIn[ind2d(3, 3)] = 1

        t0 = wall_time()
        for i in range(2 * (tam - 3)):
            tabulOut = UmaVidaSpark(tabulIn, tam)
            tabulIn = UmaVidaSpark(tabulOut, tam)
        t1 = wall_time()

        if Correto(tabulIn, tam):
            print("Ok, RESULTADO CORRETO")
        else:
            print("Nok, RESULTADO ERRADO")
        t2 = wall_time()

        print(
            f"tam={tam}; tempos: init={t1-t0:.7f}, comp={t2-t1:.7f}, fim={t2-t0:.7f}, tot={t2-t0:.7f}"
        )

if name == "main":
    main()
