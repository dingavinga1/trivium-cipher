# trivium-cipher
A pure python-based implementation of the industry leading stream cipher- Trivium. 

## What is Trivium?
Trivium is the industry standard for stream ciphers. The most common application of Trivium is cellular network communication. This cipher is based on <b>CSPRNG(Cryptographicaly Secure Pseudo-Random Number Generation)</b>

## Usage
This implementation allows encryption of text files using Trivium. Currently it only supports files using standard UTF-8 encoding. However, there are plans for extending this implementation to all binary files. <br/><br/>
Here is how to use it:

Use ```trivium.py -h``` for the help menu which displays the following output:<br/>
```
Usage:
  trivium.py <IV> <KEY> <INPUT FILE> <OUTPUT FILE>
  
  IV= Initial Vector (10 characters)
  Key= Initial state of LFSR 2 (10 characters)
  Input File= File that needs to be altered
  Output File= File to save altered contents in
```
## How Trivium works
Trivium uses the power of <b>Linear Feedback Shift Registers (LFSRs)</b> which are implemented on the hardware level for bit rotation. However, in Trivium it comes with some kinks. Here is a circuit diagram of the hardware level implementation:

![Internal-structure-of-the-stream-cipher-Trivium](https://user-images.githubusercontent.com/88616338/198330201-bf7dd161-12d0-46c7-b055-d8f5d59e1272.png)

The recursive representation of Trivium is as follows:
- a<sub>i</sub> = c<sub>i−66</sub> + c<sub>i−111</sub> + c<sub>i−110</sub> • c<sub>i−109</sub> + a<sub>i−69</sub>
- b<sub>i</sub> = a<sub>i−66</sub> + a<sub>i−93</sub> + a<sub>i−92</sub> • a<sub>i−91</sub> + b<sub>i−78</sub>
- c<sub>i</sub> = b<sub>i−69</sub> + b<sub>i−84</sub> + b<sub>i−83</sub> • b<sub>i−82</sub> + c</sub>i−87</sub>

Output equation:
- r<sub>i</sub> = c<sub>i−66</sub> + c<sub>i−111</sub> + a<sub>i−66</sub> + a<sub>i−93</sub> + b<sub>i−69</sub> + b<sub>i−84</sub>

To create the CSPRNG properly, we need to load the registers with some initial vector. For this, we go through the following steps:
- Load an 80 bit key into the first 80 bits of the first LFSR
- Load an 80 bit Initial Vector into the first 80 bits of the second LFSR
- Turn on the 3 right-most bits in the third LFSR

## Credits
This project is free to use. However, it would be appreciated if you fork this repository if you use my implementation for your own project. 
