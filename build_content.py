from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as E
import re,json
base=Path('C:/Users/ronal/OneDrive/Área de Trabalho/Faculdade/4. PLANEJAMENTO ESTRATÉGICO')
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
questions=[]
meta=[
 ('SWOT','Média','Separe o que pertence à organização do que vem do ambiente.', ['“Falhas” descreve um problema, mas não é o nome do quadrante SWOT.','Processos internos deficientes são fraquezas; mudanças externas favoráveis são oportunidades.','Ameaças são externas e negativas; forças são internas e positivas. O caso exige o inverso.','A ordem importa: primeiro há uma limitação interna, depois uma condição externa favorável.','O primeiro termo não é um quadrante e o segundo descreve uma capacidade interna positiva.']),
 ('SWOT','Média','Use a nomenclatura do cruzamento da Aula 1, slide 20.', ['Manutenção combina forças com ameaças.','Sobrevivência combina fraquezas com ameaças.','Crescimento combina fraquezas com oportunidades, conforme o quadro da aula.','Desenvolvimento combina forças com oportunidades.','Inovação pode integrar ações, mas não nomeia esse cruzamento no quadro da aula.']),
 ('SWOT','Difícil','O enunciado classifica a cobertura da imprensa, não a reputação interna já consolidada.', ['Não há uma capacidade interna favorável.','A cobertura negativa é uma pressão externa desfavorável. O gabarito fornecido a classifica como ameaça.','A reputação deteriorada pode ser analisada como fraqueza em outro enunciado; aqui o fator pedido é a cobertura externa.','Ponto fraco equivale a fraqueza interna. O objeto específico é a cobertura da imprensa.','A cobertura descrita prejudica a organização; não é uma condição favorável.']),
 ('SWOT','Média','Observe de onde vêm os fatores: fornecedores, concorrentes e macroambiente.', ['Forças e fraquezas são fatores internos, enquanto os exemplos são externos.','Ameaças e oportunidades pertencem ao ambiente externo, incluindo o ambiente de tarefa e o macroambiente.','Mistura uma capacidade interna com uma condição externa.','Mistura uma limitação interna com uma condição externa.','Mistura uma capacidade interna com uma condição externa.']),
 ('SWOT','Fácil','Pergunte onde surgem produtividade, rotatividade e cumprimento de prazos.', ['Ameaças se originam no ambiente externo.','Os três problemas são limitações internas que prejudicam o desempenho.','Risco é um termo amplo; o quadrante específico é fraquezas.','Forças são capacidades favoráveis, opostas aos problemas descritos.','Oportunidades são condições externas favoráveis.']),
 ('Porter','Média','O caso enfatiza a chegada de empresas ao setor.', ['O caso não informa pressão de quem fornece insumos.','Venda direta não comprova poder de barganha dos clientes.','O foco é a entrada de novas empresas com outra estrutura produtiva e comercial. Esse é o gabarito da lista.','Substituto atende à mesma necessidade por solução diferente; automação não basta para caracterizá-lo.','A entrada pode intensificar a rivalidade depois. A pergunta da lista destaca a ameaça de entrada.']),
 ('Porter','Média','Combine a amplitude do público atendido com a fonte da vantagem.', ['O diferencial é valor percebido, não o menor custo de produção.','O diferencial existe, mas o escopo é restrito a um nicho.','Nicho restrito e atributos valorizados pelo público caracterizam enfoque em diferenciação.','Diversificação trata da expansão de negócios/produtos, não dessa escolha de vantagem e escopo.','Integração vertical trata de etapas da cadeia produtiva, ausente no caso.']),
 ('Identidade','Fácil','Procure a expressão “o que faz, para quem faz e como faz”.', ['Visão descreve uma posição futura desejada.','Missão define o propósito presente e os limites de atuação.','Valores orientam princípios e condutas.','Metas especificam resultados e prazos.','Benchmarking compara práticas e resultados de outras organizações.']),
 ('Canvas','Fácil','Diferencie quem coopera, o que a empresa possui e o que executa.', ['Recursos-chave são ativos/capacidades essenciais, não a lista de aliados.','Pessoas e instituições que viabilizam o negócio por alianças entram em parcerias-chave.','Atividades-chave descrevem ações essenciais, como desenvolver e entregar.','Canais são meios de comunicação e distribuição ao cliente.','Custos registram as principais saídas do modelo.']),
 ('GUT','Fácil','A ferramenta compara problemas por três critérios.', ['A GUT ordena prioridades; a causa-raiz requer investigação adicional.','Gravidade, urgência e tendência permitem comparar a prioridade de intervenção.','Lucratividade não é um dos três critérios.','A ferramenta não define metas financeiras.','A GUT prioriza problemas; não é uma matriz de stakeholders.']),
 ('Identidade','Fácil','Diferencie propósito atual e aspiração futura.', ['Visão expressa o futuro desejado.','Valores expressam princípios de comportamento.','Missão comunica a razão de existir e a atuação presente.','Metas são resultados específicos com prazo.','Estratégia define escolhas e caminhos para alcançar objetivos.']),
 ('Porter','Média','O dado decisivo é a concentração em um grupo específico.', ['Não se descreve eficiência para obter menor custo.','Diferenciação isolada não explicita a restrição de escopo que o caso enfatiza.','A concentração dos esforços em um nicho caracteriza enfoque. A personalização pode sustentá-lo.','Expansão é uma direção de crescimento, não a estratégia genérica pedida.','Não há entrada em produtos e mercados novos para caracterizar diversificação.']),
 ('Porter','Média','Leia os dois fatos explícitos: negociação de preço e facilidade de entrada.', ['O enunciado não destaca imposição de condições pelos fornecedores.','Consumidores pressionam preços: compradores. Facilidade de entrada: novos entrantes.','Não se descreve uma solução diferente que substitua o software.','Acionistas não constituem uma das cinco forças. Barreiras explicam a ameaça de entrada.','O caso não descreve sindicatos nem soluções substitutas.']),
 ('Porter','Média','Qual é a fonte da disposição do cliente a pagar mais?', ['Atributos únicos e valorizados sustentam a diferenciação e o preço premium.','Não há escopo restrito nem vantagem de baixo custo descritos.','A proposta se apoia em unicidade percebida, não em custo mínimo.','Crescimento não identifica a fonte de vantagem competitiva pedida.','Não se descreve aquisição/controle de etapas da cadeia produtiva.']),
 ('Canvas','Fácil','O enunciado pergunta quem ajuda a viabilizar o negócio.', ['Recursos são ativos/capacidades, enquanto parceiros são agentes com os quais se coopera.','Parceiros estratégicos e entidades auxiliares compõem parcerias-chave.','Atividades indicam o que executar, não quem coopera.','Canais ligam a empresa ao cliente por comunicação e distribuição.','Receitas registram como o modelo captura dinheiro.'])
]
for n in range(1,4):
 p=next(base.glob(f'*Lista {n} (gabarito).docx'))
 with ZipFile(p) as z:root=E.fromstring(z.read('word/document.xml'))
 pars=root.findall('.//w:p',ns);active=False;cur=None
 for par in pars:
  text=''.join(t.text or '' for t in par.findall('.//w:t',ns)).strip()
  if text=='Questões':active=True;continue
  if not active or not text:continue
  m=re.match(r'^(\d+)\s*[–\-)]+\s*(.*)',text)
  if m:
   if cur:questions.append(cur)
   cur={'id':f'L{n}Q{m[1]}','source':f'Lista {n} · questão {m[1]}','origin':'Lista','stem':m[2],'options':[],'answer':None}
  elif cur:
   m=re.match(r'^([A-E])\)\s*(.*)',text)
   if m:
    idx=len(cur['options']);cur['options'].append(m[2])
    if par.find('.//w:highlight',ns) is not None:cur['answer']=idx
   else:cur['stem']+='\n'+text
 if cur:questions.append(cur)
