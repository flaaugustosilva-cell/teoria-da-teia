# Análise 4: o tamanho das partes paralela e série frente à raiz prima (centro da janela, todas as ordens)

Data: 20/11/2026. Script: `scripts/h1b_C3_analise.py`. Saída: `analise_partes.txt`.

Os níveis estão separados assim:

- **(D)** demonstrado;
- **(V)** verificado exatamente nos dados;
- **(O)** observação exploratória, que não é teste e não é conjectura registrada.

**Notação:**

- a_n: soma rotulada de (−1)^B sobre todas as ordens com n elementos;
- con_n: a mesma soma, só sobre as conexas;
- Prim_n, Ser_n e Par_n: as partes de raiz prima, série e paralela;
- b_n: a soma só sobre as ordens **sem pontos isolados**.

Para n = 11, todos os valores vêm da rota R1 (`RESULTADOS_C3.md`).

## 1. Duas identidades exatas (D)

**(i) Fórmula exponencial nos totais.** Como o sinal se multiplica na união disjunta,

  a_n = Σ_{k=1}^{n} C(n−1, k−1) con_k a_{n−k},

em que k é o tamanho da componente que contém o rótulo 1. A parte paralela é a soma dos termos com k < n. Logo, **C2′(n) ⟺ con_n + Σ_{k<n} C(n−1, k−1) con_k a_{n−k} < −1.**

**(ii) Pontos isolados.**

- Um ponto isolado não cria nem altera intervalos. Ele só soma 1 a n, e por isso multiplica o sinal por −1.
- Escolhendo quais j rótulos são isolados, obtém-se

  a_n = Σ_{j=0}^{n} C(n, j)(−1)^j b_{n−j}, e a inversa é b_n = Σ_{j=0}^{n} C(n, j) a_{n−j}.

- Em termos de séries geradoras exponenciais: A(x) = e^{−x}·B(x).
- A inversão foi conferida exatamente de n = 0 a 11.

## 2. De onde vem a parte paralela positiva (V)

O termo dominante de Par_n é **"uma ordem conexa de n − 1 elementos mais um ponto isolado"**, que vale −(n−1)·con_{n−1}. Ele é positivo quando con_{n−1} < 0, e responde por esta fração de Par_n:

| n | 8 | 9 | 10 | 11 |
| --- | --- | --- | --- | --- |
| fração de Par_n | 59% | 93% | 74% | 91% |

O mecanismo, portanto, é simples: **o ponto isolado inverte o sinal** de uma parte que já era negativa.

**A parte série** é dominada pelos termos "ponto embaixo" (k = 1) e "ponto em cima" (k = n − 1). Em n = 11 há termos grandes de sinais opostos, −2,1×10¹⁰ e +9,7×10⁹, que quase se cancelam: o resultado é +1,8×10⁹.

## 3. Cotas por contagem não servem (V para n ≤ 10, com a tendência em O)

A cota mais simples seria limitar |Par_n| pelo **número** de ordens desconexas e |Ser_n| pelo número de ordens do tipo série. Ela **falha em todo n ≤ 10**:

- em n = 10, |Prim_n| = 2,6×10⁹, enquanto existem 4,7×10¹¹ ordens desconexas e 9,0×10¹¹ do tipo série;
- o viés das ordens de raiz prima (soma com sinal dividida pelo número delas) cai depressa: −1,1×10⁻¹, −5,5×10⁻², −3,3×10⁻², −6,4×10⁻³, −2,0×10⁻³ e −4,9×10⁻⁴ para n = 5 a 10;
- a fração de ordens desconexas cai devagar: 0,28, 0,22, 0,17, 0,13, 0,10 e 0,07.

A cota por contagem, portanto, piora com n.

**Consequência:** nenhuma demonstração de C2′ pode vir só de contar ordens. Ela precisa usar o **sinal** das partes paralela e série, isto é, os cancelamentos internos delas.

## 4. Condição suficiente pelo domínio de b_n (D, com a verificação em V)

Pela identidade 1(ii):

  |a_n − b_n| ≤ Σ_{j≥1} C(n, j)·|b_{n−j}|.

Daí, se b_n < 0 e D_n := |b_n| − Σ_{j≥1} C(n, j)|b_{n−j}| > 1, então **a_n < −1**, isto é, vale C2′(n), com |a_n| ≥ D_n. Isso é demonstrado.

**Verificação** (b_n exato):

| n | b_n | Σ_{j≥1} C(n, j)·\|b_{n−j}\| | D_n | D_n / \|b_n\| |
| --- | --- | --- | --- | --- |
| 5 | +140 | 31 | 109 | 0,78 |
| 6 | −9.362 | 901 | 8.461 | 0,90 |
| 7 | −86.324 | 68.587 | 17.737 | **0,21** |
| 8 | −2.601.762 | 960.765 | 1.640.997 | 0,63 |
| 9 | −49.017.252 | 27.327.895 | 21.689.357 | 0,44 |
| 10 | −2.876.134.802 | 619.612.501 | 2.256.522.301 | 0,78 |
| 11 | −69.837.965.428 | 34.795.600.027 | 35.042.365.401 | 0,50 |

Para n = 6 a 11, b_n < 0 e D_n > 1. Logo C2′ vale de n = 6 a 11, agora explicada pelo domínio das ordens sem pontos isolados.

- **n = 5:** b₅ > 0, o que é coerente com a exceção a₅ > 0.
- **n = 7:** é o caso mais apertado. D₇ = 17.737 e |a₇| = 17.739: a cota é quase exata, porque todas as correções têm o mesmo sinal.

## 5. Observações (O): não são conjecturas registradas

- **Os ímpares são frágeis.** A razão D_n/|b_n| vale 0,21, 0,44 e 0,50 nos ímpares (n = 7, 9, 11), contra 0,90, 0,63 e 0,78 nos pares. A razão de crescimento |b_n|/|b_{n−1}| é 9,2, 18,8 e 24,3 nos ímpares e 30,1 e 58,7 nos pares. Para que a condição do item 4 continue valendo, basta, grosso modo, que |b_n|/|b_{n−1}| cresça mais depressa que 2n. Nos ímpares a folga existe, mas é pequena.
- **O que a exploração sugere** (só depois de um registro próprio):
  - (a) b_n < 0 com D_n > 1 para todo n ≥ 6. Isso implicaria C2′ para todo n.
  - (b) Uma redução análoga para os pontos únicos no topo e no fundo da soma ordinal, que são os termos dominantes da parte série.

  Ambas foram inspiradas por n ≤ 11. Nenhum teste independente é viável em n = 12 nesta máquina: são cerca de 1,1×10⁹ classes.
- **O que falta para uma demonstração de verdade:** uma cota **inferior** para |b_n| (ou para |Prim_n|) que cresça mais depressa que n·|b_{n−1}|. Ainda não temos nenhuma ideia de como obtê-la.

## 6. Alcance

Tudo aqui vale para **todas as ordens** em θ = π.

- Para n ≤ 10, C2′ equivale a C2 oficial.
- Em n = 11, C2′ é a afirmação sobre a população auxiliar.
- Nada aqui toca H1\* fora do centro da janela.
