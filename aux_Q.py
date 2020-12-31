import matplotlib.pyplot as plt
import zipfile
from zipfile import ZipFile
import pickle
import time
import os
from statistics import mean


def plot(timesteps, returns, epochs, frequency):
    plt.figure()
    plt.plot([i for i in range(epochs)], timesteps)
    plt.plot([frequency*i for i in range(epochs//frequency)], [mean(timesteps[frequency*i:frequency*(i+1)])
                                                               for i in range(epochs//frequency)])
    plt.savefig('exp/time/AverageTimePerEpoch_'+str(epochs)+'.png')
    # plt.show()
    plt.close()
    plt.figure()
    plt.plot([i for i in range(epochs)], returns)
    plt.plot([frequency*i for i in range(epochs//frequency)], [mean(returns[frequency*i:frequency*(i+1)])
                                                               for i in range(epochs//frequency)])
    plt.savefig('exp/returns/AverageReturnsPerEpoch_'+str(epochs)+'.png')
    # plt.show()
    plt.close()


def dump(Q, state_blocks, action_blocks, lim):

    folder_name = 'Q_'+str(time.time())
    os.mkdir(folder_name)
    Qfile = folder_name + '/Q_' + str(lim) + '.txt'
    Qfilehandler = open(Qfile, 'wb')
    Bfile = folder_name+'/state_blocks_' + str(lim) + '.txt'
    Bfilehandler = open(Bfile, 'wb')
    Afile = folder_name+'/action_blocks_' + str(lim) + '.txt'
    Afilehandler = open(Afile, 'wb')

    pickle.dump(Q, Qfilehandler)
    pickle.dump(state_blocks, Bfilehandler)
    pickle.dump(action_blocks, Afilehandler)


def load(folder_name, lim):
    Q = pickle.load(open(folder_name + '/' +
                         'Q_' + str(lim) + '.txt', 'rb'))
    state_blocks = pickle.load(
        open(folder_name + '/' + 'state_blocks_' + str(lim) + '.txt', 'rb'))
    action_blocks = pickle.load(
        open(folder_name + '/' + 'action_blocks_' + str(lim) + '.txt', 'rb'))
    return Q, state_blocks, action_blocks