assert len(questions)==15
for q,(topic,difficulty,hint,reasons) in zip(questions,meta):
 assert q['answer'] is not None and len(q['options'])==5
 q.update(topic=topic,difficulty=difficulty,hint=hint,reasons=reasons,prob='Muito alta' if topic in ['SWOT','Porter','Canvas','Identidade'] else 'Alta',evidence='Tema cobrado nas listas e desenvolvido nos slides. A estimativa se refere ao tema, não à repetição literal desta questão.')

# Preserve source highlights separately from the pedagogical correction.
q=next(q for q in questions if q['id']=='L2Q1')
q.update(accepted=[2,4],excludeExam=True,notice='Questão ambígua. O DOCX destaca E: Rivalidade entre concorrentes. A chegada de empresas também sustenta C: Ameaça de novos entrantes. No treino, ambas são aceitas com ressalva; esta questão não entra no modo prova.',difficulty='Difícil')
q['reasons'][2]='Leitura defensável: a chegada de novas empresas destaca a ameaça de entrada. O gabarito fornecido, porém, marca rivalidade; ambas as leituras são aceitas neste treino.'
q['reasons'][4]='É a opção destacada no gabarito fornecido. A entrada já ocorrida pode intensificar a rivalidade. O texto também admite foco na ameaça de novos entrantes; ambas as leituras são aceitas neste treino.'
q=next(q for q in questions if q['id']=='L3Q3')
q.update(answer=1,originalAnswer=0,excludeExam=True,notice='Divergência no material. O DOCX destaca A: Rivalidade e poder dos fornecedores. O trecho decisivo descreve compradores negociando preços e facilidade de entrada. O treino adota B, coerente com a Aula 2, slide 8. A questão não entra no modo prova.',difficulty='Difícil')
q['reasons'][0]='O DOCX destaca esta opção, mas o texto não informa poder de fornecedores. O cenário destaca explicitamente a negociação dos compradores e a facilidade de entrada, correspondentes à opção B original.'

