# O centro da janela (β = π/2) como contagem com sinal — exploração (fora de registro)

Flavio Augusto da Silva · 20/11/2026 (Brasília). Exploratório. Saída: `n9n10/exploratorio_contagem_sinal.txt`.

## Redução exata (demonstrada)

Em θ = 2β = π, e^(iπB) = (−1)^B e B ≡ n + N₀ + N₁ (mod 2). Logo a soma rotulada sobre qualquer classe de teias é (−1)ⁿ vezes uma **contagem com sinal**:

T_n(classe) = Σ_{ordens rotuladas da classe} (−1)^(N₀ + N₁),  𝒵_classe(π) = (−1)ⁿ·T_n/n!

com N₀ = número de ligações e N₁ = número de pares com exatamente um elemento entre eles. Para n ≤ 10, como toda teia de altura ≥ 3 cabe em 3+1, T_n(boa) = T_n(todas) − T_n(ruim).

Duas consequências imediatas:
- **Teorema 1′ no centro:** T_n(ruim) = (−1)^(n+1) para todo n. Confere com a enumeração de n = 1 a 10.
- **C1 no centro vira uma desigualdade entre inteiros:** |T_n(boa)| > 3ⁿ.

## Valores exatos (n = 1 a 10)

| n | T_n(todas) | T_n(ruim) | T_n(boa) | 3ⁿ | \|T_n(boa)\|/n! |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 3 | 0 |
| 2 | −1 | −1 | 0 | 9 | 0 |
| 3 | −5 | 1 | −6 | 27 | 1,00 |
| 4 | −13 | −1 | −12 | 81 | 0,50 |
| 5 | −169 | 1 | −170 | 243 | 1,42 |
| 6 | −10.261 | −1 | −10.260 | 729 | 14,25 |
| 7 | 17.739 | 1 | 17.738 | 2.187 | 3,52 |
| 8 | −2.181.341 | −1 | −2.181.340 | 6.561 | 54,10 |
| 9 | 27.904.687 | 1 | 27.904.686 | 19.683 | 76,90 |
| 10 | −2.494.684.501 | −1 | −2.494.684.500 | 59.049 | 687,47 |

Para as teias **conexas** (pela fórmula exponencial; conferida sem sinal contra o número conhecido de ordens conexas, 1, 2, 12, 146, 3.060, …): 1, −2, 0, −14, −140, −9.662, +80.444, −3.139.614, +54.773.940, −3.164.932.862.

## Leitura

- Os sinais e os tamanhos são irregulares, tanto no total quanto nas conexas. Uma involução que troca sinal costuma deixar um resto com estrutura limpa (sinal fixo, crescimento regular). Nada disso aparece, o que é um indício, não uma prova, de que essa estratégia não dá fórmula fechada aqui.
- A busca da sequência na OEIS não pôde ser feita (o site bloqueia acesso automático). Fica para conferência manual.
- O problema do centro da janela fica bem posto e puramente combinatório: **|Σ_{ordens rotuladas} (−1)^(N₀+N₁)| > 3ⁿ + 1 para n ≥ 6?** Vale de n = 6 a 10. Para n ≥ 11, a pergunta vale para "todas as ordens", que só coincide com "teias boas + ruins" enquanto toda teia de altura ≥ 3 couber em 3+1.
