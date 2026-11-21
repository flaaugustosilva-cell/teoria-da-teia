# Pré-registro: conjectura C3 (sinal das ordens de raiz modular prima) e teste em n = 11

Data: 20/11/2026. Este documento foi publicado **antes** de calcular qualquer quantidade das ordens de raiz prima em n = 11.

O código do teste é o modo `c3` de `scripts/h1b_soma_ordinal.py`, fixado neste commit com sha256 `f1b09058ce630ff13f8878ae50585e03770a842f9f9bc50d1e7dde79487c5552`. Esse modo ainda não foi executado.

## 1. Definições exatas

- **População:** **todas** as ordens parciais em n elementos. Não há condição de altura nem de incorporação em 3+1. **Não** é a população oficial das teias boas.
- **Ordem de raiz modular prima:** uma ordem com n ≥ 2 cujo grafo de comparabilidade **e** cujo grafo de incomparabilidade são ambos conexos. A definição operacional é exatamente esta, e é a do código (`tipo == 2` em `h1b_paridade_explora.estrutura`). Por Gallai, ela corresponde à raiz prima da decomposição modular. **Não** é o mesmo que "ordem sem módulos não triviais".
- **Soma com sinal:**

  Prim_n = Σ_{P rotulada em {1, …, n}, de raiz prima} (−1)^{B(P)},

  em que (−1)^B = (−1)^{n + N₀ + N₁}. Cada ordem rotulada conta +1 ou −1, então Prim_n é um inteiro exato.

## 2. Conjectura C3

  **Prim_n < 0 para todo n ≥ 5.**

**Dados que a inspiraram** (`ANALITICO_3.md`, item 5): Prim_n = −120, −2.880, −108.360, −1.779.624, −64.647.576 e −2.577.258.960 para n = 5 a 10. Também Prim₄ = −24. Esses números não contam como teste.

Há também a versão restrita às boas (altura ≥ 3), que é negativa de n = 6 a 10. Ela **não** é a registrada aqui. Fica fora para não haver duas populações num mesmo teste.

## 3. Teste em n = 11

**Rota R1, que dá o veredito.** Pela identidade demonstrada em `ANALITICO_3.md`:

  Prim₁₁ = T_todas(11) − Par₁₁ − Ser₁₁.

- Par₁₁ e Ser₁₁ saem da recursão a partir das somas refinadas das ordens de tamanho ≤ 10 (dados de `n9n10`, já usados).
- T_todas(11) sai das 20 partes **já publicadas** da investigação auxiliar de n = 11 (`n11aux/`, commit c05eb41). Lá estão a soma exata de n!/|Aut| por (B, altura ≥ 3, conexa), para todas as 46.749.427 classes.
- **Validações obrigatórias antes do veredito:**
  - total de classes nas partes = 46.749.427 (A000112(11));
  - soma das ruins (altura ≤ 2) = −1, como manda a fórmula fechada.

  Se alguma falhar, não há veredito.

**Rota R2, confirmação independente** (não executada agora; recomendada para uma etapa seguinte): gerar de novo as ordens de n = 11 com o genposetg, classificar cada uma pelo tipo e somar Prim₁₁ diretamente.

- Leva cerca de 2 horas nesta máquina.
- Se R1 e R2 discordarem, o veredito fica suspenso e o erro é relatado.

**Critério:**

- **SUCESSO** se Prim₁₁ < 0;
- **FALHA** se Prim₁₁ ≥ 0.

É um inteiro exato, sem estatística nem tolerância.

**Descritivo, registrado:** os valores de Par₁₁ e Ser₁₁, e a razão Prim₁₁ / T_todas(11).

## 4. Dependência que precisa ficar declarada

O sinal de T_todas(11) **já é conhecido** antes deste registro. Da investigação auxiliar, T_todas(11) = −(11!·1014,39…) − 1 ≈ −4,05×10¹⁰. Par₁₁ e Ser₁₁ ainda não foram calculados.

Então o teste não é totalmente cego: se Par₁₁ + Ser₁₁ for pequeno, ou também negativo, Prim₁₁ será negativo quase por consequência. O teste só tem força de verdade se Par₁₁ + Ser₁₁ for grande e positivo; por isso esses valores são relatados. Nenhum valor das ordens de raiz prima em n = 11 foi calculado nem visto.

## 5. O que o resultado significa e o que não significa

- **Sucesso:** C3 vale em n = 11, um caso fora dos dados que a inspiraram. Isso **não** demonstra C3 para todo n.
- **Nenhum resultado** demonstra C2 oficial em n = 11, porque a população oficial ali é a das incorporáveis, que não foi determinada. Também não diz nada sobre H1\* fora de θ = π.
- **As três afirmações continuam separadas:** (1) raiz prima negativa; (2) total negativo; (3) boas dominam ruins em toda a janela.
- **Falha:** C3 está refutada como enunciada. Isso não afeta C2′ em n = 11, que já é conhecida (T_todas(11) < −1).

## 6. Ordem de execução

1. Publicar este registro (commit).
2. Rodar `python h1b_soma_ordinal.py c3 n9n10 dados/h1b/n11aux`.
3. Registrar o resultado em `RESULTADOS_C3.md`.
