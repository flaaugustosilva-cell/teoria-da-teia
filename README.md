# Teoria da Teia — Estado atual

Atualizado em 18/11/2026 · Flavio Augusto da Silva

**Nota sobre a regra da maior anticadeia:** [versão acadêmica](NOTA_ANTICADEIA.md) · [versão em linguagem simples](NOTA_ANTICADEIA_SIMPLES.md)

Este é o resumo vivo da teoria. Os resultados vêm de simulações em Python que estão na pasta [`scripts`](scripts/), cada uma com instruções de uso no topo do arquivo.

## A teoria em poucas linhas

O espaço-tempo é uma teia de nós ligados por relações de antes e depois. A teia tem duas faces: a **ordem**, de onde vem o tempo, e o **corte**, de onde vem a entropia. Desde 13/11/2026 a teia descreve só a gravidade, e o objetivo é unir relatividade geral e mecânica quântica. Na linguagem da física, é a abordagem dos conjuntos causais (causal sets).

Para virar teoria completa faltam cinco peças: uma lei de crescimento da teia; uma quântica da teia (peso para cada teia possível); a matéria mudando a teia; a relatividade geral completa saindo da regra; e uma previsão própria.

## O que está estabelecido

Resultados conferidos com três tamanhos de teia e mais de uma realização. A maioria reproduz a literatura; os marcados como próprios não foram vistos publicados nas fontes lidas.

| Resultado | Número | Origem |
| --- | --- | --- |
| Limite do grão pelos dados de Lee 2020 | R₀ ≤ 34 µm (95%) | ajuste próprio |
| Moléculas de horizonte seguem a área (2+1 e 3+1) | coeficientes 0,219 e 0,1745 | reproduz Barton e outros (2019) |
| A contagem segue a área também na fusão de dois horizontes | razão 0,21 a 0,27 (teoria 0,219) | teste próprio (`fusao_horizontes.py`) |
| Supressão quântica das teias de duas camadas é em janelas | janela 1: grão 5,7 a 8,1 l_P (α 0,0077 a 0,0155) | soma exata própria (`janelas_supressao.py`, `camadas_variaveis.py`); condição de Loomis e Carlip |
| Tensão entre entropia e supressão | grão da entropia 0,83 l_P, abaixo da janela; faltam ~47 nats por molécula | comparação própria |
| Tensão entre entropia e Λ flutuante | densidade ~10⁴ vezes diferente | comparação própria |
| Corte pela maior cadeia acerta o caso 1+1 sem ajuste | entropia logarítmica, inclinação 0,25 | regra própria (`corte_cadeia.py`) |
| Começo pequeno: no tempo de Planck a radiação quase satura a entropia máxima | razão 0,62, caindo como t^(−1/2) | reproduz Layzer, Frautschi (`comeco_pequeno.py`) |

## O que caiu

Ideias testadas e refutadas. Ficam registradas para não serem repetidas.

| Ideia | Por que caiu |
| --- | --- |
| Grão como √(l_P·R_H) | refutada pelo limite de Lee 2020 |
| Λ flutuante (Modelo 1) explica a expansão | 0 histórias aceitáveis em 2,36 milhões contra BAO + supernovas |
| Memória de Λ sobre os nós salva o modelo | acerta dados tardios, falha na radiação de fundo e na nucleossíntese |
| Regras locais de crescimento (reflexões 3 a 6) | dão árvore ou escada; dependem da ordem de nascimento |
| Bônus de diamantes vazios no peso (reflexão 7) | o máximo é uma pilha de três camadas |
| Assinatura de intervalos como peso (reflexão 8) | em teias gerais acerta a vizinhança e erra a escala grande |
| Invariância por dizimação (reflexão 9) | aceita teias demais (fila, camadas cheias, teia vazia) |
| Corte "de Chladni" por dizimação (reflexão 11) | em 1+1 dá lei de volume (N^0,72) |
| Picos da soma de histórias como régua (reflexão 13) | o número de picos vem da massa posta à mão, não da teia (`picos_feynman.py`) |
| Corte "cadeia × camadas" com constante fixa | falha em 1+1 (`corte_camadas.py`) |

