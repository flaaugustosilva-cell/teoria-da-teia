# Estrutura fina de W_b: paridade, vizinhança e Fourier (exploração, fora de registro)

Flavio Augusto da Silva · 20/11/2026 (Brasília). Etapa 1 (exploração) da decisão do autor de 18:08. Nada aqui é teste, lei ou conjectura. Código: `scripts/h1b_estrutura_fina.py`; saída: `exploratorio_estrutura_fina.txt`.

**Populações, mantidas separadas:**
- **OFICIAL**, n = 5 a 10: ordens de altura ≥ 3; todas cabem em 3+1 (certificado).
- **AUXILIAR**, n = 11: todas as ordens de altura ≥ 3 ("não ruins"); não é a definição oficial.

## 1. Paridade: 𝒵(π) = W_par − W_ímpar

| n | População | W_par − W_ímpar | Relativo a W | Só conexas | Só desconexas |
| --- | --- | --- | --- | --- | --- |
| 5 | oficial | +1,42 | +5,0 × 10⁻² | +2,42 | −1,00 |
| 6 | oficial | −14,25 | −8,7 × 10⁻² | −11,92 | −2,33 |
| 7 | oficial | −3,52 | −3,0 × 10⁻³ | −14,10 | +10,58 |
| 8 | oficial | −54,10 | −5,1 × 10⁻³ | −75,52 | +21,42 |
| 9 | oficial | −76,90 | −6,3 × 10⁻⁴ | −147,93 | +71,04 |
| 10 | oficial | −687,47 | −3,8 × 10⁻⁴ | −868,27 | +180,80 |
| 11 | auxiliar | −1.014,39 | −2,9 × 10⁻⁵ | −1.881,57 | +867,18 |

- O sinal é negativo (pende para B ímpar) em todos os tamanhos de n = 6 a 11.
- A parte conexa é negativa de n = 6 a 11. A parte desconexa tem sinal oposto a partir de n = 7 e cancela parte da conexa.

## 2. Vizinhança: resíduo r = W − G

G é o envelope suave, uma média gaussiana de largura desvio/4, escolhida antes de olhar os resíduos.

| n | População | Σ\|r\|/W | Autocorrelação de r nos passos 1 / 2 / 3 / 4 |
| --- | --- | --- | --- |
| 5 | oficial | 1,22 | +0,25 / −0,18 / −0,34 / −0,38 |
| 6 | oficial | 0,87 | +0,48 / −0,08 / −0,48 / −0,61 |
| 7 | oficial | 0,64 | +0,64 / +0,01 / −0,56 / −0,81 |
| 8 | oficial | 0,45 | +0,70 / +0,05 / −0,58 / −0,89 |
| 9 | oficial | 0,31 | +0,72 / +0,07 / −0,59 / −0,92 |
| 10 | oficial | 0,21 | +0,73 / +0,09 / −0,58 / −0,93 |
| 11 | auxiliar | 0,14 | +0,74 / +0,12 / −0,54 / −0,89 |

A estrutura fina encolhe em relação a W, mas a sua forma se estabiliza: positiva no passo 1, quase zero no 2, e fortemente negativa nos passos 3 e 4. Isso é uma modulação quase periódica de período ≈ 8,5 em B.

## 3. Fourier: 𝒵(θ) = Ĝ(θ) + r̂(θ)

- Na janela (θ ≥ 2π/3), o envelope é desprezível: |Ĝ|/|𝒵| ≤ 10⁻⁹ em todos os n. **A soma na janela é inteiramente estrutura fina.**
- O pico de |r̂| (fora de θ < 0,5) fica em θ* = 0,740 (n = 5, 6, 7), 0,741 (8), 0,742 (9, 10) e 0,743 (11, auxiliar). O período correspondente é 2π/θ* ≈ 8,5.
- Os harmônicos 3θ* ≈ 2,23, 4θ* ≈ 2,97 e 5θ* ≈ 3,71 (equivalente a 2,57) caem dentro da janela.

## Leitura (sem conclusão)

A hipótese de trabalho do autor, W_b ≈ G(b)·f(b) com f quase periódica, é compatível com os dados: há uma modulação de frequência θ* ≈ 0,742, estável com n, e a janela enxerga os seus harmônicos. Uma possível origem, ainda não testada, é a própria ação: os passos de B são −1 (N₀), +9 (N₁), −16 (N₂) e +8 (N₃), e 9θ, 16θ e 8θ ficam simultaneamente perto de múltiplos de 2π para θ perto de 0,7–0,8. Se for isso, a estrutura fina viria da aritmética dos coeficientes de Benincasa–Dowker combinada com a distribuição conjunta de (N₀, N₁, N₂, N₃), e não de uma propriedade especial das teias. Essa ideia é candidata à etapa 2 (formalização) e não foi testada.
