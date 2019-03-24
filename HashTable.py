import sys


class Data:
    data = ""

    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


def hashFunc(word):
    i = 0
    num = 0
    for letter in word:
        num += (ord(letter)) * (17 ** i)  # num= s[0]%LC + s[1]*p**1%LC + s[2]*p**2%LC...
        num = num % 51  # where s[n] is an each letter of the word: "word"
        i += 1
    return num


arrOfData = [Data() for i in range(51)]  # Initializing the array to Data(None,None)


def eachLine(line):
    data = Data(line, None)  # none= null in .py
    words = line.split()
    if len(words) != 1:  # line consisting of a word with the number so 2 total
        hf = hashFunc(words[0])  # getting the int hf value of the word on the line
        if arrOfData[hf].data == None:
            arrOfData[hf] = data
            words[1].replace("\n", ' ')
            print(words[0] + " " + words[1] + " stored at location", hf, " with 0 collision")
            return 0
        else:
            dataFetched = arrOfData[hf]  # words[0] moss 22 != moss 25
            wordsFetched = dataFetched.data.split()
            coll = 1
            while wordsFetched[0] != words[0] and dataFetched.next != None:
                dataFetched = dataFetched.next
                wordsFetched = dataFetched.data.split()
                coll += 1
            if wordsFetched[0] == words[0]:
                print("^Error: Duplicate label " + words[0] + " already exist at", hf)
                return 1
            else:
                dataFetched.next = data
                print(str(words) + " stored at location ", hf, "with ", coll, " collisions")
                return 0
    elif len(words) == 1:
        hf = hashFunc(words[0])  # getting the int hf value of the word on the line
        dataFetched = arrOfData[hf]
        if dataFetched.data == None:
            print("Does not exist")
        else:
            wordsFetched = dataFetched.data.split()
            while True:
                if wordsFetched[0] == words[0]:
                    wordsFetched[1].replace("\n", '')
                    return wordsFetched
                dataFetched = dataFetched.next
                if dataFetched == None:
                    # print("Does not exist")
                    return "DNE"
                else:
                    wordsFetched = dataFetched.data.split()
    else:
        print("Invalid input")

# Main method below
# if __name__=="__main__":
#     try:
#         file = open("opcode.txt", "r")  # opening the file with the file name in " "
#     except FileNotFoundError:
#         print("File not found. Please run again!")
#         sys.exit()
#     except IndexError:
#         print("File not found. Please run again!")
#         sys.exit()
#
#     for line in file:
#         eachLine(line)
#     # End of for loop
#     file.close()
