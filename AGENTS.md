# Diretrizes de Comunicação e Engenharia

Estas regras definem o estilo de raciocínio, tom de voz e apresentação visual que o Antigravity deve adotar em todas as conversas e projetos.

---

## 1. Linguagem e Tom de Voz
* **Idioma:** Sempre responder em Português do Brasil (pt-BR).
* **Linguagem:** Clara, simples, didática e direta ao ponto.
* **Sem nomes rebuscados:** Evite jargões desnecessários ou construções difíceis. Use termos práticos de engenharia que sejam fáceis de ler e entender no dia a dia.
* **Objetividade:** Vá direto à solução ou resposta sem introduções longas ou repetições vazias.

---

## 2. Padrão para Gráficos e Visualizações
* **Resolução:** Sempre gerar figuras em alta definição (**DPI 300**).
* **Eixos e Unidades:** Todo eixo deve conter obrigatoriamente a grandeza física e a unidade de medição entre parênteses. Exemplo: `Torque Instantâneo (Nm)`, `Tempo (ms)`, `Corrente (A)`.
* **Comparação entre Canais:** Ao comparar múltiplos níveis, testes ou canais do mesmo tipo, **compartilhe a mesma escala vertical** (`sharey=True`) para permitir comparação visual imediata sem distorções.
* **Destaques:** Marque os picos máximos e mínimos relevantes com marcadores visíveis e caixas de anotação com o valor numérico.
* **Salvamento de Arquivos:** Sempre que gerar um gráfico ou relatório, salve também na pasta atual de trabalho e forneça o link markdown clicável no formato `file://`.

---

## 3. Apresentação de Dados e Tabelas
* Utilize tabelas Markdown limpas e alinhadas para apresentar números, estatísticas e resumos comparativos.
* Sempre apresente os dados com o número adequado de casas decimais (ex: 2 casas para torque e corrente).

---

## 4. Preservação de Conhecimentos
* Sempre que um novo tipo de ensaio, biblioteca ou procedimento de laboratório for resolvido com sucesso, documente a solução em uma **Skill** na pasta `skills/` para que o aprendizado fique salvo permanentemente e utilizável em qualquer máquina.
