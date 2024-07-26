"""
Python Library for MCP23S17 io expander using Raspberry Pi 5

Version for Edinburgh DAH course, replacing webiopi library

"""

import spidev

class MCP23S17:
  """Python Library for MCP23S17 io expander using Raspberry Pi 5"""

  def __init__(self, chip=0, address=0x20):
    """Initialise MCP23S17 with an SPI chip number (0 or 1) and custom address"""

    # 3 bits of address to work with, starting from 0x20
    if address < 0x20 or address > 0x27:
      raise ValueError('MCP23S17 says: Invalid device ID chosen ({:02X})! Options are 0x20-0x27'.format(address))
    self.address = address
    self.doPrint = False

    # Use the spidev library for communication
    if chip not in [0,1]:
      raise ValueError('MCP23S17 says: Invalid chip chosen (' + str(chip) + ')! Options are 0 or 1')
    self.spi = spidev.SpiDev(0, chip)
    self.spi.max_speed_hz=10000000
    self.spi.mode = 0
    self.spi.lsbfirst = False
    #self.spi.cshigh = False

  def __del__(self):

    self.close()

  def printRawData(self, value):
    """Display all binary communication to and from the MCP23S17"""

    self.doPrint = value

  def digitalCount(self):
    """Return the number of I/O pins"""

    return 16

  def rawIO(self, a, b, c):
    """Direct binary communication with the MCP23S17"""

    # Write command to MCP23S17, read its response
    data = self.spi.xfer2([a, b, c])

    if self.doPrint:
      print( "to MCP23S17: " + str( [a, b, c] ) )
      print( "from MCP23S17: " + str( data ) )

    return data[2]

  def portReadA(self):
    """Read from all bank A pins simultaneously, one binary bit per pin"""

    return self.rawIO( (self.address << 1) + 1, 18, 0 )

  def portReadB(self):
    """Read from all bank B pins simultaneously, one binary bit per pin"""

    return self.rawIO( (self.address << 1) + 1, 19, 0 )

  def portRead(self):
    """Read from all pins simultaneously, one binary bit per pin"""

    return ( self.portReadB() << 8 ) + self.portReadA()

  def digitalRead(self, channel):
    """Read high or low value from a specified pin"""

    if channel < 0 or channel > 15:

      raise ValueError('MCP23S17 says: Invalid channel chosen (' + str(channel) + ')! Options are 0-15')

    elif channel < 8:

      return bool( self.portReadA() & ( 1 << channel ) )

    else:

      return bool( self.portReadB() & ( 1 << (channel-8) ) )

  def portWriteA(self, value):
    """Write to all bank A pins simultaneously, one binary bit per pin"""

    self.rawIO( (self.address << 1) + 0, 18, value )

  def portWriteB(self, value):
    """Write to all bank B pins simultaneously, one binary bit per pin"""

    self.rawIO( (self.address << 1) + 0, 19, value )

  def portWrite(self, value):
    """Write to all pins simultaneously, one binary bit per pin"""

    self.portWriteA( value & 0xFF )
    self.portWriteB( ( value >> 8 ) & 0xFF )

  def digitalWrite(self, channel, value):
    """Write high or low value to a specified pin"""

    if channel < 0 or channel > 15:

      raise ValueError('MCP23S17 says: Invalid channel chosen (' + str(channel) + ')! Options are 0-15')

    elif channel < 8:

      # Get current state
      currentState = self.portReadA()

      # Zero the relevant channel
      newState = currentState & ~( 1 << channel )

      # Set the channel high if requested
      if value:
        newState += ( 1 << channel )

      self.portWriteA( newState )

    else:

      # Get current state
      currentState = self.portReadB()

      # Zero the relevant channel
      newState = currentState & ~( 1 << (channel-8) )

      # Set the channel high if requested
      if value:
        newState += ( 1 << (channel-8) )

      self.portWriteB( newState )

  def getModeA(self):
    """Get the mode of all bank A pins simultaneously, one binary bit per pin"""

    return self.rawIO( (self.address << 1) + 1, 0, 0 )

  def getModeB(self):
    """Get the mode of all bank B pins simultaneously, one binary bit per pin"""

    return self.rawIO( (self.address << 1) + 1, 1, 0 )

  def setModeA(self, value):
    """Set the mode of all bank A pins simultaneously, one binary bit per pin"""

    self.rawIO( (self.address << 1) + 0, 0, value )

  def setModeB(self, value):
    """Set the mode of all bank B pins simultaneously, one binary bit per pin"""

    self.rawIO( (self.address << 1) + 0, 1, value )

  def setMode(self, channel, value):
    """Set the mode (input or output) of a specific pin"""

    if channel < 0 or channel > 15:

      raise ValueError('MCP23S17 says: Invalid channel chosen (' + str(channel) + ')! Options are 0-15')

    elif channel < 8:

      # Get current state
      currentState = self.getModeA()

      # Zero the relevant channel
      newState = currentState & ~( 1 << channel )

      # Set the channel high if requested
      if value:
        newState += ( 1 << channel )

      self.setModeA( newState )

    else:

      # Get current state
      currentState = self.getModeB()

      # Zero the relevant channel
      newState = currentState & ~( 1 << (channel-8) )

      # Set the channel high if requested
      if value:
        newState += ( 1 << (channel-8) )

      self.setModeB( newState )

  def setInput(self, channel):
    """Set the mode of a specific pin to input"""

    self.setMode(channel, 1)

  def setOutput(self, channel):
    """Set the mode of a specific pin to output"""

    self.setMode(channel, 0)

  def close(self):
    """Disconnect SPI communication with the MCP23S17"""

    self.spi.close()

