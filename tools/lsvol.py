import sys, struct, machfs
data = open(sys.argv[1],'rb').read()
# walk Apple partition map
off=None
for i in range(1,64):
    b=data[i*512:(i+1)*512]
    if b[:2]!=b'PM': break
    start,size=struct.unpack('>II',b[8:16]); ptype=b[48:80].split(b'\0')[0]
    if ptype==b'Apple_HFS': off=start*512; ln=size*512
v=machfs.Volume(); v.read(data[off:off+ln])
print('Volume:', v.name)
def walk(d,p):
    for k,x in d.items():
        if isinstance(x,machfs.Folder): walk(x,p+k+':')
        elif 'paint' in k.lower() or 'clipboard' in k.lower() or 'scrap' in k.lower() or x.type in (b'APPL',) and 'paint' in k.lower():
            vers=''
            try:
                import macresources
                for r in macresources.parse_file(x.rsrc):
                    if r.type==b'vers': vers=r.data[6:6+r.data[6]+1][1:].decode('mac_roman'); break
            except Exception as e: pass
            print(p+k, x.type, x.creator, len(x.data), len(x.rsrc), vers)
walk(v,'')
