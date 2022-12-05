from decimal import Overflow
from typing import Literal, SupportsIndex

#stores raw bytes for encoding. Use the FreeDWrapper as an interface for regular ints
class FreeD:
    identifier: 'bytes'
    cameraID: 'bytes'
    pitch: 'bytes'
    yaw: 'bytes'
    roll: 'bytes'
    pos_z: 'bytes'
    pos_y: 'bytes'
    pos_x: 'bytes'
    zoom: 'bytes'
    focus: 'bytes'
    reserved: 'bytes'

    def __init__(self, pitch: 'int', yaw: 'int', roll: 'int', pos_z: 'int',  pos_y: 'int', pos_x: 'int', zoom: 'int', focus: 'int') -> None:
        # if (any([x > 0xFFFFFF or x < 0x00 for x in [pitch, yaw, roll, pos_z, pos_y, pos_x, zoom, focus]])):
        #     raise ValueError("Maximum of 3 bytes allowed in location fields")

        self.identifier = b'\xD1'
        self.cameraID = b'\xFF'
        self.reserved = b'\x00\x00'
        self.pitch = pitch.to_bytes(3, 'big', signed=True)
        self.yaw = yaw.to_bytes(3, 'big', signed=True)
        self.roll = roll.to_bytes(3, 'big', signed=True)
        self.pos_z = pos_z.to_bytes(3, 'big', signed=True)
        self.pos_y = pos_y.to_bytes(3, 'big', signed=True)
        self.pos_x = pos_x.to_bytes(3, 'big', signed=True)
        self.zoom = zoom.to_bytes(3, 'big', signed=False)
        self.focus = focus.to_bytes(3, 'big', signed=False)

    #calculates a checksum according to the protocol
    @staticmethod
    def checksum(*args) -> 'bytes':
        checksum = int(0x40)
        for arg in args:
            for byte in arg:
                checksum = (checksum - int(byte)) % 256

        assert (checksum < 256 and checksum >= 0)
        return checksum.to_bytes(1, 'big', signed=False)

    #encodes self into an array of bytes
    def encode(self) -> 'bytes':
        data = (self.identifier, self.cameraID, self.pitch, self.yaw,
                self.roll, self.pos_z, self.pos_y, self.pos_x, self.zoom,
                self.focus, self.reserved)

        serial = self.identifier + self.cameraID + self.pitch + self.yaw + \
            self.roll + self.pos_z + self.pos_y + self.pos_x + self.zoom + \
            self.focus + self.reserved + FreeD.checksum(*data)
        assert (len(serial) == 29)  # somethings gone wrong if not
        return serial


# int type that is limited to 3 bytes (sort of a hack)
class ThreeBytes(int):
    field: 'int'
    INT_MAX: 'int' = 0xFFFFFF
    INT_MIN: 'int' = 0x00

    def __init__(self, new: 'int'):
        if (new > self.INT_MAX or new < self.INT_MIN):
            raise ValueError("Maximum of 3 bytes allowed!")

        self.field = new

    def __add__(self, __x: int) -> int:

        if (self.field + __x > self.INT_MAX or self.field + __x < self.INT_MIN):
            raise OverflowError("Resulting value would be too large to store!")
        return self.field + __x

    def __sub__(self, __x: int) -> int:
        if (self.field - __x > self.INT_MAX or self.field - __x < self.INT_MIN):
            raise OverflowError("Resulting value would be too large to store!")
        return self.field - __x

    def __mul__(self, __x: int) -> int:
        if (self.field * __x > self.INT_MAX or self.field * __x < self.INT_MIN):
            raise OverflowError("Resulting value too large to store!")
        return self.field * __x
    
    def to_bytes(self, length: SupportsIndex, byteorder: Literal["little", "big"], *, signed: bool = ...) -> bytes:
        return self.field.to_bytes(length, byteorder, signed=signed)

#signed variant of 3bytetype
class ThreeBytesSigned(ThreeBytes):
    INT_MAX: 'int' = 8388608
    INT_MIN: 'int' = -8388608

# native types for FreeD raw bytes
class FreeDWrapper:
    pitch: 'ThreeBytesSigned'
    yaw: 'ThreeBytesSigned'
    roll: 'ThreeBytesSigned'
    pos_z: 'ThreeBytesSigned'
    pos_x: 'ThreeBytesSigned'
    pos_y: 'ThreeBytesSigned'
    zoom: 'ThreeBytes'
    focus: 'ThreeBytes'

    def __init__(self, pitch: 'int', yaw: 'int', roll: 'int', pos_z: 'int',  pos_y: 'int', pos_x: 'int', zoom: 'int', focus: 'int') -> None:
        # if (any([x > 0xFFFFFF or x < 0x00 for x in [pitch, yaw, roll, pos_z, pos_y, pos_x, zoom, focus]])):
        #     raise ValueError("Maximum of 3 bytes allowed in location fields")

        self.pitch = ThreeBytesSigned(pitch)
        self.yaw = ThreeBytesSigned(yaw)
        self.roll = ThreeBytesSigned(roll)
        self.pos_z = ThreeBytesSigned(pos_z)
        self.pos_y = ThreeBytesSigned(pos_y)
        self.pos_x = ThreeBytesSigned(pos_x)
        self.zoom = ThreeBytes(zoom)
        self.focus = ThreeBytes(focus)

    #returns a struct with byte representations of fields, ready to encode into an array.
    def createFreeD(self) -> 'FreeD':
        return FreeD(self.pitch, self.yaw, self.roll, self.pos_z, self.pos_y, self.pos_x, self.zoom, self.focus)
