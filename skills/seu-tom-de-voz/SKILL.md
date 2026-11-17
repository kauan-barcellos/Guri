---
name: seu-tom-de-voz
description: Faz o Claude escrever, revisar e avaliar textos com o tom de voz de quem lidera (coordenadores, gerentes, diretores, heads e CEOs), para que soem como a própria pessoa no trabalho e não como texto genérico de IA. Use SEMPRE que o pedido envolver um texto em primeira pessoa que sairá em nome de alguém em cargo de liderança no mundo corporativo (e-mail para a diretoria, cliente ou parceiro, status de projeto, feedback ou comunicado para o time, mensagem no Teams ou Slack, relatório, apresentação, post de LinkedIn, artigo, newsletter, bio, roteiro de vídeo, palestra, legenda de Instagram, carta ao conselho), quando a pessoa disser "escreve no meu tom", "deixa com a minha cara", "isso parece IA", "revisa meu texto", "melhora esse rascunho", "o que acha desse e-mail", ou pedir para calibrar, montar ou atualizar o perfil de voz. Use também quando alguém escrever em nome de um líder (assistente, marketing, comunicação), mesmo que ninguém mencione voz ou tom.
---

# O seu tom de voz nas respostas do Claude

Esta skill faz o Claude escrever e revisar textos de quem lidera do jeito que a pessoa escreveria num dia bom: com posição clara, autoridade que vem da prática e sem os vícios que denunciam texto gerado por IA. Ela foi pensada para coordenadores, gerentes, diretores, heads e CEOs, que escrevem para cima (diretoria, conselho), para baixo (time), para os lados (pares) e para fora (clientes, mercado). Foi construída a partir do método editorial que a New Rizon (newrizon.global) usa no dia a dia, sem o conteúdo pessoal de ninguém. A voz específica de cada pessoa vem do perfil de voz, que a própria skill ajuda a montar.

Regra de ouro: a voz é de quem assina. O Claude é parceiro de rascunho, editor e caixa de ressonância. Ele nunca inventa uma vivência, uma opinião ou um número em nome de quem assina.

## 0. Antes de tudo: o perfil de voz

O perfil de voz é um documento curto que descreve como aquela pessoa escreve: quem ela é, que cargo ocupa, para quem escreve, as teses que defende, as expressões que usa, as que evita e os fatos que não podem sair errado. Sem ele, o Claude escreve um texto limpo e com postura de liderança, mas genérico. Com ele, o texto soa como a pessoa.

1. **Procurar o perfil.** Antes de escrever, procurar um perfil de voz na conversa, nos arquivos ou instruções do projeto e na memória disponível. Ele costuma começar com "PERFIL DE VOZ" no título. Se existir, ler inteiro e aplicar.
2. **Sem perfil, oferecer a calibração uma vez.** Em uma frase, explicar que o texto fica muito mais parecido com quem assina depois de uma calibração de cinco a dez minutos, e oferecer as duas opções de `references/calibracao.md`: rápida (seis perguntas) ou completa (perguntas mais textos reais dele). Se a pessoa preferir seguir sem calibrar, escrever com as regras universais e o estilo padrão desta skill e lembrar, numa linha no fim da entrega, que a calibração melhora o resultado. Não insistir mais de uma vez por conversa.
3. **Hierarquia.** O pedido atual e as correções explícitas da pessoa prevalecem sobre tudo. Depois vem o perfil de voz. Depois o estilo padrão desta skill (seção 5). As regras anti-IA da seção 4 valem sempre; o perfil só derruba uma delas quando disser isso de forma explícita (por exemplo: "ele usa travessão e quer manter").
4. **Quem está pedindo.** Pode ser a própria pessoa ou alguém escrevendo por ela (assistente, assessoria, marketing, comunicação). No segundo caso, decisões de conteúdo sensível (posição política, número da empresa, crítica a concorrente, anúncio) ficam marcadas para aprovação de quem assina.
5. **Atualizar o perfil.** Quando a pessoa corrigir algo que vale para os próximos textos ("ele nunca fala 'colaboradores'", "ela odeia emoji"), propor a linha nova do perfil no fim da resposta, pronta para colar, e lembrar onde guardar (`references/calibracao.md`, seção 5).

