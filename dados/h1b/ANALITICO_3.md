# Análise 3: identidade da soma ordinal e redução às ordens de raiz modular prima

Data: 20/11/2026.

- Os itens 1 a 4 são **demonstrações**.
- O item 5 é uma **verificação exata por computador** até n ≤ 10. Ela não substitui as demonstrações; serve para conferir que as definições do código são as do texto.
- Script: `scripts/h1b_soma_ordinal.py`. Saída: `verificacao_soma_ordinal.txt`.

## Notação

- **Contagens de intervalos:** para uma ordem finita P, N_k(P) é o número de pares x < y com exatamente k elementos z tais que x < z < y.
- **Ação:** B(P) = n − N₀ + 9N₁ − 16N₂ + 8N₃ = n + c·N, com c = (−1, 9, −16, 8). O sinal no centro da janela é (−1)^B = (−1)^{n + N₀ + N₁}.
  - Para não confundir com a ação, escrevo β(P) = N₀ + N₁. Na sua mensagem esse número aparece como "B".
- **Perfis:**
  - u_a(P) é o número de elementos com exatamente a elementos acima;
  - d_b(P) é o número de elementos com exatamente b elementos abaixo.
- **Estatísticas das bordas:**
  - M = u₀ (máximos) e U = u₁;
  - m = d₀ (mínimos) e D = d₁.
- **Soma ordinal:** P ⊕ Q coloca todos os elementos de P abaixo de todos os de Q.
- **União disjunta:** P + Q.

## 1. Intervalos na soma ordinal (lema)

Em P ⊕ Q:

- **(i)** Para p, p′ ∈ P, o intervalo (p, p′) em P ⊕ Q é o mesmo que em P, porque nenhum elemento de Q está abaixo de um elemento de P. Vale o análogo para Q.
- **(ii)** Para p ∈ P e q ∈ Q, sempre p < q, e

  {r : p < r < q} = {r ∈ P : p < r} ∪ {s ∈ Q : s < q},

  uma união disjunta. Portanto o número de elementos entre p e q é a + b, em que a é o número de elementos de P acima de p e b o número de elementos de Q abaixo de q.

**Consequência, para todo k:**

  N_k(P ⊕ Q) = N_k(P) + N_k(Q) + X_k, em que X_k = Σ_{a+b=k} u_a(P)·d_b(Q).

Como n também soma (n_P + n_Q), vale para todo θ:

  B(P ⊕ Q) = B(P) + B(Q) + c·X.

**No centro, θ = π:** X₀ + X₁ = u₀d₀ + u₀d₁ + u₁d₀ = M(P)m(Q) + M(P)D(Q) + U(P)m(Q). Logo

  (−1)^{B(P⊕Q)} = (−1)^{B(P)} (−1)^{B(Q)} (−1)^{Δ(P,Q)}, com Δ = M(P)m(Q) + U(P)m(Q) + M(P)D(Q).

É a fórmula da sua mensagem. Como só a paridade importa, Δ depende apenas das paridades de M, U, m e D.

## 2. União disjunta

Na união P + Q, os intervalos não se misturam. Então N_k, n e B somam, e o sinal se multiplica. As quatro estatísticas m, D, M e U também somam.

## 3. As estatísticas das bordas também se compõem

Em P ⊕ Q:

- **Mínimos:** m(P ⊕ Q) = m(P).
- **Máximos:** M(P ⊕ Q) = M(Q).
- **D:** um elemento q de Q tem |P| + (número de elementos de Q abaixo de q) elementos abaixo. Isso vale 1 só se |P| = 1 e q for mínimo em Q. Logo D(P ⊕ Q) = D(P) + [|P| = 1]·m(Q).
- **U:** pela mesma conta, U(P ⊕ Q) = U(Q) + [|Q| = 1]·M(P).

Então o **estado** σ = (m, D, M, U) mod 2, junto com o tamanho, se propaga de forma fechada nas duas operações.

## 4. Recursão exata (teorema)

**Os três tipos.** Toda ordem com n ≥ 2 é de exatamente um destes tipos:

- **paralela:** o grafo de comparabilidade é desconexo;
- **série:** o grafo de incomparabilidade é desconexo;
- **raiz modular prima:** os dois grafos são conexos.

Paralela e série não acontecem juntas, porque o complemento de um grafo desconexo é conexo. A ordem de um elemento é contada no tipo "raiz prima" (é a convenção do código). Pelo teorema de Gallai, o tipo "raiz prima" corresponde à raiz prima da decomposição modular. A definição usada, porém, é a operacional acima.

**Decomposição única das ordens tipo série.** Sejam C₁, …, C_k as componentes do grafo de incomparabilidade, com k ≥ 2.

