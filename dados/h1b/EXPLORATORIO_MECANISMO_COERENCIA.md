# Exploração (fora de registro): de onde vem o excesso de coerência da faixa de cerca de 3 dimensões

Data: 24/11/2026. Desenho proposto pelo Flavio (três mecanismos e dois controles), com os detalhes abaixo.

- **Scripts:** `scripts/h1b_mecanismo_coerencia.py` e `scripts/h1b_mecanismo_altura.py`.
- **Saídas:** `mecanismo_coerencia_n8_9.txt`, `mecanismo_coerencia_n10_11.txt`, `mecanismo_altura_X.txt` e os JSON.
- **Definições congeladas:** todas as ordens, n = 8 a 11; peso n!/|Aut| (proporcional a 1/|Aut|); faixa de Myrheim–Meyer 2,5 ≤ d < 3,5; janela com 241 pontos.

Os níveis estão marcados assim:

- **(D)** demonstrado;
- **(V)** verificado;
- **(O)** observação.

Nada foi registrado como conjectura.

## 0. Base e validação

**(D) A coerência só depende do histograma de B da classe** (observação do Flavio). Como Z_g(θ) = Σ_b W_g(b)·e^{iθb}, tudo sai do histograma conjunto H(R, b): o peso das ordens com R pares comparáveis e ação b.

**(V) Validação do cálculo.**

- A coerência real calculada pelo histograma coincide **exatamente** com a publicada, para n = 8, 9, 10 e 11.
- O controle por subconjuntos aleatórios é, na prática, um **piso de ruído amostral**. Para um subconjunto em que cada classe entra com probabilidade q:

  E|Z_sub|² = q²|𝒵|² + q(1−q)Σw².

  Calculei a mediana prevista por essa fórmula (distribuição de Rice). Ela fica a até 10% das medianas dos controles guardados em todas as faixas e todos os n (por exemplo, n = 11, faixa de 3 dimensões: prevista 6,37×10⁻⁴, observada 7,03×10⁻⁴). Isso permitiu calcular o piso de cada fatia sem sortear de novo.

## 1. Mecanismo 1: a distribuição de B explica? Os degraus

Faixa de 2,5 a 3,5. Coerência mediana na janela, em quatro degraus:

| n | independência (histograma da população) | tilt: média e variância de B | tilt: + paridade | **real** | piso do controle |
| --- | --- | --- | --- | --- | --- |
| 8 | 5,9×10⁻³ | 5,0×10⁻³ | 1,85×10⁻² | **8,68×10⁻²** | 2,86×10⁻² |
| 9 | 2,6×10⁻³ | 3,5×10⁻³ | 4,6×10⁻³ | **2,91×10⁻²** | 8,5×10⁻³ |
| 10 | 6,9×10⁻⁴ | 8,7×10⁻⁴ | 1,18×10⁻³ | **1,41×10⁻²** | 2,4×10⁻³ |
| 11 | 1,55×10⁻⁴ | 1,60×10⁻⁴ | 3,57×10⁻⁴ | **5,66×10⁻³** | 6,4×10⁻⁴ |

O "tilt" é o histograma de B da população inteira deformado para ter a mesma média, a mesma variância e (na segunda coluna de tilt) a mesma fração de B ímpar da classe. Ele preserva a estrutura aritmética fina da população.

- **A classe tem B mais estreito que a população** (desvio 19,8 contra 31,7 em n = 11). Mas isso, sozinho, **quase não gera coerência**: os tilts ficam **abaixo do piso** em n = 9 a 11.
- **Média, variância e paridade de B explicam pouco e cada vez menos:** 21% da coerência real em n = 8 e 6% em n = 11.
- **O excesso está na estrutura fina do histograma W_g(b),** não nos seus momentos.

## 2. De onde vem a estrutura fina: uma identidade e as fatias por R

**(D) Identidade.** Com R = N₀ + N₁ + N₂ + N₃ + R₄₊ (todos os pares comparáveis):

  **B = n − R + X,  X = 10N₁ − 15N₂ + 9N₃ + R₄₊.**

Verificada classe a classe em n = 8 a 11.

Numa fatia de R fixo, e^{iθB} = e^{iθ(n−R)}·e^{iθX}. Então **a coerência da fatia é exatamente a coerência da distribuição de X dentro dela.**

**(V) Coerência por fatia, em relação ao piso** (n = 11):

- R = 11 a 19: razão de 16 a 22;
- R = 20 a 30: razão de 4 a 13;
- R ≥ 31: razão de 1 a 3.

Em n = 9, as fatias R ≤ 12 dão 4 a 8.

**(V) A fatia é coerente porque X fica concentrado.** Em n = 11:

| R | valores de X com 90% do peso | desvio de X |
| --- | --- | --- |
| 15 | 12 | 16,7 |
| 18 | 27 | 21,8 |
| 25 | 93 | 30,4 |
| 35 | 120 | 37,0 |

Os valores mais frequentes de X são múltiplos de 10 (ex.: +20, +30). Correspondem a ordens em que os pares comparáveis são só elos e intervalos de 1 elemento, com X = 10·N₁.

**(V) As fatias interferem entre si.** Dentro da faixa, o alinhamento de fase |Σ_R Z_R| / Σ_R |Z_R| é só 0,30, 0,21, 0,18 e 0,15 (n = 8 a 11). Isso acontece porque cada fatia tem o deslocamento e^{−iθR}. Por isso a razão da faixa (8,9 em n = 11) fica abaixo da de cada fatia (16 a 22).

