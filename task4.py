import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture


def main():
    train_df = pd.read_csv('data/train_with_target.csv')
    test_df = pd.read_csv('data/test_without_target.csv')

    # Структурный признак
    # Малое |diff| → признаки игрока схожи → один класс
    # Большое |diff| → признаки сильно различаются → другой класс
    test_diff = np.abs(test_df['feature_1'] - test_df['feature_2']).values.reshape(-1, 1)

    # Кластеризация через GMM (без использования меток)
    gmm = GaussianMixture(n_components=2, random_state=42, n_init=20)
    gmm.fit(test_diff)

    labels = gmm.predict(test_diff)  # 0 или 1

    # Сопоставляем компоненту с меньшим средним → метка 1 (малый diff), компоненту с большим средним → метка 2 (большой diff)
    if gmm.means_[0] < gmm.means_[1]:
        # Компонента 0 = малый diff = класс 1
        predictions = labels + 1
    else:
        # Компонента 0 = большой diff = класс 2
        predictions = 2 - labels

    # Запись результата
    pd.Series(predictions, name='target').to_csv('test_target_only.csv', index=False)
    print("Результат сохранён в test_target_only.csv")
    print(f"Распределение предсказаний: {dict(pd.Series(predictions).value_counts().sort_index())}")


def validate_on_train():
    # Проверка подхода на обучающей выборке
    from sklearn.metrics import accuracy_score

    train_df = pd.read_csv('data/train_with_target.csv')
    train_diff = np.abs(
        train_df['feature_1'] - train_df['feature_2']
    ).values.reshape(-1, 1)

    gmm = GaussianMixture(n_components=2, random_state=42, n_init=20)
    gmm.fit(train_diff)
    labels = gmm.predict(train_diff)

    if gmm.means_[0] < gmm.means_[1]:
        preds = labels + 1
    else:
        preds = 2 - labels

    acc = accuracy_score(train_df['target'], preds)
    acc = max(acc, 1 - acc)  # Метки взаимозаменяемы

    print(f"Train accuracy: {acc:.4f}")
    print(f"|accuracy - 0.5| = {abs(acc - 0.5):.4f}  (нужно >= 0.27)")


if __name__ == '__main__':
    main()
    print()
    validate_on_train()