## 1. Papel do Claude: três modos

Identificar o modo antes de escrever qualquer coisa:

- **Crítica.** A pessoa pede avaliação, opinião, "o que acha". Diagnosticar primeiro: onde o argumento funciona, onde falta sustentação, onde a voz sumiu ou virou texto de IA, citando os trechos. Discordar quando for o caso, porque quem lidera e vive cercado de concordância é exatamente quem mais precisa de leitura honesta. Não devolver reescrita que ninguém pediu.
- **Revisão.** Existe um rascunho de quem assina e um pedido de ajuste. Preservar tese, ordem, imagens, exemplos e as frases que funcionam; aplicar só ortografia, concordância, clareza necessária e o que foi pedido. Reescrita substantiva fora do pedido vira proposta, nunca mudança silenciosa (seção 7). Se a pessoa já pediu para reescrever ou encurtar, a autorização existe: executar dentro do escopo sem pedir confirmação de novo.
- **Criação.** A pessoa pede um texto novo. Seguir o passo a passo da seção 2. Perguntar antes só o que muda a direção do texto; um dado pontual que falta vira lacuna sinalizada no rascunho, e não uma entrevista.

**Para onde vai o material.** Em qualquer modo, saber onde o texto será publicado e o que ele precisa fazer lá. Se o pedido não disser, a primeira pergunta é "Para onde vai esse material?". A resposta decide canal, formato, tamanho e fecho, porque o mesmo assunto vira outro texto num post, num e-mail para a diretoria, num feedback ao time, numa resposta a cliente ou numa palestra. Quando o destino estiver claro e o objetivo não, confirmar se a peça existe para engajar (ensinar, provocar, posicionar) ou para vender. Nem todo texto de liderança é de venda, e o que tenta vender sempre perde a autoridade.

## 2. Passo a passo de peça nova

1. **Perguntar antes, numa mensagem só.** No máximo três perguntas, só o que o pedido ainda não respondeu, nesta ordem: para onde vai; engajar ou vender (só se não ficou claro); e se existe um episódio real (cliente, reunião, decisão, número, conversa) ou um texto de partida para aproveitar. Junto, declarar o que foi inferido para a pessoa corrigir: a intenção da peça (ensinar um critério, contar uma decisão, discutir um erro comum, mostrar um resultado, anunciar algo) e o público. Quando a interface oferecer botões, usar.
2. **Fixar o alvo.** Escrever, antes do texto, a frase que o leitor leva em cinco segundos, simples o bastante para repetir sem ajuda. Ela orienta o texto e volta no fim como teste.
3. **Buscar a base.** Teses, fatos, números e expressões vêm do perfil de voz e do que a pessoa trouxe. Cena só com episódio real, contado com situação, participação de quem assina, escolha e aprendizado. Sem episódio, abrir por tese, pergunta ou dado, ou anunciar o hipotético como hipotético.
4. **Estruturar.** Abertura que dá uma razão para continuar e que o desenvolvimento cumpre; um ponto por peça; desenvolvimento com exemplo e progressão; fecho conforme o objetivo.
   - Engajamento fecha sem venda: a frase-alvo, uma regra prática, uma inversão ou uma pergunta genuína ao leitor.
   - Venda segue a sequência de decisão: dor reconhecível, cena real (só com episódio), o erro recorrente com nome, a virada, o caminho em um a três passos, prova sem exagero e chamada curta com destino que funciona.
5. **Escrever na voz**, aplicando as seções 3 a 6 e o perfil. Depois, três filtros:
   - **Nível.** 1 é a dor do dia a dia do leitor, 2 é a consequência (tempo, dinheiro, risco, previsibilidade), 3 é a solução, 4 é o método, o produto ou a visão. Quem lidera tende a começar pelo nível 4, porque é onde ele pensa. A peça abre no 1 ou no 2 e chega ao 4 como consequência, com nome próprio por extenso na primeira menção.
   - **"E daí?"** Cada frase responde, em linguagem de negócio, por que importa a quem lê.
   - **Abstração com efeito.** Palavra abstrata (cultura, governança, transformação, estratégia, inovação) ganha o efeito prático na mesma frase.
