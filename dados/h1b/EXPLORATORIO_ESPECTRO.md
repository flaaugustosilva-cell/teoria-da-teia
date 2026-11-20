# Cancelamento global em 𝒵_boa — estrutura espectral (exploração, fora de registro)

Flavio Augusto da Silva · 20/11/2026 (Brasília). Opção 2 da decisão do autor (14:45). Exploratório: nenhum critério foi fixado antes, e nada aqui é teste de hipótese nem lei. Dados exatos de n = 5 a 10, peso 1/|Aut|. Código: `scripts/h1b_N_espectro.py`; saída: `n9n10/exploratorio_espectro.txt`.

## Reformulação usada

𝒵_boa(θ) = Σ_b W_b·e^(iθb). A janela θ = 2β ∈ [2π/3, 4π/3] é centrada em θ = π. Com θ = π + φ e |φ| ≤ π/3:

𝒵_boa(π + φ) = Σ_b (−1)^b·W_b·e^(iφb)

Então a janela "enxerga" o espectro com sinal alternado. No centro, 𝒵_boa(π) = W_par − W_ímpar. Como B ≡ n + N₀ + N₁ (mod 2), a paridade de B é a de n + (número de ligações) + (número de intervalos com um elemento dentro). Como W_b é real, |𝒵_boa(2π − θ)| = |𝒵_boa(θ)|: tudo é simétrico em torno do centro da janela.

## Pergunta 1: estrutura espectral

| n | Valores de B ocupados | Desvio | Assimetria | Curtose exc. | Parte não suave |
| --- | --- | --- | --- | --- | --- |
| 5 | 18 de 71 | 11,7 | −1,01 | +1,81 | 0,524 |
| 6 | 51 de 122 | 15,0 | −0,75 | +1,75 | 0,264 |
| 7 | 110 de 182 | 18,2 | −0,58 | +1,49 | 0,151 |
| 8 | 180 de 258 | 21,5 | −0,48 | +1,22 | 0,083 |
| 9 | 255 de 343 | 24,9 | −0,41 | +0,98 | 0,048 |
| 10 | 339 de 444 | 28,3 | −0,37 | +0,80 | 0,029 |

"Parte não suave" = Σ|W_b − W̄_b|/W, com W̄ a média ponderada (1/4, 1/2, 1/4) dos vizinhos. O espectro fica mais preenchido, mais suave e mais próximo da gaussiana com n.

## Pergunta 2: interferência

| n | W_par − W_ímpar = 𝒵_boa(π) | Relativo a W | Mediana de \|𝒵_boa\|/W na janela |
| --- | --- | --- | --- |
| 5 | +1,42 | 5,0 × 10⁻² | 0,14 |
| 6 | −14,3 | 8,7 × 10⁻² | 0,052 |
| 7 | −3,52 | 3,0 × 10⁻³ | 0,023 |
| 8 | −54,1 | 5,1 × 10⁻³ | 0,0060 |
| 9 | −76,9 | 6,3 × 10⁻⁴ | 0,0026 |
| 10 | −687,5 | 3,8 × 10⁻⁴ | 0,00069 |

Na janela, o tamanho de 𝒵_boa depende da estrutura fina do espectro (paridade e vizinhança), não da forma geral: um espectro perfeitamente suave daria cancelamento quase total sob o sinal alternado. Em termos relativos, essa estrutura fina encolhe com n; em termos absolutos, cresce, porque W cresce mais rápido.

## Pergunta 3: zeros e quase-zeros (grade de 400.001 pontos)

| n | Mínimos locais | Mínimo de \|𝒵_boa\| (ℓ/l_P) | Relativo a W | Limiar de C1 (3ⁿ/n!) | Mínimo / limiar |
| --- | --- | --- | --- | --- | --- |
| 5 | 9 | 0,252 (6,27 e 7,58) | 8,9 × 10⁻³ | 2,025 | 0,12 |
| 6 | 11 | 1,80 (6,18 e 7,65) | 1,1 × 10⁻² | 1,013 | 1,8 |
| 7 | 15 | 2,58 (5,93 e 7,84) | 2,2 × 10⁻³ | 0,434 | 5,9 |
| 8 | 18 | 0,539 (6,66 e 7,24) | 5,1 × 10⁻⁵ | 0,163 | 3,3 |
| 9 | 25 | 23,4 (6,61 e 7,28) | 1,9 × 10⁻⁴ | 0,0542 | 432 |
| 10 | 19 | 150 (6,55 e 7,34) | 8,3 × 10⁻⁵ | 0,0163 | 9.245 |

Os quase-zeros vêm aos pares, simétricos em torno de θ = π. Não há tendência limpa: o caso de n = 8 é muito mais fundo que os vizinhos.

## Leitura

A pergunta do autor — existe uma propriedade da distribuição de B que impeça 𝒵_boa de se aproximar demais de zero na janela? — fica mais precisa: **a propriedade teria de ser sobre a estrutura fina do espectro (paridade e correlações entre valores vizinhos de B), não sobre a forma geral, que tende à gaussiana e, sozinha, levaria a cancelamento quase total.** Um alvo concreto, e o mais simples, é o centro da janela, onde tudo se reduz a W_par − W_ímpar: um saldo de sinais, isto é, uma contagem com sinal das teias pela paridade de n + N₀ + N₁. Nenhuma conjectura foi formulada; qualquer uma precisaria de n ≥ 11 para ser testada de forma independente.
