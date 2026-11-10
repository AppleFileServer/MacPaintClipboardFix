import sys, struct, macresources, collections
data=open(sys.argv[1],'rb').read()
rs=list(macresources.parse_file(data))
c=collections.Counter(r.type for r in rs)
print(dict(c))
def ps(b,o):
    n=b[o]; return b[o+1:o+1+n].decode('mac_roman'), o+1+n
for r in rs:
    t=r.type.decode('mac_roman') if isinstance(r.type,bytes) else r.type
    d=bytes(r.data)
    hdr=f"== {t} {r.id} name={r.name!r} len={len(d)}"
    if t=='MENU':
        mid,w,h,proc,_,en=struct.unpack('>hhhhhI',d[:14])
        title,o=ps(d,14)
        print(hdr, f"menuID={mid} enable={en:032b}", repr(title))
        i=1
        while d[o]!=0:
            s,o=ps(d,o); icon,key,mark,style=d[o:o+4]; o+=4
            enabled = bool(en & (1<<i)) and bool(en&1)
            print(f"   {i:2d} {s!r} key={chr(key) if key else ''!r} mark={mark} style={style} enabled={enabled}")
            i+=1
    elif t in('DITL',):
        n=struct.unpack('>h',d[:2])[0]+1; o=2; print(hdr,f"{n} items")
        for i in range(n):
            o+=4; rect=struct.unpack('>4h',d[o:o+8]); o+=8; typ=d[o]; ln=d[o+1]; o+=2
            body=d[o:o+ln]; o+=ln+(ln&1)
            tt=typ&0x7f
            if tt in(4,5,6,7,8,16): body=body.decode('mac_roman')
            print(f"   {i+1} type={typ} rect={rect} {body!r}")
    elif t in('DLOG','ALRT'):
        print(hdr, d.hex())
        if t=='DLOG':
            print('   rect',struct.unpack('>4h',d[:8]),'proc',struct.unpack('>h',d[8:10]),'items',struct.unpack('>h',d[18:20]), ps(d,20)[0] if len(d)>20 else '')
        else:
            print('   rect',struct.unpack('>4h',d[:8]),'itemsID',struct.unpack('>h',d[8:10]),'stages',d[10:12].hex())
    elif t=='STR ':
        print(hdr, repr(ps(d,0)[0]))
    elif t=='STR#':
        n=struct.unpack('>h',d[:2])[0];o=2;print(hdr)
        for i in range(n):
            s,o=ps(d,o);print('  ',i+1,repr(s))
    elif t in('MPNT','vers'):
        print(hdr, repr(d))
    elif t in('BNDL','FREF','CNTL','WIND','SIZE'):
        print(hdr, d.hex(), repr(d))
    else:
        print(hdr)
