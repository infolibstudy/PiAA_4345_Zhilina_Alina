import heapq

USE_PRECISE_ALGORITHM = True
USE_FILE_INPUT = True


def log_to_file(text):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(str(text) + "\n")


# Функция для поиска приближенного решения (АВБГ "улучшенный")
def get_improved_nearest_insertion(cost, N):
    log_to_file(f"\n[АВБГ] Запуск алгоритма поиска приближенного решения, N={N}")
    if N <= 1:
        log_to_file("[АВБГ] N <= 1, возвращаем 0, [0]")
        return 0, [0]

    # Инициализация начального маршрута и массива посещений
    path = [0]
    vis = [False] * N
    vis[0] = True
    log_to_file("[АВБГ] Инициализация: начальный путь=[0]")

    # Шаг 1: Формируем стартовый цикл из двух вершин
    best_k = -1
    min_c = float('inf')

    # Перебираем все города для поиска ближайшего к стартовому
    log_to_file("[АВБГ] Шаг 1: Поиск ближайшего города к стартовому (0)")
    for k in range(1, N):
        c = cost[0][k] + cost[k][0]
        log_to_file(
            f"[АВБГ]   Проверка города {k}: c = cost[0][{k}] + cost[{k}][0] = {cost[0][k]} + {cost[k][0]} = {c}")
        if c < min_c:
            log_to_file(f"[АВБГ]   --> Найдено новое минимальное c: {c} < {min_c}. Выбираем {k}")
            min_c = c
            best_k = k

    # Добавляем найденный город в начальный маршрут
    path.append(best_k)
    vis[best_k] = True
    log_to_file(f"[АВБГ] В начальный маршрут добавлен город {best_k}. Текущий путь: {path}")

    # Шаг 2: Вставляем остальные вершины, минимизируя прирост стоимости
    log_to_file("[АВБГ] Шаг 2: Вставка остальных вершин")
    for _ in range(2, N):
        best_k = -1
        best_insert_idx = -1
        min_delta = float('inf')
        log_to_file(f"[АВБГ] Итерация вставки. Текущий путь: {path}")

        # Пропускаем города, которые уже включены в цикл
        for k in range(N):
            if vis[k]:
                continue

            log_to_file(f"[АВБГ]   Оценка вставки непосещенного города {k}:")
            # Проверяем каждую позицию в текущем цикле для вставки
            for i in range(len(path)):
                u = path[i]
                v = path[(i + 1) % len(path)]
                delta = cost[u][k] + cost[k][v] - cost[u][v]
                log_to_file(
                    f"[АВБГ]     Позиция между {u} и {v}: delta = cost[{u}][{k}] + cost[{k}][{v}] - cost[{u}][{v}] = {cost[u][k]} + {cost[k][v]} - {cost[u][v]} = {delta}")

                # Сохраняем лучшую позицию, дающую минимальный прирост пути
                if delta < min_delta:
                    log_to_file(f"[АВБГ]     --> Найдена лучшая позиция! min_delta обновлена: {min_delta} -> {delta}")
                    min_delta = delta
                    best_k = k
                    best_insert_idx = i + 1

        # Вставляем выбранный город в оптимальную позицию маршрута
        path.insert(best_insert_idx, best_k)
        vis[best_k] = True
        log_to_file(f"[АВБГ] Город {best_k} вставлен на позицию {best_insert_idx}. Новый путь: {path}")

    # Подсчет финальной стоимости построенного пути
    total_cost = 0
    log_to_file("[АВБГ] Подсчет финальной стоимости построенного пути:")
    for i in range(len(path)):
        u = path[i]
        v = path[(i + 1) % len(path)]
        w = cost[u][v]
        log_to_file(f"[АВБГ]   Ребро {u} -> {v}, вес {w}. total_cost = {total_cost} + {w} = {total_cost + w}")
        total_cost += w

    log_to_file(f"[АВБГ] Итог АВБГ: стоимость = {total_cost}, путь = {path}\n")
    return total_cost, path