- Dois elementos de componentes diferentes são sempre comparáveis.
- Se x ∈ C_i, y ∈ C_j, x < y e x′ ∈ C_i é incomparável com x, então x′ < y. De fato, se fosse y < x′, teríamos x < y < x′, contradizendo a incomparabilidade de x e x′.
- Pela conexidade de C_i, então todos os elementos de C_i ficam abaixo de y. Repetindo o argumento dentro de C_j, todos ficam abaixo de todos os elementos de C_j.
- Assim as componentes ficam linearmente ordenadas, e a ordem é C₁ ⊕ C₂ ⊕ … ⊕ C_k.

Por isso, cada ordem tipo série se escreve **de um único jeito** como P₁ ⊕ Q, em que P₁ é a componente de baixo (indecomponível em série: tipo paralela, raiz prima, ou um ponto) e Q é uma ordem qualquer.

**Somas refinadas.** Seja X_n[σ] a soma de (−1)^B sobre as ordens rotuladas em n elementos de um dado tipo e estado σ. Escrevo:

- A_n para todas as ordens;
- Par_n para as paralelas;
- Ser_n para as do tipo série;
- Prim_n para as de raiz prima;
- I_n = Par_n + Prim_n para as indecomponíveis em série;
- Con_n = Ser_n + Prim_n para as conexas.

Então:

- **Série:**

  Ser_n[σ] = Σ_{k=1}^{n−1} C(n, k) · Σ_{σ₁, σ₂} I_k[σ₁] · A_{n−k}[σ₂] · (−1)^{Δ(σ₁, σ₂)},

  em que só entram os pares (σ₁, σ₂) que compõem σ pelo item 3. O fator C(n, k) escolhe quais rótulos vão para a parte de baixo.
- **Paralelo** (fórmula exponencial no grupo (ℤ/2)⁴ dos estados, com ⊛ = convolução por XOR):

  Par_n = Σ_{k=1}^{n−1} C(n−1, k−1) · Con_k ⊛ A_{n−k}.
- **Total:** A_n = Par_n + Ser_n + Prim_n.

**Corolário.** A soma rotulada T_todas(n) = Σ_σ A_n[σ] é uma expressão exata e fixa nas somas refinadas das ordens de raiz prima de tamanho ≤ n, com 16 números por tamanho. **Todo o problema do sinal no centro se reduz às ordens de raiz modular prima.**

Esta recursão usa só o estado mod 2, então vale **só em θ = π**. Para outros θ, a fórmula do item 1 continua valendo, mas o estado teria de guardar os perfis completos (u₀, …, u₃ e d₀, …, d₃) e não só as paridades.

## 5. Verificação exata para n ≤ 10 (todas as ordens)

- **(a) Ponto a ponto:** N_k(P ⊕ Q) = N_k(P) + N_k(Q) + X_k, para k = 0 a 3, confere em **todos os 524.009 pares** de classes com |P| + |Q| ≤ 10.
- **(b1)** As partes paralela e série de cada n ≤ 10, calculadas pelos dados, são reproduzidas exatamente a partir dos tamanhos menores.
- **(b2) Recursão pura:** usando como dado **apenas** as somas das ordens de raiz prima, ela reproduz exatamente as somas de todas as ordens para n = 1 a 10.

| n | raiz prima | paralelo | série | todas |
| --- | --- | --- | --- | --- |
| 4 | −24 | +1 | +10 | −13 |
| 5 | −120 | +29 | +260 | +169 |
| 6 | −2.880 | −599 | −6.782 | −10.261 |
| 7 | −108.360 | +62.705 | +27.916 | −17.739 |
| 8 | −1.779.624 | +958.273 | −1.359.990 | −2.181.341 |
| 9 | −64.647.576 | +26.869.253 | +9.873.636 | −27.904.687 |
| 10 | −2.577.258.960 | +670.248.361 | −587.673.902 | −2.494.684.501 |

A soma das ordens de raiz prima é negativa em todo n de 4 a 10. Isso é o que inspirou a conjectura C3 (`PREREGISTRO_C3.md`) e **não** conta como teste dela.

## O que isto não demonstra

As três afirmações continuam separadas:

1. a soma das ordens de raiz prima é negativa (C3, conjectura);
2. a soma total é negativa (C2′ e C2, conjecturas);
3. as boas dominam as ruins em toda a janela (H1\*, demonstrado só para n = 5 a 10).

A identidade explica **como** a primeira alimenta a segunda, mas não diz que a parte paralela mais a série não possam inverter o sinal. Isso dependeria do tamanho relativo das partes, e nada aqui o controla. A terceira afirmação envolve θ ≠ π, e a recursão por paridade não alcança esses pontos.
