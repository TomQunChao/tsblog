import pyshark
import base64
captures = pyshark.FileCapture('attachment.pcapng')
payload = b""
for capture in captures:
    if hasattr(capture.tcp,"payload") :
        if capture.ip.src == '192.168.1.103':
            payload += base64.b16decode(bytes(capture.tcp.payload.replace(":","").upper(),encoding='utf-8'))
            # print(payload)

f = open("out.h264","wb")
ind=payload.find(b'\x00\x00\x00\x01\x67\x42')
f.write(payload[ind:])
