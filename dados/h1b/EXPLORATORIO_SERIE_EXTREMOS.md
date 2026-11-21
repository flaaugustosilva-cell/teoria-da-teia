# Exploração (fora de registro): a parte série pelos elementos extremos

Data: 21/11/2026. A população é a de **todas as ordens**, em θ = π. Script: `scripts/h1b_serie_extremos.py`. Saída: `exploratorio_serie_extremos.txt`.

Os níveis estão marcados assim:

- **(D)** demonstrado;
- **(V)** verificado exatamente nos dados;
- **(O)** observação, que não é conjectura registrada.

## 0. Duas correções na pergunta de partida

**Sinal do ponto acrescentado.** Na convenção da ação, s = (−1)^{n+N₀+N₁}. Acrescentar um ponto também soma 1 a n. Assim:

- s({∗} ⊕ P) = −s(P)·(−1)^{m(P)+D(P)};
- s(P ⊕ {∗}) = −s(P)·(−1)^{M(P)+U(P)}.

O −1 extra é o mesmo do ponto isolado. Sem ele, todos os sinais previstos sairiam trocados.

**A parte série não tem viés negativo consistente.** O sinal dela alterna com n:

| n | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ser_n | +260 | −6.782 | +27.916 | −1.359.990 | +9.873.636 | −587.673.902 | +1.787.428.412 |

Por isso a pergunta passa a ser: **os elementos extremos explicam essa oscilação, e quanto da magnitude?**

## 1. Identidades (D, com V para n = 2 a 10)

Uma ordem com menor elemento ⊥ é, de um único jeito, {⊥} ⊕ P, em que P é qualquer ordem nos outros n − 1 elementos. O rótulo de ⊥ pode ser escolhido de n formas. Escrevendo A_k[σ] para as somas refinadas por estado σ = (m, D, M, U) mod 2:

- **Com menor elemento:** S_⊥(n) = −n·τ_⊥(n−1), em que τ_⊥(k) = Σ_σ A_k[σ](−1)^{m+D} é uma soma "torcida".
- **Com maior elemento:** S_⊤(n) = −n·τ_⊤(n−1), com τ_⊤(k) = Σ_σ A_k[σ](−1)^{M+U}.
- **Com os dois:** a ordem é {⊥} ⊕ P ⊕ {⊤}, com P em n − 2 elementos. O par (⊥, ⊤) tem |P| elementos entre si, então entra em N₀ ou em N₁ só quando |P| ≤ 1. Logo

  S_⊥⊤(n) = n(n−1)·Σ_σ A_{n−2}[σ](−1)^{m+D+M+U}·(−1)^{[n−2 ≤ 1]}.

- **Dualidade:** inverter a ordem preserva todos os N_k e troca (m, D) por (M, U). Então τ_⊥ = τ_⊤ e S_⊥ = S_⊤.
- **Tipo:** toda ordem com um elemento extremo é do tipo série, porque o extremo fica isolado no grafo de incomparabilidade.
- **Verificação:** as três identidades, a dualidade e a inclusão no tipo série conferem exatamente em todo n de 2 a 10.

## 2. Interseção e resíduo (V; n = 11 pela identidade, com Ser₁₁ de R1 = R2)

Por inclusão–exclusão, S_ext = S_⊥ + S_⊤ − S_⊥⊤. O resíduo é R_n = Ser_n − S_ext, isto é, as ordens do tipo série **sem** menor e **sem** maior elemento.

| n | S_⊥ = S_⊤ | S_⊥⊤ | S_ext | Ser_n | resíduo R_n | S_ext/Ser |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | +265 | +340 | +190 | +260 | +70 | 0,73 |
| 6 | −4.446 | −1.350 | −7.542 | −6.782 | +760 | 1,11 |
| 7 | +5.943 | −37.422 | +49.308 | +27.916 | −21.392 | 1,77 |
| 8 | −909.896 | −754.712 | −1.065.080 | −1.359.990 | −294.910 | 0,78 |
| 9 | +318.645 | −11.383.416 | +12.020.706 | +9.873.636 | −2.147.070 | 1,22 |
| 10 | −240.523.330 | −226.255.410 | −254.791.250 | −587.673.902 | −332.882.652 | 0,43 |
| 11 | +5.018.509.507 | +9.583.604.470 | +453.414.544 | +1.787.428.412 | +1.334.013.868 | 0,25 |

## 3. Resposta à pergunta central

- **O sinal é explicado pelos extremos.** Em todo n de 5 a 11, S_ext tem o mesmo sinal que Ser_n. A oscilação da parte série vem das ordens com menor ou maior elemento.
- **A magnitude não é.** O resíduo tem sinal irregular e pesa cada vez mais: cerca de 57% de Ser₁₀ e 75% de Ser₁₁. A fração explicada pelos extremos cai para 0,43 e 0,25. **Existe, portanto, um resíduo estrutural** que precisa ser controlado.
- **Há forte cancelamento dentro dos próprios extremos.** Em n = 11, S_⊥ + S_⊤ = +1,00×10¹⁰ e S_⊥⊤ = +9,58×10⁹, o que deixa só +4,5×10⁸.

## 4. Estrutura (O, com a parte formal em D)

**(D)** O resíduo não é uma fonte independente. Ele é formado pelas somas ordinais P₁ ⊕ … ⊕ P_k, com k ≥ 2, em que a primeira e a última peça têm pelo menos 2 elementos. Pela recursão de `ANALITICO_3.md`, ele é uma expressão exata nas somas refinadas de ordens menores. A única entrada livre de toda a recursão continua sendo a das ordens de raiz prima.

**(O)** Por número de peças ordinais, o resíduo se distribui assim:

- as somas de 2 peças são negativas de n = 7 a 10, com viés −0,12, −0,034, −0,014 e −0,0039;
- os estratos com muitas peças têm viés próximo de ±1, mas pouco peso;
- o sinal não é regular entre os estratos.

**(O)** As somas torcidas alternam de sinal com n em todo n de 1 a 10: τ(n)·(−1)^{n+1} > 0. Os valores são +1, −1, +1, −53, +741, −849, +113.737, −35.405, +24.052.333 e −456.228.137. É exatamente essa alternância que dá a oscilação de S_⊥, e com ela a da parte série. Ainda não tenho explicação para ela, e ela foi vista justamente nos dados que a sugeriram.

## 5. Alcance

- Tudo aqui é sobre **todas as ordens** em θ = π.
- A parte série é determinada pelos tamanhos menores, então nada aqui é uma nova fonte de sinal. A questão é de **magnitude**: o quanto as partes série e paralela podem compensar a parte de raiz prima.
- Nada foi registrado como conjectura.
