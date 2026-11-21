# Análise 5: cota de C_n = Par_n + Ser_n por somas com sinal (centro da janela)

Data: 21/11/2026. Script: `scripts/h1b_cota_C.py`. Saída: `cota_C.txt`.

Os níveis estão marcados assim:

- **(D)** demonstrado;
- **(V)** verificado exatamente, com inteiros;
- **(O)** observação.

Nenhuma conjectura foi registrada.

**Populações:**

- **todas as ordens:** n = 5 a 11; n = 11 usa os valores confirmados por R1 = R2;
- **oficial:** altura ≥ 3, n = 5 a 10, no item 6. Só descritivo, porque a recursão não vale dentro dela.

## 1. Identidades refinadas dos extremos (D)

São casos particulares da identidade de `ANALITICO_3.md`, aplicada com uma das partes igual a um ponto (sinal −1, estado (m, D, M, U) = (1, 0, 1, 0)). Para {⊥} ⊕ P, com |P| ≥ 1:

- s = −s(P)·(−1)^{m(P)+D(P)};
- o novo estado é (m, D, M, U) = (1, m(P), M(P), U(P) + [|P| = 1]).

O caso P ⊕ {⊤} sai por dualidade, e {⊥} ⊕ P ⊕ {⊤} pela composição dos dois. As somas totais correspondentes foram verificadas em `EXPLORATORIO_SERIE_EXTREMOS.md`.

## 2. Expressão exata de C_n (D, com V para n = 4 a 10)

Para n ≥ 2:

  C_n = E_n + Q_n, com E_n = E_iso + E_ext e Q_n = Q_par + Q_ser.

As quatro partes são:

- **E_iso** (ordens com algum ponto isolado) = a_n − b_n = Σ_{j≥1} C(n, j)(−1)^j b_{n−j}.
- **E_ext** (ordens com menor ou maior elemento) = S_⊥ + S_⊤ − S_⊥⊤. Ela é disjunta de E_iso para n ≥ 2.
- **Q_par** (paralelas sem ponto isolado) = b_n − con_n = Σ_{k=2}^{n−2} C(n−1, k−1)·con_k·b_{n−k}. Sai da fórmula exponencial b = exp(con₍≥2₎).
- **Q_ser** (série sem menor e sem maior elemento) = Σ_{k=2}^{n−2} C(n, k)·Σ_{σ₁,σ₂} I_k[σ₁]·A′_{n−k}[σ₂]·(−1)^{Δ(σ₁,σ₂)}. Aqui A′ são as ordens **sem** maior elemento.

Leitura:

- **E_n é a parte "de um ponto"**: um ponto isolado, embaixo ou em cima.
- **Q_n é a parte dos compostos não triviais**: os dois fatores têm pelo menos 2 elementos.

**Verificação:** cada uma das quatro partes, calculada pela fórmula a partir dos tamanhos menores, é igual à contagem direta em todo n de 4 a 10.

## 3. Comparação com |Prim_n| (V; todas as ordens)

Notação: Q̄ = Σ_k |parte do tamanho k|, com os estados somados exatamente dentro de cada k. Q̃ = Σ_k Σ_{pares de estados} |…|.

| n | Prim_n | \|C\|/\|P\| | (\|Par\|+\|Ser\|)/\|P\| | \|Par\|/\|P\| | \|Ser\|/\|P\| | \|E\|/\|P\| | \|Q\|/\|P\| | (\|E\|+Q̄)/\|P\| | (\|E\|+Q̃)/\|P\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | −120 | 2,41 | 2,41 | 0,24 | 2,17 | 1,83 | 0,58 | 2,41 | 5,24 |
| 6 | −2.880 | 2,56 | 2,56 | 0,21 | 2,36 | 2,93 | 0,37 | 3,63 | 6,73 |
| 7 | −108.360 | **0,84** | 0,84 | 0,58 | 0,26 | 1,09 | 0,25 | 1,34 | 3,94 |
| 8 | −1.779.624 | **0,23** | 1,30 | 0,54 | 0,76 | 0,36 | 0,14 | **0,84** | 4,62 |
| 9 | −64.647.576 | **0,57** | 0,57 | 0,42 | 0,15 | 0,51 | 0,06 | **0,73** | 3,98 |
| 10 | −2.577.258.960 | **0,03** | 0,49 | 0,26 | 0,23 | 0,05 | 0,02 | **0,30** | 3,01 |
| 11 | −77.098.086.120 | **0,48** | 0,48 | 0,45 | 0,02 | 0,39 | 0,09 | **0,62** | 4,36 |

**Respostas às perguntas da etapa:**

