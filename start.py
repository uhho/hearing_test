from datetime import datetime
from time import sleep
from pysine import sine
import alsaaudio
import threading
from pyfiglet import Figlet
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

signal = None
data = []
detected = False


def player(m):
    """Plays sounds with different frequencies and volume levels"""
    global signal
    global detected

    volumes = [1, 2, 4, 6, 8, 10, 14, 18, 22, 26, 30]
    frequencies = [125, 250, 500, 1000, 2000, 4000, 8000]

    # shuffle frequencies
    frequencies = np.repeat(frequencies, 2)
    np.random.shuffle(frequencies)

    m.setvolume(0)
    sleep(0.1)
    for freq in frequencies:
        detected = False
        for vol in volumes:
            print(freq, vol)
            for n in range(3):
                m.setvolume(vol)
                sleep(0.1)
                signal = [freq, vol, datetime.now()]
                sine(frequency=freq, duration=0.5)
                if detected:
                    break
            if detected:
                break
        sleep(2)


def listener():
    """Listens to user input"""
    global signal
    global data
    global detected

    while 1:
        r = input()
        if signal:
            d = signal + [datetime.now()]
            print(f'Recording event: {d}')
            data.append(d)
            detected = True


def greeing(m, opening=True):
    """Plays simple greeting to check sound"""
    frequencies = [261, 329, 391]
    durations = [0.2, 0.2, 0.5]
    m.setvolume(30)
    sleep(0.1)
    if opening:
        _ = [sine(frequency=f, duration=d) for f, d in zip(frequencies, durations)]
    else:
        _ = [sine(frequency=f, duration=d) for f, d in zip(frequencies[::-1], durations)]
    m.setvolume(0)
    sleep(0.1)


def analyse_results(data):
    now = datetime.now()
    """Stores and visualizes results"""
    # load data to DataFrame
    df = pd.DataFrame(data, columns=['frequency', 'volume', 'played', 'heard'])
    df['reaction_time'] = (df['heard'] - df['played']).dt.microseconds // 1000
    df.to_csv(f'./results_before_{now:%Y%m%d%H%M%S}.csv', index=None)

    # average multiple results
    df = df.groupby(['frequency']).mean().reset_index()

    # save data
    df.to_csv(f'./results_{now:%Y%m%d%H%M%S}_data.csv', index=None)

    # visualize results
    fig, ax = plt.subplots(1)
    ax.plot(df['frequency'].astype(str), df['volume'], marker='x')
    ax.set(title=f"Hearing capacity", ylim=[0, 100], xlabel='Hz', ylabel='volume')
    ax.grid()
    plt.gca().invert_yaxis()
    plt.savefig(f'./results_{now:%Y%m%d%H%M%S}_capacity.png')
    plt.clf()
    plt.close()

    # visualize reaction time
    fig, ax = plt.subplots(1)
    ax.plot(df['frequency'].astype(str), df['reaction_time'], marker='x')
    ax.set(title=f"Reaction time", xlabel='Hz', ylabel='ms')
    ax.grid()
    plt.savefig(f'./results_{now:%Y%m%d%H%M%S}_reaction.png')
    plt.clf()
    plt.close()

    return df


if __name__ == '__main__':

    f = Figlet(font='slant')
    print(f.renderText('HEARING TEST'))

    print('*' * 67)
    print('* Welcome to Hearing Test                                         *')
    print('*                                                                 *')
    print('* Please put on your headphones.                                  *')
    print('* Hit [ENTER] when you start hearing pulsing sound.               *')
    print('*' * 67)

    m = alsaaudio.Mixer()
    # play greeting
    greeing(m, opening=True)

    print('Test will start in 5 seconds...')
    sleep(5)
    # start listener
    p2 = threading.Thread(target=listener, daemon=True)
    p2.start()
    # start player
    player(m)

    # play greeting
    greeing(m, opening=False)

    analyse_results(data)
    print('Test is finished. Please check visualizations.')
