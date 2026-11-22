# Análise 8: os caracteres (0,1,1,1) e (0,1,0,1) e a regra geral das operações de um ponto

Data: 22/11/2026. Script: `scripts/h1b_carater_0111.py`. Saída: `carater_0111.txt`. População: todas as ordens, θ = π.

Os níveis estão marcados assim:

- **(D)** demonstrado;
- **(V)** verificado exatamente, com inteiros, n ≤ 10;
- **(O)** observação.

Nenhuma conjectura foi registrada.

## 0. Conferência das definições (commit 9dc76ba)

- Os componentes vêm na ordem (c_m, c_D, c_M, c_U), como em `idx(m, D, M, U)` e `bits(c)` de `h1b_soma_ordinal.py` e `h1b_caracteres.py`.
- Logo (0,1,1,1) é χ_n = Σ_P s(P)(−1)^{D+M+U}, e no script ela é calculada como `(-1)**(D + maxi + U)`.
- Aqui s(P) = (−1)^{n+N₀+N₁}. D conta os elementos com exatamente 1 elemento abaixo, M os máximos e U os elementos com exatamente 1 elemento acima.
- Também estudo κ := (0,1,0,1), isto é, Σ_P s(P)(−1)^{D+U}.

## 1. Transições de estado das três operações de um ponto (D)

Valem para |P| ≥ 2. Os casos de fronteira com |P| ≤ 1 foram tratados à parte e as fórmulas abaixo são usadas para n ≥ 3. Todas saem de `ANALITICO_3.md`, e o −1 vem sempre de n → n + 1.

| Operação | Sinal | Novo estado (m, D, M, U) |
| --- | --- | --- |
| ponto isolado, P ⊔ {∗} | s → −s | (m+1, D, M+1, U) |
| ponto embaixo, {⊥} ⊕ P | s → −s·(−1)^{m+D} | (1, m, M, U) |
| ponto em cima, P ⊕ {⊤} | s → −s·(−1)^{M+U} | (m, D, 1, M) |

O ponto em cima é uma operação diferente do ponto isolado. Ele cria relações com todos os elementos, e por isso entram M e U.

## 2. Regra geral para os 16 caracteres (D, com V para n ≤ 10)

Para o caráter c = (c_m, c_D, c_M, c_U), aplicando a tabela ao peso s(P)(−1)^{c·σ}:

- **Ponto isolado:** o peso é multiplicado por −(−1)^{c_m+c_M}. Logo Â_n[c] = Σ_j C(n, j)·f^j·Â⁽⁰⁾_{n−j}[c], com f = −(−1)^{c_m+c_M}. Ou seja, a regra é e^{x} quando c_m + c_M é ímpar e e^{−x} quando é par.
- **Ponto embaixo:** o peso de {⊥} ⊕ P é −(−1)^{c_m} vezes o peso de P no caráter (1+c_D, 1, c_M, c_U). Logo a parte "com menor elemento" de Â_n[c] vale n·(−(−1)^{c_m})·Â_{n−1}[(1+c_D, 1, c_M, c_U)].
- **Ponto em cima:** o peso de P ⊕ {⊤} é −(−1)^{c_M} vezes o peso de P no caráter (c_m, c_D, 1+c_U, 1). Logo a parte "com maior elemento" vale n·(−(−1)^{c_M})·Â_{n−1}[(c_m, c_D, 1+c_U, 1)].

As três regras foram verificadas para todos os 16 caracteres e todo n de 3 a 10. Para os pontos isolados, de 1 a 10.

**Casos já vistos, agora como consequência da regra:**

| Caráter | Ponto isolado | Ponto embaixo | Ponto em cima |
| --- | --- | --- | --- |
| D = (0,1,0,0) | troca o sinal | fixo, troca o sinal | vai para χ, com −1 |
| χ = (0,1,1,1) | **invariante** | fixo, troca o sinal | vai para κ, com **+1** |
| **κ = (0,1,0,1)** | **troca** | **fixo, troca** | **fixo, troca** |
| τ = (1,1,0,0) | invariante | vai para D, com +1 | vai para (1,1,1,1), com −1 |

## 3. κ é o atrator das operações de um ponto (D)

**κ é o único fixo.** Ser fixo pelo ponto embaixo exige c_D = 1 e c_m = 0. Ser fixo pelo ponto em cima exige c_U = 1 e c_M = 0. Logo **κ = (0,1,0,1) é o único caráter fixo pelas duas**, e as três operações de um ponto **trocam** o sinal de κ.

**Todo caráter chega a κ.** Duas aplicações do ponto embaixo levam qualquer caráter a c_m = 0 e c_D = 1. Duas do ponto em cima levam a c_M = 0 e c_U = 1.

