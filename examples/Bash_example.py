import subprocess

#Set your VDD Here

VDD = 3.3


#Set the DAC5571 Address, Either 0x4d or 0x4c

address = "0x4d"

while(True):


    bool_value = True
    voltage = 0

    while (bool_value):
            voltagein = input("Enter Voltage 0-"+ str(VDD)+  ": \n")

            if (voltagein == "exit" or voltagein == "quit" or voltagein == "q"):
                exit()

            try:
                attempt = float(voltagein)
            except ValueError:
                print("Wrong Value Type")
                continue

            voltage = float(voltagein)

            if (voltage <= VDD and voltage >= 0 ):
                bool_value = False

    normalizedvoltage = int(voltage / VDD * 4095)



    HexVoltage =  hex(normalizedvoltage)

    hexlist = list(HexVoltage)

    length = len(hexlist)

    majordigit = hexlist[2]
    minordigit = ''.join(hexlist[3:5])

    bashCommand = "i2cset -y 1 "+address+" 0x0" + majordigit + " 0x" + minordigit


    if length == 4:
        minordigit = ''.join(hexlist[2:4])
        bashCommand = "i2cset -y 1 "+address+" 0x00 0x" + minordigit

    if length == 3:
        minordigit = hexlist[2]
        bashCommand = "i2cset -y 1 "+address+" 0x00 0x0" + minordigit

    print(bashCommand)

    try:
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()\

    except subprocess.CalledProcessError as e:
        print("Error executing command: ", e)
        continue


    print("Voltage Propertly Set\n--------------------------------")

    continue
