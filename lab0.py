# No Imports Allowed!

def Reverse(lst): 
    """
    Since the .reverse() method for python lists does not return a new list, 
    the purpose of this method is to create a helper function that makes the 
    implementation of the "backwards" method easier by actually returning a 
    list (new_lst)
    """
    i = len(lst) - 1 #establishes a max index from to decrement in while loop
    new_lst = []
    while i >= 0:
        new_lst.append(lst[i]) #appends new elements to list in reverse order
        i = i - 1 #decrements index tand gets closer to front of original list
    return new_lst 

def copy(lst): #note to self--could have just used .copy(list) method
    """
    Note to self: could have just implemented the list method .copy(list), 
    which returns a new list. Purpose of method was to make the duplication of 
    left and right sample lists slightly easier by ensuring that there was a 
    method to return the new list.
    """
    i = 0
    new_lst = []
    while i < len(lst):
        new_lst.append(lst[i])
        i = i + 1
    return new_lst

#def copy_until(lst, end):
#    i = 0
#    new_lst = []
#    while i < end:
#        new_lst.append(lst[i])
#        i = i + 1
#    return new_lst

def add_list(list1, list2): 
    """
    For this method, given two lists of equal length, it will proceeed to add 
    the components of the list at equal indexes and return a new list that has 
    the combined individual components of the given parameters. This is to act 
    as a helper function for the "mix" method below
    """
    new_list = []
    for i in range(len(list1)): #assumes equal list length for both lists
        A = list1[i] + list2[i] #adds elements at equivalent list indexes
        new_list.append(A) #appends the new element to the new list
    return new_list

def backwards(sound):
    """
    This function should take a sound (in our representation, as a dictionary) 
    as its input, and it should return a new sound that is the reversed version
    of the original (but without modifying the object representing the original
    sound!)
    """
    new_rate = sound['rate'] #copies the original rate, because it remains unchanged
    new_left = Reverse(sound['left']) 
    new_right = Reverse(sound['right'])
    new_sound = {'rate': new_rate, 'left': new_left, 'right' : new_right} 
    return new_sound


def mix(sound1, sound2, p):
    """
    We'll implement this behavior as a function called mix. mix should take 
    three inputs: two sounds (in our dictionary representation) and a "mixing 
    parameter" pp (a float such that 0 \leq p \leq 10≤p≤1). The resulting sound
    should take pp times the samples in the first sound and 1-p1−p times the 
    samples in the second sound, and add them them together to produce a new 
    sound. The two input sounds should have the same sampling rate. If you are 
    provided with sounds of two different sampling rates, you should return 
    None instead of returning a sound.
    """
    mix1 = p
    mix2 = 1 - p
    if sound1['rate'] != sound2['rate']: #accounts for the case in which the rates are not the same
        return None
    rate = sound1['rate'] #proceeds to consider the case in which the rates are the same
    a = len(sound1['right']) #creates an index for both the sounds 1 and 2 to use in conditionals
    b = len(sound2['right'])
    if len(sound1['right']) != len(sound2['right']): 
        if a > b: #case in which the second sound is shorter in duration and the first sound needs to be shortened prior to scaling
            new_sound1 = {'rate' : sound1['rate'], 'left': sound1['left'][:b], 'right' : sound1['right'][:b]} #shortened first list
            multiplied_list1_left = [element * mix1 for element in new_sound1['left']] #scaled sound1 left
            multiplied_list1_right = [element * mix1 for element in new_sound1['right']] #scaled sound1 right
            multiplied_list2_left = [element * mix2 for element in sound2['left']] #scaled sound2 left
            multiplied_list2_right = [element * mix2 for element in sound2['right']] #scaled sound2 right
            full_left = add_list(multiplied_list1_left, multiplied_list2_left) #utilizes "add" method to combine both lists for left and right
            full_right = add_list(multiplied_list1_right, multiplied_list2_right) 
            mixed_sound = {'rate': rate, 'left': full_left, 'right' : full_right} #creates and returns new mixed sound
            return mixed_sound
        else: #case in which the first sound is shorter in duration and the second sounds needs to be shortened prior to scaling
            """
            This else condition follows the same thought process/procedure as previous conditional
            """
            new_sound2 = {'rate' : sound1['rate'], 'left': sound2['left'][:a], 'right' : sound2['right'][:a]} 
            multiplied_list1_left = [element * mix1 for element in sound1['left']]
            multiplied_list1_right = [element * mix1 for element in sound1['right']]
            multiplied_list2_left = [element * mix2 for element in new_sound2['left']]
            multiplied_list2_right = [element * mix2 for element in new_sound2['right']]
            full_left = add_list(multiplied_list1_left, multiplied_list2_left)
            full_right = add_list(multiplied_list1_right, multiplied_list2_right)
            mixed_sound = {'rate': rate, 'left': full_left, 'right' : full_right}
            return mixed_sound


