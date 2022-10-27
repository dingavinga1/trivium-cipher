import sys

class Byte:
    def __init__(self, character, bin=False): #constructor for Byte object
        if bin==False:
            char=ord(character)
            self.binStr=format(char, "b").rjust(8, '0')
        else:
            self.binStr=character

    def getRaw(self): #returns string of 1s and 0s from a Byte object
        return self.binStr

    def getConvert(self): #resolve a Byte into an ascii character
        return chr(eval('0b'+self.binStr))

    def xor(self, second): #xor each character represented bit of a Byte
        a=second.getRaw()
        c=[str(int(self.binStr[i])^int(a[i])) for i in range(8)]
        return Byte(chr(eval('0b'+''.join(c))))

def getBinStr(byteArr): #Converts a 'Byte' Array into a string of 1s and 0s
    return ''.join(i.getRaw() for i in byteArr)

def getByteArr(string): #Converts a strings to 'Byte' Array
    return [Byte(i) for i in string]

def XOR(ch1, ch2): #XOR FUNCTION FOR CHARACTER
    return str(int(ch1)^int(ch2))

def AND(ch1, ch2): #AND FUNCTION FOR CHARACTER
    return str(int(ch1)&int(ch2))

LFSR1=''
LFSR2=''
LFSR3=''

def nextKeyBit(): #generates single next bit of key stream using the properties of trivium cipher
    global LFSR1, LFSR2, LFSR3

    i1=LFSR1[-1]
    i2=LFSR1[65]
    i3=AND(LFSR1[90], LFSR1[91])
    XOR1=XOR(XOR(i1, i2), i3)

    j1=LFSR2[-1]
    j2=LFSR2[68]
    j3=AND(LFSR2[81], LFSR2[82])
    XOR2=XOR(XOR(j1, j2), j3)

    k1=LFSR3[-1]
    k2=LFSR3[65]
    k3=AND(LFSR3[108], LFSR3[109])
    XOR3=XOR(XOR(k1, k2), k3)

    si=XOR(XOR(XOR1, XOR2), XOR3) #output bit (s0)

    IN1=XOR(LFSR1[68], XOR3)
    IN2=XOR(LFSR2[77], XOR1)
    IN3=XOR(LFSR3[86], XOR2)

    #emulating shift capability
    LFSR1=LFSR1[:-1]
    LFSR2=LFSR2[:-1]
    LFSR3=LFSR3[:-1]
    LFSR1=IN1+LFSR1
    LFSR2=IN2+LFSR2
    LFSR3=IN3+LFSR3

    return si

def get8bits(): #generates an 8 bit key stream for encrypting a byte of data
    string=''
    for i in range(8):
        string+=nextKeyBit()
    #print(Byte(string, True).getRaw())
    return Byte(string, True)

if len(sys.argv)<=1:
    print("[-] Invalid Arguments. Please use -h for help")
    exit()

if sys.argv[1]=='-h': #help for running the program
    print("Usage:\n\ttrivium.py <IV> <KEY> <INPUT FILE> <OUTPUT FILE>\n")
    print("\tIV= Initial Vector (10 characters)")
    print("\tKey= Initial state of LFSR 2 (10 characters)")
    print("\tInput File= File that needs to be altered")
    print("\tOutput= File to save altered contents in")
    exit()

if len(sys.argv)!=5: #check for correct number of arguments
    print("[-] Invalid Arguments. Please use -h for help")
if len(sys.argv[1])!=10: #check for 80 bit IV
    print("[-] IV must be of 10 characters (80-bits)")
    exit()
if len(sys.argv[2])!=10: #check for 80 bit key
    print("[-] Key must be of 10 characters (80-bits)")
    exit()

LFSR1=getBinStr(getByteArr(sys.argv[1])).ljust(93, '0') #loads IV into first lfsr
print("[+] IV successfully loaded into LFSR1")
LFSR2=getBinStr(getByteArr(sys.argv[2])).ljust(84, '0') #loads key into second lfsr
print("[+] Key successfully loaded into LFSR1")
LFSR3='111'.rjust(111, '0') #sets third lfsr initial state

for i in range(144): #warmup round for trivium
    get8bits()

ofile=open(sys.argv[4], "w", encoding='utf8') #opens file to store encrypted/decrypted data

with open(sys.argv[3], "r", encoding='utf8') as ifile: #opens file to encrypt/decrypt
    while 1:
        nextChar=ifile.read(1) #reads 8 bits from file
        if not nextChar:
            break
        ofile.write(Byte(nextChar).xor(get8bits()).getConvert()) #writes encrypted byte to output file

ofile.close()
print("[+] Success")

