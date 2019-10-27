import sys
import time

debug = False

class ProgressBar:

    __count = 0
    __progressPerExec = 0
    __times = 0
    __debug = False

    def __init__(self, times, chosenDebug):
        self.__times = times
        self.__progressPerExec = 100 / times
        debug = chosenDebug
        

    def progressOnce(self):
        if not self.__debug:
            if self.__count == 0:
                print("[" + (" " * 100) + "]" + "0%")
            sys.stdout.write("\033[F")
            self.__count += 1
            progress = int(self.__count * self.__progressPerExec)
            out = "["
            out += "=" * progress
            if progress != 100:
                out += ">"
            out += " " * (100 - progress)
            if progress != 100:
                out = out[:-1]
            out += "]" 
            out += str(progress) + "%"

            time.sleep(0.5)

            print(out)

    def progress(self):

        for count in range(101):
            sys.stdout.write("\033[F")
            i = count + 1
            out = "["
            out += "=" * count
            if count != 100:
                out += ">"
            out += " " * (100 - count)
            
            out += "]" 
            out += str(count) + "%"

            time.sleep(0.05)

            print(out)        

        print("COMPLETE!!!")

class JsonWEncryption:

    label = ""
    sender = ""
    message = ""
    target = ""

    def __init__(self,chosenDebug,msg):
        debug = chosenDebug
        self.label = msg[2:9]

        self.message = msg[13:-2]
        count = 0
        lettern = 0
        for letter in self.message:
            
            if letter in "message":
                count += 1
                if count == 6:
                    self.message = self.message[(lettern + count + 5):]
                    if debug:
                        print("message found")
                    break
                pass
            else:
                lettern = lettern + 1 + count
                count = 0

        count = 0
        lettern = 0
        for letter in self.message:
            if letter in "target":
                count += 1
                if count == 6:
                    self.message = self.message[:lettern - 3]
                    if debug:
                        print("target found")
                    break
                pass
            else:
                lettern = lettern + 1 + count
                count = 0


        self.sender = msg[20:]

        count = 0
        for letter in self.sender:
            count += 1
            try:
                if letter != ".":
                    int(letter)
                
            except:
                self.sender = self.sender[:count - 1]  
                break

        self.target = msg[-18:-3]

        for letter in self.target:
            if letter == ".":
                break
            else:
                try:
                    int(letter)
                    break
                except:
                    self.target = self.target[1:]  