def echo(sound, num_echos, delay, scale):
    """
    Next, we'll implement a classic effect: the echo filter. We simulate an 
    echo by starting with our original sound, and adding one or more additional
    copies of the sound, each delayed by some amount and scaled down so as to 
    be quieter. We will implement this filter as a function called echo(sound, 
    num_echos, delay, scale). This function should take the following arguments:

        sound: a dictionary representing the original sound
        num_echos: the number of additional copies of the sound to add
        delay: the amount (in seconds) by which each "echo" should be delayed
        scale: the amount by which each echo's samples should be scaled
    """
    rate = sound['rate'] #creates a new variable to copy over the rate from the previous sound (as rate remains unchanged)
    end = num_echos + 1 #creates the appropriate index for the for loop for the number of times the sound needs to be duplicated
    original_left = copy(sound['left']) #copies the original sound for left and right speaker samples
    original_right = copy(sound['right'])
    new_ls = [] #new lists for the left and right samples, they will be double lists, lists within lists
    new_rs = []
    sample_delay = round(delay*sound['rate']) #calculates the number of samples that it needs to be delayed by (as seen on website)
    for i in range(end): #begins the for loop to duplicate for all the echos requested in the method parameters
        new_scale = scale ** i #accounts for the scale factor given the iteration of the echo
        im_ls = [] #intermediary left and right lists
        im_rs = []
        for j in range(len(original_left)): #for loop to append every individual echo copy to the list of lists in the new_ls and rs lists established
            new_l_sample = new_scale * original_left[j]
            im_ls.append(new_l_sample)
            new_r_sample = new_scale * original_right[j]
            im_rs.append(new_r_sample)
        new_ls.append(im_ls) #double left and right lists created
        new_rs.append(im_rs)
#    print(new_ls)
#    print(new_rs)
    final_length = (num_echos * sample_delay) + len(original_left) #calculates the length of the final left and right side sample lists
    final_ls = [0]*final_length #establishes the initial set of 0s for a list of the outlined final_length
    final_rs = [0]*final_length
    for echo_index in range(end):
        shift = echo_index * sample_delay #calculates the shift for every echo
        for index in range(len(new_ls[echo_index])):
            final_ls[index+shift] = new_ls[echo_index][index] + final_ls[index+shift] #adds the new values in appropriately with the shifts for indexing purposes
            final_rs[index+shift] = new_rs[echo_index][index] + final_rs[index+shift]
    new_sound = {'rate' : rate, 'left' : final_ls, 'right' : final_rs} #creates and returns the new sound
    return new_sound


def pan(sound):
    """
    So far, we have not really taken advantage of the fact that we are working 
    with stereo sounds (for each of the effects above, we applied the same 
    results to the left and right channels). We'll change that in this section,
    using stereo sound to create a really neat spatial effect. We achieve this 
    effect by adjusting the volume in the left and right channels separately, 
    so that the left channel starts out at full volume and ends at 0 volume 
    (and vice versa for the right channel).
    """
    rate = sound['rate'] #establishes the rate for the final sound to be returned
    left_samples = copy(sound['left']) #copies the sound for the left and right sample lists to be modified
    right_samples = copy(sound['right'])
    new_ls = [] #new left and right lists to be returned in the new sound
    new_rs = []
    N = len(right_samples) #establishes the mathematical constant required in the for loop/conditionals
    for i in range(len(left_samples)):
        if i == 0: #considers the case in which the sample is the first/last in either list for the first two conditionals
            new_ls.append(left_samples[i])
            new_rs.append(0)
        elif i == len(left_samples) - 1:
            new_ls.append(0)
            new_rs.append(right_samples[i])
        else: #case in which constants need to be applied
            new_scale_left = (1 - (i / (N - 1))) * (left_samples[i])
            new_ls.append(new_scale_left)
            new_scale_right = (i / (N - 1)) * (right_samples[i])
            new_rs.append(new_scale_right)
    new_sound = {'rate' : rate, 'left' : new_ls, 'right' : new_rs}
    return new_sound
    

def remove_vocals(sound):
    """
    As a final example for this lab (unless you are interested to try some of 
    the optional additional pieces discussed below!) is a little trick for 
    (kind of) removing vocals from a piece of music, creating a version of the 
    song that would be appropriate as a backing track for karaoke night.
    
    Our approach is going to seem weird at first, but we will explain why it 
    works (at least on some pieces of music) in a bit. For now, we'll describe 
    our algorithm. For each sample in the input, we compute (left-right), i.e.,
    the difference between the left and right channels at that point in time, 
    and use that value as both the left and right values in the output at that 
    time.
    """
    rate = sound['rate'] #establishes rate for the new sound
    left_samples = copy(sound['left']) #copies the left and right samples for the new sound
    right_samples = copy(sound['right'])
    new_ls = [] #intializes new lists for left and right samples
    new_rs = []
    for i in range(len(left_samples)):
        diff = left_samples[i] - right_samples[i] #calculates the accurate number for the difference between samples at equal indexes
        new_ls.append(diff) #appends differences to each list
        new_rs.append(diff)
    new_sound = {'rate' : rate, 'left' : new_ls, 'right' : new_rs} #creates and returns a new sound
    return new_sound 


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

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    # hello = load_wav('sounds/hello.wav')
    # write_wav(backwards(hello), 'hello_reversed.wav')

    
    # Code to create mystery.wav reversal for 009 Lab Submission:
    # mystery = load_wav('sounds/mystery.wav')
    # write_wav(backwards(mystery), 'mystery_reversed.wav')
    # synth = load_wav('sounds/synth.wav')
    # water = load_wav('sounds/water.wav')
    # write_wav(mix(synth, water, 0.2), 'mixed_sound.wav')
    # car = load_wav('sounds/car.wav')
    # write_wav(pan(car), 'new_car.wav')
    # coffee = load_wav('sounds/coffee.wav')
    # write_wav(remove_vocals(coffee), 'new_coffee.wav')
#     chord = load_wav('sounds/chord.wav')
#     write_wav(echo(chord, 5, 0.3, 0.6), 'new_chord.wav')
