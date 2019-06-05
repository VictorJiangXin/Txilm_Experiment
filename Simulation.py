import numpy as np
import random
import matplotlib.pyplot as plt
from tqdm   import tqdm
import time


def ctor_experiment_once(m, n, k):
    TXID_LEN = 63
    temp_len = 0
    index = [i for i in range(m)]
    # transaction in block is one subset of mempool_tx, so we just need know the the index
    random.shuffle(index)
    block_tx_index = sorted(index[0:n])
    # get m different txid
    while temp_len != m:
        txid_mempool = np.random.randint(0, 2**TXID_LEN, m)
        temp_len = len(set(txid_mempool))
    txid_mempool.sort()
    block_tx_hash = txid_mempool[block_tx_index] % (2 ** k)
    txid_mempool_hash = txid_mempool % (2 ** k)

    num = 0
    current_tx_index = block_tx_index[num]
    for i in range(m):
        if i < current_tx_index and txid_mempool_hash[i] == block_tx_hash[num]:
            return True
        elif i == current_tx_index:
            num += 1
            if num == n:
                return False
            current_tx_index = block_tx_index[num]
    return False


def noctor_experiment_once(m, n, k):
    """Do one experiment

    Default TXID: 63bit
    """
    TXID_LEN = 63
    temp_len = 0
    index = [i for i in range(m)]
    # transaction in block is one subset of mempool_tx, so we just need know the the index
    random.shuffle(index)
    non_block_tx_index = sorted(index[n:m])
    block_tx_index = sorted(index[0:n])
    # get m different txid
    while temp_len != m:
        txid_mempool = np.random.randint(0, 2**TXID_LEN, m)
        temp_len = len(set(txid_mempool))

    block_tx_hash = txid_mempool[block_tx_index] % (2 ** k)
    mempool_without_blockTx_hash = txid_mempool[non_block_tx_index] % (2 ** k)
    if len(set(block_tx_hash)) < n:
        return True
    for tx_hash in block_tx_hash:
        if tx_hash in mempool_without_blockTx_hash:
            return True
    return False



def experiment():
    K = [i for i in range(20, 41)]
    M = [1000, 3000, 5000]
    N = [100, 300, 500]
    EXPERIMENT_TIMES = 100000
    for m in M:
        for n in N:
            simulation_noctor = []
            simulation_ctor = []
            approx_noctor = [1 - (1 - 0.5 ** k) ** (m * n + n * n / 2) for k in K]
            approx_ctor_n = [1 - (1 - 0.5 ** k) ** (m + n / 2) for k in K]
            approx_ctor = [1 - (1 - 0.5 ** k) ** (m) for k in K]
            start_time = time.time()
            for k in K:
                count_noctor = 0
                count_ctor = 0
                for times in tqdm(range(EXPERIMENT_TIMES)):
                    if noctor_experiment_once(m, n, k):
                        count_noctor += 1
                    if ctor_experiment_once(m, n, k):
                        count_ctor += 1
                simulation_noctor.append(count_noctor / EXPERIMENT_TIMES)
                simulation_ctor.append(count_ctor / EXPERIMENT_TIMES)
            with open(str(m) + '_' + str(n) + '_' + 'sim.csv', 'w') as f:
                f.write('k, approx_noctor, simulation_noctor, approx_ctor_withn, approx_ctor, simulation_ctor\n')
                for i in range(len(K)):
                    f.write('{}, {}, {}, {}, {}, {}\n'.format(K[i], approx_noctor[i], simulation_noctor[i], approx_ctor_n[i], approx_ctor[i], simulation_ctor[i]))
            print('experiment m = {} n = {} complete. Time cost:{}'.format(m, n, time.time() - start_time))


if __name__ == '__main__':
    experiment()


