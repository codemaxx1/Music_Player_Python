# c = combat
# n = normal/nature
#

from gtts import gTTS  # importing libraries
import time
import os
import re
# import .GPIO as GPIO
import sys
import vlc
import pafy
import random
from select import select
import subprocess

#change the volume
#volume = 100
#os.system('amixer cset numid=1 90%')

Instance = vlc.Instance()
player = Instance.media_player_new()
duration = 100
timeStart = 120
first = True
play = True
deltaTime = 100
countArray = []

genre = ''


def terandelleResponse(audio):
    print(audio)
    '''for line in audio.splitlines():
        tts = gTTS(text=str(audio))
        tts.save('Mtts.mp3')
        os.system('mpg321 Mtts.mp3')
        '''

# speech recognition system returns the text
def myCommand():
    #global volume
    global player
    global play
    global timeStart
    global genre
    global duration
    global deltaTime

    # time.sleep(1.5)
    duration = float(player.get_length() / 1000)
    deltaTime = deltaTime


    if (play == True):
        deltaTime = time.time() - timeStart
        print("\t"*7 + 'Time remaining: ' + str(round((duration - deltaTime)/60)) + ":" + str(round(duration - deltaTime) % 60))


    if (deltaTime > duration):
        # time.sleep(duration)
        commands().music('next')
        print("\t"*7 +  "did you forget about the video?\n")

    command = ''

    timeout = duration
    input1 = 'next'

    print("\n\n\ncommand? ('toggle' = pause/play, 'next' = next, 'combat' = combat, 'normal' = normal, 'boss' = boss)\n")
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        input2 = str(sys.stdin.readline())
        #print( '"'+str(input2.split('\n')[0])+'"')
        input1 = input2.split('\n')
        input1 = input1[0]



    if input1 == "toggle":
        command = 'pause music'
        print('toggle song')

    if input1 == "next":
        command = 'next music'
        print('next song')

    if input1 == "combat":
        genre = 'c'
        print("combat")

    if input1 == 'normal':
        genre = ''
        print('normal')

    if input1 == 'boss':
        genre = 'b'
        print('boss mode')

    if input1 == 'exit':
        print('exiting')
        sys.exit("user inputted exit command")

    return command



def assistant(command):
    # print(command)
    musicOrderArray = command.split(' ')
    musicOrder = musicOrderArray[0]
    # print(musicOrder)
    commands().music(musicOrder)


# commands().sentry()

class commands:

    def music(self, order):
        global player
        global play
        global duration
        global timeStart
        global genre
        global first
        global countArray
        # genre = ''

        print("\t"*7 + "genre = " + '"' + genre + '"')

        if order == "next":
            player.stop()
            file = open('Music Links.txt', 'r')
            array = []
            average = 0
            sumPlays = 1
            lineNumber = 0
            i = 0
            
            for line in file:
                array.append(line)
                if first:
                    countArray.append(0)
            file.close()
            
            random.shuffle(array)
            print("\t"*7 + '# of lines in file:' + str(len(array)))
            print("\t"*7 + "genre = " + '"' + genre + '"')
            for i in countArray:
                sumPlays += countArray[i]
            average = float(sumPlays / len(array))
            first = False
            print("\t"*7 + 'average plays: ' + str(average))
            URLlineRandom = random.randint(0, len(array))

            splittedArray = array[URLlineRandom].split(':')
            print("\t"*7 + "split Array:" + str(splittedArray))
            #print("array[-3] = " + str(splittedArray[-3]))

            #print('length of countArray:' + str(len(countArray)))
            for i in range(len(countArray)):
                #print('testing term number: ' + str(i))
                #next
                #splittedArray = array[i].split(':')
                #print("splittedArray:" + str(splittedArray))
                #print("array[-3] = " + str(splittedArray[-3]))
                #if (genre in splittedArray[-3] and genre != '' and genre == 'c'):
                #if (genre in splittedArray[-3] and genre != ' ' and genre != '' and genre == 'c'):
                if(True):
                    specArray = array[URLlineRandom].split(':')
                    if(specArray[-3] != ' ' and specArray[-3] != 'c' and (countArray[i] < countArray[URLlineRandom])):
                        URLlineRandom = i
                        print('combat sting override')

                    elif(specArray[-3] == ''):
                        URLlineRandom = i
                        print('general combat sting override')

                elif (genre in splittedArray[-3] and genre != '' and genre == 'b'):
                    specArray = array[URLlineRandom].split(':')
                    if(specArray[-3] != '' and (countArray[i] < countArray[URLlineRandom])):
                        URLlineRandom = i
                        print('boss sting override')

                    elif(specArray[-3] == ''):
                        URLlineRandom = i
                        print('general combat sting override')


                else:
                    if countArray[i] < countArray[URLlineRandom] and genre == '':
                        URLlineRandom = i
                        print('normal stirng ovewrride')



            '''if (countArray[URLlineRandom] > (average + 1)):
                # break
                commands().music('next')
                '''
            countArray[URLlineRandom] += 1
            print("\t"*7 + 'this song\'s number of plays: ' + str(countArray[URLlineRandom]))

            print("\t"*7 + 'random int :' + str(URLlineRandom))


            URLlineNumber = array[URLlineRandom]
            listOfInfo = URLlineNumber.split(':')
            songURL = 'https:' + listOfInfo[-1]
            #print('song name: ' + str(listOfInfo[1]) + "\nauthor: " + str(listOfInfo[0]))

            terandelleResponse('\n'*3 + '*'*20 + ' song name: ' + str(listOfInfo[1]) + ". Author: " + str(listOfInfo[0]) + ' ' +'*'*20 + '\n')   #

            play = True
            #print('go!')
            video = pafy.new(songURL)
            best = video.getbestaudio()
            #best = video.getbest()
            playurl = best.url
            # print('best url:'+str(playurl))
            Instance = vlc.Instance()
            player = Instance.media_player_new()
            Media = Instance.media_new(playurl)
            Media.get_mrl()
            player.set_media(Media)
            player.play()
            timeStart = time.time()
            time.sleep(1.5)
            duration = float(player.get_length() / 1000)


        if order == 'pause':
            if order == "pause" and play == True:
                play = False
                player.pause()

            else:
                play = True
                player.pause()

            time.sleep(1)


# end of commands class





'''
operating sequence
'''
commands().music('next')

while True:
    try:
        assistant(myCommand())


    except:
        print('error')

        time.sleep(0.2)
