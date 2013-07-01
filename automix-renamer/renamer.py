'''
Created on Jun 8, 2013

@author: neuro
'''

import sys, os, getopt, unicodedata, random
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

infolder = ''
shuffle = True
reshuffle = False

def precheck(argv):
    global infolder    
    global shuffle
    global reshuffle
    try:
        opts, args = getopt.getopt(argv,"hnri:",["infolder="])
    except getopt.GetoptError:
        print 'renamer.py -i <inputfolder>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'renamer.py -i <inputfolder> [-n]'
            sys.exit()
        elif opt in ("-n", "--noshuffle"):
            shuffle = False
        elif opt in ("-r", "--reshuffle"):
            reshuffle = True
        elif opt in ("-i", "--ifolder"):
            infolder = arg.strip()
    if os.path.exists(infolder):
        print 'path ', infolder, 'is valid'
        args
        
    else:
        print 'specified path does not exist. exiting.'
        exit(2)
        
def checkfolder():
    os.chdir(infolder)
    invalids = []
    nummp3 = 0
    for files in os.listdir('.'):
        if not files.endswith(".mp3"):
            invalids.append(files)
        else:
            nummp3 = nummp3 + 1
    print 'Found ', nummp3, ' mp3 files'
    if nummp3 == 0:
        print 'Nothing to process. Exiting'
        exit(2)
    if len(invalids) > 0:
        print 'Found invalid files:'
        for invalid in invalids:
            print '  --> ', invalid
        print 'Exiting'
        exit(2)

def mp3stats():
    cdlength = 0
    cdsize = 0
    for files in os.listdir('.'):
        audio = MP3(files)
        cdlength = cdlength + audio.info.length
        cdsize = cdsize + os.path.getsize(files)
    hours = int(cdlength / 3600)
    minutes = int((cdlength - hours * 3600) / 60)
    seconds = int(cdlength - hours * 3600 - minutes * 60)
    print 'Total CD length:', hours, 'hours,', minutes, 'minutes,', seconds, 'seconds.'
    print 'Total CD size:', cdsize/1000000, 'MB.'
    
def renamebytags():
    for files in os.listdir('.'):
        tags = EasyID3(files)
        artist = unicodedata.normalize('NFKD', tags["artist"][0])
        title = unicodedata.normalize('NFKD', tags["title"][0])
        print ' --> Renaming "', files, '" to "', artist, '-', title,'".'
        newname = str(artist + '-' + title + '.mp3')
        os.rename(files, newname)
    print 'Done.'
    
def shufflesongs():
    songs = os.listdir('.')
    random.shuffle(songs)
    counter = 1
    for song in songs:
        prepend = ''
        if counter < 10:
            prepend = '0' + str(counter)
        else:
            prepend = str(counter)
        if reshuffle == True:
            shuffledname = prepend + '-' + song[3:]
        else:   
            shuffledname = prepend + '-' + song    
        os.rename(song, shuffledname)
        counter = counter + 1
    
if __name__ == '__main__':
    precheck(sys.argv[1:])
    checkfolder()
    mp3stats()
    if reshuffle == True:
        print '-------reshuffling tracks---------'
        shufflesongs()
        print "Success. Exiting."
        exit(0)
    print '-------processing tags---------'
    renamebytags()
    if shuffle == True:
        print '-------shuffling tracks--------'
        shufflesongs()
    print "Success. Exiting."
