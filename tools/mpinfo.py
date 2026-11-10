import sys, struct, machfs, macresources, re
data=open(sys.argv[1],'rb').read()
for i in range(1,64):
    b=data[i*512:(i+1)*512]
    if b[:2]!=b'PM': break
    start,size=struct.unpack('>II',b[8:16])
    if b[48:80].split(b'\0')[0]==b'Apple_HFS': off=start*512; ln=size*512
v=machfs.Volume(); v.read(data[off:off+ln])
f=v['Graphics']['MacPaint']
print('created',f.crdate,'modified',f.mddate)
open(sys.argv[2],'wb').write(f.rsrc)
from collections import Counter
rs=list(macresources.parse_file(f.rsrc))
print(Counter(r.type for r in rs))
for r in rs:
    if r.type in (b'STR ',b'DITL',b'ALRT',b'STR#'):
        t=re.findall(rb'[\x20-\x7e\xa9]{5,}',r.data)
        print(r.type,r.id,t[:6])
    if r.type==b'CODE': print('CODE',r.id,r.name,len(r.data))
