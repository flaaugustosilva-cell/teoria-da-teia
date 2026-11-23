# Análise 9: a parte de raiz modular prima por módulos substituídos (κ e o caráter trivial)

Data: 23/11/2026. Script: `scripts/h1b_raiz_prima_modulos.py`. Saída: `raiz_prima_modulos.txt`. População: todas as ordens, θ = π.

Os níveis estão marcados assim:

- **(D)** demonstrado;
- **(V)** verificado exatamente;
- **(O)** observação.

**Nenhuma conjectura foi registrada,** e em especial nenhuma sobre a alternância da raiz prima.

**Três cuidados mantidos, a pedido do Flavio:**

1. Redução estrutural não é explicação do sinal.
2. Não se supõe que a raiz prima alterne.
3. As somas são sempre com sinal. Nunca se toma o módulo de uma contribuição, e o estado (m, D, M, U) é preservado exatamente.

## 1. Decomposição por substituição (D)

**Teorema de Gallai.** Toda ordem P de raiz modular prima se escreve de **um único jeito** como P = Q[M₁, …, M_k], em que:

- Q é **estritamente prima**: não tem módulos não triviais, e k ≥ 4;
- cada Mᵢ é uma ordem qualquer, que é o módulo máximo no lugar do ponto qᵢ.

Reciprocamente, para Q estritamente prima, qualquer escolha de Mᵢ dá uma ordem com raiz Q.

**Intervalos.**

- Para x, y ∈ Mᵢ, o intervalo em P é o mesmo que em Mᵢ. Um elemento de fora se relaciona igualmente com todo Mᵢ, então não pode ficar entre dois elementos dele.
- Para x ∈ Mᵢ, y ∈ Mⱼ e qᵢ < qⱼ, o número de elementos entre x e y é:

  (elementos de Mᵢ acima de x) + (elementos de Mⱼ abaixo de y) + Σ_{qᵢ < q_l < qⱼ} |M_l|.

**Consequência: o sinal.** Um par cruzado só entra em N₀ + N₁ quando:

- **(a)** qᵢ ⋖ qⱼ é cobertura em Q. A contribuição é X(Mᵢ)m(Mⱼ) + U(Mᵢ)m(Mⱼ) + X(Mᵢ)D(Mⱼ), o mesmo Δ da soma ordinal;
- **(b)** há exatamente um q_l entre qᵢ e qⱼ e |M_l| = 1. A contribuição vai para N₁ e vale X(Mᵢ)·m(Mⱼ).

Escrevo X para o número de máximos, para não confundir com o M dos módulos. Como n = Σ|Mᵢ|, vale

  s(P) = Π s(Mᵢ) · (−1)^{Σ_(a) Δ + Σ_(b) X·m}.

**Consequência: o estado.** Um elemento x ∈ Mᵢ tem abaixo dele os seus elementos abaixo em Mᵢ mais Σ_{q_l < qᵢ} |M_l|. Daí:

- m(P) = Σ_{qᵢ mínimo} m(Mᵢ);
- D(P) = Σ_{qᵢ mínimo} D(Mᵢ) + Σ_{qᵢ com um só q_l abaixo, |M_l| = 1} m(Mᵢ);
- X(P) e U(P) saem do mesmo jeito, por dualidade.

**Leitura estrutural (D).** A parte de raiz prima se separa exatamente em duas:

- **(i) estritamente primas:** todos os módulos são pontos. É a parte genuinamente nova de cada n;
- **(ii) com algum módulo de tamanho ≥ 2:** ela é função das ordens estritamente primas de tamanho k < n e das estatísticas, com sinal e com estado, dos módulos, que são ordens menores.

Isso é uma **redução estrutural**, não uma explicação do sinal.

## 2. Verificação (V)

- **Ponto a ponto.** Foram 2.065 substituições aleatórias Q[M₁…M_k], com Q estritamente prima de 4 a 6 pontos e módulos de 1 a 4 elementos, n ≤ 10. Em todas, o sinal e o estado da fórmula coincidem com o cálculo direto, e o algoritmo de módulos recupera exatamente os Mᵢ.
- **Ordens estritamente primas encontradas** (classes): 1 com k = 4 (a ordem "N"), 4 com k = 5 e 28 com k = 6.
- **Agregado.** Para cada n de 4 a 10, a soma das duas partes reproduz exatamente a parte de raiz prima de `ANALITICO_8.md`.
- **Não feito:** reconstruir a parte (ii) só a partir de dados de tamanhos menores. A soma sobre os estados de k módulos cresce como 16^k, e precisaria de um método de matriz de transferência.

## 3. Os números (O)

| n | κ: estritamente prima | κ: com módulos | fração com módulos | trivial: estritamente prima | trivial: com módulos |
| --- | --- | --- | --- | --- | --- |
| 4 | −24 | 0 | 0 | −24 | 0 |
| 5 | −120 | −480 | 0,80 | −120 | 0 |
| 6 | +840 | +4.680 | 0,85 | −3.480 | +600 |
| 7 | +33.600 | −190.680 | — | −80.640 | −27.720 |
| 8 | +2.684.640 | +6.096.440 | 0,69 | **+1.448.160** | −3.227.784 |
| 9 | −60.056.640 | −228.741.912 | 0,79 | −65.378.880 | +731.304 |
| 10 | +1.092.299.040 | +10.765.681.920 | 0,91 | −1.439.998.560 | −1.137.260.400 |

**Sinal em relação a (−1)^n, no caráter κ:**

- **parte com módulos:** acompanha em todo n de 5 a 10;
- **parte estritamente prima:** acompanha em n = 5, 6, 8, 9 e 10, mas **não** em n = 4 nem em n = 7. Em n = 7 ela é positiva, e a parte com módulos é negativa e maior.

**Por perfil de módulos.** Separando por (número de módulos não triviais, tamanho do maior módulo), **todos** os seis perfis de maior peso têm o mesmo sinal em cada n = 8, 9 e 10. Por exemplo, em n = 10, "um módulo de 2 elementos" vale +3,79×10⁹ e "dois módulos de 2" vale +1,86×10⁹.

**No caráter trivial (ligado a C3).** A parte estritamente prima é **positiva** em n = 8 (+1.448.160). Ali, C3 vale só porque a parte com módulos (−3.227.784) é maior. Ou seja: **nem no caráter trivial as ordens estritamente primas têm sinal regular.**

## 4. Respostas

**A raiz prima em κ admite decomposição exata por módulos substituídos, preservando caracteres e sinais?** Sim (D, com V):

- a parte com módulos é herdada de ordens menores, por uma fórmula fechada para sinal e estado;
- a parte genuinamente nova é a das ordens estritamente primas.

**Quanto de κ é herdado?** Entre 69% e 91% da parte de raiz prima, para n = 8 a 10. Essa parte herdada acompanha o padrão (−1)^n em todo n de 5 a 10, e em todos os perfis principais (O).

**E a parte nova?** Ela é **irregular**: contra o padrão em n = 4 e 7, e com sinal não regular também no caráter trivial.

**Leitura.** A regularidade observada no centro da janela parece vir, de novo, da **composição** (agora a substituição de módulos), e não das ordens estritamente primas. **Isso não explica o sinal** (cuidado 1): ainda falta mostrar por que a substituição de módulos transmite o padrão de κ, como fizemos para as operações de um ponto.

**Em aberto:**

- uma regra de transformação de κ ao trocar um ponto de Q por um módulo, que seria o análogo das regras do `ANALITICO_8.md`;
- a matriz de transferência para reconstruir a parte (ii) a partir de tamanhos menores.
