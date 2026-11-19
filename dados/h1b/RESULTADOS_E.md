# H1, segunda etapa — entrega E: resultados

Flavio Augusto da Silva · rodado em 19/11/2026, 16:00–16:06 (Brasília), depois do pré-registro ([`PREREGISTRO.md`](PREREGISTRO.md), commit 8b30242). Semente 20261121; nenhum parâmetro mudado.

## Veredito pré-registrado: E-c, inconclusivo

| Critério | Resultado | Passou? |
| --- | --- | --- |
| E1: R² ≥ 0,90 em n = 40, 80, 160 | 0,048 / 0,020 / 0,007 | não |
| E1: resíduo com expoente ≤ 1,2 | 2,23 | não |
| E2: \|assimetria\| < 0,1 e \|curtose exc.\| < 0,2 em n = 160 (só diagnóstico) | −0,049 e +0,138 | sim |
| E3: colapso em ω = nθ (≥ 80% dentro de 3 erros) | 0 de 9 (desvios de 14 a 75 erros) | não |
| E3: modelo decisivo (ΔAIC ≥ 10) | exponencial, ΔAIC = 29.650, mas χ²/gl de 2.696 a 11.295 nos três modelos | formalmente sim, sem valor sem colapso |
| E3: estrutura fina desprezível | 0 de 4 pontos válidos (desvios de 4,9 a 82 erros) | não |

Definição fixada depois do registro, mas antes de qualquer resultado: no teste de estrutura fina, o erro combinado junta o erro da medida, a incerteza dos parâmetros e os termos com k ≠ 0.

## Pontos abaixo da resolução

- Ângulos pequenos: n = 40 a partir de θ = 0,16; n = 80 a partir de 0,045; n = 160 a partir de 0,02.
- Janela (x = 6, 7, 8): os 15 pontos são compatíveis com zero (maior desvio de 1,4 erros). Em n = 40, |φ|² < ~3 × 10⁻⁶.
- Estrutura fina: 5 de 9 pontos.

## Falhas de convergência

Nenhuma.

## Exploratório (fora do registro; não muda o veredito)

Em `h1b_E_exploratorio.txt`:

1. O desvio de B cresce como n^1,09. Com u = desvio·θ, Q coincide com a gaussiana e^(−u²) só até u ≈ 1; acima disso fica muito maior (n = 40, u = 6,1: 3,6 × 10⁻⁵ contra 1,2 × 10⁻¹⁶). A fase decai mais devagar que uma gaussiana, embora a distribuição de B se aproxime da gaussiana.
2. A variância de B vem de N₁ e N₂ (pesos 9 e −16), que flutuam juntos e se cancelam em parte; não vem do tamanho, da altura nem dos extremos da teia.

## Conclusão

O experimento não decidiu H1. A hipótese de trabalho de E (modo global com colapso em nθ) foi rejeitada pelos critérios registrados. Pela ordem registrada, seguem B e depois C.

## Como reproduzir

```
cd scripts
python h1b_E_dados.py 10 20 40 80
python h1b_E_dados.py 160
python h1b_E_analise.py
python h1b_E_exploratorio.py
```

Os arquivos `h1b_E_n*.npz` desta pasta são os dados usados; `h1b_E_analise.py` rodado sobre eles reproduz `h1b_E_relatorio.txt`.