# Оценка 1: Полусумма весов двух легчайших ребер для каждого куска
def calc_LB1(num_pieces, get_cost):
    log_to_file(f"[LB1] Запуск вычисления LB1 для {num_pieces} кусков")
    lb1_sum = 0

    for i in range(num_pieces):
        log_to_file(f"[LB1]   Обработка куска i={i}:")
        min_in, min2_in, arg_in = float('inf'), float('inf'), -1
        min_out, min2_out, arg_out = float('inf'), float('inf'), -1

        # Поиск минимального и второго минимального входящего ребра
        for j in range(num_pieces):
            if i == j: continue

            c_in = get_cost(j, i)
            log_to_file(f"[LB1]     Проверка входящего ребра {j} -> {i}: вес {c_in}")
            if c_in < min_in:
                min2_in = min_in
                min_in = c_in
                arg_in = j
                log_to_file(f"[LB1]       Обновление: min_in={min_in} (из {arg_in}), min2_in={min2_in}")
            elif c_in < min2_in:
                min2_in = c_in
                log_to_file(f"[LB1]       Обновление: min2_in={min2_in}")

            # Поиск минимального и второго минимального исходящего ребра
            c_out = get_cost(i, j)
            log_to_file(f"[LB1]     Проверка исходящего ребра {i} -> {j}: вес {c_out}")
            if c_out < min_out:
                min2_out = min_out
                min_out = c_out
                arg_out = j
                log_to_file(f"[LB1]       Обновление: min_out={min_out} (в {arg_out}), min2_out={min2_out}")
            elif c_out < min2_out:
                min2_out = c_out
                log_to_file(f"[LB1]       Обновление: min2_out={min2_out}")

        log_to_file(
            f"[LB1]   Итоги для куска {i}: min_in={min_in} (от {arg_in}), min2_in={min2_in} | min_out={min_out} (к {arg_out}), min2_out={min2_out}")
        # Прибавление весов с учетом возможного совпадения компонентов
        if arg_in == arg_out and arg_in != -1:
            val1 = min_in + min2_out
            val2 = min2_in + min_out
            added_val = min(val1, val2)
            log_to_file(
                f"[LB1]   Совпадение arg_in и arg_out ({arg_in}). Считаем: min({min_in} + {min2_out}, {min2_in} + {min_out}) = min({val1}, {val2}) = {added_val}")
            lb1_sum += added_val
        else:
            added_val = min_in + min_out
            log_to_file(f"[LB1]   Разные источники. Считаем: min_in + min_out = {min_in} + {min_out} = {added_val}")
            lb1_sum += added_val

        log_to_file(f"[LB1]   Текущая сумма lb1_sum = {lb1_sum}")

    # Округление полусуммы весов вверх
    result = (lb1_sum + 1) // 2
    log_to_file(f"[LB1] Итоговая сумма {lb1_sum}. Возвращаем ({lb1_sum} + 1) // 2 = {result}")
    return result


# Оценка 2: Минимальное Остовное Дерево (МОД) на кусках
def calc_LB2(num_pieces, get_cost):
    log_to_file(f"[LB2] Запуск вычисления LB2 (МОД) для {num_pieces} кусков")
    LB2 = 0

    # Подготовка структур для алгоритма Прима (построение МОД)
    min_e = [float('inf')] * num_pieces
    in_mst = [False] * num_pieces
    min_e[0] = 0

    # Выбор непосещенной вершины с минимальным весом присоединения
    for _ in range(num_pieces):
        v = -1
        for j in range(num_pieces):
            if not in_mst[j] and (v == -1 or min_e[j] < min_e[v]):
                v = j

        if min_e[v] == float('inf'):
            log_to_file("[LB2] Обнаружена недостижимая вершина (inf), прерывание цикла МОД")
            break

        # Пометка вершины как посещенной и добавление веса в оценку
        in_mst[v] = True
        old_LB2 = LB2
        LB2 += min_e[v]
        log_to_file(f"[LB2]   Выбрана вершина v={v} с мин. ребром {min_e[v]}. LB2 = {old_LB2} + {min_e[v]} = {LB2}")

        # Обновление минимальных расстояний от дерева до оставшихся вершин
        for to in range(num_pieces):
            if not in_mst[to]:
                c = min(get_cost(v, to), get_cost(to, v))
                if c < min_e[to]:
                    log_to_file(f"[LB2]     Обновление расстояния до {to}: min_e[{to}] снижено с {min_e[to]} до {c}")
                    min_e[to] = c

    log_to_file(f"[LB2] Итоговое значение LB2 = {LB2}")
    return LB2


