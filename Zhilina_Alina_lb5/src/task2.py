from collections import deque

# Очистка лог-файла перед началом работы
with open("log_2.txt", "w", encoding="utf-8") as f:
    f.write("[ИНИЦИАЛИЗАЦИЯ] Запуск алгоритма Ахо-Корасик\n")
    f.write("=" * 70 + "\n")


def write_log(msg):
    with open("log_2.txt", "a", encoding="utf-8") as f:
        f.write(msg + "\n")


# Фиксированный алфавит и размер словаря
CHAR_TO_INDEX = {'A': 0, 'C': 1, 'G': 2, 'T': 3, 'N': 4}
INDEX_TO_CHAR = {0: 'A', 1: 'C', 2: 'G', 3: 'T', 4: 'N'}
ALPHABET_LENGTH = 5


class TrieNode:
    _id_counter = 0  # Глобальный счетчик для нумерации узлов в логах

    def __init__(self):
        self.id = TrieNode._id_counter
        TrieNode._id_counter += 1

        # Переходы к дочерним узлам для каждого символа алфавита
        self.transitions = [None] * ALPHABET_LENGTH
        self.suffix_link = None
        self.terminal_link = None

        # Идентификаторы шаблонов и счетчики длин цепочек
        self.patterns = []
        self.suffix_chain = 0
        self.terminal_chain = 0


