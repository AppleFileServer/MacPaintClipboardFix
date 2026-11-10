import re, sys, zlib
for path in sys.argv[1:]:
    data = open(path, 'rb').read()
    blobs = [data]
    for m in re.finditer(rb'stream\r?\n', data):
        start = m.end(); end = data.find(b'endstream', start)
        try: blobs.append(zlib.decompress(data[start:end]))
        except Exception: pass
    names = set()
    for b in blobs:
        names.update(re.findall(rb'/BaseFont\s*/([A-Za-z0-9+#_.-]+)', b))
    prod = re.findall(rb'/(?:Producer|Creator)\s*\(([^)]*)\)', b''.join(blobs[:1]))
    print(path.split('/')[-1], sorted(n.decode() for n in names), [p.decode('latin1') for p in prod][:2])
