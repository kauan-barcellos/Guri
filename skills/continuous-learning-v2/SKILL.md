---
name: continuous-learning-v2
description: >-
  Motor de instintos e aprendizado contínuo (baseado em affaan-m/ECC).
  Observa correções do usuário, extrai instintos atômicos com pontuação de confiança e evolui lições validadas em regras permanentes.
---

# Continuous Learning v2: Motor de Instintos

Este guia estabelece o protocolo de aprendizado contínuo do agente, convertendo correções, preferências operacionais e soluções de contorno em conhecimento persistente e autoevolutivo.

---

## 1. Conceito Central e Ciclo de Vida

Em vez de depender de comandos manuais para salvar lições, o agente monitora ativamente as interações e correções durante as sessões de trabalho.

```
+------------------+      +-------------------+      +-------------------+      +-------------------+
|  1. Observar     | ---> | 2. Criar Instinto | ---> | 3. Pontuar        | ---> | 4. Promover       |
| Correção/Ajuste  |      | Registro Atômico  |      | Confiança (0 a 1) |      | Skill / GEMINI.md |
+------------------+      +-------------------+      +-------------------+      +-------------------+
```

1. **Observar:** Identificar quando o usuário corrige um comportamento, expressa uma preferência explícita ("prefiro X", "não faça assim", "utilize sempre Y") ou quando uma solução técnica contorna um erro persistente.
2. **Criar Instinto:** Isolar a regra em formato atômico (gatilho claro e ação obrigatória), sem poluir o contexto global imediatamente.
3. **Pontuar Confiança:** Avaliar a frequência e a consistência da observação ao longo das sessões.
4. **Promover:** Quando o instinto atinge o limiar de confiança estipulado, transformá-lo em uma Skill oficial ou em diretriz permanente no arquivo de regras do projeto.

---

## 2. Estrutura do Registro de Instinto

Os instintos identificados em nível de projeto são mantidos no arquivo de estado da sessão ou no registro local de memória (`INSTINCTS.md` ou integrado ao `PROJECT_MEMORY.md`):

```markdown
### Instinto: [NOME_CURTO]
* **Gatilho (Quando):** Condição exata ou tipo de tarefa onde o padrão se aplica.
* **Ação Obrigatória (Fazer):** O comportamento técnico exigido.
* **Ação Proibida (Evitar):** O comportamento anterior que gerou a correção.
* **Nível de Confiança:** [0.4 / 0.7 / 0.9]
* **Ocorrências:** [Número de validações bem-sucedidas]
* **Última Atualização:** [Data/Hora]
```

---

## 3. Escala e Critérios de Confiança

* **Nível 0.4 (Observado):**
  * Primeira vez que o usuário expressa uma preferência ou faz uma correção específica.
  * O agente registra o instinto localmente e o segue na sessão ativa, mas ainda não generaliza para novos projetos.
* **Nível 0.7 (Validado):**
  * O padrão foi confirmado em uma segunda interação ou validado em um teste empírico sem contradições.
  * O agente aplica a regra proativamente em tarefas semelhantes no mesmo repositório.
* **Nível 0.9 (Promovido):**
  * O padrão foi repetido 3 ou mais vezes com sucesso comprovado.
  * O agente propõe ou executa a promoção do instinto para uma Skill definitiva em `config/skills/` ou adiciona ao arquivo global de regras.

---

## 4. Regras de Higiene e Sanitização

1. **Zero Vazamento de Dados Sensíveis:** Nunca salvar em instintos credenciais, chaves de API, senhas, IPs privados ou dados pessoais (em estrita conformidade com a LGPD e o sanitizador de segredos).
2. **Atomicidade:** Cada instinto deve resolver um único problema específico. Se houver múltiplos ajustes, divida em registros separados.
3. **Não Suposição:** Registrar apenas o que foi explicitamente demonstrado ou solicitado, sem inferir regras hipotéticas sem evidência empírica.
