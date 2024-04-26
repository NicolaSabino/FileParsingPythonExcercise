# Acceleration file parser - Code challenge

Consider an embedded system in which the main processor receives a stream of data from a variety of
sensors. The data stream consists of a sequence of messages, in ASCII text format. One data source is a 3-
axis accelerometer. Within the data stream, accelerometer messages have the following structure:

```txt
#G4XXXYYYZZZCC\r\n
```

The message always begins with the identifier #G4 and ends with \r\n. The message is fixed length. The
two hex digits, CC, represent a checksum for the message. CC is calculated by adding the ASCII values
corresponding to the hex digits from the # to the last character before the checksum itself. The addition
is 8 bit, so it overflows each time the sum exceeds 255.

For example:

```txt
#G4001FFF03DA8\r\n
```

The checksum is “A8”. The 8-bit sum of the preceding characters is 168 (0xA8). XXX, YYY and ZZZ
correspond the accelerometer's X, Y and Z axis readings. Each axis reading is a 12-bit value, represented
in the message using 3 hexadecimal digits.

For example:

```txt
#G4001FFF03DA8\r\n
XXX=001
YYY=FFF
ZZZ=03D
```

The axis readings are signed values and are encoded using 2's complement. In 12-bit 2's complement, the
representable range is -2048 to +2047. So, in the above example, the y-axis value of 0xFFF corresponds to
the decimal value -1. Note that a 1G acceleration due to gravity is reported as decimal 64 or 0x40. Hence
the maximum absolute force that can be reported is 2048/64 = 32G.

## Instructions

You will be provided with a text file containing sample data. You are required to write a Python program
that performs the following:

1. Reads the data from the sample data file. Data reading should be performed in a loop, with each line
of being read during each iteration of the loop.

2. For each iteration of the loop, each line of data from step 1 should be provided as input to a method
of a Python class that parses the input to extract accelerometer data messages. Your code should
validate the checksum to ensure that the message is not corrupt. Messages with an invalid checksum
should be ignored.

3. When an accelerometer message is extracted, it should be further parsed to extract the X, Y and Z axis
values as described previously. The axis values should be represented as floating point values, in units of
G where, as discussed previously, 0x40 corresponds to 1G.

4. The decoded accelerometer axis value should be written to an output text file.

5. The first line of the output file should be an ISO-8601 UTC timestamp of the form YYYY-MM-
DDTHH:MM:SSZ. Each subsequent line of the file should correspond to one decoded accelerometer
message and have the form

6. The Python class should provide a method to enable a Z-axis offset. The Z-axis values in the data file
include a 1G acceleration due to gravity. If the Z-axis offset is enabled, then a 1G offset should be applied
to the Z-axis values before they are writing to the output file.

7. If an absolute axis value of more than 0.2G is detected on the Y-axis for 3 or more consecutive
accelerometer messages, the text `[ALERT]` should be appended to the last message of the sequence in
the output file, e.g.

    ```txt
    ...
    X=0.10, Y=0.10, Z=0.
    X=0.10, Y=0.41, Z=0.
    X=0.10, Y=0.43, Z=0.
    X=0.10, Y=0.42, Z=0.10 [ALERT]
    ...
    ```

8. The Python class should collect the following statistics about the accelerometer data:
    a. Total number of valid accelerometer messages parsed
    b. Total number of accelerometer messages with invalid checksum
    c. Maximum values of X, Y and Z axes
    d. Total number of alerts encountered

Your program should output these statistics to the standard output after the main data processing loop
has completed.
