import struct, zlib, sys
def unpackbits(d,o,n):
    out=bytearray()
    while len(out)<n:
        c=d[o]; o+=1
        if c<128: out+=d[o:o+c+1]; o+=c+1
        elif c>128: out+=bytes([d[o]])*(257-c); o+=1
    return bytes(out),o
def decode(d):
    o=10
    assert d[o:o+2]==b'\x11\x01'; o+=2
    imgs=[]
    while o<len(d):
        op=d[o]; o+=1
        if op==0xFF: break
        if op==0x01:
            ln=struct.unpack('>h',d[o:o+2])[0]; o+=ln
        elif op==0xA0: o+=2
        elif op==0xA1:
            o+=2; ln=struct.unpack('>h',d[o:o+2])[0]; o+=2+ln
        elif op in (0x98,0x90):
            rb=struct.unpack('>h',d[o:o+2])[0]; o+=2
            b=struct.unpack('>4h',d[o:o+8]); o+=8
            src=struct.unpack('>4h',d[o:o+8]); o+=8; dst=struct.unpack('>4h',d[o:o+8]); o+=8
            mode=struct.unpack('>h',d[o:o+2])[0]; o+=2
            h=b[2]-b[0]; rows=[]
            for y in range(h):
                if op==0x98 and rb>=8:
                    if rb>250: ln=struct.unpack('>h',d[o:o+2])[0]; o+=2
                    else: ln=d[o]; o+=1
                    row,_=unpackbits(d,o,rb); o+=ln
                else: row=d[o:o+rb]; o+=rb
                rows.append(row)
            imgs.append((rb,b,dst,rows)); print('bits',rb,b,src,dst,mode)
        else:
            print('unknown op',hex(op),'at',o-1); break
    return imgs
def png(path,w,h,rows):
    raw=b''.join(b'\x00'+bytes(255-x for x in r) for r in rows)  # 1=black -> invert for PNG gray1 (0=black)
    def chunk(t,c): return struct.pack('>I',len(c))+t+c+struct.pack('>I',zlib.crc32(t+c)&0xffffffff)
    ihdr=struct.pack('>IIBBBBB',w,h,1,0,0,0,0)
    open(path,'wb').write(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',ihdr)+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))
for n in sys.argv[2:]:
    d=open(f"{sys.argv[1]}/PICT{n}.bin",'rb').read()
    for i,(rb,b,dst,rows) in enumerate(decode(d)):
        w=b[3]-b[1]; h=b[2]-b[0]
        # scale 2x for legibility
        big=[]
        for r in rows:
            bits=''.join(f'{x:08b}' for x in r)[:w]
            bits2=''.join(c*2 for c in bits); bits2+= '0'*((-len(bits2))%8)
            br=bytes(int(bits2[k:k+8],2) for k in range(0,len(bits2),8))
            big+= [br,br]
        png(f"{sys.argv[1]}/PICT{n}_{i}.png",w*2,h*2,big)
for n in sys.argv[2:]:
    d=open(f"{sys.argv[1]}/PICT{n}.bin",'rb').read()
    allrows=[]
    for (rb,b,dst,rows) in decode(d): allrows+=rows
    big=[]
    for r in allrows:
        bits=''.join(f'{x:08b}' for x in r)[:416]
        bits2=''.join(c*2 for c in bits)
        br=bytes(int(bits2[k:k+8],2) for k in range(0,len(bits2),8)); big+=[br,br]
    png(f"{sys.argv[1]}/PICT{n}_full.png",832,len(big),big)
