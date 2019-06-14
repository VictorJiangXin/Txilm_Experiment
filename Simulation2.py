import numpy as np
import random
import matplotlib.pyplot as plt
from tqdm   import tqdm
import time


def Txilm_simulation_once(s, m, n, k):
    TXID_LEN = 63
    temp_len = 0

    index = [i for i in range(s)]
    random.shuffle(index)
    mempool_index = sorted(index[0 : m])
    random.shuffle(index)
    block_index = sorted(index[0 : n])
    common_index = list(set(mempool_index).intersection(set(block_index)))
    if len(common_index) == 0:
        return False

    while temp_len != s:
        unconfirm_tx = np.random.randint(0, 2**TXID_LEN, s)
        temp_len = len(set(unconfirm_tx))

    unconfirm_tx.sort()
    unconfirm_tx_hash = unconfirm_tx % (2 ** k)

    num = 0
    current_tx_index = common_index[num]
    for i in range(m):
        if mempool_index[i] < current_tx_index and unconfirm_tx_hash[mempool_index[i]] == unconfirm_tx_hash[current_tx_index]:
            return True
        elif mempool_index[i] == current_tx_index:
            num += 1
            if num == len(common_index):
                return False
            current_tx_index = common_index[num]
    return False


def experiment():
    K = [i for i in range(15, 17)]
    S = 10000
    m_S = [0.8]
    n_m = [0.01, 0.1, 0.95]
    EXPERIMENT_TIMES = 100000
    for p1 in m_S:
        for p2 in n_m:
            m = int(S * p1)
            n = int(m * p2)
            simulation_ctor = []
            approx_ctor_n = [1 - (1 - 0.5 ** k) ** (m + n / 2) for k in K]
            approx_ctor = [1 - (1 - 0.5 ** k) ** (m) for k in K]
            start_time = time.time()
            for k in K:
                count_ctor = 0
                for times in tqdm(range(EXPERIMENT_TIMES)):
                    if Txilm_simulation_once(S, m, n, k):
                        count_ctor += 1
                simulation_ctor.append(count_ctor / EXPERIMENT_TIMES)
                print('m/s = {}, m = {}, n = {}, n/m = {}, psc = {}'.format(p1, m, n, p2, count_ctor / EXPERIMENT_TIMES))
            with open('n_m-{}-m-{}-n-{}.csv'.format(p1, m, n), 'w') as f:
                f.write('k, approx_ctor_withn, approx_ctor, simulation_ctor\n')
                for i in range(len(K)):
                    f.write('{}, {}, {}, {}\n'.format(K[i], approx_ctor_n[i], approx_ctor[i], simulation_ctor[i]))
            print('experiment m = {} n = {} complete. Time cost:{}'.format(m, n, time.time() - start_time))


if __name__ == '__main__':
    experiment()
    