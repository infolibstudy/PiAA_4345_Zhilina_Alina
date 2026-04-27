#include <iostream>
#include <string>
#include <vector>
#include <fstream>

using namespace std;

int main() {
    // Инициализация файла для записи логов
    ofstream log("log.txt");
    log << "--- Начало работы алгоритма КМП ---\n";

    // ускорение ввода-вывода
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // считываем образец и текст
    string pat, txt;
    getline(cin, pat);
    getline(cin, txt);

    log << "Считан образец (pat): '" << pat << "'\n";
    log << "Считан текст (txt): '" << txt << "'\n\n";

    int patLen = pat.size();
    int txtLen = txt.size();

    // построение префикс-функции для образца
    log << "--- Построение префикс-функции ---\n";
    vector<int> pref(patLen, 0);
    log << "Инициализация массива pref нулями. Длина массива: " << patLen << "\n";

    for (int i = 1; i < patLen; ++i) {
        log << "\nИтерация i=" << i << ", текущий символ pat[" << i << "] = '" << pat[i] << "'\n";
        int k = pref[i - 1];
        log << "  Начальное значение k (из pref[" << i - 1 << "]): " << k << "\n";

        while (k > 0 && pat[i] != pat[k]) {
            log << "  Несовпадение: pat[" << i << "] ('" << pat[i] << "') != pat[" << k << "] ('" << pat[k] << "')\n";
            log << "  Откат k к pref[" << k - 1 << "]\n";
            k = pref[k - 1];
            log << "  Новое значение k = " << k << "\n";
        }
        if (pat[i] == pat[k]) {
            log << "  Совпадение: pat[" << i << "] == pat[" << k << "] ('" << pat[i] << "'). Увеличиваем k.\n";
            ++k;
        } else {
            log << "  Совпадений нет, k остается равным " << k << "\n";
        }
        pref[i] = k;
        log << "  -> Записываем pref[" << i << "] = " << k << "\n";

        // Фиксация текущего вида массива префикс-функции
        log << "  Текущий массив pref: [";
        for (int j = 0; j < patLen; ++j) {
            log << pref[j] << (j == patLen - 1 ? "" : ", ");
        }
        log << "]\n";
    }

    // поиск всех вхождений образца в тексте (алгоритм КМП)
    log << "\n--- Поиск вхождений образца в тексте ---\n";
    vector<int> answers;
    int k = 0; // длина текущего совпадения
    log << "Начальная длина совпадения k = 0\n";

    for (int i = 0; i < txtLen; ++i) {
        log << "\nИтерация по тексту i=" << i << ", текущий символ txt[" << i << "] = '" << txt[i] << "'\n";
        log << "  Текущая длина совпадения k = " << k << "\n";

        while (k > 0 && txt[i] != pat[k]) {
            log << "  Несовпадение: txt[" << i << "] ('" << txt[i] << "') != pat[" << k << "] ('" << pat[k] << "')\n";
            log << "  Откат k к pref[" << k - 1 << "]\n";
            k = pref[k - 1];
            log << "  Новое значение k = " << k << "\n";
        }
        if (txt[i] == pat[k]) {
            log << "  Совпадение: txt[" << i << "] == pat[" << k << "] ('" << txt[i] << "'). Увеличиваем k.\n";
            ++k;
        } else {
            log << "  Совпадений нет, k остается равным " << k << "\n";
        }
        if (k == patLen) {
            log << "  !!! Найдено полное вхождение образца (k == " << patLen << "). Индекс начала: " << (i - patLen + 1) << "\n";
            answers.push_back(i - patLen + 1);

            log << "  Откат k для поиска следующих вхождений к pref[" << k - 1 << "]\n";
            k = pref[k - 1]; // продолжение поиска следующих вхождений
            log << "  Новое значение k = " << k << "\n";
        }
    }

    log << "\n--- Завершение алгоритма ---\n";
    log << "Всего найдено вхождений: " << answers.size() << "\n";
    log.close();

    // вывод результата
    if (answers.empty()) {
        cout << -1 << "\n";
    } else {
        for (size_t idx = 0; idx < answers.size(); ++idx) {
            if (idx > 0) cout << ",";
            cout << answers[idx];
        }
        cout << "\n";
    }

    return 0;
}