## Problemas abertos

O nó central é o corte: quantas vibrações de um campo contam como entropia na teia. Ele decide os três primeiros itens ao mesmo tempo.

1. **O corte da entropia de emaranhamento.** Precisa sair das relações da teia, sem número ajustado, e dar lei de área em 1+1, 2+1 e 3+1. Candidata atual: a maior anticadeia (abaixo).
2. **Os 47 nats por molécula.** Hipótese em aberto: seriam a soma das ~49 espécies de partículas do Modelo Padrão. Testável só quando o corte estiver fixado em 3+1.
3. **As janelas de supressão com três camadas.** Resolvido na literatura no essencial: as teias em camadas, inclusive as mais comuns (Kleitman–Rothschild), são suprimidas com a ação completa sempre que o grão está acima de um limiar (Mathur, Singh e Surya 2020; Carlip e Carlip 2022; arXiv:2311.18238). Atualização (18/11): a condição de 2311.18238 (eq. 5) é tan[½β(ℓ/ℓ_p)²] > 1,76, escrita sem valor absoluto, e os autores a leem como um limiar (ℓ > 1,136 ℓ_p). A nossa soma exata (n = 400) mostra supressão em toda a faixa β ≈ 1,05 a 2,09, sem mudar nada ao passar de 90°, e o fim dela fora disso. A condição deles só cobre a primeira metade da janela; a versão correta é com |tan|, e a janela 1 vai de 1,133 a 1,60 ℓ_p. A borda de baixo coincide com a deles; a de cima e a existência de outras janelas não estão no artigo. Soma exata de 3 camadas (n = 9, 12 e 13, scripts/tres_camadas.py): a supressão também é simétrica em torno de 90° (confirma o |tan|), é mais forte dentro da janela 1 e cresce com n a um ritmo parecido com o de 2 camadas; n ainda é pequeno demais para ver as bordas.
4. **Escolher a dimensão (peça 2).** Nenhum peso sem alvo posto à mão produz espaço-tempo em teias gerais.
5. **A matéria mudando a teia (peça 3).** Nada feito; necessária para ver estrutura se formar.
6. **Uma previsão própria (peça 5).** Candidata fraca: α de Λ dentro da janela 1 (0,0077 a 0,0155); hoje não testável.

## Último resultado e próximo passo

Regra do corte pela maior anticadeia (17/11): em cada região, contam tantas vibrações quantos nós tem o maior conjunto de nós sem relação entre si (a camada mais larga). Sem nenhum número ajustado, é a primeira regra que passa em 1+1 e em 2+1 (`corte_anticadeia.py`).

| Teste | Resultado | Esperado |
| --- | --- | --- |
| 1+1 | entropia logarítmica, inclinação 0,171 | 0,167 |
| 2+1, região pequena | cresce como N^0,28; ~7,5 nats por molécula | lei de área: N^0,33 |
| 2+1, região maior | cresce como N^0,31; ~4,2 nats por molécula | lei de área: N^0,33 |

**Em 3+1 (17/11, noite, revisado):** com mais rodadas e moléculas contadas na teia, um campo escalar deixa de **5 a 9 nats por molécula** (média ~6), e a entropia cresce como N^0,58 a 0,68 (lei de área: N^0,50). Com até 4000 nós a região interna é pequena demais e o corte quase não age nela; o regime certo não é alcançável nem aqui nem no PC do autor. Com as ~49 espécies, o grão sairia entre ~13 e ~18 l_P, faixa que cobre várias janelas e intervalos: inconclusivo. A contribuição de férmions não pode ser calculada: não há formulação aceita de espinores em conjuntos causais (`anticadeia_dimensoes.py`).

Cuidados: os nats por molécula mudam entre as duas regiões; poucas realizações; 3+1 não testado. A escala usada (N^((d−1)/d)) já existe na literatura com coeficiente escolhido à mão (Surya, X e Yazdi, arXiv:2008.07697); fixá-lo pela maior anticadeia pode ser próprio.

