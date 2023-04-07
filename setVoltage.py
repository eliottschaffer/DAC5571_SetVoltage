import subprocess

# Set the maximum voltage value (VDD)
VDD = 3.3

# Set the I2C address of the DAC5571 (either 0x4d or 0x4c)
address = "0x4d"

# Loop indefinitely to continuously prompt the user for a desired voltage
while(True):

    # Initialize the flag variable and voltage variable
    bool_value = True
    voltage = 0

    # Prompt the user for a voltage value until a valid value is entered
    while (bool_value):
        voltagein = input("Enter Voltage 0-"+ str(VDD)+  ": \n type 'exit', 'quit', or 'q' to terminate the program")

        # Allow the user to exit the loop by typing 'exit', 'quit', or 'q'
        if (voltagein == "exit" or voltagein == "quit" or voltagein == "q"):
            exit()

        try:
            attempt = float(voltagein)
        except ValueError:
            # Print an error message if the entered value is not a valid number
            print("Wrong Value Type")
            continue

        # Convert the input voltage to a float and validate that it falls within the acceptable range
        voltage = float(voltagein)
        if (voltage <= VDD and voltage >= 0 ):
            bool_value = False

    # Normalize the voltage value and convert it to a hexadecimal string
    normalizedvoltage = int(voltage / VDD * 4095)

    HexVoltage =  hex(normalizedvoltage)

    # Convert the hexadecimal string to a list of characters, extract major and minor digits, and construct the I2C compatible command to set the DAC
    hexlist = list(HexVoltage)

    length = len(hexlist)

    majordigit = hexlist[2]
    minordigit = ''.join(hexlist[3:5])

    bashCommand = "i2cset -y 1 "+address+" 0x0" + majordigit + " 0x" + minordigit

    # If the hexadecimal string is 4 characters long, set the minor digit to the last two characters
    if length == 4:
        minordigit = ''.join(hexlist[2:4])
        bashCommand = "i2cset -y 1 "+address+" 0x00 0x" + minordigit

    # If the hexadecimal string is 3 characters long, set the minor digit to the last character
    if length == 3:
        minordigit = hexlist[2]
        bashCommand = "i2cset -y 1 "+address+" 0x00 0x0" + minordigit

    print(bashCommand)

    try:
        # Execute the I2C command
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    except subprocess.CalledProcessError as e:
        # Print an error message if there is an error executing the I2C command
        print("Error executing command: ", e)
        continue

    # Print a message


