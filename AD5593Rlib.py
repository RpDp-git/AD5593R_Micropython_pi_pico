#POINTERS
AD5593R_MODE_CONF = 0x00
AD5593R_MODE_DAC_WRITE = 0x10
AD5593R_MODE_ADC_READBACK = 0x40
AD5593R_MODE_DAC_READBACK = 0x50
AD5593R_MODE_GPIO_READBACK = 0x60
AD5593R_MODE_REG_READBACK = 0x70

#REGISTER_ADDRESSES
AD5593R_REG_NULL = 0x00
AD5593R_REG_ADC_SEQUENCE = 0x02
AD5593R_REG_GP_CONTROL = 0x03
AD5593R_REG_ADC_CONFIG = 0x04
AD5593R_REG_DAC_CONFIG = 0x05
AD5593R_REG_PULL_DOWN = 0x06
AD5593R_REG_LDAC_MODE = 0x07
AD5593R_REG_GPIO_WR_CONFIG = 0x08
AD5593R_REG_GPIO_WR_DATA = 0x09
AD5593R_REG_GPIO_RD_CONFIG = 0x0A
AD5593R_REG_POWER_REF_CTRL = 0x0B
AD5593R_REG_OPEN_DRAIN_CFG = 0x0C
AD5593R_REG_THREE_STATE = 0x0D
AD5593R_REG_RESERVED = 0x0E
AD5593R_REG_SOFT_RESET = 0x0F

# ADAC Configuration Data Bytes
# --------------------------------
# write into MSB after _ADAC_POWER_REF_CTRL command to enable VREF


class AD5593R:
    
    AD5593R_ADDR = 0x10 #Enter I2C address
    
    def __init__(self, i2c, address=AD5593R_ADDR, IO_config = ['ADC','ADC','ADC','ADC','DAC','DAC','DAC','DAC']): #By default 4xADC and 4xDAC
        self.i2c = i2c
        self.address = address
        self.enable_vref()       #Enables internal reference
        self.set_ldac_mode(0x00) #Auto transfer values of the DAC register into DAC voltage
        self.IO_config = IO_config
        self.dac_channels = []
        self.adc_channels = []
        self.set_IO()

    def set_IO(self): # sets channels as ADCs or DACs according to IO_config 
        self.dac_channels = []
        self.adc_channels = []
        for i, ch in enumerate(self.IO_config):
            if ch == 'DAC':
                self.dac_channels.append(i)
            elif ch == 'ADC':
                self.adc_channels.append(i)
        
        self.set_dac_channels(self.dac_channels)
        self.set_adc_channels(self.adc_channels)
        self.set_adc_sequence(self.adc_channels) #conversion sequence

    def enable_vref(self): #2.5v internal reference
        pointer_byte = (AD5593R_MODE_CONF << 4) | AD5593R_REG_POWER_REF_CTRL
        self.i2c.writeto_mem(self.address, pointer_byte ,bytearray([0x02, 0x00]))
    
    def disable_vref(self):
        pointer_byte = (AD5593R_MODE_CONF << 4) | AD5593R_REG_POWER_REF_CTRL
        self.i2c.writeto_mem(self.address, pointer_byte ,bytearray([0x00, 0x00]))

    def set_dac_channels(self, channels):
        pointer_byte = (AD5593R_MODE_CONF << 4) | AD5593R_REG_DAC_CONFIG
        dac_config = sum([1 << ch for ch in channels])
        self.i2c.writeto_mem(self.address, pointer_byte ,bytearray([AD5593R_REG_NULL,dac_config]))

    def set_ldac_mode(self, mode): 'Auto Transfer or not'
        pointer_byte = (AD5593R_MODE_CONF << 4) | AD5593R_REG_LDAC_MODE
        self.i2c.writeto_mem(self.address, pointer_byte , bytearray([AD5593R_REG_NULL,mode]))

    def write_dac(self, channel, value):
        pointer_byte = AD5593R_MODE_DAC_WRITE | (channel & 0x07)
        msb = (value >> 8) & 0xFF
        lsb = value & 0xFF
        self.i2c.writeto_mem(self.address, pointer_byte , bytearray([msb, lsb]))

    def read_dac(self, channel): #Read back a value from the DAC register
        pointer_byte = AD5593R_MODE_DAC_READBACK | (channel & 0x07)
        self.i2c.writeto(self.address, bytearray([pointer_byte]))
        data = self.i2c.readfrom(self.address, 2)
        value = (data[0] << 8) | data[1]
        value = value & 0x0FFF
        return value
    
    def set_adc_sequence(self, channels,repeat = False):
        pointer_byte = (AD5593R_MODE_CONF << 4) | AD5593R_REG_ADC_SEQUENCE
        seq_data = sum([1 << ch for ch in channels])
        rep_byte = 0x02 if repeat else 0x00
        self.i2c.writeto_mem(self.address, pointer_byte, bytearray([rep_byte,seq_data]))

    def set_adc_channels(self, channels):
        pointer_byte = (AD5593R_MODE_CONF << 4) | AD5593R_REG_ADC_CONFIG
        adc_config = sum([1 << ch for ch in channels])
        self.i2c.writeto_mem(self.address, pointer_byte, bytearray([AD5593R_REG_NULL,adc_config]))

    def read_adc(self, channel):
        pointer_byte = AD5593R_MODE_ADC_READBACK
        self.set_adc_sequence([channel])
        self.i2c.writeto(self.address, bytearray([pointer_byte]))
        data = self.i2c.readfrom(self.address, 2)
        value = (data[0] << 8) | data[1]
        value = value & 0x0FFF
        return value
