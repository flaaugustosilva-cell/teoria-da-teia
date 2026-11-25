# Comparação: a janela da Teia e a supressão das teias ruins na literatura de conjuntos causais

Data: 24/11/2026 (revisto no mesmo dia, depois da leitura completa de Loomis–Carlip; ver seção 6). Scripts: `scripts/h1b_literatura_bicamada.py` (opção `separa`) e `scripts/h1b_literatura_isolados.py`. Saídas: `literatura_bicamada.txt`, `literatura_separa.txt`, `literatura_isolados.txt`.

Os níveis estão marcados assim:

- **(D)** demonstrado;
- **(V)** verificado exatamente;
- **(L)** afirmação da literatura, lida nos artigos;
- **(O)** observação.

**Fontes:**

- S. P. Loomis e S. Carlip, *Suppression of non-manifold-like sets in the causal set path integral*, Class. Quantum Grav. 35 (2018), arXiv:1709.00064.
- P. Carlip e S. Carlip, *Path integral suppression of badly behaved causal sets*, arXiv:2209.00327.
- S. Carlip, *Causal Sets and an Emerging Continuum*, Gen. Relativ. Gravit. (2024), arXiv:2405.14059.

**Limite da leitura:** Loomis–Carlip foi lido por inteiro, mas pela versão HTML (ar5iv) e por ferramenta automática; P. Carlip e S. Carlip e Carlip (2024), só em parte. Equações citadas aqui devem ser conferidas no PDF antes de qualquer texto para fora.

## 1. A convenção é a mesma (L e D)

- P. Carlip e S. Carlip escrevem I/ħ = 2√(2/3)(ℓ/ℓ_p)²·(n − N₀ + 9N₁ − 16N₂ + 8N₃). É exatamente a nossa ação, com θ = 2√(2/3)(ℓ/ℓ_p)².
- O "β" da literatura é, portanto, **β = θ/2**, que é o nosso β.
- Loomis–Carlip usam a mesma estrutura (S/ħ = μ·B, β = μ/2).

## 2. A janela da Teia é a fase de supressão de Loomis–Carlip (L e D)

**Correção (24/11, depois da leitura completa).** A primeira versão deste arquivo dizia que a condição de Loomis–Carlip é só |cos β| < 1/2. **Estava errado.** A condição deles tem duas partes:

- **(L) Eq. 4.14:** tan β > 0 **e** |cos β| < 1/2. Juntas, dão **tan β > √3**, isto é, β ∈ (π/3, π/2) (a menos de múltiplos de π). É uma condição **de um lado só**.
- **(L) Eq. 4.15 (já no artigo de 2018):** uma cota mais fina, tan β > (27/4·e^{−1/2} − 1)^{1/2} ≈ 1,759, que dá |μλ₀| ≈ 2,108 e ℓ ≈ 1,452 ℓ_p **na normalização deles**. Eles dizem que não sabem se esse limite é ótimo.
- **(D) O outro lado vem de graça:** como B é inteiro, |𝒵(2π − θ)| = |𝒵(θ)|. Então o lado θ ∈ (π, 4π/3) é o espelho de θ ∈ (2π/3, π).

**Como fica a comparação:**

- **A nossa "janela 1":** π/3 ≤ β ≤ 2π/3, isto é, θ ∈ [2π/3, 4π/3], ou seja, |cos β| ≤ 1/2.
- **(D)** A janela = (condição tan β > √3 de Loomis–Carlip) ∪ (o seu espelho) ∪ (o centro β = π/2, onde tan β é infinita). Não é "exatamente a condição deles", como eu tinha escrito; é a condição deles **mais a simetria de espelho**.
- **O nosso Teorema 1′** usa q = 2|cos β|, a mesma quantidade que aparece na metade |cos β| < 1/2.

**Consequência:** a janela não é uma previsão própria da Teia. É a condição já conhecida da teoria de conjuntos causais, e o Teorema 1 (|𝒵_ruim| ≤ 3ⁿ/n!) é uma versão exata, para n finito, do mesmo fenômeno.

**A condição mais fina** (Eq. 4.15 de Loomis–Carlip 2018, repetida por P. Carlip e S. Carlip 2022 e Carlip 2024) é tan β > (27/4·e^{−1/2} − 1)^{1/2} = 1,759, isto é, β ∈ (1,0539; π/2), ou θ ∈ (2,108; π).

