#include <iostream>
#include <vector>
#include <fstream>
#include <string>

using namespace std;

// Структура для хранения информации о квадрате
struct Square {
    int x, y, size;
};

int N;
int board[40][40]; // Двумерный массив (доска)
int LIMIT;
vector<Square> current_solution;
vector<Square> best_solution;

// Файл логов
ofstream log_file;


// Рекурсивная функция поиска
bool solve(int current_count, int filled_area) {
    string ind = string(current_count * 4, ' ');
    log_file << ind << "--> [ВХОД] Уровень: " << current_count << " | Заполненная площадь: " << filled_area << "/" << N * N << "\n";

    // Вся площадь столешницы заполнена, ответ найден
    if (filled_area == N * N) {
        log_file << ind << "    [УСПЕХ] Вся площадь заполнена! Решение найдено.\n";
        best_solution = current_solution;
        return true;
    }
    // Исчерпан лимит - отсечение ветки
    if (current_count == LIMIT) {
        log_file << ind << "    [ОТСЕЧЕНИЕ] Достигнут лимит в " << LIMIT << " квадратов. Возврат.\n";
        return false;
    }

    // Ищем первую свободную ячейку (сверху вниз, слева направо)
    int tx = -1, ty = -1;
    for (int y = 0; y < N; ++y) {
        for (int x = 0; x < N; ++x) {
            if (board[y][x] == 0) {
                ty = y; tx = x;
                break;
            }
        }
        if (ty != -1) break;
    }

    log_file << ind << "    [ПОИСК] Первая свободная ячейка: x=" << tx << ", y=" << ty << "\n";

    // Ищем максимально возможный размер квадрата для этой ячейки
    int max_s = 1;
    while (ty + max_s < N && tx + max_s < N) {
        bool ok = true;
        for (int i = 0; i <= max_s; ++i) {
            if (board[ty + max_s][tx + i] != 0 || board[ty + i][tx + max_s] != 0) {
                ok = false;
                break;
            }
        }
        if (!ok) break;
        max_s++;
    }

    log_file << ind << "            Максимальный размер квадрата для этой ячейки: " << max_s << "x" << max_s << "\n";

    // Перебираем размеры от большего к меньшему
    for (int s = max_s; s >= 1; --s) {
        log_file << ind << "    [ДЕЙСТВИЕ] Ставим квадрат " << s << "x" << s << " в координаты (x=" << tx << ", y=" << ty << ")\n";

        // Ставим квадрат (заполняем массив 1)
        for (int y = ty; y < ty + s; ++y)
            for (int x = tx; x < tx + s; ++x)
                board[y][x] = 1;

        current_solution.push_back({tx, ty, s});

        // Углубляемся. Если нашли решение - возвращаем его
        if (solve(current_count + 1, filled_area + s * s)) {
            return true;
        }

        // Иначе - бэктрекинг (убираем квадрат и пробуем другой)
        log_file << ind << "    [БЭКТРЕКИНГ] Откат. Убираем квадрат " << s << "x" << s << " из (x=" << tx << ", y=" << ty << ")\n";
        current_solution.pop_back();
        for (int y = ty; y < ty + s; ++y)
            for (int x = tx; x < tx + s; ++x)
                board[y][x] = 0;
    }

    // Если ни один размер квадрата не подошёл, возвращаем false
    log_file << ind << "<-- [ВЫХОД] Ни один размер для ячейки (" << tx << ", " << ty << ") не привёл к решению. Идём назад.\n";
    return false;
}

// Вспомогательная функция для нахождения минимального делителя
int get_min_factor(int n) {
    for (int i = 2; i * i <= n; ++i) {
        if (n % i == 0) return i;
    }
    return n;
}

int main() {
    // Открываем файл для записи логов
    log_file.open("log.txt");
    if (!log_file.is_open()) {
        cerr << "Не удалось открыть файл log.txt для записи!\n";
        return 1;
    }

    int original_N;
    if (!(cin >> original_N)) return 0;

    log_file << "=== СТАРТ ПРОГРАММЫ ===\n";
    log_file << "Исходный размер столешницы: N = " << original_N << "\n";

    // Масштабирование для составных чисел
    int d = get_min_factor(original_N);
    int scale = original_N / d;

    N = d; // Ищем решение только для наименьшего делителя
    log_file << "Минимальный делитель: " << d << ". Масштабный множитель: " << scale << "\n";
    if (original_N != N) {
        log_file << "Ищем решение для упрощенной доски N = " << N << "\n";
    }

    if (N == 2) {
        log_file << "Сработал базовый случай для N=2 (или четных чисел).\n";
        best_solution = { {0, 0, 1}, {1, 0, 1}, {0, 1, 1}, {1, 1, 1} };
    } else {
        int K = N / 2 + 1; // Размер углового квадрата
        int n_k = N - K;   // Размер двух соседних квадратов

        // Итеративное углубление. Минимум для простых чисел начинается с 6.
        for (LIMIT = 6; LIMIT <= N * N; ++LIMIT) {
            log_file << "\n----------------------------------------\n";
            log_file << "ЗАПУСК ПОИСКА С ЛИМИТОМ КВАДРАТОВ = " << LIMIT << "\n";
            log_file << "----------------------------------------\n";

            // Сбрасываем доску и текущее решение
            for (int i = 0; i < N; ++i)
                for (int j = 0; j < N; ++j)
                    board[i][j] = 0;
            current_solution.clear();

            log_file << "Расстановка 3 базовых квадратов:\n";
            // 1. Ставим левый верхний квадрат
            for (int y = 0; y < K; ++y)
                for (int x = 0; x < K; ++x)
                    board[y][x] = 1;
            current_solution.push_back({0, 0, K});
            log_file << "  - Квадрат " << K << "x" << K << " в (0, 0)\n";

            // 2. Ставим правый верхний квадрат
            for (int y = 0; y < n_k; ++y)
                for (int x = K; x < N; ++x)
                    board[y][x] = 1;
            current_solution.push_back({K, 0, n_k});
            log_file << "  - Квадрат " << n_k << "x" << n_k << " в (" << K << ", 0)\n";

            // 3. Ставим левый нижний квадрат
            for (int y = K; y < N; ++y)
                for (int x = 0; x < n_k; ++x)
                    board[y][x] = 1;
            current_solution.push_back({0, K, n_k});
            log_file << "  - Квадрат " << n_k << "x" << n_k << " в (0, " << K << ")\n";

            int filled_area = K * K + 2 * n_k * n_k;

            // Запускаем поиск (3 квадрата уже поставлены)
            if (solve(3, filled_area)) {
                log_file << "\n>>> РЕШЕНИЕ НАЙДЕНО ПРИ ЛИМИТЕ = " << LIMIT << " <<<\n";
                break;
            }
        }
    }

    log_file.close();

    // Вывод ответа
    cout << best_solution.size() << "\n";
    for (const auto& sq : best_solution) {
        cout << sq.x * scale + 1 << " "
             << sq.y * scale + 1 << " "
             << sq.size * scale << "\n";
    }

    return 0;
}
