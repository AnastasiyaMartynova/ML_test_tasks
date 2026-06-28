import math


def ternary_min(f, lo, hi, iters=200):
    # Минимизация выпуклой функции f на отрезке [lo, hi] с помощтю тройного деления отрезка
    for _ in range(iters):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if f(m1) < f(m2):
            hi = m2
        else:
            lo = m1
    x = (lo + hi) / 2
    return f(x)


def main():
    # Система координат: O = (0, 0) - станция метро
    # Проспект - ось X (восток положителен), Бульвар - ось Y (север положителен)
    A = (-1800.0, 0.0) # Курьер стартует на Проспекте, в 1800 м западнее метро
    V = (160.0, 150.0) # Офис: 160 м восточнее и 150 м севернее метро (вне улиц)
    B_Y = 2100.0 # Постамат на Бульваре, в 2100 м севернее метро

    # Скорости до офиса (обычный шаг)
    V_PROSPECT_WALK = 1.7
    V_BOULEVARD_WALK = 2.0
    V_OPEN_WALK = 1.2

    # Скорости после офиса (лёгкий бег)
    V_STREET_RUN = 2.3
    V_OPEN_RUN = 1.2

    # Этап 1: путь из A в V
    # Стратегия A1: курьер идет по Проспекту от A до точки (p, 0), затем по открытой территории напрямую до V
    def time_A1(p):
        dist_street = abs(p - A[0])
        dist_open = math.hypot(V[0] - p, V[1] - 0.0)
        return dist_street / V_PROSPECT_WALK + dist_open / V_OPEN_WALK

    # Стратегия B1: курьер идет по Проспекту от A до метро O, затем по Бульвару от O до точки (0, q), затем по открытой территории до V
    def time_B1(q):
        dist_prospect = abs(0.0 - A[0])
        dist_boulevard = abs(q - 0.0)
        dist_open = math.hypot(V[0] - 0.0, V[1] - q)
        return (dist_prospect / V_PROSPECT_WALK + dist_boulevard / V_BOULEVARD_WALK + dist_open / V_OPEN_WALK)

    best_A1 = ternary_min(time_A1, -10000.0, 10000.0)
    best_B1 = ternary_min(time_B1, -10000.0, 10000.0)
    phase1 = min(best_A1, best_B1)

    # Этап 2: путь из V в B (лёгким бегом)
    # Стратегия A2: курьер идет по открытой территории от V до точки (0, q) на Бульваре, затем бежит по Бульвару до B
    def time_A2(q):
        dist_open = math.hypot(V[0] - 0.0, V[1] - q)
        dist_boulevard = abs(B_Y - q)
        return dist_open / V_OPEN_RUN + dist_boulevard / V_STREET_RUN

    # Стратегия B2 (на случай, если окажется выгоднее): идет по открытой территории от V до точки (p, 0) на Проспекте, бежит по Проспекту до O, затем по Бульвару от O до B
    def time_B2(p):
        dist_open = math.hypot(V[0] - p, V[1] - 0.0)
        dist_prospect = abs(0.0 - p)
        dist_boulevard = abs(B_Y - 0.0)
        return (dist_open / V_OPEN_RUN + dist_prospect / V_STREET_RUN + dist_boulevard / V_STREET_RUN)

    best_A2 = ternary_min(time_A2, -10000.0, 10000.0)
    best_B2 = ternary_min(time_B2, -10000.0, 10000.0)
    phase2 = min(best_A2, best_B2)

    total = phase1 + phase2
    print(f"{total:.2f}")


if __name__ == "__main__":
    main()
