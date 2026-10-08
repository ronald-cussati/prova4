from pathlib import Path
import json,re
questions=json.loads(Path('work/questions.json').read_text(encoding='utf-8'))
study=json.loads(Path('work/study.json').read_text(encoding='utf-8'))
for q in questions:
 t=next(t for t in study['topics'] if t['id']==q['topic'])
 q['prob']=t['prob']
assert len(questions)==42 and len(study['essays'])==6
assert len(set(q['id'] for q in questions))==42
for q in questions:
 assert len(q['options'])==len(q['reasons'])==5
 assert all(q['reasons']) and 0<=q['answer']<5
 assert q['hint'] and q['source'] and q['evidence']
 assert len(set(q['options']))==5
for d in study['essays']:assert len(d['rubric'])==4
template=Path('work/template.html').read_text(encoding='utf-8')
template=template.replace('<legend class="hidden">Escolha uma alternativa</legend>','<legend class="sr-only">Escolha uma alternativa</legend>').replace('<span class="hidden">Alternativa','<span class="sr-only">Alternativa')
html=template.replace('__QUESTIONS__',json.dumps(questions,ensure_ascii=False).replace('</','<\\/')).replace('__STUDY__',json.dumps(study,ensure_ascii=False).replace('</','<\\/'))
out=Path('outputs');out.mkdir(exist_ok=True)
(out/'index.html').write_text(html,encoding='utf-8')
scripts=re.findall(r'<script>(.*?)</script>',html,re.S)
Path('work/app.js').write_text('\n'.join(scripts),encoding='utf-8')
print('Built index.html:',len(html.encode('utf-8')),'bytes; 42 objective questions, 6 essays.')
