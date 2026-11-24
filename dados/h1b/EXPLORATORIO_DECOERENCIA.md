# Exploração (fora de registro): a dimensão está nas teias ou emerge da interferência entre elas?

Data: 24/11/2026. Script: `scripts/h1b_decoerencia.py` (e os dois controles registrados na saída). Saída: `decoerencia.txt`. Janela θ ∈ [2π/3, π], ação de 4 dimensões, n = 8 a 10. Nada foi registrado como conjectura.

## 0. Formalismo

A pergunta do Flavio (inspirada no experimento de escolha retardada de Wheeler) é se a dimensionalidade é:

- **Modelo A:** uma propriedade de cada teia;
- **Modelo B:** uma propriedade que só aparece na combinação com fases.

Na teoria de conjuntos causais, a soma 𝒵 = Σ w·e^{iθB} é uma soma de **amplitudes sobre histórias**, e existe um formalismo pronto para isso: a **medida quântica de Sorkin** (ver a revisão de Surya, Living Reviews in Relativity, 2019).

- **Uma propriedade é uma partição** das teias em classes A_g.
- **Cada classe tem amplitude** Z_g = Σ_{P ∈ A_g} w·e^{iθB}.
- **A matriz de decoerência** é D_gh = Z_g·Z̄_h. A soma de todas as entradas é |𝒵|².
- **"Antes" da combinação:** o peso clássico p_g = W_g/W.
- **"Depois" da combinação:** a medida quântica normalizada μ_g = |Z_g|²/Σ_h |Z_h|².
- **Índice de decoerência:** I = Σ_{g≠h} |D_gh| / Σ_g D_gg.
  - Se I ≪ 1, as classes não interferem, e a propriedade se comporta como "clássica" (Modelo A).
  - Se I ≳ 1, elas interferem, e a propriedade não é um atributo definido das teias.

Usei duas partições:

- **(1)** faixas de dimensão de Myrheim–Meyer;
- **(2)** o grupo de perfil de intervalos mais próximo: diamantes de 2, 3 e 4 dimensões, ou camadas.

As duas foram aplicadas a todas as ordens e à população oficial, com resultados quase idênticos.

## 1. As classes de dimensão interferem fortemente (O)

- **Índice de decoerência na janela:** mediana de 1,1 a 1,8, nunca abaixo de 0,15.
- **Cancelamento entre as classes:** |𝒵|² é só de 8% a 31% de Σ_g |Z_g|² (mediana). Há interferência destrutiva forte entre elas.

**Consequência:** na janela, "dimensão" **não** é uma propriedade decoerente. O Modelo A, uma dimensão intrínseca que se comporta classicamente, **não** é sustentado nesses tamanhos.

## 2. A combinação muda o perfil dimensional (O)

Faixas de Myrheim–Meyer, todas as ordens. Peso clássico → medida quântica (mediana na janela):

| faixa | n = 8 | n = 9 | n = 10 |
| --- | --- | --- | --- |
| d < 1,5 | 0,054 → 0,064 | 0,045 → 0,035 | 0,018 → 0,006 |
| 1,5 a 2,5 | 0,886 → 0,597 | 0,892 → 0,591 | 0,927 → 0,571 |
| **2,5 a 3,5** | **0,060 → 0,304** | **0,063 → 0,290** | **0,055 → 0,411** |
| 3,5 a 4,5 | 0,0002 → 0,0001 | 0,0000 → 0,0000 | 0,0000 → 0,0000 |

- A classe com cara de **3 dimensões** passa de cerca de 5% do peso para 29% a 41% da medida quântica.
- A partição por perfil de intervalos mostra o mesmo deslocamento. Por exemplo, em n = 9 o grupo "d = 3" passa de 0,039 para 0,450.

**Ressalva:** como as classes interferem (item 1), μ **não** é uma probabilidade. A variação ao longo da janela também é enorme: de 0,0002 a 0,91 em n = 10.

## 3. Controle: é só efeito de tamanho? (O)

Uma classe pequena cancela menos as suas próprias fases, só por ter menos membros. Para separar esse efeito, comparei a coerência interna |Z_g|/W_g de cada faixa com a de **subconjuntos aleatórios de classes com o mesmo peso** (20 sorteios por caso):

| faixa | n = 8 | n = 9 | n = 10 |
| --- | --- | --- | --- |
| d < 1,5 | 1,8 | 1,7 | 1,9 |
| 1,5 a 2,5 | 1,9 | 1,6 | 2,1 |
| **2,5 a 3,5** | **2,8** | **3,6** | **6,0** |