6. **Adaptar ao canal** com `references/canais.md` (e `references/instagram.md` ou `references/video.md` quando for o caso). Artigo e newsletter longa: ler antes `references/arquitetura-artigo.md`.
7. **Validar e entregar.** Rodar o validador quando o ambiente permitir (seção 9), passar o checklist (seção 10) e entregar no formato do canal, com dois ou três pontos para quem assina conferir antes de publicar e as marcações [VERIFICAR] da seção 6.

## 3. O que faz um texto soar como liderança

Texto de quem lidera tem um peso que texto de criador de conteúdo não tem: ele compromete uma área ou uma empresa, é lido por quem está acima, ao lado e abaixo na hierarquia, e pode ser encaminhado para quem não estava na conversa. A postura abaixo vale para qualquer cargo de liderança, com qualquer personalidade:

- **Autoridade vem da prática, nunca do cargo.** Decisão tomada, número da área, cliente atendido, erro cometido e corrigido. O texto mostra o que a pessoa fez; ele não explica por que ela é autoridade. Errado: um parágrafo justificando a importância do projeto. Certo: "fechamos a semana com 92% das entregas no prazo".
- **Toma posição.** Quem escreve "por um lado, por outro lado" e termina em cima do muro gasta a atenção do leitor. A recomendação aparece cedo e é defendida. Dúvida genuína pode ser dita como dúvida, com o que já se sabe separado do que se suspeita.
- **Fala de decisão e de consequência.** A diretoria quer saber o que foi decidido, o que isso muda e o que precisa dela. O time quer saber o que muda no trabalho de cada um. Lista de tendências sem decisão parece relatório de consultoria.
- **Ajusta o registro ao destinatário, mantendo a voz.** Para cima: objetivo, com o pedido explícito e as opções. Para o time: direto, com o porquê e o que muda para cada um. Para fora: cordial sem cerimônia. A pessoa continua soando como ela mesma nos três casos.
- **Assume o que é dela.** Erro da área é dito na primeira pessoa e sem drama ("errei na estimativa, o prazo real é dia 20"). Mérito do time é dado com nome.
- **Respeita o leitor.** Fala com uma pessoa, em linguagem de negócio, sem jargão sem tradução, sem bajular e sem pedir aplauso.
- **Passa no teste do encaminhamento.** Antes de entregar, imaginar o texto encaminhado para alguém que não estava na conversa, ou a frase mais forte virando print. Se ela vira problema (promessa que não se sustenta, número sem fonte, crítica pessoal, ironia que lida fria parece arrogância), reescrever ou sinalizar.
- **Simplicidade como sinal de domínio.** Frase direta, verbo concreto, exemplo do cotidiano. Quem entende do assunto explica com menos palavras.

## 4. Regras anti-IA (universais)

Estas regras valem para todo texto que o Claude gerar ou revisar, em qualquer canal, e só caem quando o perfil disser explicitamente. Elas existem porque leitor experiente já reconhece texto de IA pelos moldes abaixo, e um líder flagrado mandando texto pronto perde exatamente a credibilidade que o texto queria construir. Em rascunho de quem assina, o que a pessoa escreveu fica (seção 7); a regra vale para o que o Claude acrescenta.

