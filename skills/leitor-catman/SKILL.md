---
name: leitor-catman
description: >-
  Guia e scripts para leitura, processamento e análise de arquivos de aquisição de dados do software HBM catman (.BIN e .TST).
  Use sempre que precisar inspecionar canais, ler sinais de alta frequência (DAQ), filtrar/decimar dados sem ruído,
  ou calcular parâmetros de ensaios de torque e ferramentas de impacto (picos, frequência de golpes IPM e relação com corrente).
---

# Leitor e Analisador de Aquisições HBM catman (.BIN / .TST)

Este guia prático ensina como abrir, inspecionar e analisar dados brutos de aquisição gerados pelo software **catmanEasy / catmanAP** e módulos **HBM QuantumX**.

---

## 📌 1. O que são esses arquivos?

* **Arquivo `.BIN`:** Contém as medições brutas em alta frequência (amostras salvas em ponto flutuante de 64 bits). Pode ter dezenas de megabytes com milhões de pontos.
* **Arquivo `.TST`:** É um arquivo de texto/cabeçalho leve que acompanha o `.BIN`. Ele guarda a data/hora real de início, taxa de amostragem padrão (ex: 19.200 Hz), versão do software e modelo dos sensores/módulos.

---

## 🛠️ 2. Passos Obrigatórios para Leitura

### Passo 1: Não carregue o arquivo inteiro sem inspecionar
Como arquivos de 19,2 kHz têm milhões de pontos, sempre inspecione primeiro os nomes dos canais e a duração antes de tentar carregar tudo na memória:

```python
from apread import APReader

leitor = APReader("CAMINHO_DO_ARQUIVO.BIN")
for grupo in leitor.Groups:
    print(f"Grupo: {grupo.Name} | Pontos: {len(grupo.Channels[0].data):,}")
    for canal in grupo.Channels:
        unidade = canal.extHeader.get('PhysUnit', '').strip()
        print(f"  - {canal.Name} ({unidade})")
```

### Passo 2: Decimação com Anti-Aliasing (Média de Bloco)
Ao reduzir a taxa de amostragem (por exemplo, de 19.200 Hz para 1.000 Hz para gerar um gráfico leve):
* **Nunca faça apenas `dados[::fator]`** (pular amostras perde os picos reais de impacto e gera falso ruído por *aliasing*).
* **Sempre aplique média de bloco**:
  ```python
  def decimar_com_media(dados, fator):
      if fator <= 1:
          return dados
      resto = len(dados) % fator
      bloco = dados[:-resto] if resto else dados
      return bloco.reshape(-1, fator).mean(axis=1)
  ```

### Passo 3: Base de Tempo Absoluta (Data e Hora UTC)
O canal de tempo do catman (`Channel[0]`) marca o tempo relativo a partir de `0.0 s`. Para achar o timestamp real:
* O início está em `canal.extHeader['T0']` (formato dias do Excel).
* Conversão: `timestamp_unix = (T0 - 25569) * 86400`.

---

## ⚡ 3. Análise de Ensaios com Chave de Impacto

Em testes de ferramentas de aperto por impacto (como a chave CIWLI2045):

1. **Pico Máximo de Torque ($T_{max}$):**
   * O ponto mais alto registrado durante a rajada de impacto.
2. **Torque Médio Sustentado:**
   * Média aritmética de todos os picos de impacto detectados na rajada. Esse valor mostra a verdadeira energia de aperto entregue pela ferramenta.
3. **Cadência de Golpes (IPM - Impactos por Minuto):**
   * Detecte os picos de impacto (`scipy.signal.find_peaks` com distância mínima de ~15 ms).
   * $\text{Frequência (Hz)} = \frac{1}{\Delta t_{\text{médio entre golpes}}}$
   * $\text{IPM} = \text{Frequência (Hz)} \times 60$.
4. **Rebote Negativo ($T_{min}$):**
   * A oscilação negativa de recuo elástico gerada após cada martelada da bigorna.
5. **Relação com a Corrente:**
   * Conforme a corrente consumida pelo motor aumenta (Nível 1 $\rightarrow$ Nível 2 $\rightarrow$ Nível 3), a cadência (IPM) e a média sustentada de impacto aumentam proporcionalmente. O pico máximo pode estabilizar devido à saturação elástica da junta.

---

## 📊 4. Padrão Visual dos Gráficos

* Manter sempre **DPI 300** para relatórios nítidos.
* Usar unidades nos eixos: `Torque Instantâneo (Nm)` e `Tempo (ms)` ou `Tempo (s)`.
* Quando comparar níveis diferentes, usar sempre **a mesma escala no eixo Y** (compartilhada) para facilitar a comparação visual imediata.