def add(topic,difficulty,prob,source,stem,hint,options,answer,reasons,evidence=None):
 questions.append(dict(id=f'A{len(questions)-14:02}',topic=topic,difficulty=difficulty,prob=prob,source=source,origin='Autoral',stem=stem,hint=hint,options=options,answer=answer,reasons=reasons,evidence=evidence or 'Aplicação autoral de conteúdo explícito dos slides. A estimativa é qualitativa e se refere ao tema.'))

add('Níveis','Média','Alta','Aula 1 · slides 12–16',
'Uma empresa define atuar nacionalmente em três anos. A gerência de TI cria um plano semestral de capacidade, e a equipe agenda as rotinas de backup. Esses três atos correspondem, respectivamente, a quais níveis?',
'Classifique pela abrangência da decisão e pela responsabilidade, sem depender apenas do prazo.',
['Tático, estratégico e operacional.','Estratégico, operacional e tático.','Operacional, tático e estratégico.','Estratégico, tático e operacional.','Tático, operacional e estratégico.'],3,
['A atuação nacional define a direção global, não apenas uma área.','O plano da gerência traduz a direção na área; o backup executa rotinas. A ordem dos dois últimos foi invertida.','A decisão global não é execução rotineira, e o backup não define o futuro da organização.','Direção global é estratégica; desdobramento na área é tático; rotina de execução é operacional.','A decisão global é estratégica, e a rotina de backup é operacional.'])
add('Identidade','Média','Muito alta','Aula 2 · slide 6; Listas 2–3',
'Um plano registra: I. “Existimos para simplificar a gestão das clínicas.” II. “Ser a principal referência regional em 2028.” III. “Tratar dados com transparência.” IV. “Reduzir o tempo de suporte para 30 minutos até dezembro.” A sequência correta é:',
'Identifique propósito, futuro, princípio e resultado verificável.',
['Missão, visão, valores e meta.','Visão, missão, valores e meta.','Missão, meta, visão e valores.','Valores, visão, missão e meta.','Missão, visão, meta e valores.'],0,
['I define propósito atual; II projeta o futuro; III orienta conduta; IV fixa resultado mensurável e prazo.','O propósito presente e a aspiração futura foram invertidos.','II é uma posição futura; III é princípio; IV é resultado verificável.','I explica a razão de existir; III não define o propósito da organização.','Transparência é princípio; tempo de resposta com prazo é meta.'])
add('SWOT','Difícil','Alta','Aula 1 · slides 18–20; Lista 1',
'Uma empresa tem equipe técnica reconhecida, mas sofre com retrabalho. Um edital financiará digitalização, enquanto um concorrente estrangeiro entra no mercado. Qual leitura associa corretamente uma ação ao cruzamento SWOT da aula?',
'Mantenha a nomenclatura da aula: desenvolvimento usa forças e oportunidades.',
['Usar a equipe no edital configura manutenção.','Corrigir retrabalho ante o rival configura crescimento.','Usar a equipe no edital configura desenvolvimento.','Usar a equipe contra o rival configura sobrevivência.','Corrigir retrabalho ante o rival configura desenvolvimento.'],2,
['Equipe é força e edital é oportunidade: desenvolvimento. Manutenção exige ameaça.','Retrabalho é fraqueza e rival é ameaça: sobrevivência.','Equipe é força e edital é oportunidade. Sua combinação caracteriza desenvolvimento no quadro da aula.','Força mais ameaça caracteriza manutenção.','Fraqueza mais ameaça caracteriza sobrevivência.'])
add('Porter','Difícil','Muito alta','Aula 2 · slides 7–8; Listas 2–3',
'Um ERP disputa clientes com outros ERPs. Alguns usuários deixam a categoria e passam a controlar o negócio por planilhas. Ao mesmo tempo, um único provedor de nuvem eleva seus preços. A sequência das forças é:',
'Diferencie concorrente da mesma categoria, outra solução para a necessidade e fornecedor de insumo.',
['Substitutos, rivalidade e compradores.','Rivalidade, entrantes e fornecedores.','Entrantes, substitutos e compradores.','Rivalidade, substitutos e fornecedores.','Compradores, rivalidade e entrantes.'],3,
['Outros ERPs representam rivalidade; o provedor é fornecedor.','Planilhas já disponíveis substituem a solução, sem exigir entrada de uma empresa no setor.','A disputa com ERPs existentes é rivalidade; nuvem é insumo fornecido.','ERPs existentes rivalizam; planilhas são substitutos; nuvem representa poder do fornecedor.','Não há barganha explícita dos compradores nem entrada descrita na sequência.'])
add('Porter','Difícil','Muito alta','Aula 2 · slides 9–12',
'Uma empresa vende exclusivamente para pequenos escritórios jurídicos. Padroniza o serviço e automatiza o atendimento para operar com custo inferior ao dos concorrentes desse nicho. A estratégia descrita é:',
'Analise duas dimensões independentes: escopo do mercado e fonte da vantagem.',
['Liderança em custo em mercado amplo.','Enfoque em custo no segmento escolhido.','Diferenciação ampla pelo uso de tecnologia.','Enfoque em diferenciação pela automação.','Desenvolvimento de mercado pela especialização.'],1,
['Existe baixo custo, mas o escopo informado é restrito.','A empresa atende um nicho e busca baixo custo dentro dele: enfoque em custo.','Tecnologia não implica diferencial percebido; aqui seu efeito declarado é reduzir custo.','A fonte de vantagem explicitada é custo, não unicidade valorizada.','Especialização no nicho não demonstra entrada em um mercado novo.'])
add('BSC e OKR','Média','Alta','Aula 2 · slides 14–18',
'Um BSC acompanha margem operacional, retenção de clientes, taxa de defeitos e capacitação da equipe. A qual perspectiva pertence a taxa de defeitos?',
'Procure o objeto medido diretamente, não todas as consequências que ele pode provocar.',
['Financeira, porque defeitos elevam despesas.','Clientes, porque falhas afetam satisfação.','Processos internos, pela qualidade da execução.','Aprendizado, pela necessidade de treinamento.','Financeira, porque qualidade aumenta receita.'],2,
['Custos podem ser consequência, mas o indicador mede diretamente qualidade do processo.','Satisfação é consequência possível; defeitos medem a execução interna.','A taxa de defeitos mede qualidade do processo produtivo ou de prestação de serviço.','Capacitação é aprendizado; defeitos medem desempenho do processo.','Receita é uma medida financeira distinta do indicador apresentado.'])
add('BSC e OKR','Difícil','Alta','Aula 2 · slides 14–18',
'Um mapa estratégico prevê que capacitar analistas reduzirá erros, elevará a satisfação e melhorará a retenção, contribuindo para a receita. Qual interpretação é a mais adequada?',
'Uma seta no mapa estratégico representa uma relação que precisa ser acompanhada.',
['A capacitação pertence à perspectiva financeira.','A receita torna dispensáveis os indicadores anteriores.','A satisfação substitui a medida de qualidade interna.','As perspectivas são independentes entre si.','Há uma hipótese de causa e efeito a monitorar.'],4,
['Capacitação integra aprendizado e crescimento, mesmo quando afeta resultados financeiros.','Indicadores anteriores ajudam a verificar por que o resultado financeiro ocorre ou falha.','Qualidade e satisfação pertencem a objetos e perspectivas distintos.','O mapa liga perspectivas para traduzir a estratégia.','O encadeamento é uma hipótese estratégica: acompanhar as medidas ajuda a verificar se a relação se realiza.'])
add('BSC e OKR','Difícil','Alta','Aula 2 · slide 19',
'O objetivo de um OKR é “Tornar o suporte mais confiável”. Qual resultado-chave mede melhor a realização desse objetivo no trimestre?',
'Diferencie uma entrega de atividade da mudança de desempenho esperada.',
['Realizar três reuniões de melhoria com a equipe.','Reduzir chamados reabertos de 12% para 5% até o fim do trimestre.','Implantar uma nova ferramenta para registrar chamados.','Produzir um manual atualizado para cada atendente.','Contratar dois analistas para reforçar o atendimento.'],1,
['Reuniões são atividades; não demonstram por si a confiabilidade obtida.','A taxa de reabertura mede resultado, com linha de base, alvo e prazo verificáveis.','A implantação é iniciativa; seu impacto no suporte ainda precisa ser medido.','O manual é uma entrega de apoio, não a melhora do desempenho em si.','Contratação é iniciativa de capacidade; não comprova confiabilidade.'])
add('GUT','Média','Alta','Aula 2 · slide 20 e imagem GUT; Lista 2 · Q5',
'Uma equipe usa G × U × T. O problema X recebe (5, 2, 4), Y recebe (3, 5, 3) e Z recebe (4, 4, 2). Pela pontuação, qual é a ordem de prioridade?',
'Calcule os três produtos antes de comparar. A soma produz outra ordenação.',
['X, Y e Z.','Z, X e Y.','Y, Z e X.','X, Z e Y.','Y, X e Z.'],4,
['X = 40, menor que Y = 45.','Z = 32, a menor pontuação dos três.','Y lidera, mas X = 40 supera Z = 32.','Y = 45 deve vir antes dos outros dois.','Y = 45, X = 40 e Z = 32. A ordem decrescente é Y, X, Z.'])
add('GUT','Difícil','Alta','Aula 2 · slide 20 e imagem GUT',
'Duas falhas têm impacto semelhante e precisam de solução no mesmo prazo. A primeira permanece estável; a segunda se agrava a cada dia. Na GUT, qual critério diferencia diretamente as falhas?',
'Pergunte qual critério olha para a evolução do problema se nada for feito.',
['Gravidade, pelo impacto atual.','Urgência, pelo prazo de solução.','Tendência, pela evolução provável.','Gravidade, pela frequência diária.','Urgência, pelo custo acumulado.'],2,
['O impacto foi descrito como semelhante.','O prazo de solução foi descrito como igual.','Tendência mede a evolução ou agravamento provável ao longo do tempo.','A frequência pode ajudar a análise, mas o dado decisivo é a piora futura.','Custo pode influenciar impacto; urgência trata do tempo disponível para agir.'])
add('Canvas','Difícil','Muito alta','Aula 2 · slides 21–30; Listas 2–3',
'No Canvas de um software: I. consultorias que indicam clientes e ajudam na implantação; II. equipe e plataforma próprias; III. desenvolver integrações; IV. assinatura mensal. A sequência dos blocos é:',
'Separe agentes aliados, ativos, ações e mecanismo de entrada de dinheiro.',
['Parcerias, recursos, atividades e receitas.','Recursos, parcerias, atividades e custos.','Canais, atividades, recursos e receitas.','Parcerias, atividades, recursos e custos.','Relacionamento, recursos, canais e receitas.'],0,
['Aliados são parcerias; equipe/plataforma são recursos; desenvolver é atividade; assinatura é receita.','Consultorias são agentes aliados; equipe própria é recurso. Assinatura é receita, não custo.','O caso descreve cooperação, ativos e execução. Não descreve canais no item III.','Os itens II e III foram invertidos, e assinatura não é custo.','Relacionamento trata de como manter vínculos com clientes; desenvolver integrações é atividade.'])
add('Canvas','Média','Muito alta','Aula 2 · slides 22–25',
'Uma startup anuncia “reduzir o retrabalho na conciliação de pequenas lojas”. Ela faz demonstrações por webinars e mantém suporte individual após a venda. Os três elementos correspondem a:',
'Benefício prometido, meio de comunicação e forma de vínculo têm papéis diferentes.',
['Segmento, relacionamento e canais.','Recursos, canais e atividades.','Proposta de valor, parcerias e canais.','Proposta de valor, canais e relacionamento.','Atividades, segmento e relacionamento.'],3,
['A promessa de reduzir retrabalho é proposta de valor; webinar é canal.','O benefício não é um ativo, e suporte individual caracteriza relacionamento neste caso.','Webinar é meio de comunicação, não um parceiro. Suporte descreve vínculo.','Benefício ao cliente é proposta de valor; webinar é canal; suporte individual é relacionamento.','Atividade é o que se faz para entregar valor; aqui o primeiro elemento é o valor prometido.'])
add('Ambiente','Média','Média','Aula 3 · slides 2–4',
'Uma empresa atende públicos muito diferentes, com fornecedores especializados por segmento. Porém, suas exigências e regras mudam pouco ao longo dos anos. O ambiente é predominantemente:',
'Diversidade de elementos e velocidade de mudança são eixos distintos.',
['Homogêneo e instável.','Heterogêneo e estável.','Homogêneo e estável.','Heterogêneo e instável.','Estável e necessariamente simples.'],1,
['Há diversidade de públicos e fornecedores, mas pouca mudança.','Diversidade indica heterogeneidade; pouca mudança indica estabilidade.','A estabilidade está correta, mas a diversidade contradiz homogeneidade.','A heterogeneidade está correta, porém as exigências mudam pouco.','Estabilidade não elimina diversidade ou complexidade.'])
add('Ambiente','Difícil','Média','Aula 3 · slide 2',
'Ao mapear o ambiente, um gestor registra: negociação com um fornecedor, disputa com concorrente, alta geral dos juros e mudança demográfica. Quais pertencem, respectivamente, ao ambiente de tarefa e ao ambiente geral?',
'Tarefa envolve atores próximos das operações; geral envolve condições amplas.',
['Juros e demografia; fornecedor e concorrente.','Fornecedor e juros; concorrente e demografia.','Fornecedor e concorrente; juros e demografia.','Concorrente e demografia; fornecedor e juros.','Fornecedor e demografia; concorrente e juros.'],2,
['Os grupos estão invertidos.','Fornecedor é tarefa, mas juros são uma condição econômica geral.','Fornecedor e concorrente são atores próximos; juros e demografia são condições do macroambiente.','Demografia é geral, enquanto fornecedor integra tarefa.','Demografia é geral, e concorrente integra tarefa.'])
add('BCG e ciclo','Média','Média','Aula 3 · slide 6',
'Um produto tem alta participação relativa em um mercado de baixo crescimento. Outro tem baixa participação relativa em um mercado de alto crescimento. Na BCG, são, respectivamente:',
'Use simultaneamente os dois eixos; crescimento não é participação.',
['Estrela e abacaxi.','Interrogação e estrela.','Vaca leiteira e abacaxi.','Estrela e interrogação.','Vaca leiteira e interrogação.'],4,
['Estrela exige alto crescimento; abacaxi exige baixo crescimento.','O primeiro tem alta participação; o segundo tem baixa.','O segundo está em mercado de alto crescimento, por isso não é abacaxi.','O primeiro tem baixo crescimento, por isso não é estrela.','Alta participação/baixo crescimento é vaca leiteira; baixa participação/alto crescimento é interrogação.'])
add('BCG e ciclo','Difícil','Média','Aula 3 · slide 6',
'A direção considera investir em uma interrogação para ganhar participação. Qual avaliação respeita a lógica da BCG sem transformar o modelo em uma regra automática?',
'A matriz descreve posição relativa; decisões também exigem viabilidade e capacidade de investir.',
['Avaliar potencial e recursos antes de buscar torná-la estrela.','Retirar o produto porque o baixo crescimento impede expansão.','Colher caixa porque toda interrogação já domina seu mercado.','Tratá-la como vaca leiteira porque o setor cresce rapidamente.','Investir sem análise porque o alto crescimento garante retorno.'],0,
['Interrogação tem baixo share e alto crescimento. Investir pode aumentar participação, mas exige análise e não garante sucesso.','O crescimento é alto; retirada pode ser opção após análise, não pela condição afirmada.','Interrogação tem baixa participação, não domínio do mercado.','Vaca leiteira combina alta participação com baixo crescimento.','Crescimento do mercado não garante rentabilidade ou capacidade competitiva.'])
add('BCG e ciclo','Média','Média','Aula 3 · slide 5',
'Um produto já tem ampla adoção. O ritmo de crescimento das vendas diminui, e a empresa prioriza eficiência, retenção e diferenciação para defender a posição. A fase predominante é:',
'A desaceleração do crescimento pode ocorrer antes da queda das vendas.',
['Introdução.','Crescimento inicial.','Declínio.','Maturidade.','Interrogação.'],3,
['Introdução envolve lançamento e adoção ainda limitada.','O caso descreve adoção ampla e desaceleração, não expansão inicial.','Declínio pressupõe redução das vendas; desaceleração do crescimento não basta.','Adoção ampla e crescimento mais lento caracterizam maturidade.','Interrogação é uma posição na BCG, não uma fase do ciclo de vida.'])
add('Marketing','Média','Média','Aula 3 · slides 7–8',
'Uma loja revê a política de descontos, passa a vender em um marketplace e cria uma campanha de divulgação. A sequência dos elementos do mix é:',
'Condições monetárias, acesso ao produto e comunicação têm Ps distintos.',
['Promoção, praça e preço.','Preço, praça e promoção.','Preço, promoção e praça.','Produto, preço e promoção.','Praça, produto e preço.'],1,
['Descontos integram preço; a campanha integra promoção.','Descontos são preço; marketplace é praça/distribuição; campanha é promoção.','Marketplace é canal de distribuição, enquanto campanha é comunicação.','Descontos não são o produto e marketplace não define preço.','Os três elementos foram atribuídos a objetos diferentes dos descritos.'])
add('Marketing','Média','Média','Aula 3 · slide 8',
'Dois equipamentos têm características físicas equivalentes. Uma marca oferece instalação, entrega e pós-venda superiores. Considerando a representação da oferta nos slides, qual análise é adequada?',
'Observe as camadas além do objeto físico no diagrama da aula.',
['A oferta se limita ao objeto físico entregue.','O pós-venda pertence apenas à decisão de preço.','Os serviços alteram somente o canal de promoção.','A equivalência física torna as ofertas idênticas.','Serviços associados podem ampliar o valor da oferta.'],4,
['O diagrama inclui atendimento, entrega e pós-venda além do físico.','Pós-venda compõe o serviço associado à oferta; pode afetar preço, mas não se reduz a ele.','Serviços associados não são apenas divulgação.','Experiência e serviços podem diferenciar propostas com objetos equivalentes.','A camada de serviços amplia a oferta percebida e pode sustentar diferenciação.'])
add('Fundamentos','Média','Média','Aula 1 · slides 8–11',
'Antes de entrar em um segmento, uma gestora avalia suas capacidades, estuda concorrentes e adapta o plano às condições locais. Qual lição de Sun Tzu está mais diretamente aplicada?',
'O enunciado combina informação sobre os dois lados e adaptação ao terreno.',
['Concentrar toda a análise no volume de recursos.','Preservar a tática mesmo quando o ambiente mudar.','Conhecer a si e ao rival, ajustando-se ao contexto.','Substituir informações pela lealdade dos liderados.','Escolher o confronto direto em qualquer circunstância.'],2,
['O foco descrito é conhecimento e adaptação, não apenas volume.','A flexibilidade faz parte das lições apresentadas.','Conhecer capacidades próprias, concorrentes e contexto fundamenta a escolha estratégica.','Lealdade é relevante na aula, mas não substitui inteligência.','A aula ressalta saber quando lutar e até vencer sem lutar.'])
add('Fundamentos','Difícil','Média','Aula 1 · slides 10–11',
'Uma liderança prepara alternativas para mudanças regulatórias e investe em competências internas, embora reconheça que eventos externos podem alterar o resultado. Na abordagem de Maquiavel apresentada na aula, isso expressa:',
'Virtù é capacidade de agir; fortuna remete às circunstâncias e ao acaso.',
['Virtù para agir diante da fortuna e do contexto.','Fortuna como domínio completo das circunstâncias.','Virtù como dependência integral de favores externos.','Fortuna como substituição do planejamento pela sorte.','Virtù como manutenção de uma decisão sem adaptação.'],0,
['A habilidade e o preparo permitem responder às circunstâncias, sem eliminar o acaso.','Fortuna não significa controle completo do contexto.','Virtù envolve habilidade e capacidade de ação, não dependência integral.','Reconhecer o acaso não dispensa preparo e análise.','A aula destaca adaptação e pragmatismo, não rigidez.'])
add('Popper','Difícil','Média','P Estratégico · AV1 · proposta sobre indução e Popper',
'Após estudar três empresas bem-sucedidas que adotaram squads, um consultor afirma: “Squads elevam o desempenho de qualquer organização.” Qual crítica é mais consistente com a proposta da atividade sobre Popper?',
'Pergunte se observar casos favoráveis prova uma afirmação universal.',
['Três casos garantem validade se forem muito conhecidos.','A afirmação é válida se os gestores relatarem satisfação.','A popularidade da prática dispensa buscar contraexemplos.','Os casos sugerem uma hipótese que requer testes críticos.','A hipótese só é científica se nunca puder ser contrariada.'],3,
['Prestígio e repetição de casos favoráveis não provam universalidade.','Satisfação relatada não demonstra a regra universal ou sua causalidade.','Popularidade não substitui confronto com evidências contrárias.','Casos favoráveis inspiram hipótese, mas testes e condições de refutação são necessários.','A possibilidade de ser contrariada por evidências é central à falseabilidade.'], 'Tema explícito em uma atividade fornecida, sem repetição nas listas. Prioridade secundária; não foi presumida a leitura do artigo citado.')
add('Popper','Difícil','Média','P Estratégico · AV1 · proposta sobre benchmarking',
'Uma empresa quer reproduzir o processo de uma líder do setor. Qual procedimento torna o benchmarking mais confiável diante dos limites da indução?',
'Comparação útil exige contexto, medida de resultado e possibilidade de abandonar a hipótese.',
['Copiar o processo e atribuir desvios à falta de disciplina.','Adaptar a prática e testar resultados com critérios definidos.','Selecionar apenas relatos em que a prática teve sucesso.','Tratar a reputação da líder como evidência causal suficiente.','Adotar a prática e medir somente a adesão dos funcionários.'],1,
['Atribuir todo desvio à execução protege a hipótese contra refutação.','Comparar contextos, adaptar e testar permite verificar se a prática ajuda nesse caso.','Selecionar apenas sucessos introduz viés de seleção e oculta fracassos.','Reputação não demonstra que a prática causou o sucesso.','Adesão mede uso da prática, não comprova o resultado estratégico.'], 'Cobrança explícita na atividade sobre Popper e benchmarking; não aparece nas listas objetivas fornecidas.')
add('Integração','Difícil','Alta','Planejamento Estratégico · AV1 · estrutura do pitch; Aulas 1–2',
'Uma consultoria identifica baixa retenção em um software para clínicas. A direção escolhe diferenciar-se por atendimento especializado. Qual desdobramento apresenta maior coerência entre estratégia e controle?',
'Ligue o problema, a fonte de valor e uma medida do resultado esperado.',
['Aumentar campanhas e medir somente o número de anúncios.','Reduzir preços e medir apenas o volume de visitas ao site.','Treinar suporte e medir retenção com meta e prazo definidos.','Ampliar segmentos e acompanhar o total de apresentações.','Contratar vendedores e registrar somente reuniões internas.'],2,
['Anúncios medem atividade de divulgação, sem verificar a retenção ou a qualidade do suporte.','Desconto não sustenta diretamente o diferencial escolhido, e visitas não medem retenção.','Capacitação apoia o atendimento especializado; retenção com meta e prazo verifica o resultado pretendido.','Ampliação de segmentos não segue necessariamente o posicionamento escolhido e apresentações não verificam retenção.','Contratações e reuniões são iniciativas, sem indicador do resultado estratégico.'])
add('BSC e OKR','Difícil','Alta','Aula 2 · slides 14–19; Planejamento Estratégico · AV1 · indicadores',
'Um plano apresenta: objetivo “melhorar a experiência”; indicador “tempo médio de primeira resposta”; meta “até 30 minutos até dezembro”; iniciativa “treinar a equipe”. Qual afirmação distingue corretamente esses elementos?',
'Direção, régua, valor desejado e ação não são intercambiáveis.',
['O treinamento é o indicador da experiência.','A meta é a direção sem um valor verificável.','O indicador é a ação executada pela equipe.','O objetivo já substitui a necessidade de uma meta.','O indicador mede, e a meta fixa o resultado desejado.'],4,
['Treinamento é uma ação. O tempo de resposta é a medida.','A meta contém alvo e prazo; a direção ampla é o objetivo.','Indicador é uma medida, não uma iniciativa.','O objetivo amplo precisa de critérios verificáveis para acompanhamento.','Indicador é a régua; meta estabelece o valor e o prazo. A iniciativa busca produzir o resultado.'])

