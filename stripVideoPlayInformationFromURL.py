



if __name__ == "__main__":
        try:
            print("starting")
            file = 'Music Links bkup.txt'


            with open(file, 'r', encoding='utf-8') as fileRead:
                data = fileRead.readlines()

            for line in range(len(data)):

                videoData = data[line]
                splitDataArray = videoData.split(':')
                songName = splitDataArray[1]
                songAuthor = splitDataArray[0]
                songGenre = splitDataArray[2]
                videoURL = splitDataArray[-1]

                if('&' in videoURL):
                    print("& in line")
                    splitOnVideoInfo = videoURL.split("&")
                    URL = splitOnVideoInfo[0]
                    data[line] = str(songAuthor + ":" + songName + ":" + songGenre + ":" + URL + '\n')
                    print("new line:" + str(data[line]))

            #print(data)


            with open(file, 'w', encoding='utf-8') as fileWrite:
                fileWrite.writelines(data)

            print("done")
        except NameError as e:
            print("error:" + str(e))

