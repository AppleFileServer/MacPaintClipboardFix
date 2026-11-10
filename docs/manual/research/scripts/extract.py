import sys, macresources
for r in macresources.parse_file(open(sys.argv[1],'rb').read()):
    if bytes(r.type) in (b'CODE',b'PICT'):
        open(f"{sys.argv[2]}/{bytes(r.type).decode()}{r.id}.bin",'wb').write(bytes(r.data))