- Ela cobre a janela quase toda pelo lado de baixo (θ < π).
- O lado θ ∈ (π, 4π/3) é o espelho, porque como B é inteiro, |𝒵(2π − θ)| = |𝒵(θ)|.
- Ela deixa de fora só a borda θ ∈ (2,094; 2,108).
- Carlip (2024) traduz isso como ℓ ≳ 1,136 ℓ_p. **(D)** É o mesmo número que o 1,452 ℓ_p de Loomis–Carlip: a diferença é só a normalização (1,452² / 1,136² = 1,633 = 2√(2/3), o fator da nossa ação). Com ℓ_p = √(8πGħ), a convenção do repositório, isso dá cerca de 5,69 l_P, que é **a borda inferior da nossa janela** (5,677 l_P).

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
- **Onde está essa parte (V, n = 80):** os maiores termos da soma por número de minimais estão em a ≈ n/2, com módulos de cerca de 10²³, e se cancelam até cerca de 10¹³.
- **Correção (25/11):** eu tinha concluído daí que a parte que sobra "não vem de um canto". **Estava errado.** Ela vem justamente de um canto: as ordens com só 2 ou 3 elementos minimais (ou maximais). Ver a seção 7 e `EXPLORATORIO_RESIDUO_ASSINTOTICO.md`.
- **As três explicações que eu tinha listado** (classe diferente, normalização diferente, extremidades da integral) foram conferidas na seção 6. As duas primeiras caem: a classe é a mesma e a normalização bate. O que sobra é um detalhe de contagem, explicado na seção 6.

## 4. Por que isso importa para a Teia (O)

- **A pergunta certa é a comparação, não a supressão.** Como a amplitude das teias ruins não vai a zero (−1 exato no centro, até 3ⁿ na janela), "as ruins são suprimidas" não basta. É preciso que as **boas** fiquem acima desse resíduo. É exatamente o H1\*, e foi isso que testamos (demonstrado por computador para n = 5 a 10).
- **O que a Teia tem de próprio aqui:**
  - **(a)** resultados **exatos e não assintóticos**: Teoremas 1 e 1′, −1 exato no centro, b_n = 2 − 2ⁿ;
  - **(b)** a comparação direta com as teias boas em n ≤ 11, que a literatura não faz;
  - **(c)** a observação de que a forma assintótica e^{−bn²} não descreve a soma completa das ordens de altura ≤ 2, e o motivo exato (seção 6).
- **O que a Teia não tem de próprio:** a ação, a janela e a ideia de supressão por interferência são todas da teoria de conjuntos causais.

## 5. Próximos passos

1. ~~Conferir no PDF a Eq. 4.2.~~ **Feito em 25/11** (seção 6, parte "Conferência no PDF").
2. **Testar se as teias boas superam o resíduo de forma assintótica** (H1\* para todo n). Esse é o ponto em que a Teia pode contribuir de fato ao problema central de emergência do contínuo.

## 6. De onde vem a discrepância (D, com V; a ligação com o artigo é L, a conferir)

**O que está no artigo (L, leitura por ferramenta).**

- **A classe:** "duas camadas" = não existem três elementos distintos x ≺ y ≺ z. É **exatamente** a nossa altura ≤ 2.
- **A variável:** p = N₀/N_max, com N_max = n(n−1)/2.
- **A contagem:** binomial, rotulada (Eq. 4.2), com entropia ln|C_{p,n}| = ¼h(2p)n² + o(n²) (Eq. 4.5).
- **O método:** a soma em N₀ vira uma integral em p ∈ [0, 1/2], resolvida por ponto de sela. O apêndice controla os termos de Taylor de ordem mais alta (cerca de 0,0116). Não há tratamento de correções de tamanho e^{cn}.

**A separação exata (D).** Abrindo (y^a − 1)^{n−a} pelo binômio, a soma exata se separa em dois pedaços:

- **o termo "bipartido livre"** F = Σ_a C(n, a)·y^{a(n−a)}: escolher quem fica na camada de baixo e depois **qualquer** conjunto de relações de baixo para cima;
- **o resto**, que é a inclusão–exclusão que garante que cada ordem seja contada uma vez só.

**O que o termo bipartido livre conta (D, com prova curta; V por força bruta, n = 1 a 5, três valores de θ, diferença ≤ 3×10⁻¹³).**

  F·e^{iθn} = Σ sobre as ordens de altura ≤ 2 de **2^{iso}**·e^{iθB}, em que iso = número de pontos isolados.

- **Prova:** dada a ordem, quem está abaixo de alguém tem de ficar embaixo, e quem está acima de alguém tem de ficar em cima. Só os pontos isolados podem ir para qualquer lado. Então cada ordem aparece 2^{iso} vezes.
- **Em funções geradoras exponenciais:** F̂(x) = e^{e^{iθ}x}·Â(x). A soma exata é a do bipartido livre "descontada" de um fator por ponto isolado.

**Conferência no PDF (25/11; L, leitura do PDF por ferramenta automática).**

