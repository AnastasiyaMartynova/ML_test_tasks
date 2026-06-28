import json
from collections import defaultdict


def build_char_map(train_data: list[dict]) -> dict[str, str]:
    # Строит таблицу перекодировки: source_char -> target_char. Используются только пары с len(source) == len(target) для выравнивания
    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for ex in train_data:
        src, tgt = ex["source"], ex["target"]
        if len(src) == len(tgt):
            for s, t in zip(src, tgt):
                counts[s][t] += 1

    # Для каждого символа - наиболее частое соответствие
    char_map = {sc: max(mapping, key=mapping.get) for sc, mapping in counts.items()}
    return char_map


def decode(text: str, char_map: dict[str, str]) -> str:
    # Применяет таблицу перекодировки, неизвестные символы оставляет как есть
    return "".join(char_map.get(c, c) for c in text)


def main():
    # Загрузка данных
    with open("train_data.json", encoding="utf-8") as f:
        train_data = json.load(f)

    with open("test_data.json", encoding="utf-8") as f:
        test_data = json.load(f)

    # Обучение: построение таблицы перекодировки
    char_map = build_char_map(train_data)
    print(f"Уникальных символьных соответствий: {len(char_map)}")

    # Инференс: декодировка тестовых примеров
    results = []
    for ex in test_data:
        translation = decode(ex["source"], char_map)
        results.append({"source": ex["source"], "translation": translation})

    # Сохранение результата
    with open("submission.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Переведено {len(results)} примеров в submission.json")

    # Пример результатов
    print("\nПример переводов:")
    for r in results[:5]:
        print(f"  SRC: {r['source']}")
        print(f"  TRN: {r['translation']}")
        print()


if __name__ == "__main__":
    main()
