import matplotlib.pyplot as plt

fps = ['crop', 'scheibe', 'palette', 'precision']

def parse(fp, t):
    f = open(fp).read().split()
    return f[t::2]

def plot(fp):
    fig, ax1 = plt.subplots()
    ax1.set_xlabel(fp)
    ax1.plot(parse(fp, 1), color='b', label='found')
    ax1.set_ylabel('amount of found image')
    ax2 = ax1.twinx()
    ax2.plot(parse(fp, 0), color='r', label='time')
    ax2.set_ylabel('time')
    ax1.set_ylim(0, 1000)
    ax2.set_ylim(bottom=0)
    # ax1.legend(loc=0)
    # ax2.legend(loc=0)
    fig.savefig(fp+'.png')
    fig.clf()

for name in fps:
    plot(name)
