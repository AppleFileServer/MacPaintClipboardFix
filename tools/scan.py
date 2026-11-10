import sys, macresources
rs=list(macresources.parse_file(open(sys.argv[1],'rb').read()))
traps={0xA9FC:'ZeroScrap',0xA9FA:'UnloadScrap',0xA9F9:'InfoScrap',0xA9FD:'GetScrap',0xA9FB:'LoadScrap',0xA9FE:'PutScrap',0xA000:'_Open',0xA001:'_Close',0xA013:'_FlushVol',0xA015:'_GetVol',0xA215:'_HGetVol',0xA008:'_Create',0xA210:'_GetFileInfo/HFS',0xA060:'_HFSDispatch'}
for r in rs:
    if r.type!=b'CODE': continue
    d=r.data
    hits=[]
    for i in range(0,len(d)-1,2):
        w=(d[i]<<8)|d[i+1]
        if w in traps: hits.append((i,traps[w]))
    if hits: print('CODE',r.id,len(d),hits)
    # lowmem refs
    for lm,name in ((0x0A58,'SysMap'),(0x0210,'BootDrive'),(0x0960,'ScrapInfo/ScrapSize'),(0x0970,'ScrapTag')):
        pat=bytes([lm>>8,lm&255])
        for i in range(0,len(d)-3,2):
            if d[i:i+2] in (b'\x30\x38',b'\x3f\x38',b'\x20\x78',b'\x22\x78',b'\x32\x38',b'\x34\x38',b'\x2f\x38',b'\x41\xf8',b'\x43\xf8') and d[i+2:i+4]==pat:
                print('  CODE',r.id,'off',hex(i),name, d[i:i+4].hex())
