import json
from collections import defaultdict


def build_char_map(train_data):
    # Строится маппинг: символ шифра -> символ оригинала
    # Для каждого символа из source считаются голоса (какому символу target он соответствует), и выбирается наиболее частый вариант
    # Используются только пары одинаковой длины (посимвольное соответствие)
    votes = defaultdict(lambda: defaultdict(int))

    for item in train_data:
        src = item["source"]
        tgt = item["target"]
        if len(src) == len(tgt):
            for s, t in zip(src, tgt):
                votes[s][t] += 1

    char_map = {}
    for cipher_char, targets in votes.items():
        best = max(targets, key=lambda x: targets[x])
        char_map[cipher_char] = best

    return char_map


def translate(text, char_map):
    # Перевод строки с помощью символьного маппинга. Неизвестные символы остаются как есть
    return "".join(char_map.get(c, c) for c in text)


def main():
    with open("train_data.json", "r", encoding="utf-8") as f:
        train_data = json.load(f)

    with open("test_data.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)

    # Маппинг символов
    char_map = build_char_map(train_data)
    print(f"Построен маппинг из {len(char_map)} символов")

    # Перевод тестовых данных
    results = []
    for item in test_data:
        source = item["source"]
        translation = translate(source, char_map)
        results.append({"source": source, "translation": translation})

    with open("submission.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Сохранено {len(results)} переводов в submission.json")

    print("\nПримеры переводов:")
    for item in results[:5]:
        print(f"  Источник:  {item['source']}")
        print(f"  Перевод:   {item['translation']}")
        print()


if __name__ == "__main__":
    main()
