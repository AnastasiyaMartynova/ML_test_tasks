import sys


def main():
    s = sys.stdin.read().strip()
    n = len(s)

    NEG = -10 ** 9  # "недостижимое" значение

    # dp[r] - это максимальное количество цифр, которое можно выбрать (с сохранением порядка) из уже просмотренного префикса так,
    # чтобы сумма выбранных цифр имела остаток r при делении на 3
    dp = [0, NEG, NEG]

    # best_at[c] - копия dp, сделанная непосредственно ПЕРЕД тем, как была обработана последняя встреченная цифра c.
    # То есть best_at[c][r] - это максимальное количество цифр, которое можно выбрать из части строки СТРОГО ДО последнего вхождения
    # цифры c, чтобы сумма выбранных цифр была r (mod 3).
    best_at = [[NEG, NEG, NEG] for _ in range(10)]
    recorded = [False] * 10

    # best_len - максимальная длина числа (по числу оставшихся цифр), которое заканчивается на "00", "25", "50" или "75" и делится на 3
    best_len = NEG

    for ch in s:
        d = int(ch)

        # Проверка на то, не образует ли текущая цифра окончание "00"/"50"/"25"/"75" вместе с какой-то более ранней цифрой c (она будет предпоследней).
        if d == 0:
            # "00": нужна цифра c = 0, сумма 0 + 0 = 0 -> r = 0
            if recorded[0]:
                val = best_at[0][0]
                if val > NEG and val + 2 > best_len:
                    best_len = val + 2
            # "50": нужна цифра c = 5, сумма 5 + 0 = 5 -> r = (-5) % 3 = 1
            if recorded[5]:
                val = best_at[5][1]
                if val > NEG and val + 2 > best_len:
                    best_len = val + 2
        elif d == 5:
            # "25": нужна цифра c = 2, сумма 2 + 5 = 7 -> r = (-7) % 3 = 2
            if recorded[2]:
                val = best_at[2][2]
                if val > NEG and val + 2 > best_len:
                    best_len = val + 2
            # "75": нужна цифра c = 7, сумма 7 + 5 = 12 -> r = (-12) % 3 = 0
            if recorded[7]:
                val = best_at[7][0]
                if val > NEG and val + 2 > best_len:
                    best_len = val + 2

        # Нужно зааомнить состояние dp ПЕРЕД учётом текущей цифры - пригодится, если позже эта цифра сыграет роль предпоследней
        best_at[d] = dp[0], dp[1], dp[2]
        recorded[d] = True

        # Обновление dp, добавляя текущую цифру (по желанию её можно как взять в выбранное подмножество, так и пропустить)
        vr = d % 3
        a0, a1, a2 = dp
        prev0 = (a0, a1, a2)[(0 - vr) % 3]
        prev1 = (a0, a1, a2)[(1 - vr) % 3]
        prev2 = (a0, a1, a2)[(2 - vr) % 3]
        c0 = prev0 + 1 if prev0 > NEG else NEG
        c1 = prev1 + 1 if prev1 > NEG else NEG
        c2 = prev2 + 1 if prev2 > NEG else NEG
        dp = [a0 if a0 > c0 else c0,
              a1 if a1 > c1 else c1,
              a2 if a2 > c2 else c2]

    max_length = 0  # Всегда можно удалить все цифры и получить 0

    if '0' in s:
        max_length = max(max_length, 1)  # Оставить единственный 0

    if best_len > NEG:
        max_length = max(max_length, best_len)

    print(n - max_length)


if __name__ == "__main__":
    main()