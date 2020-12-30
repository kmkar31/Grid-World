import matplotlib.pyplot as plt
import zipfile
from zipfile import ZipFile
import pickle
import time
from statistics import mean


def plot(timesteps, returns, epochs):
    plt.figure()
    plt.plot([i for i in range(epochs)], timesteps)
    plt.plot([100*i for i in range(epochs//100)], [mean(timesteps[100*i:100*(i+1)])
                                                   for i in range(epochs//100)])
    plt.savefig('exp/time/AverageTimePerEpoch_'+str(epochs)+'.png')
    # plt.show()
    plt.figure()
    plt.plot([i for i in range(epochs)], returns)
    plt.plot([100*i for i in range(epochs//100)], [mean(returns[100*i:100*(i+1)])
                                                   for i in range(epochs//100)])
    plt.savefig('exp/returns/AverageReturnsPerEpoch_'+str(epochs)+'.png')
    # plt.show()


def dump(Q, state_blocks, action_blocks, lim):

    filename = str(lim) + '_' + str(len(state_blocks)) + \
        '_' + str(time.time()) + '.zip'

    Qfile = 'Q_' + str(lim) + '.txt'
    Qfilehandler = open(Qfile, 'wb')
    Bfile = 'state_blocks_' + str(lim) + '.txt'
    Bfilehandler = open(Bfile, 'wb')
    Afile = 'action_blocks_' + str(lim) + '.txt'
    Afilehandler = open(Afile, 'wb')

    with ZipFile(filename, 'w') as zip:
        zip.write(pickle.dump(Q, Qfilehandler))
        zip.write(pickle.dump(state_blocks, Bfilehandler))
        zip.write(pickle.dump(action_blocks, Afilehandler))


def load(filename, lim):
    if not(zipfile.is_zipfile(filename)):
        print("Invalid File")
        return
    with open(filename, 'r'):
        Q = pickle.load(ZipFile.extract('Q_' + str(lim) + '.txt'))
        state_blocks = pickle.load(ZipFile.extract(
            'state_blocks_' + str(lim) + '.txt'))
        action_blocks = pickle.load(ZipFile.extract(
            'action_blocks_' + str(lim) + '.txt'))
    return Q, state_blocks, action_blocks
