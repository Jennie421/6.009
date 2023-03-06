# No Imports Allowed!

def backwards(sound):
    """
    Create a reversed version of a sound. 
    Parameters: 
        * sound(dict): the original sound.
    Returns: 
        a new sound that is the reversed version of the original. 
    """
    # create reversed left and right sound tracks  
    left_backwards = sound['left'][::-1]
    right_backwards = sound['right'][::-1]

    backwards = {
        'rate': sound['rate'], 
        'left': left_backwards,
        'right': right_backwards,
    } 
    return backwards


def mix(sound1, sound2, p):
    """
    Mix together two sounds with the same sampling rates. 
    Parameter:
        * sound 1, sound 2(dict): sounds represented by dictionaries
        * p (float): mixing parameter; 0 <= p <= 1; 
                    sound1's samples are scaled by p;
                    sound2's samples are scaled by 1-p;
    Returns:
        If two sounds have different sampling rates, return None.
        Otherwise, return a new sound that is the mixed version of two sounds.
    """
    if sound1['rate'] != sound2['rate']:
        return None
    
    # the output length is the minimum of the lengths of input sounds
    output_length = min(len(sound1['left']), len(sound2['left']))
    
    # scale sound1 samples by a factor of p
    # scale sould2 samples by a factor of (p-1)
    left_sound1, left_sound2, right_sound1, right_sound2 = [], [], [], []
    for i in range(output_length):
        left_sound1.append (sound1['left'][i] * p)
        right_sound1.append (sound1['right'][i] * p)
        left_sound2.append (sound2['left'][i] * (1-p))
        right_sound2.append (sound2['right'][i] * (1-p))
 
    left_mix, right_mix = [], []
    for i in range(0, output_length): 
        left_mix.append(left_sound1[i] + left_sound2[i])
        right_mix.append(right_sound1[i] + right_sound2[i])

    mix = {
        'rate': sound1['rate'], 
        'left': left_mix,
        'right': right_mix,
    }
    return mix


def echo(sound, num_echos, delay, scale):
    """
    Create a new sound with a echo effect for a given sound. 
    Parameters:
        * sound (dict): a dictionary representing the original sound
        * num_echos (int): the number of additional copies of the sound to add
        * delay (float): the amount (in seconds) by which each "echo" should be delayed
        * scale (float): the amount by which each echo's samples should be scaled
    Returns:
        a new sound with the echo effect upoon the original version.
    """

    # the number of samples each 'echo' should be delayed by
    sample_delay = round(delay * sound['rate'])

    # initialize the output with the final length after delay, prevent running out of indices 
    left_echo = sound['left'] + [0] * num_echos * sample_delay  
    right_echo = sound['right'] + [0] * num_echos * sample_delay

    for i in range(1, num_echos + 1):
        for sample_index in range(len(sound['left'])):
            # each new copy is scaled down more than the one preceding it
            # add in a delayed and scaled-down copy of the sound's samples
            left_echo[sample_index + i * sample_delay] += sound['left'][sample_index] * scale ** i
            right_echo[sample_index + i * sample_delay] += sound['right'][sample_index] * scale ** i

    echo = {
        'rate': sound['rate'], 
        'left': left_echo,
        'right': right_echo,
    }
    return echo


def pan(sound):
    """
    Create a new sound with a spatial effect for a stereo sound.
    Parameters:
        * sound (dict): a dictionary representing the original sound
    Returns: 
        a new sound with the spatial effect upon the original sound
        the volume in the left and right channels of the original sound is adjusted separately, 
        so that the left channel starts out at full volume and ends at 0 volume (and vice versa for the right channel).
    """

    left_pan, right_pan = [], []
    N = len(sound['left']) # the number of samples of sound
    for i in range(N):
        # append scaled sample to new sound tracks 
        left_pan.append (sound['left'][i] * (1 - ((i)/(N - 1))))
        right_pan.append (sound['right'][i] * ((i)/(N - 1)))

    pan = {
        'rate': sound['rate'], 
        'left': left_pan,
        'right': right_pan,
    }
    return pan


def remove_vocals(sound):
    """
    Creates a new sound wih vocals in the given sound removed. 
    Parameters:
        * sound (dict): a dictionary representing the original sound
    Returns: 
        a new sound with the orginal sound's vocals removed. 
    """
    # create a list to store (left - right) of each sample pair
    diff = []
    sample_length = len(sound['left'])
    for i in range(sample_length):
        diff.append(sound['left'][i]-sound['right'][i])
    
    # compute the output sound 
    remove_vocals = {
        'rate': sound['rate'], 
        'left': diff,
        'right': diff,
    }
    return remove_vocals

# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds

import io
import wave
import struct

def load_wav(filename):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    f = wave.open(filename, 'r')
    chan, bd, sr, count, _, _ = f.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    left = []
    right = []
    for i in range(count):
        frame = f.readframes(1)
        if chan == 2:
            left.append(struct.unpack('<h', frame[:2])[0])
            right.append(struct.unpack('<h', frame[2:])[0])
        else:
            datum = struct.unpack('<h', frame)[0]
            left.append(datum)
            right.append(datum)

    left = [i/(2**15) for i in left]
    right = [i/(2**15) for i in right]

    return {'rate': sr, 'left': left, 'right': right}


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, 'w')
    outfile.setparams((2, 2, sound['rate'], 0, 'NONE', 'not compressed'))

    out = []
    for l, r in zip(sound['left'], sound['right']):
        l = int(max(-1, min(1, l)) * (2**15-1))
        r = int(max(-1, min(1, r)) * (2**15-1))
        out.append(l)
        out.append(r)

    outfile.writeframes(b''.join(struct.pack('<h', frame) for frame in out))
    outfile.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # loading file 
    mystery = load_wav('sounds/mystery.wav')
    chord = load_wav('sounds/chord.wav')
    synth = load_wav('sounds/synth.wav')
    water = load_wav('sounds/water.wav')
    car = load_wav('sounds/car.wav')
    coffee = load_wav('sounds/coffee.wav')
    
    # writing file 
    write_wav(backwards(mystery), 'mystery_reversed.wav')
    write_wav (mix(synth, water, 0.2), 'synth_water_mixed.wav')
    write_wav(echo(chord, 5, 0.3, 0.6), 'chord_echo.wav')
    write_wav(pan(car), 'car_pan.wav')
    write_wav(remove_vocals(coffee), 'coffee_remove_vocals.wav')