**Resultado de 17/11 à noite (2+1, três regiões, 6 a 8 rodadas):** a ideia de uma "constante de ~15 nats" caiu: a região média dá a mesma entropia que a maior, porque o diamante grande é finito e a região maior já sente o lado de fora. Medindo como S cresce com N numa região fixa, um campo escalar em 2+1 deixa ~5 a 7 nats por molécula (erro de 15% a 20%), não firme. Para firmar seria preciso uma região muito menor que o diamante grande, o que exige teias bem maiores que 4000 nós.

**Próximo passo:** levar o cálculo a teias maiores (dezenas de milhares de nós), com um método que não guarde a matriz inteira, ou registrar a regra da anticadeia como resultado parcial.

**Teias grandes (17/11, noite):** um método novo (`grande.py`) calcula só as vibrações que a regra guarda e chega a 16 mil nós em 2+1. Ele bate com o método antigo em 4 mil nós (1% a 2%), mas em 12 mil nós superestima a entropia em ~8% com o ajuste padrão (`convergencia.py`). Os resultados grandes já obtidos (crescimento ~N^0,45) estão inflados por esse erro e ainda não valem. Próximo: refazer com o ajuste mais preciso.

**Kaggle, 2+1 até 24 mil nós (18/11):** com o método rápido validado (erro de 0,1% contra o exato em 8 mil nós), a entropia cresce como N^0,42 a 0,48 se ajustada como potência, acima da lei de área (0,33). Mas uma lei de área com uma constante negativa ajusta igualmente bem, e aí o coeficiente fica em ~10 a 12 nats por molécula, coerente nas três regiões. Com 4 tamanhos de teia não dá para separar as duas leituras; seriam precisas teias de 100 mil nós ou mais. A regra não foi refutada nem confirmada em 2+1 (`analise_kaggle.py`).

**Maior anticadeia mais rápida (18/11):** calculada como fluxo sobre as ligações diretas (`largura_fluxo.py`), em vez de emparelhamento sobre todas as relações. Resultado idêntico em 1, 2, 4 e 8 mil nós; com 16 mil nós leva 35 s, contra 4 a 46 min antes. `grande2.py` junta isso ao método rápido e reproduz exatamente as rodadas anteriores. Próximo: teias de 32 e 48 mil nós no Kaggle.

**Comparação com a literatura (18/11):** em 1+1 a regra guarda praticamente o mesmo número de vibrações que o corte escolhido à mão por Sorkin e Yazdi (58 / 82 / 122 contra 62 / 88 / 125), e os dois tendem a 2√N. A regra explica por que aquele corte funciona e o generaliza sem parâmetro. Em 2+1 ela implica uma constante de corte c₃ ≈ 0,14 a 0,17, subindo devagar; em 3+1 a constante implicada triplica entre 1000 e 4000 nós, então ali a regra não equivale a um corte fixo. Os valores usados na literatura em 3D e 4D não foram publicados (`joelho.py`, `c_implicito.py`).

**Busca na literatura (18/11):** que o corte de 1+1 guarda ~√N modos já era conhecido. Nas fontes lidas, ninguém identifica esse número com a maior anticadeia nem propõe a largura como regra de corte sem parâmetro em qualquer dimensão. Isso não prova ineditismo. O que pode ser novo: o coeficiente (os dois dão 2√N) e a forma intrínseca, sem coordenadas.

## Regras de trabalho

- Todo número é repetido com três tamanhos de teia e mais de uma realização.
- Coincidência com um número da fórmula é alerta, não resultado.
- Antes de chamar algo de novo, procura-se na literatura.
- Textos de autoria desconhecida, inclusive de outras IAs, são ideias a testar, nunca apoio.

## Como rodar os scripts

Precisa de Python 3 com `numpy` e `scipy` (e `mpmath` para `camadas_variaveis.py` e `camadas_absoluto.py`):

```
pip install numpy scipy mpmath
cd scripts
python corte_anticadeia.py 2
```

Os scripts usam uns aos outros; rode-os de dentro da pasta `scripts`.

As contas e simulações foram feitas com a ajuda de um assistente de IA (Claude). O histórico completo, com todas as correções, fica num registro privado do autor.
