import sys
from PIL import Image
out, files = sys.argv[1], sys.argv[2:]
ims = [Image.open(f).convert('RGB') for f in files]
w, h = ims[0].size
cols = min(4, len(ims)); rows = (len(ims)+cols-1)//cols
sheet = Image.new('RGB', (cols*w + (cols-1)*10, rows*h + (rows-1)*10), (120,120,120))
for i, im in enumerate(ims):
    sheet.paste(im, ((i%cols)*(w+10), (i//cols)*(h+10)))
sheet.save(out)
