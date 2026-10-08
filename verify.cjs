const {chromium}=require('C:/Users/ronal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
(async()=>{
 let browser;
 try{browser=await chromium.launch({headless:true})}catch(err){browser=await chromium.launch({headless:true,channel:'msedge'})}
 const context=await browser.newContext({viewport:{width:1440,height:1050}});
 const page=await context.newPage();const errors=[];
 page.on('pageerror',e=>errors.push(String(e)));
 const url='file:///'+path.resolve('outputs/index.html').replace(/\\/g,'/');
 await page.goto(url);await page.screenshot({path:'work/home-desktop.png',fullPage:true});
 await page.getByRole('button',{name:'Resumo essencial',exact:true}).click();
 await page.getByRole('button',{name:'SWOT',exact:true}).click();
 assert(await page.locator('#topic-1').evaluate(e=>e.open));
 await page.locator('#topic-1').screenshot({path:'work/summary-desktop.png'});
 await page.getByRole('button',{name:'Treinar este tema',exact:true}).nth(1).click();
 assert.equal(await page.locator('input[name="answer"]').count(),5);
 assert(await page.locator('#confirmAnswer').isDisabled());
 const qid=await page.evaluate(()=>state.practice.ids[state.practice.position]);
 const qi=await page.evaluate(id=>({a:Q[id].answer,w:[0,1,2,3,4].find(i=>!good(Q[id],i))}),qid);
 await page.locator('#hint').click();assert(await page.locator('.hint-box').isVisible());
 await page.locator(`input[name="answer"][value="${qi.w}"]`).check();
 await page.locator('#confirmAnswer').click();
 assert.match(await page.locator('.feedback-title').innerText(),/revisão/);
 assert.equal(await page.locator('.reason').count(),5);
 await page.screenshot({path:'work/practice-desktop.png',fullPage:true});
 await page.locator('#nextQuestion').click();
 const answer=await page.evaluate(()=>Q[state.practice.ids[state.practice.position]].answer);
 await page.locator(`input[name="answer"][value="${answer}"]`).check();await page.locator('#confirmAnswer').click();
 assert.match(await page.locator('.feedback-title').innerText(),/acertou|aceita/);
 await page.reload();assert.equal(await page.evaluate(()=>Object.keys(state.history).length),2);
 await page.getByRole('button',{name:'Discursivas',exact:true}).click();
 await page.locator('#essayDraft').fill('A equipe é força, o retrabalho é fraqueza, o edital é oportunidade e o concorrente é ameaça.');
 await page.locator('#essayHint').click();assert(await page.locator('.hint-box').isVisible());
 await page.locator('#revealEssay').click();await page.locator('[data-rubric="0"]').check();
 assert.match(await page.locator('#essayScore').innerText(),/1\/4/);
 await page.getByRole('button',{name:'Prova 8 + 2',exact:true}).click();await page.locator('#startExam').click();
 const examMeta=await page.evaluate(()=>({n:state.exam.ids.length,d:state.exam.essayIds.length,excluded:state.exam.ids.some(id=>Q[id].excludeExam),unique:new Set(state.exam.ids).size}));
 assert.deepEqual(examMeta,{n:8,d:2,excluded:false,unique:8});
 assert.equal(await page.locator('.feedback').count(),0);
 for(let i=0;i<8;i++){
  await page.locator(`[data-exam-position="${i}"]`).click();
  let a=await page.evaluate(()=>Q[state.exam.ids[state.exam.position]].answer);
  await page.locator(`input[name="examAnswer"][value="${a}"]`).check();
 }
 for(let i=8;i<10;i++){await page.locator(`[data-exam-position="${i}"]`).click();await page.locator('#examDraft').fill('Resposta de teste para verificar salvamento e autoavaliação.');}
 await page.locator('#examHint').click();await page.locator('#finishExam').click();await page.locator('#reallyFinish').click();
 assert.equal(await page.locator('.result-item').count(),8);
 assert.equal(await page.locator('.essay-model').count(),2);
 assert.match(await page.locator('.result-stat').first().innerText(),/8\/8/);
 await page.locator('[data-exam-check]').first().check();assert.match(await page.locator('#selfScore').innerText(),/1\/8/);
 await page.screenshot({path:'work/result-desktop.png',fullPage:true});
 // Validate every bank item and every model against the DOM renderer.
 const coverage=await page.evaluate(()=>{
  let list=[];
  for(const q of QUESTIONS){let order=shuffle([0,1,2,3,4]);let selected=q.answer;let html=answerOptions(q,order,selected,true,true)+feedbackHTML(q,order,selected);let div=document.createElement('div');div.innerHTML=html;if(div.querySelectorAll('.reason').length!==5||div.querySelectorAll('.answer').length!==5)throw Error('Incomplete '+q.id);list.push(q.id)}
  return {count:list.length,essays:STUDY.essays.length,correctText:QUESTIONS.filter(q=>!q.notice).every(q=>q.reasons[q.answer].length>15)};
 });assert.deepEqual(coverage,{count:42,essays:6,correctText:true});
 // Exercise narrow layouts at 390px and 320px, all primary views.
 await page.setViewportSize({width:390,height:844});
 for(const name of ['home','summary','practice','exam','essays','plan']){
  await page.evaluate(p=>go(p,false),name);
  if(name==='summary')await page.evaluate(()=>document.querySelectorAll('.module').forEach(d=>d.open=true));
  const metrics=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,width:window.innerWidth}));
  assert(metrics.scroll<=metrics.width+1,`${name} overflow: ${JSON.stringify(metrics)}`);
  if(name==='home')await page.screenshot({path:'work/home-mobile.png',fullPage:true});
  if(name==='practice')await page.screenshot({path:'work/practice-mobile.png',fullPage:true});
 }
 await page.setViewportSize({width:320,height:740});
 for(const name of ['home','summary','practice','essays','plan']){
  await page.evaluate(p=>go(p,false),name);
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);assert(!overflow,name+' overflow at 320px');
 }
 await page.setViewportSize({width:390,height:844});
 await page.locator('#menuToggle').click();assert(await page.locator('#sidebar').isVisible());await page.getByRole('button',{name:'Visão geral',exact:true}).click();assert(!await page.locator('#sidebar').isVisible());
 assert.deepEqual(errors,[]);
 fs.writeFileSync('work/verification.json',JSON.stringify({status:'passed',questions:42,essays:6,desktop:'1440×1050',mobile:['390×844','320×740'],checks:['correct and incorrect feedback','all five rationales','hints','42 item render coverage','local persistence','essay save and rubric','exam 8+2 with exclusion','exam correction after finish','self-assessment','mobile navigation','no horizontal document overflow','no runtime errors']},null,2));
 console.log('PASS: 42 questions, 6 essays, quiz flows, persistence, exam, mobile layouts and runtime errors.');
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