Em termos de cadeias de pontos extremos, **todo caráter é levado a κ**, e dentro de κ cada ponto acrescentado inverte o sinal. É aí que nasce, estruturalmente, a alternância (−1)^n.

**A cadeia D ← χ ← κ.** O ponto em cima leva D em χ, e leva χ em κ. A irregularidade que o ponto em cima "importa" para D (`EXPLORATORIO_TRES_FRENTES.md`) vem de χ, e χ por sua vez importa κ.

## 4. κ: transmissão e alternância, testadas separadamente

**Transmissão (D, com V):** com n ≥ 3,

- parte "menor elemento" = −n·κ_{n−1};
- parte "maior elemento" = −n·κ_{n−1};
- parte "os dois" = +n(n−1)·κ_{n−2} (n ≥ 4);
- pontos isolados: κ = e^{−x}·κ⁽⁰⁾.

Todas as partes de um ponto vêm de κ em tamanhos menores, com o sinal trocado a cada ponto.

**Alternância (V e O):**

| n | κ_n | um ponto / total | resto paralelo | resto série | resto raiz prima |
| --- | --- | --- | --- | --- | --- |
| 4 | −45 | 0,87 | +12 | +6 | −24 |
| 5 | −231 | −2,33 | 0 | −170 | −600 |
| 6 | +15.323 | 0,40 | +1.260 | +2.440 | +5.520 |
| 7 | −489.315 | 0,62 | +17.640 | −44.072 | −157.080 |
| 8 | +18.915.683 | 0,55 | −639.492 | +301.826 | +8.781.080 |
| 9 | −713.621.455 | 0,64 | +31.029.264 | +3.277.986 | −288.798.552 |
| 10 | +30.298.578.939 | 0,62 | −1.514.422.740 | +1.044.427.188 | +11.857.980.960 |

- κ_n tem sinal (−1)^n de **n = 6 a 10** (não em n = 4 e 5).
- As partes de um ponto, que transmitem o sinal **por demonstração**, respondem por 55% a 64% de κ de n = 7 a 10.
- A parte de **raiz prima**, que é a entrada nova, tem o sinal (−1)^n de n = 5 a 10 e pesa cerca de 39% a 46% (n = 8 a 10). **Isso não está explicado.**
- O resto paralelo se opõe de n = 7 a 10, mas é pequeno (3% a 5%).

**Separando as duas perguntas:**

- **A transmissão está demonstrada.** As operações de um ponto passam o sinal de κ de um tamanho a outro, sempre invertendo.
- **A alternância não está demonstrada.** Ela depende de a parte de raiz prima ter o mesmo sinal ou não dominar, e isso só foi observado de n = 5 a 10.

## 5. χ: por que ela é irregular (D, qualitativo; V, quantitativo)

As regras de χ **conflitam**:

- o ponto embaixo troca o sinal;
- o ponto isolado **não** troca;
- o ponto em cima importa κ com sinal +, isto é, com o padrão (−1)^{n−1}, oposto ao do próprio ponto embaixo.

Um caráter assim não tem como herdar um padrão único. Os dados mostram cancelamentos enormes: a soma das partes de um ponto vale 12,65 vezes |χ₈|, 2,48 vezes χ₉ e 3,36 vezes χ₁₀. A parte "maior elemento", n·κ_{n−1}, é a maior em n = 8 a 10. **Fica explicado por que χ é irregular**: ela mistura três regras de sinal incompatíveis.

## 6. O que vem de ordens menores e o que é novo (D)

**Reconstruível a partir de ordens menores:**

- **as partes de um ponto:** são fórmulas fechadas em κ e χ de tamanhos menores (itens 2 e 4);
- **o resto paralelo sem isolados e o resto série sem extremos:** são determinados exatamente pelas somas refinadas de tamanhos menores, pela recursão de `ANALITICO_3.md`.

**Genuinamente novo em cada n:** só a parte de **raiz modular prima**. Em κ ela pesa cerca de 39% a 46% (n = 8 a 10). Em χ₁₀ ela vale −1,91 vezes o total, isto é, tem sinal oposto ao do total.

## 7. Resumo e o que continua em aberto

- **Demonstrado:** a regra geral das três operações de um ponto sobre os 16 caracteres, e que κ é o único caráter fechado sob elas, sempre com troca de sinal. Isso dá um mecanismo estrutural para alternâncias (−1)^n, e todo caráter é levado a κ por cadeias de extremos.
- **Observado (n ≤ 10):** κ alterna de n = 6 a 10; a parte de raiz prima de κ acompanha de n = 5 a 10.
- **Em aberto:** por que a parte de raiz prima de κ tem o sinal (−1)^n. Ela é o único ingrediente novo, e é a peça que faltaria para transformar a transmissão em alternância demonstrada.
