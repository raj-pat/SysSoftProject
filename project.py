from HashTable import *
import queue

# The predefined file
opFile = open("opcode.txt")
for line in opFile:  # Storing the line > "String opcode format someNum" in a hash table at the start of the program
    eachLine(line)

sicFile = open("test2.txt")
StartAdd = None
currAddress = None
literalQ = queue.Queue()

for line in sicFile:
    temp = line.strip()

    if temp != "" and temp[0] != '.':  # if the data/line isn't empty and also not a comment
        # Splitting the line based on col
        label = line[0:7].strip().upper()  # 1-8
        instruction = line[9:16].strip().upper()  # 10-17 with '+' included
        operand = line[18:30].strip().strip('\n').upper()  # 18-30
        # print(label + " " + instruction + " " + operand)            #debug
        if operand[0] == "=":  # literal defined
            literalQ.put(operand)

        if StartAdd is not None:  # None is an object; "is not" used
            retrievedData = eachLine(instruction)  # Using the hashTable to pull [String,opcode,format,someNum]"
            k = 0
            if retrievedData[1] != "ZZ" and retrievedData != "DNE":  # Is a hex number 2/3/4

                print(str(currAddress)[2:].upper() + " " + line.strip('\n').upper())
                if label != "":  # if label not empty, store it in the Symbol table
                    k = eachLine(label + " " + str(currAddress))  # Insertion
                if k == 0:
                    currAddress = hex(int(retrievedData[2], 16) + int(currAddress, 16))  # adding 2/3/4 to the address
            elif retrievedData[1] == "RESW":  # zz = Resw
                print(str(currAddress)[2:].upper() + " " + line.strip('\n').upper())
                if label != "":  # if label not empty, store it in the Symbol table (RESW)
                    k = eachLine(label + " " + str(currAddress))  # Insertion for Resw
                if k == 0: A
                currAddress = hex(int(currAddress, 16) + (int(retrievedData[2], 16)) * (int(operand)))
        else:
            print(str(currAddress)[2:].upper() + " " + line.strip('\n').upper())
            print("^Error: Invalid mneumonic ")
    elif instruction == "START":
        StartAdd = operand
        print("    " + line.strip('\n').upper())
        currAddress = hex(int(operand, 16))
