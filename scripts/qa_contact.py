from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import sys
R=Path(__file__).resolve().parents[1]
for part in sys.argv[1:]:
 files=sorted((R/'qa').glob(part+'-*.png'),key=lambda x:int(x.stem.rsplit('-',1)[-1]))
 for start in range(0,len(files),6):
  chunk=files[start:start+6];thumbs=[]
  for p in chunk:
   im=Image.open(p).convert('RGB');im.thumbnail((600,740))
   panel=Image.new('RGB',(620,im.height+35),'#eeeeee');panel.paste(im,((620-im.width)//2,25));ImageDraw.Draw(panel).text((10,6),p.stem,fill='black');thumbs.append(panel)
  h=max(t.height for t in thumbs);out=Image.new('RGB',(1240,h*((len(thumbs)+1)//2)),'white')
  for i,t in enumerate(thumbs):out.paste(t,((i%2)*620,(i//2)*h))
  out.save(R/'qa'/('contact_'+part+'_'+str(start//6+1)+'.png'))
 print(part,len(files),'pages reviewed in contact sheets')