class AhoCorasick:
    def __init__(self):
        TrieNode._id_counter = 0
        self.root = TrieNode()
        self.max_suffix_chain = 0
        self.max_terminal_chain = 0

        # Сохраняем все узлы для удобного вывода состояния автомата в лог
        self.all_nodes = [self.root]

    def add_pattern(self, pattern, pattern_id):
        curr = self.root
        write_log(f"\n[ПОСТРОЕНИЕ БОРА] Вставка шаблона: '{pattern}'. ID: {pattern_id[0]}, Длина: {pattern_id[1]}")
        prefix = ""

        # Спускаемся по дереву, создавая узлы при необходимости
        for char in pattern:
            idx = CHAR_TO_INDEX[char]
            prefix += char

            if curr.transitions[idx] is None:
                curr.transitions[idx] = TrieNode()
                self.all_nodes.append(curr.transitions[idx])
                write_log(
                    f"  -- Символ '{char}' (префикс '{prefix}'): перехода из узла {curr.id} нет. Создан новый узел {curr.transitions[idx].id}. Переходим в него.")
            else:
                write_log(
                    f"  -- Символ '{char}' (префикс '{prefix}'): переход из узла {curr.id} уже существует. Переходим в узел {curr.transitions[idx].id}.")
            curr = curr.transitions[idx]

        # Добавляем шаблон в список patterns его конечного узла
        curr.patterns.append(pattern_id)
        write_log(f"  -> Конец шаблона '{pattern}' сохранён в узле {curr.id}.")

    def build_automaton(self):
        write_log("\n" + "=" * 70)
        write_log("[ПОСТРОЕНИЕ АВТОМАТА] Шаг 1: Инициализация первого уровня")
        write_log("=" * 70)

        queue = deque()
        self.root.suffix_link = self.root
        write_log("  -- Суффиксная ссылка корня (узел 0) замкнута на себя (узел 0).")

        # Инициализируем первый уровень, связывая его с корнем
        for i in range(ALPHABET_LENGTH):
            child = self.root.transitions[i]
            char = INDEX_TO_CHAR[i]
            if child is not None:
                child.suffix_link = self.root
                child.suffix_chain = 1
                self.max_suffix_chain = max(self.max_suffix_chain, 1)
                queue.append(child)
                write_log(
                    f"  -- Прямой потомок корня: узел {child.id} (по символу '{char}'). Суф. ссылка направлена на корень (0). Узел добавлен в очередь.")
            else:
                self.root.transitions[i] = self.root
                write_log(f"  -- Отсутствует переход из корня по '{char}'. Замыкаем переход на корень (0).")

        write_log("\n" + "=" * 70)
        write_log("[ПОСТРОЕНИЕ АВТОМАТА] Шаг 2: Обход в ширину (BFS) для остальных уровней")
        write_log("=" * 70)

        # Строим ссылки через BFS для корректной обработки суффиксов
        while queue:
            curr = queue.popleft()
            write_log(f"\n  [ОБРАБОТКА УЗЛА {curr.id}] (суф. ссылка указывает на узел {curr.suffix_link.id})")

            # Устанавливаем терминальную ссылку для быстрого поиска вхождений
            if curr.suffix_link.patterns:
                curr.terminal_link = curr.suffix_link
                curr.terminal_chain = curr.suffix_link.terminal_chain + 1
                write_log(
                    f"    -- Терминальная ссылка: суффиксная ссылка (узел {curr.suffix_link.id}) является концом шаблона. Устанавливаем терм. ссылку {curr.id} -> {curr.suffix_link.id}.")
            else:
                curr.terminal_link = curr.suffix_link.terminal_link
                curr.terminal_chain = curr.suffix_link.terminal_chain
                if curr.terminal_link:
                    write_log(
                        f"    -- Терминальная ссылка: унаследована от суф. ссылки (узла {curr.suffix_link.id}). Направлена на узел {curr.terminal_link.id}.")
                else:
                    write_log(
                        f"    -- Терминальная ссылка: отсутствует (суффиксная ссылка не ведет к концу шаблона и не имеет своей терм. ссылки).")

            self.max_terminal_chain = max(self.max_terminal_chain, curr.terminal_chain)

            # Настраиваем переходы и суффиксные ссылки для потомков
            for i in range(ALPHABET_LENGTH):
                child = curr.transitions[i]
                char = INDEX_TO_CHAR[i]

                if child is not None:
                    # Суффиксная ссылка указывает на переход родителя
                    child.suffix_link = curr.suffix_link.transitions[i]
                    child.suffix_chain = child.suffix_link.suffix_chain + 1
                    self.max_suffix_chain = max(self.max_suffix_chain, child.suffix_chain)
                    queue.append(child)
                    write_log(
                        f"    -- Найден потомок по '{char}' (узел {child.id}). Переход из суф. ссылки родителя (узла {curr.suffix_link.id}) по '{char}' ведет в узел {curr.suffix_link.transitions[i].id}. Устанавливаем суф. ссылку {child.id} -> {child.suffix_link.id}. Узел добавлен в очередь.")
                else:
                    # Оптимизируем переходы, перенаправляя их через суффиксную ссылку
                    curr.transitions[i] = curr.suffix_link.transitions[i]
                    write_log(
                        f"    -- Отсутствует прямой переход по '{char}'. Достраиваем граф переходов автомата: перенаправляем по суф. ссылке в узел {curr.transitions[i].id}.")

        self._log_automaton_state()

    def _log_automaton_state(self):
        write_log("\n" + "=" * 70)
        write_log("[СОСТОЯНИЕ ИТОГОВОГО АВТОМАТА]")
        write_log("=" * 70)
        for node in self.all_nodes:
            trans = ", ".join([f"'{INDEX_TO_CHAR[i]}':{t.id if t else '0'}" for i, t in enumerate(node.transitions)])
            suflink = node.suffix_link.id if node.suffix_link else "None"
            termlink = node.terminal_link.id if node.terminal_link else "None"
            write_log(
                f" Узел {node.id:02d} | Суф. ссылка: {suflink:>4} | Терм. ссылка: {termlink:>4} | Шаблоны: {node.patterns}")
            write_log(f"         | Переходы: {trans}")
        write_log("=" * 70 + "\n")

    def search(self, text):
        write_log(f"[ПОИСК] Старт обхода текста: '{text}'\n")
        curr = self.root

        # Сканируем текст, переходя по узлам автомата
        for i, char in enumerate(text):
            if char not in CHAR_TO_INDEX:
                write_log(f"  -- Шаг {i}: символ '{char}' вне алфавита, игнорируем.")
                continue

            idx = CHAR_TO_INDEX[char]
            next_node = curr.transitions[idx]
            write_log(f"  -- Шаг {i}: считываем '{char}'. Переход: узел {curr.id} -> узел {next_node.id}")
            curr = next_node

            # Сообщаем о шаблонах, найденных непосредственно в этом узле
            if curr.patterns:
                for pid in curr.patterns:
                    write_log(f"    -> [СОВПАДЕНИЕ] Конец шаблона {pid[0]} обнаружен прямо в текущем узле {curr.id}.")
                    yield (i, pid)

            # Проходим по цепочке терминальных ссылок для поиска вложенных шаблонов
            term_node = curr.terminal_link
            if term_node is not None:
                write_log(
                    f"    -> [ПРОВЕРКА] Обнаружена терминальная ссылка на узел {term_node.id}. Спуск для проверки вложенных подстрок...")

            while term_node is not None:
                for pid in term_node.patterns:
                    write_log(
                        f"      -> [ВЛОЖЕННОЕ СОВПАДЕНИЕ] Шаблон {pid[0]} извлечен из терминального узла {term_node.id}.")
                    yield (i, pid)
                term_node = term_node.terminal_link

        write_log("\n[ЗАВЕРШЕНИЕ] Конец текста достигнут.")