Os valores são a razão real/aleatório. O intervalo dos sorteios aleatórios não chega perto dos valores reais da faixa de 2,5 a 3,5.

- **Toda classe definida por estrutura** é cerca de 2 vezes mais coerente que um subconjunto aleatório. Isso é esperado, porque agrupar teias por qualquer característica ligada à ação reduz o embaralhamento das fases.
- **A faixa de 3 dimensões fica bem acima disso, e o excesso cresce com n.** As outras ficam estáveis em torno de 2.

**Leitura (O):** é o primeiro sinal, ainda em tamanhos pequenos, de que a interferência **favorece um perfil dimensional mais alto** do que a contagem simples. As teias com cara de 3 dimensões cancelam menos entre si do que o esperado pelo tamanho da classe, e a vantagem aumenta com n. As de 4 dimensões não aparecem porque quase não existem para n ≤ 10.

## 4. O que o Modelo B pode e não pode ser (D)

**Para partições, o Modelo B estrito é impossível.** A medida de uma classe é μ(A) = |Z_A|² ≤ W_A², então uma classe sem membros tem medida zero. Uma "dimensão 4" que nenhuma teia possui não pode aparecer como peso de uma classe.

**Valores coletivos só aparecem em observáveis que não são partições,** como a média complexa ⟨r⟩_θ = Σ w e^{iθB} r / 𝒵. Ela **sai** do intervalo físico [0, 1] em 2% a 5% da janela (n = 8 e 10; Re⟨r⟩ chega a −4,0 e a +1,9). É análogo aos "valores fracos" anômalos da mecânica quântica. Sem decoerência, esses valores **não** têm leitura de dimensão física.

## 5. Resumo

| Pergunta | Resposta em n ≤ 10 |
| --- | --- |
| A dimensão é atributo decoerente das teias (Modelo A)? | Não: as classes interferem fortemente. |
| A combinação favorece uma assinatura rara individualmente? | Sim, a de cerca de 3 dimensões, com excesso de coerência que cresce com n (2,8 → 3,6 → 6,0). |
| A combinação produz 4 dimensões sem teias de 4 dimensões? | Impossível para classes. Só observáveis de interferência "anômalos", sem leitura física. |

**Limitações:**

- n é pequeno;
- o estimador de Myrheim–Meyer confunde ordens em camadas com 2 dimensões;
- usei medianas ao longo da janela;
- o crescimento do excesso foi visto nos mesmos dados que o sugerem, então ele **não é um teste**.

**Teste independente possível:** n = 11, gerando de novo as ordens com o genposetg (cerca de 2 horas), com pré-registro **antes**.

## 6. Precisões depois da revisão do Flavio (24/11/2026)

1. **Formulação da conclusão do item 1.** Onde está escrito que "dimensão não é atributo definido das teias", vale esta formulação mais precisa:

   > Para n = 8 a 10, na janela e nas partições estudadas, a dimensão não se comporta como uma propriedade clássica decoerente da soma de histórias.

   Cada teia continua pertencendo a uma classe bem definida pelo estimador. O que falha é a leitura clássica, aditiva, da soma dessas classes.
2. **μ_g não é medida quântica normalizada da partição.** μ_g = |Z_g|²/Σ_h |Z_h|² é a distribuição normalizada das contribuições **diagonais**. Como há interferência, ela não é probabilidade nem medida da partição. Isso vale sempre que os valores de 29% a 41% forem citados.
3. **O índice I** mede a magnitude dos termos fora da diagonal em relação à diagonal. É um indicador de interferência, não um critério universal de decoerência.
4. **Auditoria do controle.** O controle por subconjuntos aleatórios tinha sido rodado num comando avulso. Agora ele está congelado em `scripts/h1b_decoerencia.py` (funções `razoes_controle` e `reproduz_n8_10`). Com a mesma semente e a mesma ordem, ele reproduz exatamente os valores antes relatados (`decoerencia_controle_reproduzido.txt`): **R₃ = 2,817, 3,572 e 6,044** para n = 8, 9 e 10.
5. **Incerteza do controle.** Com outra semente e outra ordem das classes, o mesmo cálculo em n = 8 dá 2,905 em vez de 2,817. A razão tem incerteza de alguns por cento, que vem da mediana de 20 sorteios.