# Главная функция вычисления нижней оценки L
def calc_L(path, cost, N):
    log_to_file(f"\n[L] Вычисление L для пути: {path}")
    # Если маршрут уже полный, возвращаем стоимость замыкающего ребра
    if len(path) == N:
        close_edge = cost[path[-1]][path[0]]
        log_to_file(
            f"[L] Маршрут полный. Замыкающее ребро {path[-1]} -> {path[0]} имеет вес {close_edge}. Возвращаем {close_edge}.")
        return close_edge

    # Для предпоследнего шага просто добавляем единственный оставшийся город
    if len(path) == N - 1:
        vis = set(path)
        missing = -1
        for i in range(N):
            if i not in vis:
                missing = i
                break
        c1 = cost[path[-1]][missing]
        c2 = cost[missing][path[0]]
        res = c1 + c2
        log_to_file(
            f"[L] Маршрут без одной вершины ({missing}). Возвращаем {path[-1]}->{missing} ({c1}) + {missing}->{path[0]} ({c2}) = {res}")
        return res

    # Формируем список еще не посещенных вершин (свободных кусков)
    vis = set(path)
    U = [i for i in range(N) if i not in vis]
    log_to_file(f"[L] Свободные вершины (U): {U}")

    # Количество независимых компонентов (текущий путь + свободные вершины)
    num_pieces = len(U) + 1
    log_to_file(f"[L] Количество независимых компонентов: {num_pieces}")

    # Функция определения расстояний между различными компонентами графа
    def get_cost(a, b):
        if a == b: return float('inf')
        if a == 0: return cost[path[-1]][U[b - 1]]
        if b == 0: return cost[U[a - 1]][path[0]]
        return cost[U[a - 1]][U[b - 1]]

    # Вычисление двух оценок с помощью вынесенных функций
    LB1 = calc_LB1(num_pieces, get_cost)
    LB2 = calc_LB2(num_pieces, get_cost)

    # Возврат наибольшей из двух нижних оценок
    final_L = max(LB1, LB2)
    log_to_file(f"[L] max(LB1={LB1}, LB2={LB2}) = {final_L}. Возвращаем {final_L}")
    return final_L


