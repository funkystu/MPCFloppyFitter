from easygui import *
from shutil import copyfile
import os
import glob
import binpacking
#where are the samples?
#where are the virtual floppies?
samples_dir = None
floppies_dir = None

#message and images for the gui.
msg = ""
img = "mpc2k.gif"

#number of floppy folders we have.
num_floppies = 0
floppies = []

def subfolders(path_to_parent):
 try:
    return next(os.walk(path_to_parent))[1]
 except StopIteration:
    return []

while samples_dir is None:
    msg = "Please select the directory containing your samples."
    buttonbox(msg,image=img, choices=["Ok"])
    samples_dir = diropenbox()
    print("Samples Directory:")
    print(samples_dir)

    #does this directory contain samples?
    #specifically we are looking for .wav files 16bit @ 44.1
    if not any(File.endswith(".wav") for File in os.listdir(samples_dir)):
        msgbox('No WAV Files!', 'ERROR!')
        samples_dir = None

while floppies_dir is None:
    msg = "Please select the directory containing the virtual floppy drives."
    buttonbox(msg,image=img,choices=["Ok"])
    floppies_dir = diropenbox()
    print("Floppy Directory:")
    print(floppies_dir)

    #does this directory contain directories?
    #specifically we are looking for folders 1 through 99.
    num_floppies = len(subfolders(floppies_dir))
    if num_floppies is 0:
        msgbox('No Folders!', 'ERROR!')
        floppies_dir = None

    #TODO: check to make sure the folders match this format:
    #FLPTY0

    #these should be in order.
    floppies = subfolders(floppies_dir)

# Keys are file locations.
# Values are file sizes.
samples = {}
wavs = glob.glob(samples_dir+"/*.wav")
for wav in wavs:
    samples[wav] = os.stat(wav).st_size #size in bytes.

#binpack to bins of maximum size 1440kb
bins = binpacking.to_constant_volume(samples,1440000,None,None,1440000)
print(bins)
itr = 1

#copy all the files.
for b in bins:
    if itr == 100:
        break
    for sample in b:
        dest = floppies_dir + "/" + floppies[itr] + "/" + os.path.basename(sample)
        print dest
        copyfile(sample, dest)
    itr = itr + 1

msgbox("Done!", "SUCCESS!")