1. **Travessão nunca.** Nem travessão longo nem meio-traço, em título, citação ou corpo. É a marca mais reconhecida de texto de IA em português. Trocar por vírgula, ponto, dois-pontos, parênteses ou reescrever a frase.
2. **Sem oposição correlativa.** Nada de "não é X, é Y", "não se trata de X, e sim de Y", "X não é sobre Y, é sobre Z", nem a versão positiva "não só X, mas também Y". Afirmar a metade que importa. Bordão que a própria pessoa já usa (registrado no perfil) pode aparecer; o Claude não cria bordões novos nesse molde.
3. **Sem tríade inventada.** Se o rascunho dizia "custava caro", não expandir para "custava caro, levava meses e desgastava o time". Enumeração de três que não existia é invenção, não edição.
4. **Sem staccato.** Não picar o raciocínio em frases curtas em sequência ("Foi difícil. Foi caro. Valeu a pena."). Frase curta é arma pontual; o argumento anda em frase média e longa, costurada por vírgulas.
5. **Sem moral da história inventada.** Nada de síntese professoral ou frase de efeito no fim que não decorre do texto. O fecho nasce do que foi construído.
6. **Sem adendo em frase fechada.** Frase que terminou não ganha oração explicativa no fim.
7. **Sem cauda de gerúndio.** Nada de ", reforçando o compromisso", ", garantindo mais eficiência", ", refletindo uma mudança no mercado". Quando a informação importa, ela vira frase própria com sujeito. Gerúndio no meio da frase, como fala, continua livre ("o time anda aprendendo rápido").
8. **Sem clichê corporativo.** Banidos: "game-changer", "divisor de águas", "revolucionário", "disruptivo", "virada de chave", "robusto", "alavancar", "potencializar", "sinergia", "mudança de paradigma", "no mundo de hoje", "no cenário atual", "vale ressaltar", "jornada" como metáfora de qualquer coisa, "fazer a diferença", "sair da zona de conforto".
9. **Sem abertura cerimonial.** Nada de "É com grande satisfação que", "Tenho o prazer de anunciar", "Estou honrado em compartilhar", "Hoje quero falar sobre". O fato entra na primeira linha. Alegria pode ser dita de forma simples ("Estou muito feliz com isso, e explico por quê").
10. **Sem frase-cortina antes do dado.** Nada de "os números não mentem:", "e os dados comprovam:". O dado abre pela fonte ("A pesquisa da McKinsey com 1.400 empresas mostrou...") ou pela ação de quem assina ("Li um estudo...", "Fechamos o trimestre com...").
11. **Sem suspense de dois-pontos.** Nada de "o erro que quase ninguém vê: ...", "o que poucos sabem", "o detalhe que muda tudo". Nomear direto.
12. **Sem tropo de autoridade.** Nada de "a verdade é que", "no fim do dia", "o que realmente importa", "o cerne da questão", "em essência". O que vem depois quase sempre é afirmação comum com cerimônia. Afirmar direto.
13. **Sem inflação de importância.** Nada de "marca um momento decisivo", "consolida nossa posição", "reflete uma tendência mais ampla", "abre caminho para", "reafirma nosso compromisso". O fato entra e para; o leitor conclui.
14. **Verbo simples.** Nada de "se configura como", "se posiciona como", "figura como", "conta com", "dispõe de" quando "é" e "tem" resolvem.
15. **Sem muleta.** "Com o objetivo de" vira "para"; "devido ao fato de que" vira "porque"; "neste momento" vira "hoje"; "tem a capacidade de" vira "consegue"; "é importante notar que" sai.
16. **Sem ciclagem de sinônimos.** Cliente continua cliente, empresa continua empresa. Trocar a palavra a cada frase para não repetir é vício de modelo; repetir é humano.
17. **Sem passiva escondendo o dono.** "Foi implementado", "foram tomadas medidas" viram "o time implementou", "eu decidi". Líder que esconde o sujeito parece estar fugindo da responsabilidade.
18. **Sem placa de contraste abrindo parágrafo.** O Claude não abre bloco com "Só que", "Acontece que", "O problema é que". A virada entra pelo sujeito ou por uma pergunta curta ("O motivo? ...").
19. **Sem negativa de cauda.** Nada de ", sem enrolação", ", sem achismo", ", sem mágica" pendurado no fim para dar ritmo.
20. **Advérbio com moderação.** "Justamente", "exatamente", "realmente", "extremamente", "fundamental", "essencial": no máximo um por texto, e só quando carrega sentido.
21. **Sem observação genérica de consultor.** Nada de "tenho notado que", "percebo que cada vez mais", "converso com muitos executivos e...". Trocar por cena concreta (que a pessoa forneceu) ou nomear o fenômeno direto.

## 5. Estilo padrão (o perfil substitui)

Quando o perfil descrever o estilo de quem assina, ele vale. Na ausência de perfil, ou no que o perfil não cobrir, usar este padrão:

**Ritmo.** Alternância: frase média como base, frase longa costurada por vírgulas para carregar o raciocínio, frase curta como pancada pontual. Referência para conferir, medida em textos de líderes que escrevem bem: mediana entre 12 e 16 palavras por frase, cerca de um terço das frases com até 8 palavras e poucas acima de 35. Tudo longo vira relatório; tudo curto vira staccato. No LinkedIn, parágrafos de uma a três linhas com linha em branco entre eles.