# Функция метода ветвей и границ (МВиГ)
def solve_branch_and_bound(cost, N):
    # Инициализируем рекорд приближенным решением
    UB, best_path = get_improved_nearest_insertion(cost, N)

    log_to_file("\n=== ЗАПУСК МЕТОДА ВЕТВЕЙ И ГРАНИЦ ===")
    log_to_file(f"[МВиГ] Начальный UB (рекорд) = {UB}, начальный лучший путь = {best_path}")

    # Приоритетная очередь
    pq = []

    # Вычисление оценки для стартового города и инициализация очереди
    initial_L = calc_L([0], cost, N)
    log_to_file(f"[МВиГ] Стартовая оценка initial_L = {initial_L}")

    # Формат кортежа: (bound, path, S).
    # Обеспечивает сортировку по bound, затем лексикографически по пути
    heapq.heappush(pq, (initial_L, [0], 0))
    log_to_file(f"[МВиГ] В очередь помещен стартовый узел: bound={initial_L}, path=[0], S=0")

    iteration_count = 0
    # Основной цикл метода ветвей и границ
    while pq:
        iteration_count += 1
        log_to_file(f"\n[МВиГ] --- Итерация {iteration_count} ---")
        log_to_file(f"[МВиГ] Длина очереди (heapq): {len(pq)}")

        # Вывод первых 5 элементов очереди
        top_5 = pq[:5]
        log_to_file(f"[МВиГ] Первые элементы очереди:")
        for idx, item in enumerate(top_5):
            log_to_file(f"       {idx + 1}: bound={item[0]}, path={item[1]}, S={item[2]}")

        # Извлечение самого перспективного узла из очереди
        curr_bound, curr_path, curr_S = heapq.heappop(pq)
        log_to_file(f"[МВиГ] Извлечен узел: bound={curr_bound}, path={curr_path}, текущая стоимость S={curr_S}")

        # Отсечение ветви: если оценка хуже рекорда, дальше не идем
        if curr_bound > UB:
            log_to_file(f"[МВиГ] Отсечение! curr_bound ({curr_bound}) > UB ({UB}). Завершаем или пропускаем ветвь.")
            break

        # Если все города посещены, проверяем замыкание маршрута
        if len(curr_path) == N:
            close_cost = cost[curr_path[-1]][curr_path[0]]
            full_cost = curr_S + close_cost
            log_to_file(
                f"[МВиГ] Найден полный маршрут. full_cost = S ({curr_S}) + замыкание {curr_path[-1]}->{curr_path[0]} ({close_cost}) = {full_cost}")

            # Проверка на улучшение текущего рекорда
            if full_cost < UB:
                log_to_file(
                    f"[МВиГ] !!! Обновление рекорда !!! Старый UB={UB}, новый UB={full_cost}. Новый лучший путь: {curr_path}")
                UB = full_cost
                best_path = curr_path

            # Сохранение лексикографически меньшего пути при равной стоимости
            elif full_cost == UB and curr_path < best_path:
                log_to_file(
                    f"[МВиГ] Стоимость равна текущему рекорду ({UB}), но путь лексикографически меньше. Обновляем лучший путь: {curr_path}")
                best_path = curr_path
            else:
                log_to_file(f"[МВиГ] Маршрут не улучшает текущий рекорд ({UB}).")
            continue

        # Подготовка множества посещенных вершин для текущего узла
        vis = set(curr_path)
        last_v = curr_path[-1]
        log_to_file(f"[МВиГ] Ветвление из вершины {last_v}. Посещенные вершины: {vis}")

        # Генерация новых ветвей для каждого доступного города
        for nxt in range(N):
            if nxt not in vis:
                log_to_file(f"[МВиГ]   Рассматриваем переход {last_v} -> {nxt}:")
                # Формирование нового пути, расчет стоимости и оценки L
                edge_cost = cost[last_v][nxt]
                new_S = curr_S + edge_cost
                log_to_file(f"[МВиГ]     Новая стоимость new_S = {curr_S} + {edge_cost} = {new_S}")

                new_path = curr_path + [nxt]
                new_L = calc_L(new_path, cost, N)
                new_bound = new_S + new_L
                log_to_file(
                    f"[МВиГ]     Оценка для {new_path}: new_bound = new_S ({new_S}) + new_L ({new_L}) = {new_bound}")

                # Добавляем только если есть шанс улучшить рекорд
                if new_bound <= UB:
                    log_to_file(f"[МВиГ]     --> Успешно! {new_bound} <= UB ({UB}). Добавляем в очередь.")
                    heapq.heappush(pq, (new_bound, new_path, new_S))
                else:
                    log_to_file(f"[МВиГ]     --> Отсев! {new_bound} > UB ({UB}). Переход проигнорирован.")

    log_to_file(f"\n=== ЗАВЕРШЕНИЕ МВиГ. Итоговый UB={UB}, путь={best_path} ===")
    # Возврат оптимальной стоимости и маршрута
    return UB, best_path


def main():
    # Инициализация (очистка) файла логов
    with open("log.txt", "w", encoding="utf-8") as f:
        f.write("\n")

    if USE_FILE_INPUT:
        with open("matrix.txt", "r", encoding="utf-8") as f:
            lines = f.read().split()
            if not lines:
                log_to_file("Ошибка: файл пуст")
                return
            N = int(lines[0])
            values = [int(x) for x in lines[1:]]
            cost = [values[i * N : (i + 1) * N] for i in range(N)]
    else:
        # Считывание всех входных данных из стандартного потока
        N = int(input())
        cost = [[int(i) for i in input().split()] for _ in range(N)]

    log_to_file(f"Считано {N=}")
    log_to_file(f"Матрица стоимостей: {cost}")

    if USE_PRECISE_ALGORITHM:
        # Запуск метода ветвей и границ
        UB, best_path = solve_branch_and_bound(cost, N)
    else:
        # Запуск АВБГ "улучшенный"
        UB, best_path = get_improved_nearest_insertion(cost, N)

    # Форматированный вывод оптимального маршрута и его стоимости
    print(" ".join(map(str, best_path)))
    print(f"{UB}.0")

if __name__ == '__main__':
    main()
