import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def main():
    train_df = pd.read_csv('train_with_target.csv')
    test_without_target_df = pd.read_csv('test_without_target.csv')

    X = train_df[['feature_1', 'feature_2']]
    y = train_df['target']

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=31
    )

    model = CatBoostClassifier(
        iterations=100,
        verbose=False,
        random_state=31
    )
    model.fit(X_train, y_train, eval_set=(X_val, y_val))

    # y_val_pred = model.predict(X_val)
    # val_accuracy = accuracy_score(y_val, y_val_pred)
    # print(f"Val accuracy: {val_accuracy:.4f}")

    pd.Series(model.predict(test_without_target_df), name='target').to_csv('test_target_only.csv', index=False)


if __name__ == '__main__':
    main()
