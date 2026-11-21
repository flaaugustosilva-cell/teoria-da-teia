# Exploração (fora de registro): três frentes em paralelo

Data: 21/11/2026. Nada aqui foi registrado como conjectura.

As três frentes:

- **(a)** piloto de Monte Carlo e planejamento;
- **(b)** o resto do caráter D no centro da janela;
- **(c)** o perfil de intervalos comparado com regiões de 2, 3 e 4 dimensões.

Scripts: `scripts/h1b_dimensao_piloto.py` (a e c) e `scripts/h1b_D_resto.py` (b). Saídas: `dimensao_piloto_a.txt`, `dimensao_perfil_c.txt` e `carater_D_resto.txt`.

## (a) Piloto: coerência de fase de famílias de ordens na janela (O)

**O que foi medido.** Sorteei 1000 ordens por família, com n = 20, 40 e 80 elementos. As famílias são:

- pontos sorteados em diamantes causais de d = 2, 3 e 4 dimensões, que são "espaço-tempos";
- ordens em 3 camadas do tipo Kleitman–Rothschild;
- ordens em 2 camadas, que são as teias ruins.

Para cada família calculei a coerência |E[e^{iθB₄}]| para θ na janela [2π/3, π]. O piso estatístico é cerca de 0,03.

**Resultado:**

- **Todas as famílias têm a fase totalmente embaralhada na janela**, em todos os tamanhos: coerência média de 0,023 a 0,033, que é o piso.
- A largura da ação de cada família vai de 5 a 228 unidades, e θ na janela vale de 2 a 3,14. Então θ·(largura) ≫ 1 para todas.
- Ainda dá para ver diferenças na média da ação: os diamantes têm B₄ médio positivo e pequeno (de 12 a 115), e as camadas têm B₄ médio muito negativo (−714 em n = 80).

**Leitura:**

- A janela física está num regime **profundamente quântico**: a fase por unidade de ação é grande.
- Nenhuma família "sobrevive" por coerência de fase. Argumentos de fase estacionária, do tipo que favoreceria espaço-tempos suaves, **não** se aplicam aqui.
- Se houver seleção de dimensão na janela, ela tem de vir da estrutura aritmética fina (as ressonâncias já encontradas), não de coerência.
- O piloto ignora a entropia, isto é, quantas ordens há de cada tipo.

### Plano para um projeto de Monte Carlo de verdade

**Obstáculos:**

- **(1) Entropia.** As ordens em camadas são a imensa maioria (cerca de 2^{n²/4}), e uma amostragem uniforme de ordens parciais grandes já é difícil.
- **(2) Problema de sinal.** Com pesos complexos, a média de e^{iθB} sobre um conjunto amostrado é da ordem de |𝒵|/W. Isso dá cerca de 4×10⁻⁴ em n = 10 e cai com n, então seriam precisas de 10⁸ a 10¹⁰ amostras para medir com algum erro aceitável.
- **(3) Custo.** Exigiria código em C e de horas a dias de máquina.

**Desenho recomendado, se for adiante:**

- **(i) Controle com pesos positivos** (ação continuada, e^{−βB}). É o regime em que a literatura de conjuntos causais em 2 dimensões trabalha. A pergunta muda, mas o resultado é bem definido.
- **(ii) Medição da coerência por família com alta estatística** (10⁶ a 10⁷ amostras), comparando a taxa de supressão por fase com a taxa de crescimento da entropia de cada família.
- **(iii) Só depois, a pergunta com pesos complexos.**

## (c) Perfil de intervalos: quem participa da soma na janela? (O, n = 8 a 10)

**Método.**

- Cada classe exata foi classificada pelo centroide mais próximo do perfil (N₀, N₁, N₂, N₃, R₄₊)/C(n, 2) e da altura/n.
- Os centroides vêm de 4000 ordens sorteadas em diamantes de d = 2, 3 e 4 e em 3 camadas.
- A participação de cada grupo em 𝒵(θ) é Re(𝒵_grupo·𝒵̄)/|𝒵|². As participações somam 1.

**Resultado:**

- **O grupo com perfil de 4 dimensões está praticamente vazio:** peso ≤ 0,001 sem fases e participação ≈ 0 em toda a janela. Na população oficial ele é vazio.
- **As outras participações oscilam enormemente ao longo da janela.** Em n = 10, a do grupo de 3 camadas vai de −40 a +47, e as médias ficam em +1,00 (perfil de 2 dimensões), +0,09 (3 camadas) e −0,08 (3 dimensões).
- **A soma na janela é um resto de cancelamentos entre grupos, que muda de θ para θ.** Não há seleção estável de nenhum perfil.

**Conclusão de (a) e (c).** Em n ≤ 10, e também pela coerência em n ≤ 80, **não há sinal de dimensão emergente na janela**. A forma da pergunta precisa mudar: na janela, quem decide é a aritmética fina da ação, não a "forma" das ordens.

## (b) O resto do caráter D (D, com V para n ≤ 10)

**Fato novo, demonstrado e verificado (n = 3 a 10):** as ordens com **maior** elemento contribuem para D_n com exatamente **−n·Â_{n−1}[(0,1,1,1)]**.

- A prova é a mesma do ponto embaixo: w_D(P ⊕ {⊤}) = −s(P)(−1)^{D+M+U}.
- O caráter (0,1,1,1) vale 1, 3, 1, −13, −859, −4.461, −158.815, −235.453, +56.709.805 e −1.618.231.837 para n = 1 a 10. Ele é **irregular**.

**Isto localiza a irregularidade:**

- o ponto embaixo **propaga** o padrão de D (−n·D_{n−1});
- o ponto em cima **importa** um caráter irregular.

**Decomposição do resto** (sem menor, sem isolado e sem maior elemento), com o sinal em relação a (−1)^n:

- **parte paralela sem pontos isolados:** sempre com o sinal de D, em todo n de 4 a 10;
- **parte série sem extremos:** com o sinal de D, exceto em n = 7;
- **parte de raiz prima:** irregular (contra em n = 5 e 6, a favor de n = 7 a 10).

| n | D_n | menor | isolado | maior sem menor | paralelo s/ isolado | série s/ extremos | raiz prima |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | +6.150.803 | +1.608.216 | +1.209.461 | +1.520.336 | +949.340 | +413.378 | +450.072 |
| 9 | −160.741.231 | −55.357.227 | −49.352.971 | +13.553.757 | −18.013.968 | −12.014.382 | −39.556.440 |
| 10 | +4.497.486.319 | +1.607.412.310 | +1.351.610.641 | −545.907.280 | +645.778.980 | +152.015.148 | +1.286.576.520 |

**Leitura:** a regularidade de D vem dos mecanismos de composição (ponto embaixo, pontos isolados, componentes disjuntas). A irregularidade entra por dois caminhos: o ponto em cima, que traz o caráter (0,1,1,1), e a parte de raiz prima. Não há demonstração de dominância.
