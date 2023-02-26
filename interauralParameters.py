import numpy as np
import pyaudio
import random
import csv
fs = 44100


def prepare_signal(f=700, time=1.0, delta_a=0.0, delta_f=0.0, delta_t=0.0):
    m = np.ones(int(fs*time), dtype=float)
    t = np.arange(0, time, 1.0 / fs)
    fade_in = np.linspace(0, 1, 441)
    fade_out = np.linspace(1, 0, 441)
    m[:int(delta_t*fs)] = 0
    m[int(delta_t*fs):int(delta_t*fs)+441] = m[int(delta_t*fs):int(delta_t*fs)+441]*fade_in
    m[-441:] = m[-441:]*fade_out
    tone = ((1 - delta_a) * (m * np.sin(2 * np.pi * (f + delta_f) * t))).astype(np.float32)
    return np.array(tone)


def signal_split(sig1, sig2):
    splitted_sig = [sample for pair in zip(sig1, sig2) for sample in pair]
    return np.asarray(splitted_sig)


def play_sound(sound):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=2,
                    rate=fs,
                    output=True)
    stream.write(sound.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()


def interaural_parameters(name):
    counter = 0
    dif_limens = []

    if name == 'ILD':
        while counter < 5:
            delta = np.random.randint(7, 12) * 0.01
            hear_difference = None
            fin = False
            print('Trial %d' % (counter + 1))
            while fin is False:
                play_sound(signal_split(prepare_signal(delta_a=0 + delta),
                                        prepare_signal()))
                ans = input('Is sound in the center? [y / n]\n')
                if ans == 'y':
                    if hear_difference is False:
                        dif_limens.append(abs(delta))
                        fin = True
                    delta += 0.01
                    hear_difference = True
                elif ans == 'n':
                    if hear_difference is True:
                        dif_limens.append(abs(delta))
                        fin = True
                    delta -= 0.01
                    hear_difference = False
            counter += 1
    elif name == 'ITD':
        while counter < 5:
            delta = random.randint(2, 3) * 0.05
            hear_difference = None
            fin = False
            print('Trial %d' % (counter + 1))
            while fin is False:
                play_sound(signal_split(prepare_signal(delta_t=0+delta),
                                        prepare_signal()))
                ans = input('Is sound in the center? [y / n]\n')
                if ans == 'y':
                    if hear_difference is False:
                        dif_limens.append(abs(delta))
                        fin = True
                    delta += 0.01
                    hear_difference = True
                elif ans == 'n':
                    if hear_difference is True:
                        dif_limens.append(abs(delta))
                        fin = True
                    delta -= 0.01
                    hear_difference = False
            counter += 1
    elif name == 'Binaural frequency discrimination':
        while counter < 5:
            delta = np.random.randint(1, 3)
            hear_difference = None
            fin = False
            print('Trial %d' % (counter + 1))

            while fin is False:
                play_sound(signal_split(prepare_signal(f=1200, delta_f=0+delta),
                                        prepare_signal(f=1200)))
                ans = input('Do you hear the difference? [y / n]\n')
                if ans == 'y':
                    if hear_difference is False:
                        dif_limens.append(abs(delta))
                        fin = True
                    delta -= 0.5
                    hear_difference = True
                elif ans == 'n':
                    if hear_difference is True:
                        dif_limens.append(abs(delta))
                        fin = True
                    delta += 0.5
                    hear_difference = False
            counter += 1
    elif name == 'Binaural beats':
        delta = 0.5
        fin = False
        play_sound(signal_split(prepare_signal(f=400, time=2.0, delta_f=0+delta),
                                prepare_signal(f=400, time=2.0)))
        ans = input('Do you hear the beats? [y / n]\n')
        if ans == 'y':
            dif_limens.append(delta)
            while fin is False:
                delta += 0.5
                play_sound(signal_split(prepare_signal(f=400, time=2.0, delta_f=0+delta),
                                        prepare_signal(f=400, time=2.0)))
                ans2 = input('Do you hear the beats? [y / n]\n')
                if ans2 == 'n':
                    dif_limens.append(delta)
                    fin = True
        elif ans == 'n':
            while fin is False:
                delta += 0.5
                play_sound(signal_split(prepare_signal(f=400, time=2.0, delta_f=0+delta),
                                        prepare_signal(f=400, time=2.0)))
                ans2 = input('Do you hear the beats? [y / n]\n')
                if ans2 == 'y':
                    dif_limens.append(delta)
                    while fin is False:
                        delta += 0.5
                        play_sound(signal_split(prepare_signal(f=400, time=2.0, delta_f=0+delta),
                                                prepare_signal(f=400, time=2.0)))
                        ans3 = input('Do you hear the beats? [y / n]\n')
                        if ans3 == 'n':
                            dif_limens.append(delta)
                            fin = True
    return dif_limens


def main():
    options = {
        '1': 'ILD',
        '2': 'ITD',
        '3': 'Binaural frequency discrimination',
        '4': 'Binaural beats',
        '5': quit}
    while True:
        case = input("Select option:\n"
                     "1 - Interaural Level difference\n"
                     "2 - Interaural Time Difference\n"
                     "3 - Binaural frequency discrimination\n"
                     "4 - Binaural beats\n"
                     "5 - Quit\n")
        ip = interaural_parameters(options[case]() if case == '5' else options[case])
        with open('lab6_results.csv', mode='a') as result:
            results_saver = csv.writer(result)
            results_saver.writerow(['%s' % options[case], ip]) if case == '4' \
                else results_saver.writerow(['%s' % options[case], '%s' % np.mean(ip)])
            result.close()


if __name__ == "__main__":
    main()