- **Eq. 4.2:** |C_{q,p,n}| = C(αn², ½pn(n−1)), com α = q(1−q). Eles põem qn elementos em cima e (1−q)n embaixo e escolhem **qualquer** subconjunto das αn² relações possíveis. Não exigem que cada elemento de cima tenha relação e não falam de pontos isolados nem de dupla contagem.
- **Eq. 4.4:** |C_{½,p,n}| ≤ |C_{p,n}| ≤ Σ_q |C_{q,p,n}|. Daí a Eq. 4.5: ln|C_{p,n}| = ¼h(2p)n² + o(n²). Os termos o(n²) são **escritos e depois desprezados** no ponto de sela.
- **Rotulada ou não:** a seção 4 não diz. A seção 5 só menciona que há "sutilezas" entre rotuladas e não rotuladas.

**O que isso muda na leitura (D).** Para altura ≤ 2, B = n − N₀. Então a soma que eles querem, Σ_p |C_{p,n}|·e^{iS(p)}, com a contagem **exata** |C_{p,n}|, é exatamente o nosso a_n. O que eles calculam de fato é só a parte de ordem n² dessa contagem (camadas q = 1/2, relações livres), que dá o termo do meio de F. **A discrepância está inteira nos termos o(n²) desprezados.** Eles não fazem um erro de lógica no expoente n²; a conclusão em valor absoluto é que fica incompleta.

**A sela de Loomis–Carlip é o termo do meio de F, e não da soma exata (V, `literatura_separa.txt`).**

- O termo a = n/2 de F é **idêntico**, em todas as casas mostradas, a exp[(n²/4)(−iβ + ln(2 cos β))], que é a forma de sela.
- Os números:

| θ | n | \|soma exata\| | \|F\| | \|resto\| |
| --- | --- | --- | --- | --- |
| 2,5 | 40 | 1,0×10⁸ | 2,0 | 1,0×10⁸ |
| 2,5 | 80 | 5,2×10¹³ | 2,0 | 5,2×10¹³ |
| 2,9 | 80 | 4,0×10⁵ | 2,0 | 4,0×10⁵ |
| 2,114 | 80 | 5,0×10³² | 7,4×10⁷ | 5,0×10³² |

- **No interior da janela, |F| → 2:** os termos do meio somem como e^{−bn²}, e sobram só as duas pontas (todos embaixo ou todos em cima, isto é, a anticadeia contada duas vezes). **F se comporta como a literatura diz.**
- **Perto da borda (θ = 2,114),** |F| ainda cresce em n = 80. Isso vem das divisões muito desiguais (poucos elementos embaixo) e é um efeito de n finito: pela conta C(n,1)·|y|^{n−1}, ele deve sumir por volta de n ≈ 350. Não foi verificado.
- **Todo o crescimento exponencial está no resto,** isto é, na correção de contagem dos pontos isolados.

**Leitura (O).**

- Na **entropia**, contar cada ordem 2^{iso} vezes não muda nada no termo n² (as ordens com muitos isolados são raras). Por isso a aproximação é legítima para contar.
- Na **soma com fase**, o mesmo detalhe muda tudo: com o peso 2^{iso} a soma fica limitada (≈ 2); com o peso certo (1), ela cresce exponencialmente.
- A Eq. 4.2 é a contagem bipartida livre com q fixo (conferido no PDF, acima). Então a estimativa e^{−bn²} descreve o termo do meio de F, e não a soma exata sobre ordens. A afirmação "as ordens de duas camadas são exponencialmente suprimidas" continuaria certa **em relação ao número de ordens** (2^{n²/4}), mas não em valor absoluto.
- **O que isto não diz:** não diz que a conclusão física deles está errada. O que importa para a emergência do contínuo é se as ordens boas superam esse resíduo e^{cn}, o que é a pergunta do H1\*. Também não diz nada sobre as outras classes de ordens ruins que eles tratam.
- **Cuidado de nível:** a identidade e a separação são (D). A forma da Eq. 4.2 é (L), lida no PDF por ferramenta automática.

## 7. Qual parte das ordens produz o resíduo (exploratório, 25/11; O com V numérico)

Detalhes, tabelas e regras de leitura em `EXPLORATORIO_RESIDUO_ASSINTOTICO.md`. Resumo:

- **(D)** O termo a da soma, T_a = C(n,a)·(y^a − 1)^{n−a}, é exatamente a soma com fase das ordens com **exatamente a elementos minimais**.
- **(D desde 25/11: Teorema 2, `ANALITICO_11_TEOREMA2.md`; antes era V numérico, n até 640, 8 valores de θ)** A soma inteira fica igual a **2·T_{k\*}**, em que k\* é o k que maximiza |1 − y^k| (k\* = 2 para θ ≳ 2,35; k\* = 3 perto da borda de baixo). O fator 2 é o espelho: ordens com k\* maximais dão a mesma soma (a inversão da ordem não muda B).
- **Leitura:** o resíduo que não se cancela vem das camadas **mais desiguais possíveis** (2 ou 3 elementos numa camada, todo o resto na outra). É o canto oposto ao das camadas equilibradas (q = 1/2) da sela. Esse canto tem entropia desprezível (por isso some no o(n²)), mas as fases dele não se cancelam.