- **A condição-alvo |C_n| < |Prim_n| vale de n = 7 a 11.**
  - Em n = 6 ela falha, mas C₆ = −7.381 tem o **mesmo** sinal de Prim₆ e o reforça.
  - Em n = 5, C₅ é positivo e domina, e por isso a₅ > 0.
- **Separadamente ou só juntas?**
  - |Par_n| < |Prim_n| vale em todo n ≥ 5.
  - |Ser_n| < |Prim_n| vale para n ≥ 7.
  - A soma |Par| + |Ser| < |Prim| **falha em n = 8** (1,30), porque lá Par = +958.273 e Ser = −1.359.990 se cancelam.

  O cancelamento entre as partes paralela e série faz parte do mecanismo, como você previu.
- **A cota que preserva os sinais é a que funciona:**
  - (|E| + Q̄)/|Prim| < 1 vale de n = 8 a 11.
  - Tomar módulo também por estado (Q̃) dá razões de 3,0 a 6,7 em todo n: os cancelamentos entre estados são essenciais, e uma cota que os destrói não serve em nenhum tamanho.
- **A parte de um ponto domina C.** Os compostos não triviais pesam 0,25, 0,14, 0,06, 0,02 e 0,09 de |Prim| para n = 7 a 11.

## 4. Desigualdade candidata e o que está demonstrado (D)

**Lema (D).** Se Prim_n < 0 e |E_n| + Q̄_n < |Prim_n| − 1, então a_n < −1, isto é, vale C2′(n).

Prova: |C_n| = |E_n + Q_n| ≤ |E_n| + Q̄_n, pela desigualdade triangular aplicada uma vez a cada tamanho k. Daí a_n = Prim_n + C_n < Prim_n + |Prim_n| − 1 = −1.

**Validade verificada (V):**

- a hipótese do lema vale de n = 8 a 11 (todas as ordens);
- em n = 7 ela falha (1,34), embora C2′(7) seja verdadeira. Lá, E sozinho já passa de |Prim| (1,09), e só o cancelamento exato entre E (+117.893) e Q (−27.272) salva o sinal;
- em n = 6, C2′ vale pelo reforço de sinal, não por domínio.

**Domínio de validade:** n = 8 a 11, para todas as ordens. O lema é uma condição suficiente; ele não demonstra nada para n ≥ 12.

## 5. Por que isto não fecha a demonstração para todo n (O)

**E não se reduz ao termo de ordem n − 1.** A aproximação E ≈ −n·b_{n−1} − 2n·τ(n−1) erra muito: ela dá 0,07 de E em n = 10 e 1,40 de E em n = 11. Os termos de ordem n − 2 (S_⊥⊤ e o termo C(n, 2) de E_iso) são do mesmo tamanho e cancelam parte do resto.

**Prim_n e a parte de um ponto são da mesma ordem de grandeza.** A razão |Prim_n|/(n·L1_{n−1}), em que L1_{n−1} = Σ_σ |A_{n−1}[σ]|, vale:

| n | 6 | 7 | 8 | 9 | 10 | 11 |
| --- | --- | --- | --- | --- | --- | --- |
| \|Prim_n\|/(n·L1_{n−1}) | 0,19 | 0,51 | 0,40 | 0,38 | 0,36 | 0,23 |

Ela não cresce. Então não há uma separação de escalas que faça E/Prim → 0 por si só. O sinal de a_n resulta de uma competição que continua delicada até n = 11, e os ímpares são os mais apertados.

**O que falta para uma prova geral:** controlar E_n de forma exata, ou como uma combinação de somas torcidas de tamanho n − 1 e n − 2 com sinais conhecidos, frente a Prim_n. Para isso seria preciso entender o sinal e o tamanho das somas torcidas τ, que já alternam de sinal com n (observação de `EXPLORATORIO_SERIE_EXTREMOS.md`, ainda sem explicação).

## 6. População oficial (altura ≥ 3, n = 5 a 10; descritivo)

| n | Prim | Par | Ser | \|Par+Ser\|/\|Prim\| |
| --- | --- | --- | --- | --- |
| 5 | 0 | −120 | +290 | indefinida (Prim = 0) |
| 6 | −1.800 | −1.680 | −6.780 | 4,70 (mesmo sinal: reforça) |
| 7 | −99.120 | +53.340 | +28.042 | 0,82 |
| 8 | −1.685.040 | +863.688 | −1.359.988 | 0,30 |
| 9 | −63.556.416 | +25.777.584 | +9.874.146 | 0,56 |
| 10 | −2.563.084.440 | +656.073.840 | −587.673.900 | 0,03 |

O padrão é o mesmo das todas as ordens. A recursão não vale dentro da população oficial, porque a condição de altura não é fechada sob união disjunta nem sob soma ordinal, então nenhuma das identidades acima se transfere diretamente para ela.
