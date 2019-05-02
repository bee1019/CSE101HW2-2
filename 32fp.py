# Your name: Bansri Shah
# Your SBU ID: 110335850
# Your NetID: bpshah
#
# IEEE 754 32-bit Floating-Point Translator (Homework 2-2) starter code
# CSE 101, Fall 2018

# DO NOT MODIFY THE FOLLOWING HELPER FUNCTION!!!

def binToHex(bitstring):
    equivalents = {'0000': '0', '0001': '1', '0010': '2', '0011': '3', '0100': '4', '0101': '5', '0110': '6', '0111': '7', '1000': '8', '1001': '9', '1010': 'A', '1011': 'B', '1100': 'C', '1101': 'D', '1110': 'E', '1111': 'F'}
    result = ''
    bitstring.strip()

    for i in range(0, len(bitstring), 4):
        result += equivalents[bitstring[i:i+4]]

    return result

# Complete the functions that follow for this assignment
def fractionToBinary(value): # value is a string containing a base-10 value
    if value.count(".") != 1:
        return None
    else:
        value = float(value)
        result = ""
        power = 0.5

        while value > 0:
            if value >= power :
                value = value - power
                result += "1"
            else:
                result += "0"
            power = power / 2
        return result

def shiftBinaryPoint(bitstring):
    exp = 0
    mantissa = ""
    
    if bitstring.count(".") > 1:
        return None
    elif bitstring.count(".") == 0:
        bitstring += ".0"
    temp = bitstring.split(".")

    if "1" in temp[0]:
        index = temp[0].find("1")
        exp = len(temp[0][index + 1:])
        mantissa = temp[0][index + 1:] + temp[1]

    else:
        pos = temp[1].find("1")
        exp = -1 * (pos + 1)
        mantissa = temp[1][pos + 1:]

    if len(mantissa) > 23:
            mantissa = mantissa[:23]

    return [exp, mantissa]

def getBiasedExponent(exp): # exp is an integer
    binary = ""
    if exp < -127 or exp > 128:
        return None
    else:
        exp += 127
        binary = bin(exp)
        binary = binary[2:]

        while len(binary) < 8:
            binary = "0" + binary

    return binary
        

def assembleValue(isNegative, exponent, mantissa):
    result = ""
    if isNegative == True:
        result = result + "1" + exponent + mantissa
    else:
        result = result + "0" + exponent + mantissa

    while len(result) < 32:
        result += "0"

    return result
    
def encode(original): # original is a base-10 floating-point value
    isNeg = False
    if original < 0:
        isNeg = True
        original = original * -1
    else:
        isNeg = False

    original = str(original)

    if "." not in original:
        original += ".0"

    index = original.find(".")
    whole = int(original[:index])
    whole = bin(whole)
    whole = whole[2:]

    fractional = "0" + original[index:]
    fracResult = fractionToBinary(fractional)

    if fracResult == "None":
        return None

    shiftString = whole + "." + fracResult
    shiftResult = shiftBinaryPoint(shiftString)

    if shiftResult == "None":
        return None

    exp = getBiasedExponent(shiftResult[0])
    mantissa = shiftResult[1]

    result = assembleValue(isNeg, exp, mantissa)

    while len(result) < 8:
        result = "0" + result

    return binToHex(result)


# DO NOT modify or remove the code below! You can use it to test your work.

if __name__ == "__main__":
    print('Testing fractionToBinary("0.5"):     ', fractionToBinary("0.5"))
    print('Testing fractionToBinary("0..25"):   ', fractionToBinary("0..25"))
    print('Testing fractionToBinary("0.75"):    ', fractionToBinary("0.75"))
    print('Testing fractionToBinary("0.0625"):  ', fractionToBinary("0.0625"))
    print('Testing fractionToBinary("0.328125"):', fractionToBinary("0.328125"))
    print()

    print('Testing shiftBinaryPoint("01101.10100"):', shiftBinaryPoint("01101.10100"))
    print('Testing shiftBinaryPoint("1.001"):      ', shiftBinaryPoint("1.001"))
    print('Testing shiftBinaryPoint("11"):         ', shiftBinaryPoint("11"))
    print('Testing shiftBinaryPoint("1..1"):       ', shiftBinaryPoint("1..1"))
    print('Testing shiftBinaryPoint("0.011010101"):', shiftBinaryPoint("0.011010101"))
    print()

    print('Testing getBiasedExponent(25):  ', getBiasedExponent(25))
    print('Testing getBiasedExponent(130): ', getBiasedExponent(130))
    print('Testing getBiasedExponent(0):   ', getBiasedExponent(0))
    print('Testing getBiasedExponent(-3):  ', getBiasedExponent(-3))
    print('Testing getBiasedExponent(-203):', getBiasedExponent(-203))
    print()

    print('Testing assembleValue(False, "10000010", "011100"):     ', assembleValue(False, "10000010", "011100"))
    print('Testing assembleValue(False, "10000101", "00110101100"):', assembleValue(False, "10000101", "00110101100"))
    print('Testing assembleValue(True, "10000100", "000000110"):   ', assembleValue(True, "10000100", "000000110"))
    print('Testing assembleValue(True, "10000101", "101011100"):   ', assembleValue(True, "10000101", "101011100"))
    print()

    print('Testing encode(77.375): ', encode(77.375))
    print('Testing encode(-32.375):', encode(-32.375))
    print('Testing encode(11.5):   ', encode(11.5))
    print('Testing encode(-18.25): ', encode(-18.25))
    print('Testing encode(0.101):  ', encode(0.101))
    print('Testing encode(-21):    ', encode(-21))

    print()
    
