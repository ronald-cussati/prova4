from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import re,json
import pypdf
base=Path('C:/Users/ronal/OneDrive/Área de Trabalho/Faculdade/4. PLANEJAMENTO ESTRATÉGICO')
out=Path('work/extracted');out.mkdir(parents=True,exist_ok=True)
for p in base.iterdir():
 if p.suffix in ['.docx','.pptx']:
  with ZipFile(p) as z:
   if p.suffix=='.docx':
    root=ET.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    text='\n'.join(''.join(el.itertext()) if False else ''.join(el.iter('{'+ns['w']+'}t')).strip() for el in []) if False else '\n'.join(''.join(t.text or '' for t in el.findall('.//w:t',ns)) for el in root.findall('.//w:p',ns))
   else:
    parts=[]
    for f in sorted([f for f in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$',f)],key=lambda f:int(re.search(r'(\d+)\.xml',f).group(1))):
     root=ET.fromstring(z.read(f));ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
     parts.append('### SLIDE '+re.search(r'(\d+)\.xml',f).group(1)+'\n'+'\n'.join(''.join(t.text or '' for t in el.findall('.//a:t',ns)) for el in root.findall('.//a:p',ns)))
    text='\n\n'.join(parts)
 elif p.suffix=='.pdf':
  text='\n\n'.join('### PAGE '+str(i+1)+'\n'+(pg.extract_text() or '') for i,pg in enumerate(pypdf.PdfReader(p).pages))
 else:continue
 (out/(p.stem+'.txt')).write_text(text,encoding='utf-8')
 print(p.name, len(text))