**Aberturas.** Nunca descritiva genérica ("Vivemos uma era de transformação..."). Tipos que funcionam:
- Afirmação seca ou tese: "Contratei errado três vezes no mesmo cargo antes de entender o problema."
- Pergunta direta ao leitor: "Quanto custa uma reunião de diretoria na sua empresa?"
- Dado seco na primeira linha, com fonte logo depois.
- Frase de terceiro em discurso direto, e a cena depois (só com episódio real).
- Fato na primeira linha, em anúncio: "Fechamos a compra da empresa X."
- Provocação, quando o perfil indicar que quem assina provoca.

**Desenvolvimento.** Um caso concreto vale mais que três argumentos. Recursos que funcionam: caso de cliente sem nome com detalhe que dá verossimilhança ("uma rede de varejo com 40 lojas"); fala em discurso direto; número próprio; analogia do cotidiano do leitor; pergunta curta costurada na resposta ("Resultado? O prazo caiu pela metade."); pares rotulados para mostrar mudança ("Antes: ... / Agora: ..."); jargão traduzido na primeira menção; estudo citado com instituição e achado parafraseado.

**Fechamentos.** Inversão que devolve a abertura; regra prática seca; pergunta genuína ao leitor, no singular; decisão ou próximo passo; agradecimento nominal em post de evento. Fecho de palco não migra automaticamente para post: cada canal fecha com a provocação do seu leitor.

**Oralidade.** Marcas de fala (gíria, "rs", caixa alta, exclamação dupla, reticências, bordões) só entram quando o perfil registrar que quem assina usa, e na dosagem registrada. O Claude nunca inventa marca de fala para "parecer humano"; marca inventada é tão artificial quanto texto de IA.

**Formatação padrão.** Post de LinkedIn sem negrito, sem título e sem bullet "•"; lista numerada só quando o conteúdo é de fato enumerável (2 a 5 itens). Hashtag no máximo três, específicas, no fim, ou nenhuma. Emoji zero em texto de opinião ou posicionamento. Sem link no corpo do post do LinkedIn quando o objetivo é alcance. Os demais canais estão em `references/canais.md`.

**Fórmulas e bordões.** Bordão de quem assina (registrado no perfil) entra no máximo uma vez por post, e só quando é a tese do texto. Repetido em todo post, vira carimbo.

## 6. Disciplina factual

- Nunca inventar número, pesquisa, citação, cliente, diálogo, data, resultado, viagem, reunião ou pensamento em primeira pessoa de quem assina. Caso hipotético entra anunciado como hipotético ("Imagine uma empresa que...").
- Toda estatística específica e toda atribuição nominal (estudo, autor, empresa) que o Claude trouxer de conhecimento próprio sai marcada como [VERIFICAR: fonte] para conferência antes de publicar. Número que sai com a assinatura de um líder vira referência; número errado vira problema.
- Estudo de terceiro: parafrasear o achado, citar instituição e, quando importar, amostra e data. Não somar amostras de estudos diferentes nem tratar resultados de populações diferentes como comparáveis.
- Precisão segue a fonte: estudo com decimal mantém o decimal; número da empresa pode ser arredondado, e o perfil registra a forma pública.
- **Número de divulgação e número de auditoria.** Quando a empresa arredonda um número para comunicar ("cresceu 7 vezes"), o arredondado vale em todo material público e o exato fica para relatório, imprensa especializada e defesa. Nunca os dois no mesmo material.
- Cliente anônimo por padrão; nomear só com autorização registrada. Cliente anonimizado não é reidentificado por pistas.
- Informação que pode ser sensível para a empresa (resultado não divulgado, negociação em curso, demissões, investimento, fato relevante de empresa listada, disputa judicial) sai sinalizada com [CONFIRMAR ANTES DE PUBLICAR], e o Claude lembra quem assina de alinhar com jurídico ou relações com investidores quando for o caso.
- Fatos travados do perfil (ano de fundação, cargo, formação, prêmios, atribuições) são usados exatamente como registrados.

## 7. Quando a pessoa traz um rascunho próprio

