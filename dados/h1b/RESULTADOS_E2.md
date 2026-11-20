# Consolidação de E (E2): resultados

Flavio Augusto da Silva · rodado em 20/11/2026, ~02:21–02:26 (Brasília), depois do pré-registro ([`PREREGISTRO_E2.md`](PREREGISTRO_E2.md), commit 5a3427b). Semente 20261124; nenhum parâmetro mudado.

**Escopo:** só o sorteio. Nada aqui é evidência sobre H1\*.

## Vereditos

| Teste | Resultado | Veredito |
| --- | --- | --- |
| T1, colapso em u = σ_n·θ | 197 comparações, 12% dentro de 3 erros | não confirmado |
| T2, núcleo gaussiano (u ≤ 1) | 50 pontos, 38% dentro de 3 erros | não confirmado |
| T3, cauda acima da gaussiana (u ≥ 2) | 89 pontos resolvidos, 99% acima por mais de 3 erros | confirmado |
| T4, variância vinda de N₁ e N₂ | V₁₂/Var(B) = 0,947 / 0,934 / 0,951 em n = 40 / 80 / 160 | confirmado |

## O que os números mostram

- **Convergência para a gaussiana, mas sem chegar lá nos tamanhos medidos.** Em u = 1, Q/e^(−u²) vale 1,31 / 1,19 / 1,11 / 1,04 / 1,016 para n = 10 / 20 / 40 / 80 / 160. As diferenças entre tamanhos vizinhos caem (mediana dos desvios: 71 erros entre n = 20 e 40; 22,7 entre 40 e 80; 4,5 entre 80 e 160). Por isso não há colapso exato (T1) nem núcleo exatamente gaussiano (T2), mas as curvas se aproximam de e^(−u²) conforme n cresce.
- **A cauda acima da gaussiana existe e encolhe com n.** Em u = 2,9, Q = 0,225 / 0,042 / 0,0088 / 0,0014 / 0,0006 para n = 10 a 160, contra e^(−u²) = 0,00022. Ela está sempre acima, mas a diferença diminui com n.
- **A variância de B vem de N₁ e N₂ (T4).** Cada um sozinho daria mais que toda a variância de B: em n = 160, os termos diagonais de N₁ e N₂ valem 1,90 e 2,24 vezes Var(B). Os dois flutuam juntos, e a covariância (−3,18 vezes Var(B)) cancela a maior parte. O que sobra é uma diferença pequena entre duas flutuações grandes. É esse resto que cresce como n^2,2.

## Leitura (restrita ao sorteio)

O mecanismo de cancelamento no sorteio é este: B é a sobra de um cancelamento quase perfeito entre os intervalos com 1 e com 2 elementos internos. A distribuição dessa sobra se aproxima da gaussiana conforme n cresce, e a fase média segue e^(−u²) numa faixa de u cada vez maior, com uma cauda mais lenta fora dela.

Na janela, u ≈ σ_n·θ passa de 500 em n = 160, muito além de onde se mede (u ≤ 4). Então esses resultados não dizem qual lei vale na janela para n grande, nem para o sorteio.

## Pontos não resolvidos

n = 160 a partir de u = 3,1; n = 80 a partir de u = 3,7. Valores na tabela `h1b_E2_tabela.csv`.

## Como reproduzir

```
cd scripts
python h1b_E2_dados.py 10 20 40 80 160
python h1b_E2_analise.py
```
