"""
Python Library for MCP4922 DAC using Raspberry Pi 5

Version for Edinburgh DAH course, replacing webiopi library

Based on https://github.com/mrwunderbar666/Python-RPi-MCP4922

"""

import spidev

class MCP4922:
  """Python Library for MCP4922 ADC using Raspberry Pi 5"""

  def __init__(self, chip=1, vref=3.3, autoShutdown=False):
    """Initialise MCP4922 with an SPI chip number (0 or 1) and reference voltage"""

    # Configuration
    self.vref = vref
    self.doPrint = False
    self.autoShutdown = autoShutdown

    # Use the spidev library for communication
    if chip not in [0,1]:
      raise ValueError('MCP4922 says: Invalid chip chosen (' + str(chip) + ')! Options are 0 or 1')
    self.spi = spidev.SpiDev(0, chip)
    self.spi.max_speed_hz=1000000
    self.spi.mode = 0
    self.spi.lsbfirst = False
    #self.spi.cshigh = False

  def __del__(self):

    if self.autoShutdown:
      self.shutdown(0)
      self.shutdown(1)
    self.close()

  def printRawData(self, value):
    """Display all binary communication to and from the MCP4922"""

    self.doPrint = value

  def analogCount(self):
    """Return the number of DAC output pins"""

    return 2

  def analogResolution(self):
    """Return the DAC resolution"""

    return 12

  def analogMaximum(self):
    """Return the maximum value for a DAC measurement"""

    return 4095

  def analogReference(self):
    """Return the configured reference voltage"""

    return self.vref

  def analogWrite(self, channel, value):
    """Set the DAC output for a specific pin (expressed as integer)"""

    if channel == 0:
      output = 0x3000
    elif channel == 1:
      output = 0xb000
    else:
      raise ValueError('MCP4922 says: Invalid channel chosen (' + str(channel) + ')! Options are 0 or 1')

    if value > 4095:
      value = 4095
    if value < 0:
      value = 0

    output |= value
    buf0 = (output >> 8) & 0xff
    buf1 = output & 0xff

    # Write command to MCP4922
    self.spi.writebytes([buf0, buf1])

    if self.doPrint:
      print( "to MCP4922: " + str( [buf0, buf1] ) )

  def analogWriteFloat(self, channel, value):
    """Set the DAC output for a specific pin (expressed as float)"""

    self.analogWrite( channel, int( value * float( self.analogMaximum() ) ) )

  def analogWriteVolt(self, channel, value):
    """Set the DAC output for a specific pin (expressed as voltage)"""

    self.analogWriteFloat( channel, value / self.analogReference() )

  def shutdown(self, channel):
    """Turn off DAC output for a specific pin"""

    if channel == 0:
      output = 0x2000
    elif channel == 1:
      output = 0xA000
    else:
      raise ValueError('MCP4922 says: Invalid channel chosen (' + str(channel) + ')! Options are 0 or 1')

    buf0 = (output >> 8) & 0xff
    buf1 = output & 0xff

    # Write command to MCP4922
    self.spi.writebytes([buf0, buf1])

    if self.doPrint:
      print( "to MCP4922: " + str( [buf0, buf1] ) )

  def close(self):
    """Disconnect communication with the MCP4922"""

    self.spi.close()

