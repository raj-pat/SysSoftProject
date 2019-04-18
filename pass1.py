from HashTable import *
import queue
import sys

# The predefined file
opFile = open("opcode.txt")
for line in opFile:  # Storing the line > "String opcode format someNum" in a hash table at the start of the program
    eachLine(line)

try:
    sicFile = open(sys.argv[1])
except (FileNotFoundError, IndexError):
    print("Please input a valid file name and try again!")
    exit()

StartAdd = None
currAddress = None
literalQ = queue.Queue()
symTab = {}
for line in sicFile:
    temp = line.strip()

    if temp != "" and temp[0] != '.':  # if the data/line isn't empty and also not a comment
        # Splitting the line based on col
        label = line[0:7].strip().upper()  # 1-8
        instruction = line[9:16].strip().upper()  # 10-17 with '+' included
        operand = line[18:30].strip().strip('\n').upper()  # 18-30
        # print(label + " " + instruction + " " + operand) #debug

        if StartAdd is not None:  # None is an object; "is not" used
            retrievedData = eachLine(instruction)  # Using the hashTable to pull [String,opcode,format,someNum]"
            k = 0
            if operand != "":
                if operand[0] == "=":  # literal defined
                    literalQ.put(operand)
            if label != "":  # if label not empty, store it in the Symbol table
                # Insertion
                symTab[label] = str(currAddress)
            if (retrievedData[
                    1] != "ZZ" and retrievedData != "DNE") or instruction == "WORD" or instruction == "BYTE" or \
                    retrievedData[0] == "BASE":  # Is a hex number 2/3/4
                # tempFile.write(str(currAddress)[2:].upper() + "\t" + retrievedData[1] + "\t" + retrievedData[2] +"\t"
                #                + line.strip('\n').upper() + "\n")
                tempFile.write(
                    '{0:6} {1:3} {2:3} {3:8} {4:8} {5:8}\n'.format(str(currAddress)[2:].upper(), retrievedData[1],
                                                                   retrievedData[2], label, instruction, operand))

                if k == 0:
                    currAddress = hex(int(retrievedData[2], 16) + int(currAddress, 16))  # adding 2/3/4 to the address
            elif retrievedData[0] == "RESW" or retrievedData[0] == "RESB":  # zz = Resw
                tempFile.write(
                    '{0:6} {1:3} {2:3} {3:8} {4:8} {5:8}\n'.format(str(currAddress)[2:].upper(), retrievedData[1],
                                                                   retrievedData[2], label, instruction, operand))

                # Insertion for Resw
                if k == 0:
                    currAddress = hex(int(currAddress, 16) + (int(retrievedData[2], 16)) * (int(operand)))

            elif retrievedData[0] == "LTORG" or retrievedData[0] == "END":
                tempFile.write(
                    '{0:6} {1:3} {2:3} {3:8} {4:8} {5:8}\n'.format(str(currAddress)[2:].upper(), retrievedData[1],
                                                                   retrievedData[2], label, instruction, operand))
                while not literalQ.empty():
                    lit = literalQ.get()

                    tempFile.write(
                        '{0:6} {1:3} {2:3} {3:8} {4:8} {5:8}\n'.format(str(currAddress)[2:].upper(), "ZZ", "0",
                                                                       "literal", "BYTE", lit[1:]))

                    if lit[1] == 'X':
                        print(lit)
                        if (len(lit) - 4) % 2 == 0:
                            symTab[lit] = str(currAddress)
                            currAddress = hex(int(currAddress, 16) + int((len(lit) - 4) / 2))
                        else:
                            tempFile.write("^Error: Invalid literal length \n")
                    elif lit[1] == 'C':
                        symTab[lit] = str(currAddress)
                        currAddress = hex(int(currAddress, 16) + int(len(lit) - 4))
            else:
                tempFile.write(
                    '{0:6} {1:3} {2:3} {3:8} {4:8} {5:8}\n'.format(str(currAddress)[2:].upper(), retrievedData[1],
                                                                   retrievedData[2], label, instruction, operand))
                tempFile.write("^Error: Invalid mneumonic \n")
        elif instruction == "START":
            StartAdd = operand
            tempFile.write(StartAdd + "    ZZ  0   " + line.strip('\n').upper() + "\n")

            currAddress = hex(int(operand, 16))
            if label != "":
                symTab[label] = str(currAddress)
print("\n\n********Symbol Table********")
print("\tLabel\tLoc")
for key in symTab:
    print("%10s\t%6s" % (key, symTab[key].upper()[2:]))

tempFile.close()
