import serial
ser= serial.Serial('/dev/ttyUSB0', 57600)
while True:
    indata= []
    d= ''
    while (d!='\xff') and (len(indata)<100):
        d= ser.read()
        indata.append(d)
    if (indata[0]=='\xfd') and (indata[1]=='\xfe'):
        hibyte= ord(indata[2])
        lobyte= ord(indata[3])
        val= (hibyte<<8)+lobyte
        print val
