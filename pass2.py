import os

from pass1 import *


def adjustDisplacement(e, displacement):
    if e == bin(1):
        if displacement.startswith("-"):
            newDisp = negBin(displacement)[-5:]
        else:
            newDisp = displacement[2:].zfill(5)
    else:
        # 3 digits
        if displacement.startswith("-"):
            newDisp = negBin(displacement)[-3:]
        else:
            newDisp = displacement[2:].zfill(3)
    return newDisp


def negBin(negHex):  # NOTE only converts a NEGATIVE(-0x) hex number to binary
    negBinNum = bin(int(negHex, 16))[3:].zfill(20)
    newBin = ""
    flip = False
    for i in reversed(negBinNum):
        if flip == True:
            if i == '1':
                newBin += "0"
            else:
                newBin += '1'
        else:
            newBin += i
        if i == '1':
            flip = True
    return hex(int(newBin[::-1], 2))



p1File = open("tempFile.txt")
objFile = open(sys.argv[1] + ".obj", "w")
lstFile = open(sys.argv[1] + ".lst", "w")
LDBreg = "none"
lstFile.write("********************************************************\n\n")
lstFile.write("SIC/XE ASSEMBLER BY RAJ PATEL N01394161\n\n")
lstFile.write("********************************************************\n")
lstFile.write('{0:6} {1:12} {2:12} {3:12} {4:12}\n'.format("Loc", "ObjCode", "Label", "Instrut", "Operand"))
lstFile.write('{0:6} {1:12} {2:12} {3:12} {4:12}\n'.format("---", "-------", "-----", "-------", "-------"))

