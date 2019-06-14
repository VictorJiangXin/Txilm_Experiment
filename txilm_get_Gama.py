import numpy as np 
import matplotlib.pyplot as plt
from scipy.special import comb, perm


def Txilm_get_gama(s, m, n):
    """Calc proportion of intersection(m, n) / m

    p(s, m, n)_i = Comb(m, i)Comb(s-m, n-i)/Comb(s, n)
    统计goma的分布情况
    """
    # [0, 0.05, 0.1, ...]
    m = int(m)
    n = int(n)
    P = [0] * 21
    if m + n > s:
        P[0] = 0
    else:
        P[0] = comb(s - m, n) / comb(s, n)

    group_num = n / 20
    index = 1
    for i in range(1, n + 1):
        p_gama = comb(m, i) * comb(s - m, n - i) * 1.0 / comb(s, n)
        if i > index * group_num:
            index += 1
        P[index] += p_gama

    return P


def main():
    s = 200
    m_s = [0.4, 0.6, 0.8, 1]
    n_m = [0.1, 0.4, 0.8]

    rate = [0.05 * n for n in range(0, 21)]
    f = open('gama.csv', 'w')
    f.write(' , ')
    for r in rate:
        f.write('{}, '.format(r))
    f.write('\n')
    for p0 in m_s:
        for p1 in n_m:
            f.write('m/s={} n/m={}, '.format(p0, p1))
            P = Txilm_get_gama(s, s * p0, s * p0 * p1)
            for prop in P:
                f.write('{}, '.format(prop))
            f.write('\n')
    f.close()


main()


