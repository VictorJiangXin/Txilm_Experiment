import matplotlib.pyplot as plt



def plot_gama_distribute():
    with open('gama.csv', 'r') as f:
        lines = f.readlines()
    lines = lines[1:]

    x = [i * 0.05 for i in range(21)]
    title = []
    gama_distribute = []
    for line in lines:
        line = line.split(',')
        title.append(line[0])
        gama_distribute.append([float(num) for num in line[1 : len(line) - 1]])

    s_m = 0.4
    for i in range(1, len(title) + 1):
        plt.subplot(4, 3, i)
        plt.bar(left=x, height=gama_distribute[i - 1], width=0.025, alpha=0.8, color='green')
        if i % 3 == 1:
            plt.ylabel('m/s=%.1f' % (s_m))
            s_m += 0.2

        if i == 10:
            plt.xlabel('n/m={}'.format(0.1)) 
        elif i == 11:
            plt.xlabel('n/m={}'.format(0.4)) 
        elif i == 12:
            plt.xlabel('n/m={}'.format(0.8)) 
    
    plt.show()


plot_gama_distribute()