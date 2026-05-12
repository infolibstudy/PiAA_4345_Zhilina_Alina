import random


def main():
    n = int(input("Размер матрицы N: "))
    is_symmetric = input("Сделать матрицу симметричной? (y/n): ").strip().lower()[0] == "y"


    matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 0
            elif is_symmetric and i > j:
                matrix[i][j] = matrix[j][i]
            elif i < j or not is_symmetric:
                matrix[i][j] = random.randint(1, 100)

    filename = "matrix.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{n}\n")
        for row in matrix:
            f.write(" ".join(map(str, row)) + "\n")

    print(f"Матрица успешно сгенерирована и сохранена в {filename}.")


if __name__ == '__main__':
    main()
