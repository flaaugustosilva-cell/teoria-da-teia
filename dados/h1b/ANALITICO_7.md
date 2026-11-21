# Análise 7: de onde vem a alternância da parte série torcida (centro da janela, todas as ordens)

Data: 21/11/2026. Script: `scripts/h1b_caracteres.py`. Saída: `caracteres.txt`.

Os níveis estão marcados assim:

- **(D)** demonstrado;
- **(V)** verificado exatamente, n ≤ 10;
- **(O)** observação.

Nenhuma conjectura foi registrada.

**Notação:**

- caracteres: para c = (c_m, c_D, c_M, c_U) ∈ (ℤ/2)⁴, X̂[c] = Σ_σ X[σ](−1)^{c·σ};
- τ = Â[(1,1,0,0)];
- **caráter D:** D_n := Â_n[(0,1,0,0)] = Σ_P s(P)(−1)^{D(P)}, sobre todas as ordens.

## 1. A família de τ não é fechada (D)

Para peças com k, q ≥ 2, o caráter c da soma P₁ ⊕ Q é dado por

  Σ_{σ₂} A_q[σ₂](−1)^{c_M M₂ + c_U U₂} · Î_k[(c_m, c_D, m₂+D₂, m₂)].

Isso vem de somar sobre σ₁ com o expoente bilinear Δ fixado. Para c = τ entram **quatro** caracteres da peça de baixo: (1,1,0,0), (1,1,1,0), (1,1,0,1) e (1,1,1,1). Por isso não existe uma explicação usando só τ.

## 2. Padrões de sinal dos 16 caracteres (V, n = 4 a 10)

Só **quatro** caracteres das todas as ordens têm sinal regular:

- (0,1,0,0) e (0,0,0,1): sinal (−1)^n;
- (1,1,0,0) = τ e (0,0,1,1): sinal (−1)^{n+1}.

Os pares são duais um do outro: inverter a ordem troca D por U e m por M.

- Nas partes paralela e série separadas, esses mesmos caracteres são regulares.
- Na parte de **raiz prima**, **todos** os caracteres são irregulares, exceto o trivial (0,0,0,0), que é sempre negativo (é C3).

## 3. A parte série torcida é carregada pelo termo "ponto embaixo" (D, com V)

Decompondo a parte série torcida pelo tamanho k da peça de baixo:

- **k = 1 (ponto embaixo):** o peso torcido de {⊥} ⊕ Q é s(Q)(−1)^{D(Q)}. Então esse termo vale **n·D_{n−1}**.
- **k = n−1 com Q um ponto (ponto em cima):** o peso é −s(P₁)(−1)^{m+D+M+U}. Então o termo vale **−n·Î_{n−1}[(1,1,1,1)]**.

As duas fórmulas conferem em todo n de 4 a 10.

| n | série torcida | k = 1 | k = n−1 | meio |
| --- | --- | --- | --- | --- |
| 6 | −2.350 | −6.666 | +3.186 | +1.130 |
| 7 | +191.758 | +113.057 | +43.673 | +35.028 |
| 8 | −720.342 | −1.608.216 | +619.704 | +268.170 |
| 9 | +64.822.686 | +55.357.227 | −3.851.073 | +13.316.532 |
| 10 | −2.405.612.238 | −1.607.412.310 | −512.847.410 | −285.352.518 |

**O termo k = 1 tem o sinal do total em todo n de 4 a 10 (V).** Os outros termos às vezes reforçam e às vezes se opõem.

Assim, a alternância da parte série torcida **se reduz** à alternância do caráter D no tamanho n − 1. Se D_{n−1} tem sinal (−1)^{n−1}, o termo k = 1 tem sinal (−1)^{n+1}, que é o padrão observado.

## 4. O caráter D se propaga sozinho (D, com V)

**Dois mecanismos exatos.** Seja w_D(P) = s(P)(−1)^{D(P)}.

- **Ponto embaixo:** w_D({⊥} ⊕ P) = −w_D(P).
  - Prova: s({⊥} ⊕ P) = −s(P)(−1)^{m(P)+D(P)} (`ANALITICO_5.md`) e D({⊥} ⊕ P) = m(P).
  - Consequência: as ordens com menor elemento contribuem **exatamente −n·D_{n−1}** para D_n.
- **Ponto isolado:** w_D troca de sinal, porque s troca e D não muda. Logo D = e^{−x}·D⁽⁰⁾.

**Leitura indutiva.** Se D_{n−1} tem sinal (−1)^{n−1}, a parte "menor elemento" de D_n tem sinal (−1)^n. O mecanismo **leva a alternância de um tamanho para o seguinte**.

**Decomposição de D_n (V):**

| n | D_n | menor elemento (= −n·D_{n−1}) | ponto isolado | maior e sem menor | resto | (menor + isolado)/D_n |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | +139 | +76 | +61 | −40 | +42 | 0,99 |
| 5 | −1.111 | −695 | −531 | +45 | +70 | 1,10 |
| 6 | +16.151 | +6.666 | +4.921 | +5.544 | −980 | 0,72 |
| 7 | −201.027 | −113.057 | −93.983 | +67.305 | −61.292 | 1,03 |
| 8 | +6.150.803 | +1.608.216 | +1.209.461 | +1.520.336 | +1.812.790 | 0,46 |
| 9 | −160.741.231 | −55.357.227 | −49.352.971 | +13.553.757 | −69.584.790 | 0,65 |
| 10 | +4.497.486.319 | +1.607.412.310 | +1.351.610.641 | −545.907.280 | +2.084.370.648 | 0,66 |

- D_n tem sinal (−1)^n em **todo** n de 1 a 10.
- A parte "menor elemento" é exatamente −n·D_{n−1} em todo n.
- A parte "ponto isolado" tem o mesmo sinal de D_n em todo n.

## 5. Respostas e o que continua em aberto

**A cadeia explicada até aqui (D e V):**

- alternância da série torcida ← termo "ponto embaixo" = n·D_{n−1};
- alternância de D ← propagação exata −n·D_{n−1}, mais os pontos isolados.

**O que não está explicado:**

- **O resto de D_n**, isto é, as ordens sem menor elemento e sem ponto isolado (e com ou sem maior elemento). Ele pesa até 54% de D_n (n = 8). Na maioria dos n tem o mesmo sinal, mas não em todos: em n = 5 e 6, uma das partes se opõe. Nada aqui controla o seu sinal.
- **A dominância.** A indução só fecharia se as partes que propagam o sinal dominassem as outras. Os dados mostram (menor + isolado)/D_n entre 0,46 e 1,10. Então elas carregam boa parte, mas não necessariamente a maioria.
- **O elo com a parte de raiz prima.** Os caracteres da parte de raiz prima continuam irregulares, exceto o trivial. A regularidade de D vem da composição (pontos embaixo e isolados), não das ordens de raiz prima.

**Resumo:** a alternância **não é um acaso numérico**. Ela tem um mecanismo exato de propagação: um ponto embaixo ou um ponto isolado invertem o peso D. Mas o mecanismo **não está demonstrado como dominante**, então isto não é uma prova.
