---
name: python-testing
description: >-
  Padrões avançados de testes em Python com Pytest (baseado em affaan-m/ECC).
  Fixtures idiomáticas, parametrização cirúrgica de casos de borda, mocks seguros e testes assíncronos.
---

# Python Testing: Padrões Avançados com Pytest

Este guia define as diretrizes para construção de suítes de testes automatizados em Python rápidas, isoladas e fáceis de manter, garantindo cobertura real de comportamento e validação de casos de borda.

---

## 1. Princípios Estruturais (Padrão AAA)

Todo teste unitário deve seguir a separação clara em três blocos:
1. **Arrange (Preparar):** Configurar os dados de entrada, instanciar objetos e preparar dependências.
2. **Act (Agir):** Executar a função ou método específico sob teste (preferencialmente em uma única linha).
3. **Assert (Afirmar):** Validar o resultado e os efeitos colaterais com asserções explícitas.

*Regra de Ouro:* Testes unitários nunca devem tocar a rede externa nem depender de bancos de dados reais. Toda dependência lenta de I/O deve ser substituída por adaptadores em memória ou fakes controlados.

---

## 2. Gestão Idiomática de Fixtures

* **Escopos Conscientes:**
  * `scope="function"` (padrão): Para objetos mutáveis ou estados que devem ser recriados a cada teste.
  * `scope="module"` ou `scope="session"`: Para recursos somente leitura ou inicializações computacionalmente caras (como carregamento de tabelas de calibração ou modelos estáticos).
* **Uso de Fixtures Nativas do Pytest:**
  * Utilize `tmp_path` (objeto `pathlib.Path`) para manipulação de arquivos temporários durante o teste. Ele garante isolamento e limpeza automática do disco pelo Pytest.
  * Utilize `monkeypatch` para sobrescrever variáveis de ambiente ou atributos em tempo de execução sem vazar alterações para os demais testes.

---

## 3. Parametrização de Casos de Borda

Evite duplicar funções de teste para validar diferentes entradas. Utilize `@pytest.mark.parametrize` para testar limites numéricos, strings vazias, valores nulos e exceções esperadas:

```python
import pytest
from src.calculos import calcular_frequencia_golpes

@pytest.mark.parametrize(
    "delta_tempo_s, esperado",
    [
        (0.05, 1200.0),  # Intervalo típico de ensaio
        (0.10, 600.0),   # Frequência menor
        (0.02, 3000.0),  # Limite superior de ferramenta rápida
    ],
)
def test_calculo_frequencia_golpes_valores_validos(delta_tempo_s, esperado):
    # Act
    resultado = calcular_frequencia_golpes(delta_tempo_s)
    
    # Assert
    assert resultado == pytest.approx(esperado, rel=1e-2)

@pytest.mark.parametrize("delta_invalido", [0.0, -0.01])
def test_calculo_frequencia_golpes_rejeita_tempo_invalido(delta_invalido):
    with pytest.raises(ValueError, match="Intervalo de tempo deve ser positivo"):
        calcular_frequencia_golpes(delta_invalido)
```

---

## 4. Testes de Funções Assíncronas (`pytest-asyncio`)

Ao testar corrotinas assíncronas, marque explicitamente o teste com `@pytest.mark.asyncio`:

```python
import pytest
from src.servicos import coletar_amostra_stream

@pytest.mark.asyncio
async def test_coleta_amostra_stream_sucesso():
    # Arrange & Act
    dado = await coletar_amostra_stream(canal=0)
    
    # Assert
    assert dado is not None
    assert dado.status == "OK"
```

---

## 5. Mocks e Fakes Seguros

* **Substituição Cirúrgica:** Prefira criar implementações falsas em memória (Fakes/Stubs) em vez de criar cadeias complexas de `MagicMock`. Fakes respeitam as interfaces reais e não mascaram alterações de assinatura de métodos.
* **Auto-spec:** Caso utilize `unittest.mock.patch`, configure sempre `autospec=True` para garantir que o mock rejeite chamadas de métodos inexistentes na classe original.

---

## 6. Checklist de Qualidade da Suíte de Testes

* [ ] Os testes rodam de forma determinística em qualquer ordem (sem dependência entre testes).
* [ ] Nenhuma chamada a servidores externos ou portas de rede reais é realizada durante a execução da suíte unitária.
* [ ] Arquivos gerados durante o teste utilizam a fixture `tmp_path`.
* [ ] Casos de borda (valores nulos, listas vazias, divisões por zero) possuem testes parametrizados dedicados.
* [ ] O comando `pytest -q` executa em poucos segundos.