add('Crescimento','Média','Média','Aula 2 · slide 13 · diagrama',
'Uma empresa enfrenta risco de continuidade e decide reduzir despesas e adiar investimentos. Outra amplia a atuação por inovação e expansão. Segundo o diagrama de estratégias de crescimento de negócios da Aula 2, essas ações se associam, respectivamente, a:',
'Use as ações exemplificadas no diagrama, sem confundi-lo com as estratégias genéricas de Porter.',
['Manutenção e desenvolvimento.','Sobrevivência e crescimento.','Desenvolvimento e manutenção.','Crescimento e sobrevivência.','Manutenção e internacionalização.'],1,
['O diagrama associa reduzir custos e postergar investimentos à sobrevivência; inovação e expansão ao crescimento.','Sobrevivência contém redução de custos e adiamento de investimentos; crescimento contém inovação e expansão.','Desenvolvimento contém mercados, produtos/serviços e parcerias; manutenção contém nicho e especialização.','A sequência das estratégias está invertida.','O segundo caso não descreve operações internacionais.'])
add('Crescimento','Difícil','Média','Aula 2 · slide 13 · diagrama; PDF fornecido · complemento Ansoff',
'Uma empresa leva seu software atual para uma região em que ainda não atua, preservando as funções principais do produto. Na matriz produto–mercado apresentada no PDF de revisão, essa escolha é:',
'Verifique separadamente se o produto e o mercado são atuais ou novos.',
['Penetração de mercado.','Desenvolvimento de produto.','Diversificação de negócios.','Desenvolvimento de mercado.','Integração vertical.'],3,
['Penetração amplia vendas do produto atual no mercado atual. A região é nova para a empresa.','Desenvolvimento de produto exige produto novo para mercado atual.','Diversificação combina produto novo e mercado novo; o software foi mantido.','Produto atual em mercado novo caracteriza desenvolvimento de mercado.','Integração vertical envolve etapas da cadeia, não a entrada geográfica descrita.'], 'Complemento explícito do PDF de revisão. O slide 13 cita desenvolvimento de mercado, mas não apresenta a matriz Ansoff. Prioridade secundária.')
assert len(questions)==42,len(questions)
# Keep alternative lengths from systematically signalling the correct answer.
revisions={
 'A04':{3:'Rivalidade, substitutos e fornecedores.'},
 'A06':{2:'Processos internos, pela taxa de defeitos.'},
 'A08':{0:'Realizar três reuniões de melhoria do suporte até o fim do trimestre.',1:'Reduzir reaberturas de 12% para 5% até o fim do trimestre.',2:'Implantar o novo registro de chamados até o fim do trimestre.',3:'Entregar manuais de suporte revisados até o fim do trimestre.',4:'Contratar dois analistas de suporte até o fim do trimestre.'},
 'A12':{0:'Segmento de clientes, relacionamento e canais.',1:'Recursos-chave, canais e atividades-chave.',2:'Proposta de valor, parcerias-chave e canais.'},
 'A19':{4:'Serviços associados ampliam o valor percebido.'},
 'A23':{1:'Adaptar a prática e testar com critérios definidos.'},
 'A24':{2:'Treinar suporte e medir retenção com meta e prazo.'},
 'A25':{4:'Indicador mede; meta fixa valor e prazo.'}
}
for q in questions:
 for i,text in revisions.get(q['id'],{}).items():q['options'][i]=text
Path('work/questions.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2),encoding='utf-8')
print('Questions:',len(questions),'Original keys:',[(q['id'],chr(65+q['answer'])) for q in questions[:15]])