# Считываем входные данные
text = input()
pattern = input()
wildcard = input()

ac = AhoCorasick()

total_pattern_pieces = 0
chars_processed = 0

write_log("\n[ПРЕДОБРАБОТКА ШАБЛОНА] Разбиение по символу джокера")
# Разбиваем шаблон на подстроки без масок, сохраняя их стартовые позиции
for piece in pattern.split(wildcard):
    if piece:
        piece_start_pos = chars_processed + 1
        ac.add_pattern(piece, (piece_start_pos, len(piece)))
        total_pattern_pieces += 1
        write_log(f"  -- Выделена подстрока: '{piece}'. Позиция в шаблоне: {piece_start_pos}, Длина: {len(piece)}")
    else:
        write_log("  -- Пропуск пустого блока (подряд идущие джокеры или джокер с краю).")
    chars_processed += len(piece) + 1

write_log(f"  -> Итого выделено значащих подстрок: {total_pattern_pieces}")

# Строим автомат для поиска подстрок
ac.build_automaton()

# Массив, где индекс — потенциальная стартовая позиция шаблона в тексте,
# а значение — количество совпавших частей без масок
matched_pieces_count = [0] * (len(text) + 2)

write_log("\n" + "=" * 70)
write_log("[ОБРАБОТКА РЕЗУЛЬТАТОВ ПОИСКА] Подсчет совпадений для потенциальных стартовых позиций")
write_log("=" * 70)

# Ищем вхождения всех подстрок без масок
for end_pos, (piece_start_in_pattern, piece_length) in ac.search(text):
    found_piece_start_in_text = end_pos - piece_length + 2
    candidate_pattern_start = found_piece_start_in_text - piece_start_in_pattern + 1

    # Если потенциальное начало шаблона попадает в допустимые границы текста
    if 1 <= candidate_pattern_start < len(matched_pieces_count):
        matched_pieces_count[candidate_pattern_start] += 1
        write_log(f"  -- Найдена подстрока (стартовая позиция в шаблоне {piece_start_in_pattern}). "
                  f"Ожидаемое начало всего шаблона в тексте: {candidate_pattern_start}. "
                  f"Счетчик для позиции {candidate_pattern_start} увеличен до {matched_pieces_count[candidate_pattern_start]}.")
    else:
        write_log(f"  -- Найдена подстрока (стартовая позиция в шаблоне {piece_start_in_pattern}), но "
                  f"ожидаемое начало всего шаблона ({candidate_pattern_start}) выходит за границы допустимого. Игнорируем.")

write_log("\n" + "=" * 70)
write_log(f"[ФОРМИРОВАНИЕ ОТВЕТА] Отбор позиций, где совпали все {total_pattern_pieces} подстрок")
write_log("=" * 70)

# Выводим позиции, где количество совпавших подстрок равно общему количеству кусков
# Ограничиваемся только теми позициями, где шаблон физически влезает в текст
valid_max_start = len(text) - len(pattern) + 2
for start_idx in range(1, valid_max_start):
    if matched_pieces_count[start_idx] == total_pattern_pieces:
        write_log(f"  -> [УСПЕХ] Позиция {start_idx}: совпали все подстроки. Добавлена в итоговый ответ.")
        print(start_idx)
    elif matched_pieces_count[start_idx] > 0:
        write_log(f"  -- Позиция {start_idx}: совпало подстрок {matched_pieces_count[start_idx]} из {total_pattern_pieces}. Не подходит.")

print(f"Длина самой длинной цепочки из суффиксных ссылок: {ac.max_suffix_chain}")
print(f"Длина самой длинной цепочки из терминальных ссылок: {ac.max_terminal_chain}")
