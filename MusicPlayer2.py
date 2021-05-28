# importing libraries
import concurrent.futures
import time
import os
import re
import sys
import vlc
import pafy
import random
import datetime
import subprocess

from multiprocessing import Process
from threading import Thread
from gtts import gTTS
from select import select


#vlc player
global player
player = vlc.MediaPlayer()

global userInput
userInput = ""

#current day
day = datetime.datetime.today().weekday()

# timeout is a value to timeout the user input if the user doesn't input anything.  It is re-set to the length of the song
global timeout
timeout = 100

global genre
genre = ""

#gtts output system
def say(audio):
    print(audio)
    for line in audio.splitlines():
        tts = gTTS(text=str(audio))
        tts.save('tts.mp3')
        os.system('mpg321 tts.mp3')


#get the data from the array parameter
def getData(dataArray):
    global songName, songAuthor, songGenre, songURL
    splitArray = dataArray.split(':')
    songName = splitArray[1]
    songAuthor = splitArray[0]
    songGenre = splitArray[2]
    songURL = splitArray[-1]


#play the song for an inputted URL
def playSong(URL):
    global timeout
    say(songName + " by " + songAuthor)
    URL = "https:"+URL
    #get the audio link
    video = pafy.new(URL)
    audio = video.getbestaudio()
    playurl = audio.url

    #play the audio
    Media = vlc.Media(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.play()
    time.sleep(1.5)
    timeout = float(player.get_length() / 1000)


#get contents of the Music Links.txt file and add them to an array
def getFileInfo():
    file = open('Music Links.txt', 'r')
    array = []
    for line in file:
        array.append(line)
    file.close()
    return array


def playerController(command):
    global genre
    number = random.randint(0, len(getFileInfo()))


    # if an input is passed
    if(command == "next"):
        player.stop()

        # if it is Sunday
        if (day == 6 and not player.is_playing):
            genre = "i"

        fileArray = getFileInfo()
        random.shuffle(fileArray)

        fileArray = getFileInfo()

        songArray = getData(fileArray[number])

        if(genre in songGenre):
            say(command)
            playSong(songURL)
            print("*" * 50 + "songName: " + songName + "*" * 50 + "\n" + " " * 50 + "genre:" + genre + "\tsongGenre:" + songGenre)

        else:
            playerController("next")


    if command == 'toggle':
        player.pause();
        say(command)
        time.sleep(1)

    else:
        #player.play()
        print("command not found")


#
def command():
    global genre
    #timeout = player.get_length()
    timeout = 0
    print("\n\n\ncommand? ('toggle' = pause/play, 'next' = next, 'combat' = combat, 'normal' = normal, 'boss' = boss)\n")

    input1 = ""

    command = ""

    userInput = ""
    timeout = float(player.get_length() / 1000)


    print("song length:"+str(timeout))

    #get user input on a timeout
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        input2 = str(sys.stdin.readline())
        input1 = input2.split('\n')
        input1 = input1[0]


    if input1 == "toggle":
        command = 'toggle'
        print('toggle song')

    if input1 == "next":
        command = 'next'
        print('next song')

    if input1 == "combat":
        genre = 'c'
        print("combat genre")

    if input1 == 'normal':
        genre = ''
        print('normal genre')

    if input1 == 'boss':
        genre = 'b'
        print('boss genre')

    if input1 == 'exit':
        print('exiting')
        sys.exit("user inputted exit command")

    return command


playerController("next")
#actually run the things
while(1):
    try:
        playerController(command())
    except:
        print("error")
        say('error')
        time.sleep(2)
        playerController("next")