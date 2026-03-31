def get_levenshtein_distance(A, B, cost_rep=1, cost_ins=1, cost_del=1,
                             spec_rep_char=None, spec_rep_cost=None,
                             spec_del_char=None, spec_del_cost=None,
                             return_transcript=False):
    def get_del_cost(char):
        if spec_del_char is not None and char == spec_del_char:
            return spec_del_cost
        return cost_del

    def get_rep_cost(char_from, char_to):
        if char_from == char_to:
            return 0
        if spec_rep_char is not None and char_to == spec_rep_char:
            return spec_rep_cost
        return cost_rep

    def get_ins_cost(char):
        return cost_ins

    n, m = len(A), len(B)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    with open("log.txt", "w", encoding="utf-8") as log_file:
        def log(text):
            log_file.write(text + "\n")

        def log_matrix():
            header = "      " + " ".join(f"{ch:>3}" for ch in B)
            log(header)

            for r in range(n + 1):
                row_char = " " if r == 0 else A[r - 1]
                row_vals = " ".join(f"{dp[r][c]:>3}" for c in range(m + 1))
                log(f"{row_char} {row_vals}")
            log("")

        log(f"Начало вычисления расстояния Левенштейна.")
        log(f"Исходная строка: '{A}' (длина {n})")
        log(f"Целевая строка: '{B}' (длина {m})\n")

        # Инициализация базовых случаев
        log("--- Инициализация нулевого столбца ---")
        for i in range(1, n + 1):
            cost = get_del_cost(A[i - 1])
            dp[i][0] = dp[i - 1][0] + cost
            log(f"dp[{i}][0] = {dp[i][0]} (Удаление '{A[i - 1]}', стоимость: {cost})")

        log("\nМатрица после инициализации нулевого столбца:")
        log_matrix()

        log("--- Инициализация нулевой строки ---")
        for j in range(1, m + 1):
            cost = get_ins_cost(B[j - 1])
            dp[0][j] = dp[0][j - 1] + cost
            log(f"dp[0][{j}] = {dp[0][j]} (Вставка '{B[j - 1]}', стоимость: {cost})")

        log("\nМатрица после инициализации нулевой строки:")
        log_matrix()

        log("--- Заполнение основной таблицы ДП ---")
        # Заполнение таблицы ДП
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                del_cost_total = dp[i - 1][j] + get_del_cost(A[i - 1])
                ins_cost_total = dp[i][j - 1] + get_ins_cost(B[j - 1])  # Вставка
                rep_cost_total = dp[i - 1][j - 1] + get_rep_cost(A[i - 1], B[j - 1])  # Замена (или совпадение)

                dp[i][j] = min(del_cost_total, ins_cost_total, rep_cost_total)

                log(f"---")
                log(f"Клетка [{i}][{j}] | Сравниваем '{A[i - 1]}' и '{B[j - 1]}':")
                log(f"  1. Удаление '{A[i - 1]}': {dp[i - 1][j]} + {get_del_cost(A[i - 1])} = {del_cost_total}")
                log(f"  2. Вставка '{B[j - 1]}': {dp[i][j - 1]} + {get_ins_cost(B[j - 1])} = {ins_cost_total}")
                log(f"  3. Замена/Совпадение: {dp[i - 1][j - 1]} + {get_rep_cost(A[i - 1], B[j - 1])} = {rep_cost_total}")
                log(f"  Минимум для dp[{i}][{j}]: {dp[i][j]}")
                log(f"Текущая матрица:")
                log_matrix()

        log(f"Итоговое расстояние Левенштейна: {dp[n][m]}")

    if not return_transcript:
        return dp[n][m]

    # Восстановление пути
    ops = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + get_rep_cost(A[i - 1], B[j - 1]):
            ops.append('M' if A[i - 1] == B[j - 1] else 'R')
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + get_del_cost(A[i - 1]):
            ops.append('D')
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + get_ins_cost(B[j - 1]):
            ops.append('I')
            j -= 1

    ops.reverse()
    return dp[n][m], "".join(ops)


if __name__ == "__main__":
    A = input("Строка 1: ").strip()
    B = input("Строка 2: ").strip()

    cost_ins = int(input("Цена вставки: "))
    cost_del = int(input("Цена удаления: "))
    cost_rep = int(input("Цена замены: "))

    spec_rep_char = input("Особый заменитель: ").strip()
    spec_rep_cost = int(input(f"Цена замены на символ '{spec_rep_char}': "))

    spec_del_char = input("Особо удаляемый символ: ").strip()
    spec_del_cost = int(input(f"Цена удаления символа '{spec_del_char}': "))

    ans = get_levenshtein_distance(
        A, B,
        cost_rep=cost_rep,
        cost_ins=cost_ins,
        cost_del=cost_del,
        spec_rep_char=spec_rep_char,
        spec_rep_cost=spec_rep_cost,
        spec_del_char=spec_del_char,
        spec_del_cost=spec_del_cost
    )

    print(f"Ответ: {ans}")
    print("Подробный процесс вычислений сохранен в файл 'log.txt'.")
