# Exploração (fora de registro): as teias que dominam "parecem" ter que dimensão?

Data: 21/11/2026. Script: `scripts/h1b_dimensao.py`. Saída: `exploratorio_dimensao.txt`.

**Motivo.** Na teoria, o tempo deveria emergir da ordem das relações. Mas a formulação atual supõe 3+1 em dois lugares: no critério de teia boa e nos coeficientes da ação. Aqui pergunto se a soma com fases, **sozinha**, favorece teias cuja estrutura interna se parece com a de 4 dimensões.

## Fato prévio

Para n ≤ 10, o filtro "cabe em 3+1" não eliminou **nenhuma** teia, porque todas as de altura ≥ 3 cabem (certificado). Nos resultados até n = 10, o critério de teia boa já era só a altura, que é interno à teia. **A dimensão entrava apenas pelos coeficientes da ação.**

## Método

- **Medida interna de dimensão.** Usei a fração de ordenação r = (pares comparáveis)/C(n, 2) e a dimensão de Myrheim–Meyer d_MM, que resolve f(d) = r, com f(d) = Γ(d+1)Γ(d/2)/(2Γ(3d/2)).
  - Para pontos ao acaso num diamante causal de Minkowski, o valor esperado de r é f(d): 1/2 em d = 2, cerca de 0,229 em d = 3 e 0,1 em d = 4.
- **Ações** (Dowker–Glaser, arXiv:1305.2588), na convenção N₀ = elos:
  - d = 4: n − N₀ + 9N₁ − 16N₂ + 8N₃, a que já usávamos;
  - d = 2: n − 2N₀ + 4N₁ − 2N₂.

  Os coeficientes de d = 3 não foram usados, porque o texto da fonte veio corrompido na leitura.
- **Média com fases** de um observável: ⟨r⟩_θ = Σ w e^{iθB} r / Σ w e^{iθB}.
- **Participação de cada faixa de dimensão em 𝒵(π):** Re(𝒵_faixa · 𝒵̄)/|𝒵|². As participações somam 1.

## Resultados (n = 6 a 10, todas as ordens e população oficial; as duas dão quase o mesmo)

**1. Sem fases, as ordens pequenas "parecem" 2-dimensionais.** ⟨r⟩₀ fica entre 0,50 e 0,58, o que dá d_MM entre 1,8 e 2,0. Em n = 10, 93% do peso está na faixa de 1,5 a 2,5 dimensões.

É o efeito das ordens em poucas camadas: a sua fração de ordenação fica perto de 1/2 **por acaso**. Por isso este estimador, sozinho, **não distingue** uma ordem em camadas, que não se parece com nenhum espaço-tempo, de um espaço-tempo de 2 dimensões.

**2. Ordens com cara de 4 dimensões praticamente não existem nesses tamanhos.** A faixa de 3,5 a 4,5 dimensões tem peso relativo ≤ 3×10⁻³ em todo n. Em n = 8 são 29 classes (2,3×10⁻⁴ do peso), e só 4 delas têm altura ≥ 3.

**3. Com a ação de 4 dimensões, a janela não seleciona 4 dimensões.**

- **Centro da janela:** Re⟨r⟩_π fica entre 0,76 e 0,93. Isso corresponde a ordens **mais** ordenadas, mais próximas de cadeias (d_MM < 1,5), e não a 4 dimensões.
- **Ao longo da janela:** ⟨r⟩_θ oscila sem controle, por exemplo de −0,76 a +1,06 em n = 10. Na janela, |𝒵| é pequeno (cerca de 4×10⁻⁴ de W em n = 10), e a "média" com pesos complexos é a razão entre dois números pequenos. Ela **não** tem leitura de dimensão.
- **Participação em 𝒵(π), n = 10:** d < 1,5: +1,26; de 1,5 a 2,5: −5,23; de 2,5 a 3,5: +4,98; de 3,5 a 4,5: −0,01. O resultado é um cancelamento grande entre as faixas de 2 e de 3 dimensões, e a faixa de 4 dimensões não participa.
- **O θ em que ⟨r⟩ chega perto de 0,1** muda sem padrão de um n para outro (0,18 a 0,92). Não há sinal estável.

**4. A ação de 2 dimensões não serve como controle nestes tamanhos.**

- Todos os coeficientes dela são pares. Então e^{iθ(B−n)} tem período π, e θ = π dá peso igual a todas as ordens (confirmado: B − n é sempre par).
- Sem fases, r já vale cerca de 1/2. Assim o controle "a ação de 2 dimensões favorece r = 1/2" é **trivial** e não informa nada.

## Conclusão (O)

**Em n ≤ 10, não há sinal de que a ação de 4 dimensões selecione, por si só, teias com estrutura de 4 dimensões.** O teste também **não tem poder** nesses tamanhos, por três motivos:

- (a) quase não existem ordens com fração de ordenação de 4 dimensões;
- (b) na janela, a soma é um resto de cancelamentos, e a média com fases deixa de ser uma "dimensão típica";
- (c) a fração de ordenação confunde ordens em camadas com 2 dimensões.

Isso **não refuta** a ideia de dimensão emergente. Mostra que ela não pode ser testada com enumeração exata em n ≤ 11.

## O que seria preciso

- **Tamanhos muito maiores,** de dezenas a centenas de elementos. A literatura de conjuntos causais em 2 dimensões trabalha nesse regime, com amostragem de Monte Carlo e ação continuada para pesos reais. Aqui a soma tem fases e enfrenta um problema de sinal, então isso exige um projeto próprio.
- **Mais de um estimador de dimensão** (abundância de intervalos, escala do ponto médio), para separar ordens em camadas de espaço-tempo.
- **Uma pergunta bem posta para pesos complexos:** comparar o perfil de intervalos dominante na janela com o de pontos sorteados em diamantes de 2, 3 e 4 dimensões, em vez de "médias" com fases.

Nada foi registrado como conjectura.