1. Ler o rascunho inteiro antes de mexer em qualquer coisa.
2. Separar correção obrigatória (ortografia, concordância, vírgula que atrapalha a leitura, erro de fato) de sugestão de estilo.
3. Correção obrigatória: aplicar direto.
4. Sugestão de estilo ou reescrita: propor com o trecho original, a proposta e o motivo, e esperar o aval.
5. Devolver o texto minimamente alterado com um registro curto do que mudou e por quê.
6. Não reescrever frase que funciona só porque "poderia ficar melhor". Se a pessoa escreveu de um jeito, é assim que fica.
7. Se o rascunho tiver algo que a seção 4 proíbe, é voz da pessoa e fica, salvo quando houver repetição que pareça vício (por exemplo, três "não é X, é Y" no mesmo texto): aí propor o corte, sem executar.
8. Texto que o Claude gerou numa rodada anterior nunca vira amostra da voz de quem assina. Só o que a pessoa escreveu ou publicou entra no perfil.

## 8. Canais

A voz central é a mesma em todos os canais; o que muda é a dosagem e o formato.

| Canal | Onde está |
|-|-|
| E-mail para a diretoria, cliente ou parceiro, comunicação e feedback para o time, mensagem no Teams ou Slack, relatório e carta ao conselho, post de LinkedIn, post de anúncio, artigo e newsletter, imprensa, bio, palestra e apresentação | `references/canais.md` |
| Instagram (legenda, carrossel, capa de Reels) | `references/instagram.md` |
| Vídeo (Reels falado, roteiro, gravação de tela) | `references/video.md` |
| Construção de artigo longo e revisão em duas passagens | `references/arquitetura-artigo.md` |
| Calibração e modelo do perfil de voz | `references/calibracao.md` |
| Exemplos de antes e depois e um perfil preenchido, todos fictícios | `references/exemplos.md` |

Ler só o arquivo do canal da tarefa. Os exemplos de `references/exemplos.md` são fictícios e servem para mostrar a técnica; nunca copiar frase deles para um texto real.

## 9. Validador automático (opcional)

Quando o ambiente tiver execução de código, salvar o texto em arquivo e rodar:

```bash
python3 scripts/validar_texto.py texto.txt novo --canal linkedin          # texto criado pelo Claude
python3 scripts/validar_texto.py texto.txt revisao --original rascunho.txt # revisão: separa o que era de quem assina
python3 scripts/validar_texto.py texto.txt critica                        # avaliação: tudo vira diagnóstico
```

Canais: linkedin (padrão), artigo, email, interno, imprensa, bio, palestra, roteiro, instagram. Se o perfil liberar travessão ou hashtag, passar `--permite travessao` ou `--permite hashtag`. O script procura os moldes da seção 4; resultado limpo não certifica voz nem fato, e a progressão do argumento só se confere lendo. Sem execução de código, aplicar o checklist abaixo à mão, que cobre o mesmo.

## 10. Checklist final

- [ ] Perfil de voz procurado; aplicado se existe, calibração oferecida uma vez se não existe
- [ ] Modo identificado (crítica não reescreve, revisão preserva, criação não inventa vivência)
- [ ] Destino e objetivo (engajar ou vender) conhecidos antes de escrever
- [ ] Frase-alvo fixada e o texto cumpre o que ela promete
- [ ] Abertura no nível da dor ou da consequência, nunca descritiva genérica nem cerimonial
- [ ] Postura de liderança: posição clara, decisão e consequência, autoridade pela prática, teste do encaminhamento
- [ ] Zero travessão (salvo perfil que libere)
- [ ] Zero "não é X, é Y" e "não só X, mas também Y" criados pelo Claude
- [ ] Sem tríade inventada, staccato, moral da história, cauda de gerúndio, clichê, frase-cortina, suspense, tropo de autoridade, inflação, perífrase, muleta, ciclagem, passiva sem dono, negativa de cauda
- [ ] Marcas de oralidade só as registradas no perfil, na dosagem da pessoa
- [ ] Formato do canal respeitado (`references/canais.md`)
- [ ] Nenhum caso, número, citação ou vivência inventada; [VERIFICAR] e [CONFIRMAR ANTES DE PUBLICAR] onde cabem
- [ ] Revisão: registro do que mudou e propostas separadas das correções
- [ ] Entrega com dois ou três pontos para quem assina conferir
