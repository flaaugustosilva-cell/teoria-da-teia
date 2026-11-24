# Comparação: a janela da Teia e a supressão das teias ruins na literatura de conjuntos causais

Data: 24/11/2026. Script: `scripts/h1b_literatura_bicamada.py`. Saída: `literatura_bicamada.txt`.

Os níveis estão marcados assim:

- **(D)** demonstrado;
- **(V)** verificado exatamente;
- **(L)** afirmação da literatura, lida nos artigos;
- **(O)** observação.

**Fontes:**

- S. P. Loomis e S. Carlip, *Suppression of non-manifold-like sets in the causal set path integral*, Class. Quantum Grav. 35 (2018), arXiv:1709.00064.
- P. Carlip e S. Carlip, *Path integral suppression of badly behaved causal sets*, arXiv:2209.00327.
- S. Carlip, *Causal Sets and an Emerging Continuum*, Gen. Relativ. Gravit. (2024), arXiv:2405.14059.

**Limite da leitura:** os textos foram lidos parcialmente, por ferramenta automática. As definições exatas das classes e das normalizações ainda precisam ser conferidas no texto integral.

## 1. A convenção é a mesma (L e D)

- P. Carlip e S. Carlip escrevem I/ħ = 2√(2/3)(ℓ/ℓ_p)²·(n − N₀ + 9N₁ − 16N₂ + 8N₃). É exatamente a nossa ação, com θ = 2√(2/3)(ℓ/ℓ_p)².
- O "β" da literatura é, portanto, **β = θ/2**, que é o nosso β.
- Loomis–Carlip usam a mesma estrutura (S/ħ = μ·B, β = μ/2).

## 2. A janela da Teia é a fase de supressão de Loomis–Carlip (L e D)

- **Loomis–Carlip:** as ordens de duas camadas são suprimidas quando **|cos β| < 1/2**.
- **A nossa "janela 1":** π/3 ≤ β ≤ 2π/3, isto é, θ ∈ [2π/3, 4π/3]. É **exatamente** |cos β| ≤ 1/2.
- **O nosso Teorema 1′** usa q = 2|cos β|, a mesma quantidade.

**Consequência:** a janela não é uma previsão própria da Teia. É a condição já conhecida da teoria de conjuntos causais, e o Teorema 1 (|𝒵_ruim| ≤ 3ⁿ/n!) é uma versão exata, para n finito, do mesmo fenômeno.

**A condição mais recente** (P. Carlip e S. Carlip 2022, Carlip 2024) é tan β > (27/4·e^{−1/2} − 1)^{1/2} = 1,759, isto é, β ∈ (1,0539; π/2), ou θ ∈ (2,108; π).

- Ela cobre a janela quase toda pelo lado de baixo (θ < π).
- O lado θ ∈ (π, 4π/3) é o espelho, porque como B é inteiro, |𝒵(2π − θ)| = |𝒵(θ)|.
- Ela deixa de fora só a borda θ ∈ (2,094; 2,108).
- Carlip (2024) traduz isso como ℓ ≳ 1,136 ℓ_p. Com ℓ_p = √(8πGħ), a convenção do repositório, isso dá cerca de 5,69 l_P, que é **a borda inferior da nossa janela** (5,677 l_P).

## 3. A soma exata não vai a zero: discrepância com a forma assintótica (D, com V)

**O que a literatura diz (L).** Carlip (2024) escreve a supressão como Z ~ e^{−bn²}, com b > 0 sob a condição de tan β. A conta parte da entropia ln|Ω_{n,2,p}| = ¼h(2p)n² + o(n²) e usa o método de ponto de sela. O próprio autor adverte que é preciso garantir que o resto do contorno seja suprimido.

**A nossa fórmula exata (D; V contra os dados de n = 1 a 10, em θ = π e θ = 2π/3 + 0,3).** Para as ordens de altura ≤ 2, a soma **rotulada** é

  a_n(θ) = e^{iθn} Σ_a C(n, a)·(y^a − 1)^{n−a}, com y = 1 + e^{−iθ}.

Sem pontos isolados, b_n = Σ_j C(n, j)(−e^{iθ})^j·a_{n−j}.

**No centro (D):** a_n(π) = −1 para todo n ≥ 1, e b_n(π) = 2 − 2ⁿ. A condição da literatura vale em θ = π (cos β = 0, tan β = ∞), mas a soma exata **não decai**.

**Dentro da janela (V):** |a_n| e |b_n| crescem exponencialmente com n, sempre abaixo do limite 3ⁿ do Teorema 1:

| θ | n | \|b_n\| exato | termo de sela e^{(n²/4)ln(2\|cos β\|)} | 2^{n²/4} (número de ordens) |
| --- | --- | --- | --- | --- |
| 2,5 | 40 | 9,7×10¹⁶ | 8,2×10⁻⁸¹ | 2,6×10¹²⁰ |
| 2,5 | 80 | 2,4×10³² | 4,5×10⁻³²¹ | 4,4×10⁴⁸¹ |
| 2,9 | 80 | 9,2×10²⁷ | 1,8×10⁻⁹⁸⁹ | 4,4×10⁴⁸¹ |

**Leitura:**

- **A supressão relativa ao número de ordens é enorme e confirmada.** A soma é superexponencialmente menor que 2^{n²/4}. Isso concorda com a literatura em essência.
- **A soma absoluta não vai a zero.** Ela fica entre 1 e 3ⁿ (rotulada), muito acima da estimativa de sela. Algo de ordem exponencial fica fora da forma e^{−bn²}.
- **Onde está essa parte (V, n = 80):** ela **não** vem de um canto de ordens muito esparsas. Os maiores termos da soma por número de minimais estão em a ≈ n/2, com módulos de cerca de 10²³, e se cancelam até cerca de 10¹³.
- **A diferença pode ter três explicações:**
  - a classe da literatura é definida de outro modo (por exemplo, camadas com fração fixa de n e fração de elos longe de 0);
  - a normalização é outra;
  - as extremidades da integral não foram tratadas.

  **Isso precisa ser conferido no texto integral antes de qualquer afirmação de erro.**

## 4. Por que isso importa para a Teia (O)

- **A pergunta certa é a comparação, não a supressão.** Como a amplitude das teias ruins não vai a zero (−1 exato no centro, até 3ⁿ na janela), "as ruins são suprimidas" não basta. É preciso que as **boas** fiquem acima desse resíduo. É exatamente o H1\*, e foi isso que testamos (demonstrado por computador para n = 5 a 10).
- **O que a Teia tem de próprio aqui:**
  - **(a)** resultados **exatos e não assintóticos**: Teoremas 1 e 1′, −1 exato no centro, b_n = 2 − 2ⁿ;
  - **(b)** a comparação direta com as teias boas em n ≤ 11, que a literatura não faz;
  - **(c)** a observação de que a forma assintótica e^{−bn²} não descreve a soma completa das ordens de altura ≤ 2.
- **O que a Teia não tem de próprio:** a ação, a janela e a ideia de supressão por interferência são todas da teoria de conjuntos causais.

## 5. Próximos passos

1. **Ler o texto integral** de Loomis–Carlip e de P. Carlip e S. Carlip:
   - definição exata da classe de "duas camadas";
   - normalização (rotulada ou não);
   - tratamento das extremidades da integral em p.

   Se a discrepância do item 3 persistir, ela é um resultado publicável: uma fórmula fechada com o termo que sobrevive.
2. **Testar se as teias boas superam o resíduo de forma assintótica** (H1\* para todo n). Esse é o ponto em que a Teia pode contribuir de fato ao problema central de emergência do contínuo.
