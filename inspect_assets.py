from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as E
from PIL import Image,ImageOps,ImageDraw
import re
base=Path('C:/Users/ronal/OneDrive/Área de Trabalho/Faculdade/4. PLANEJAMENTO ESTRATÉGICO')
dest=Path('work/assets');dest.mkdir(exist_ok=True)
for p in base.glob('*gabarito*'):
 print('\n'+p.name)
 with ZipFile(p) as z:
  root=E.fromstring(z.read('word/document.xml'));ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
  for par in root.findall('.//w:p',ns):
   txt=''.join(t.text or '' for t in par.findall('.//w:t',ns))
   if re.match('[A-E][) ]',txt):
    styles=[]
    for r in par.findall('.//w:r',ns):
     props=r.find('w:rPr',ns)
     if props is not None:styles.extend((c.tag.split('}')[-1],c.attrib) for c in props)
    print(txt,styles)
for p in base.glob('*.pptx'):
 if 'Aula 3' not in p.name and 'Aula 2' not in p.name:continue
 with ZipFile(p) as z:
  thumbs=[]
  for f in z.namelist():
   if not f.startswith('ppt/media/'):continue
   try:
    im=Image.open(z.open(f));im.load()
    if im.width<250 or im.height<150:continue
    label=p.stem.split('Aula ')[-1]+' '+Path(f).name
    im.save(dest/(label+'.png'))
    thumb=Image.new('RGB',(440,300),'white');thumb.paste(ImageOps.contain(im.convert('RGB'),(430,270)),(5,25));ImageDraw.Draw(thumb).text((5,5),label,fill='black');thumbs.append(thumb)
   except:pass
  for k in range(0,len(thumbs),12):
   batch=thumbs[k:k+12];sheet=Image.new('RGB',(1320,300*((len(batch)+2)//3)), '#ddd')
   for i,t in enumerate(batch):sheet.paste(t,((i%3)*440,(i//3)*300))
   sheet.save(dest/('sheet'+p.stem.split('Aula ')[-1]+str(k)+'.png'))
