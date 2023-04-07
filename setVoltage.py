import smbus

def setVoltage(voltage, VDD, address):
    """
    Sets the voltage for a DAC5571 chip connected to an I2C bus.

    Args:
        voltage (float): The desired voltage to set.
        VDD (float): The maximum voltage value.
        address (int): The I2C address of the DAC5571 (either 0x4d or 0x4c).

    Returns:
        None
    """
    # Initialize the SMBus object for the specified I2C bus
    bus = smbus.SMBus(1)

    # Normalize the voltage value and convert it to a hexadecimal string
    normalized_voltage = int(voltage / VDD * 4095)
    hex_voltage = hex(normalized_voltage)
    hex_list = list(hex_voltage)

    length = len(hex_list)

    # Extract major and minor digits from the hexadecimal string and construct the I2C compatible command to set the DAC
    major_digit = hex_list[2]
    minor_digit = ''.join(hex_list[3:5])
    # These three if loops configure the address correctly depending on how many digits the hex output is
    if length == 4:
        minor_digit = ''.join(hex_list[2:4])
        bus.write_i2c_block_data(address, 0x00, [int(minor_digit, 16)])

    if length == 3:
        minor_digit = hex_list[2]
        bus.write_i2c_block_data(address, 0x00, [int('0' + minor_digit, 16)])

    if length == 5:
        bus.write_i2c_block_data(address, int('0' + major_digit, 16), [int(minor_digit, 16)])

