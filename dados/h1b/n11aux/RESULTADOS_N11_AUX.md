# Investigação auxiliar em n = 11: teias ruins contra todas as outras ordens — resultados

Flavio Augusto da Silva · rodado em 20/11/2026, 14:59–16:47 (Brasília), depois do pré-registro ([`../PREREGISTRO_N11_AUX.md`](../PREREGISTRO_N11_AUX.md), commit 4a45931).

> **Estatuto.** "Não ruins" = todas as ordens de altura ≥ 3, caibam ou não em Minkowski 3+1. **Isto não é a definição oficial de teia boa.** Nenhum resultado abaixo demonstra H1\* ou C1 para a definição oficial em n = 11: as ordens que eventualmente não cabem em 3+1 estão incluídas, e somá-las pode aumentar ou diminuir o módulo.

## Validações (todas passaram antes das respostas)

| Validação | Obtido | Esperado |
| --- | --- | --- |
| Classes geradas (A000112) | 46.749.427 | 46.749.427 |
| Σ 11!/\|Aut\| (A001035) | 1.396.281.677.105.899 | 1.396.281.677.105.899 |
| Σ 11!/\|Aut\| nas conexas (A001927) | 1.320.327.172.853.172 | 1.320.327.172.853.172 |
| T_11(ruim) (Teorema 1′) | +1 | +1 |
| Lado ruim × fórmula do E1 | diferença de 1,4 × 10⁻⁷ em ln\|Z\| | < 10⁻⁶ |

O mesmo processamento foi conferido antes em n = 9 (4 partes) contra os valores já conhecidos.

## Respostas

| Pergunta | Resultado | Resposta |
| --- | --- | --- |
| A1: \|T_11(não ruim)\| > 3¹¹ = 177.147 | T_11(não ruim) = +40.491.236.962 | vale |
| A2: \|𝒵_não-ruim\| > 3¹¹/11! = 0,004439 na janela | mínimo pontual 64,63 em ℓ/l_P = 6,574 (conferido em 60 dígitos); cota rigorosa ≥ 0,0819 | vale |
| A3: R_aux = \|𝒵_ruim\|/\|𝒵_não-ruim\| < 1 na janela | máximo rigoroso ≤ 0,700; máximo pontual na grade 3,5 × 10⁻⁷ | vale |

## Correções de método, feitas depois de ver A1 e antes de ver A2 e A3

1. A subdivisão rigorosa também fecha um intervalo quando um ponto exato já decide a pergunta (R ≥ 1 refuta A3), e tem teto de profundidade e de memória. Sem isso, uma região que não fecha cresceria sem limite.
2. As somas passaram a ser avaliadas em blocos de 20.000 ângulos. Com 436 valores de B, a avaliação de uma vez só pedia ~4 GB e o processo morria em silêncio. O resultado é idêntico.

A1 não depende de nenhuma das duas.

## Descritivo (sem valor de teste)

W_não-ruim = 34.954.385,4; B de −327 a 226 (436 valores ocupados de 554); desvio de 31,67, assimetria de −0,33, curtose em excesso de +0,65; parte não suave de 1,8%; mediana de |𝒵|/W na janela de 1,56 × 10⁻⁴. Continua a tendência de n = 5 a 10: espectro mais suave e mais gaussiano.

## Como reproduzir

```
cd scripts
./h1b_N11_roda.sh 0 2 4 6 8 10 12 14 16 18   # e, em paralelo, as partes ímpares
python h1b_N11_analise.py                     # na pasta das partes
```