**A faixa de cerca de 3 dimensões é, nestes tamanhos, a região de ordens esparsas** (poucos pares comparáveis). Nela, fixar R deixa X em poucos valores. O corte de Myrheim–Meyer em 2,5 fica perto da transição (R ≤ 18 em n = 11), mas **não** coincide com ela: R = 19 está na faixa de 2 dimensões e tem razão 19.

## 3. Mecanismo 2: geometria a B fixo (V)

Dentro de cada estrato de B, comparei a classe com o resto, em desvios-padrão do estrato, ponderando pelo peso da classe:

| n | altura | N₀ | N₁ | N₂ | N₃ |
| --- | --- | --- | --- | --- | --- |
| 9 | −1,42 | −1,79 | −1,92 | −1,78 | −0,96 |
| 11 | −1,36 | −1,49 | −1,78 | −1,75 | −1,10 |

A B fixo, a classe tem **menos intervalos de todos os tipos e é mais baixa**. Isso é em boa parte **definicional**, porque a classe é escolhida por ter poucos pares comparáveis. Mostra, porém, que ela não é "igual ao resto com outra ação".

## 4. Controle A e Controle B

**Controle A** (distribuição de ação contra subconjuntos de mesmo peso): coberto pelos itens 1 e 2. A classe tem um histograma de B fora do comum, e o que é fora do comum é a estrutura fina, não os momentos.

**Controle B** (20 permutações dos rótulos da classe **dentro** dos estratos de B; semente 20261128; mesma contagem por estrato):

| n | corr(B, R) real / permutadas | corr(B, altura) real / permutadas | coerência real / permutadas |
| --- | --- | --- | --- |
| 10 | +0,058 / −0,042 ± 0,002 | +0,107 / +0,049 ± 0,002 | 1,41×10⁻² / 1,12×10⁻² |
| 11 | +0,042 / −0,035 ± 0,001 | +0,098 / +0,043 ± 0,001 | 5,66×10⁻³ / 5,04×10⁻³ |

- **A identidade que você antecipou se confirma.** Com o mesmo histograma por contagem, a pseudo-classe conserva cerca de 80% a 90% da coerência. A diferença vem só de os pesos (|Aut|) variarem dentro do estrato.
- **A associação entre geometria e ação dentro da classe é diferente da de um subconjunto com o mesmo histograma de B.** A correlação com R muda de sinal, e a correlação com a altura é o dobro. A diferença é de dezenas de desvios-padrão das permutações, mas **pequena em valor absoluto**: cerca de 0,06 a 0,1 de correlação. Como a população está enumerada por inteiro, o tamanho do efeito importa mais que a "significância".

## 5. Um confundidor descartado (V)

As ordens de altura ≤ 2 (as teias ruins) têm N₁ = N₂ = N₃ = R₄₊ = 0, e portanto X = 0. Esse é o caso mais extremo de concentração, e elas caem em parte na faixa de 3 dimensões. **Elas não explicam o excesso.** Só com altura ≥ 3, a razão da faixa fica igual ou maior:

| n | faixa inteira | altura ≥ 3 |
| --- | --- | --- |
| 8 | 3,01 | 3,84 |
| 9 | 3,39 | 3,27 |
| 10 | 5,82 | 6,03 |
| 11 | 8,78 | 8,62 |

**Correção de uma afirmação minha, feita antes de rodar:** eu tinha dito que "X = 0 exatamente quando a altura é ≤ 2". O certo é: altura ≤ 2 ⇔ N₁ = N₂ = N₃ = R₄₊ = 0, o que **implica** X = 0. A recíproca é falsa, porque X = 0 também acontece por coincidência aritmética (ex.: N₁ = 3, N₂ = 2). Entre 66% e 95% do peso com X = 0 vem de altura ≥ 3.

## 6. Qual dos três cenários

- **Predomínio da ação (momentos de B): não.** Média, variância e paridade explicam de 6% a 21%, e cada vez menos com n.
- **Predomínio geométrico isolado: não.** A geometria só entra na coerência através do histograma de B, que é uma identidade.
- **Acoplamento: sim, nestes dados (O).** A geometria (poucos pares comparáveis, fixando R) **restringe** a combinação X = 10N₁ − 15N₂ + 9N₃ + R₄₊ a poucos valores, sobretudo múltiplos de 10. Isso gera a estrutura fina que dá coerência. A mistura de valores de R dentro da faixa depois **cancela parte** dessa coerência, pelo deslocamento e^{−iθR}.

**O que isto sugere sobre "dimensão" (O):**

- o sinal que vimos é, mais exatamente, um sinal de **esparsidade**: ordens com poucos pares comparáveis têm ação quase determinada pela geometria;
- a faixa de Myrheim–Meyer de 3 dimensões é uma forma indireta de selecionar essa esparsidade em n ≤ 11;
- isso **enfraquece** a leitura de "seleção de 3 dimensões" e **fortalece** a de "seleção por rigidez aritmética da ação em ordens esparsas";
- o crescimento de R₃ com n acompanha o aumento da razão nas fatias esparsas (cerca de 7 em n = 9 contra cerca de 20 em n = 11).

**Em aberto:**

- uma demonstração de por que, a R fixo e pequeno, X se concentra em múltiplos de 10. Isso exige entender quais configurações de intervalos têm poucos pares comparáveis;
- se o efeito continua quando R cresce junto com n, como numa região de espaço-tempo de verdade (R/C(n,2) ≈ 0,1 em 4 dimensões).