# for each line in pass1 file
for line in p1File:
    lineAddr = line[0:7].strip()
    opCode = line[7:10].strip()
    format = line[11:14].strip()
    label = line[15:23].strip()
    instruction = line[24:32].strip()
    operand1 = line[33:45].strip()
    operand = operand1
    errorOnLine = False


    # print(lineAddr + " " + opCode + " " + format + " " + label + " " + instruction + " " +
    #               operand)
    if instruction == "RESW":
        objFile.write("!\n")
        reswEndAdd = hex(int(lineAddr, 16) + (int(format, 16)) * (int(operand)))
        objFile.write(reswEndAdd[2:].upper().zfill(6) + "\n")
        if lineAddr == lastReswAddr.upper():
            objFile.write(StartAdd.zfill(6) + "\n")
        else:
            objFile.write("000000\n")

    if lineAddr == "^Error:":  # Error from pass 1
        lstFile.write(line.strip().upper() + "\n")
    elif opCode == "N":
        lstFile.write('{0:6} {1:12} {2:12} {3:12} {4:12}\n'.format(lineAddr, "", label, instruction, operand1))
    elif label == "literal":
        objCode = ""
        if operand[0] == 'C':
            for letter in operand[2:-1]:
                objCode += hex(ord(letter))[2:]
        else:
            objCode = operand[2:-1]
        lstFile.write(
            '{0:6} {1:12} {2:12} {3:12} {4:12}\n'.format(lineAddr, objCode.upper(), "=" + operand, instruction,
                                                         operand1))

    elif format == "2":
        r2 = "0"
        if operand.find(',') != -1:
            r1 = eachLine(operand[operand.find(",") - 1])[1]
            r2 = eachLine(operand[operand.find(",") + 1])[1]
        else:
            r1 = eachLine(operand)[1]
        if r1 == "N" or r2 == "N":
            objCode = "Error: Invalid operand"
        else:
            objCode = opCode + r1 + r2
        lstFile.write(
            '{0:6} {1:12} {2:12} {3:12} {4:12}\n'.format(lineAddr, objCode.upper(), label, instruction, operand1))

    elif opCode == "ZZ":
        objCode = ""
        if instruction == "START":
            objFile.write(operand.zfill(6) + "\n")
            if lastReswAddr == "":
                objFile.write(StartAdd.zfill(6) + "\n")
            else:
                objFile.write("000000\n")
        if instruction == "END":
            objFile.write("!\n")
            objFile.close()
        if instruction == "BASE" or instruction == "+BASE":
            try:

                LDBreg = symTab[operand]
            except KeyError:
                try:
                    LDBreg = symTab[operand[1:]]
                except KeyError:
                    LDBreg = "none"
                    lstFile.write("error\n")
        if instruction == "WORD":
            objCode = adjustDisplacement(bin(0), hex(int(operand, 16))).zfill(6)

        lstFile.write(
            '{0:6} {1:12} {2:12} {3:12} {4:12}\n'.format(lineAddr, objCode.upper(), label, instruction, operand1))
    elif instruction == "RSUB":
        objCode = opCode + "0000"
        lstFile.write(
            '{0:6} {1:12} {2:12} {3:12} {4:12}\n'.format(lineAddr, objCode.upper(), label, instruction, operand1))
    else:
        # format 3 normal statement
        # ni = 00(*), 11(Default) ,01(#) ,10(@)
        n = bin(0)
        i = bin(0)
        x = bin(0)
        b = bin(0)
        p = bin(0)
        e = bin(0)
        operandAddress = ""

        if operand.startswith('#'):
            i = bin(1)
            operand = operand[1:]
        elif operand.startswith('@'):
            n = bin(1)
            operand = operand[1:]
        else:  # default
            n = bin(1)
            i = bin(1)
            p = bin(1)
        dispCalc = False
        # x var
        if operand.find(",X") != -1:
            x = bin(1)
            operand = operand[:operand.find(",X")]
        # checking in SymTab, If not then checking if it's a number
        try:
            operandAddress = symTab[operand]
        except KeyError:
            dispCalc = True
            try:
                displacement = int(operand, 16)
            except ValueError:  # if the operand is not a number
                errorOnLine = True
                objCode = "Error: Invalid Operand"
                displacement = int("0", 16)

                # e var

        if instruction.startswith('+'):
            e = bin(1)

            # calculate displacement
        if dispCalc is False:
            if (n == bin(1) and i == bin(0)) or e == bin(1):  # direct addressing
                displacement = int(operandAddress, 16)
            else:
                displacement = int(operandAddress, 16) - (int(lineAddr, 16) + int(format, 16))

        if e == bin(0):
            if displacement > int("7FF", 16) or displacement < int("-7FF", 16):
                b = bin(1)
                p = bin(0)
        if b == bin(1):
            if LDBreg != "none":
                displacement = int(operandAddress, 16) - int(LDBreg, 16)
            else:
                errorOnLine = True
                objCode = "Error: Base not defined"
                displacement = int("0", 16)

            if displacement < int("0", 16):
                errorOnLine = True
                objCode = "Error: Negative Base"

        displacement = adjustDisplacement(e, hex(displacement))

        # print(operandAddress + " " + str(hex(int(lineAddr, 16) + int(format, 16))))
        # print(displacement)
        ni = hex(int(n[2:] + i[2:], 2) + int(opCode, 16))
        xbpe = hex(int(str(x[2:] + b[2:] + p[2:] + e[2:]), 2))
        if errorOnLine == False:
            objCode = str(ni[2:].zfill(2)) + str(xbpe[2:].zfill(1)) + str(displacement)
        objFile.write(objCode.upper() + "\n")
        lstFile.write(
            '{0:6} {1:12} {2:12} {3:12} {4:12}\n'.format(lineAddr, objCode.upper(), label, instruction, operand1))
p1File.close()
objFile.close()
lstFile.close()
os.remove("tempFile.txt")
os.chmod(sys.argv[1] + ".lst", 0o744)
os.chmod(sys.argv[1] + ".obj", 0o744)
print("SIC/XE ASSEMBLED\n\t\t GENERATED: " + sys.argv[1] + ".lst AND " + sys.argv[1] + ".obj")
