# FreeD-Python
A lightweight Python implementation of the FreeD protocol. 

`freed.py` contains some objects to help interface with FreeD structures. In particular are the `ThreeBytes` and `ThreeBytesSigned` types which define a fixed width integer type of 24 bits that is used in many of the FreeD protocols message payloads. This helps prevent errors like integer overflows.  

The `FreeDWrapper` object can be used to create and set up a `0xD1` Position Poll command to send to a FreeD unit/camera (such as with Unreal Engine's LiveLink plugin). This will take regular python ints and bounds check them. Use the `createFreeD()` method to create an object with raw byte fields, and then use the `encode()` method on that object to serialise it to a byte array that can be sent over the protocol of your choice (such as UDP). 

```python
#                             pitch, yaw, roll, posz, posy, posx, zoom, focus
newcameraposition = FreeDWrapper(0  ,  0,   0, 25000, 1000, -5000, 128, 300)
message = newcameraposition.createFreeD() #adds message metadata + checksum.
message.cameraid = b'\0x01' #Select a camera to send command to - by default this is 0xFF (all cameras).

bytes = message.encode()

# Do things with the bytes..
senddata(bytes)

```

Includes an example program that turns keyboard inputs into FreeD data and pipes them over a UDP socket on `localhost:40000`. The example program relies on Python 3.10 and a Windows terminal. 
