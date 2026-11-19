# E1 — As teias ruins perdem para as teias boas?

Flavio Augusto da Silva · 19/11/2026 · pré-registrado às 02:24 (Brasília), antes de qualquer rodada

## Pergunta

A soma de exp(iS) sobre as teias ruins de duas camadas fica menor que a contribuição das teias boas, e cada vez menor conforme o número de elementos n cresce? Cancelar o termo n² não basta (decisão de 19/11).

## Pré-registro

- **Ação (igual para as duas classes):** Benincasa–Dowker 4D, ε = 1. S/ħ = 2β·B, com B = n − N₀ + 9N₁ − 16N₂ + 8N₃ e β = √(2/3)·x²/(8π), onde x = ℓ/l_P.
- **Teias ruins:** todas as ordens rotuladas de altura ≤ 2. A soma é exata, pela função `lnZ` de `scripts/camadas_variaveis.py`, sem modificação.
- **Teias boas:** n pontos sorteados num diamante causal de Minkowski 3+1, com altura ≥ 3.
- **Normalização comum:** soma rotulada dividida por n!, ou seja, uma amplitude por teia não rotulada (peso 1/|Aut|).
- **Medida principal (exata):** L = ln|Z_ruim| − ln n!.
- **Hipótese declarada H1:** a soma das teias boas, por teia não rotulada, vale pelo menos 1. Com H1, ln(ruins/boas) ≤ L.
- **Cota rigorosa, sem H1:** L_rig = ln|Z_ruim| − 4n·ln(2e(n−1)), pelo teorema de Warren (citado de memória, não conferido). Se L_rig > 0, as ruins vencem com certeza.
- **Diagnóstico de H1:** Γ = |média de exp(iS)| sobre as teias boas sorteadas.
- **Parâmetros:** n = 40, 80, 120, 160; M = 20.000 sorteios por n; semente 20261119. Na janela: x = 6,0; 7,0; 8,0. Controles: x = 0,832; 5,0; 9,0.
- **Sucesso (por x da janela):** L < 0 nos quatro tamanhos e estritamente decrescente.
- **Falha:** L crescendo entre dois tamanhos seguidos, ou L(160) ≥ 0.
- **Discriminação:** os controles 0,832 e 9,0 precisam ter L(160) > L(120); se também passarem, o E1 é inconclusivo.

## Resultados (`e1_resultados.csv`)

| x = ℓ/l_P | n = 40 | n = 80 | n = 120 | n = 160 | Veredito |
| --- | --- | --- | --- | --- | --- |
| 6,0 (janela) | −86,3 | −233,0 | −400,7 | −581,7 | sucesso |
| 7,0 (janela) | −105,9 | −267,6 | −451,0 | −648,4 | sucesso |
| 8,0 (janela) | −72,4 | −203,4 | −360,4 | −535,1 | sucesso |
| 0,832 (controle) | +193,2 | +888,7 | +2.117,9 | +3.887,9 | falha, como esperado |
| 5,0 (controle) | +43,6 | +290,5 | +772,0 | +1.495,2 | falha |
| 9,0 (controle) | +138,8 | +671,2 | +1.628,5 | +3.018,0 | falha, como esperado |

- Dentro da janela, ln|Z_ruim| cresce no máximo como n, enquanto ln n! cresce como n·ln n. Fora dela, ln|Z_ruim| cresce como n².
- Cota rigorosa: L_rig > 0 só em x = 0,832 com n = 160 (+215,7). Nesse grão, as ruins vencem sem hipótese nenhuma.
- Γ dentro da janela: 0,001 a 0,013, sempre abaixo de 2 erros padrão (0,0071). As teias boas têm fases desencontradas, então H1 não recebe apoio da coerência.
- Controles: precisão de 400 contra 800 dígitos sem diferença; Γ com M/2 e com M concorda; 299 sorteios de altura ≤ 2 em n = 40 e nenhum em n ≥ 80.
- Não previsto: 99,9% das teias boas têm automorfismos (cerca de 8 elementos isolados). Pela cota por gêmeos, ln|Aut| ≈ 13,5 a 15,3 em média (`e1_diagnostico.txt`), pequeno diante das margens de 535 ou mais.

## Conclusão

Dentro da janela 1, a soma das teias ruins por teia não rotulada cai de e^(−72) para e^(−535) ou menos entre n = 40 e n = 160. Isso é exato e mais forte que cancelar o termo n². Que isso signifique supressão em relação às teias boas depende de H1, que continua sem demonstração (classe B). No grão da entropia (0,832 l_P), as teias ruins dominam (classe A, condicionada à citação de Warren).

Limites: só teias ruins de duas camadas; n ≤ 160; ε = 1; teias boas só do diamante plano 3+1.

## Como reproduzir

```
pip install numpy scipy mpmath
cd scripts
python e1_validacao.py
python e1_rodada.py
python e1_diagnostico.py
```

`e1_rodada.py` grava `e1_resultados.csv`, `e1_amostras.npz` e `e1_teias_boas.json` na pasta atual; eles devem sair idênticos aos desta pasta.
