# Uma regra sem parâmetro para o corte da entropia de emaranhamento em conjuntos causais

Flavio Augusto da Silva · estudante de Licenciatura em Ciências da Natureza (Faculdade SESI-SP de Educação, em curso) · 18/11/2026

Nota de trabalho, não revisada por especialistas. Contas e simulações feitas com a ajuda de um assistente de IA (Claude). Versão em linguagem simples: [NOTA_ANTICADEIA_SIMPLES.md](NOTA_ANTICADEIA_SIMPLES.md).

## A pergunta

Num conjunto causal, a entropia de emaranhamento de Sorkin de um campo escalar no vácuo de Sorkin–Johnston segue lei de volume. Ela só passa a seguir lei de área depois de um corte duplo no espectro do operador de Pauli–Jordan iΔ (Sorkin e Yazdi, arXiv:1611.10281). Em 1+1 o corte é λ_min = √N/(4π). Em 2+1 e 3+1 ele é escrito como λ_min = c_d·V^(2/d−1)·N^(1−1/d), com a constante c_d escolhida olhando o espectro (Belenchia e outros, arXiv:1712.04227); os valores de c_3 e c_4 não foram publicados.

## A regra

Em cada região (o diamante grande e o diamante interno), guardar de cada sinal tantos autovalores de iΔ quantos elementos tem a **maior anticadeia** da região, isto é, a largura da ordem. A largura é intrínseca: não depende de coordenadas nem do espectro do contínuo, e não tem parâmetro livre.

## Resultados

**1+1: a regra coincide com o corte de Sorkin–Yazdi.** Duas teias por tamanho:

| N | Maior anticadeia | Modos guardados pelo corte √N/(4π) | 2√N |
| --- | --- | --- | --- |
| 1000 | 58 | 62 | 63 |
| 2000 | 82 | 88 | 89 |
| 4000 | 122 | 125 | 126 |

Os dois números tendem a 2√N. Num diamante 1+1 sorteado, ordenar os elementos por uma coordenada de cone de luz e ler a outra dá uma permutação aleatória uniforme; uma anticadeia é uma subsequência decrescente dessa permutação. O comprimento médio da maior subsequência crescente (ou decrescente) de uma permutação aleatória de N elementos é ~2√N (Vershik e Kerov, 1977; Logan e Shepp, 1977), com correção de ordem N^(1/6) (Baik, Deift e Johansson, 1999); as larguras medidas ficam um pouco abaixo de 2√N, como esperado de uma correção desse tamanho. A contagem do corte √N/(4π) também fica em ~2√N nos nossos dados. Com a regra, a entropia cresce como logaritmo, com inclinação 0,171 contra ln N; o valor teórico é 1/6 ≈ 0,167 (3 teias por tamanho, N de 500 a 2000).

**2+1: perto da lei de área, sem decisão final.** Até 4 mil nós, a entropia cresce como N^0,28 a 0,31 (lei de área: N^0,33). Até 24 mil nós (método aleatorizado com erro de 0,1%, validado contra o exato em 8 mil), uma potência livre dá N^0,42 a 0,48, mas uma lei de área com constante negativa ajusta igualmente bem, com ~10 a 12 nats por molécula de horizonte, coerente em três regiões. A constante de corte que a regra implica sobe devagar: c_3 ≈ 0,14, 0,16 e 0,17 em 1, 2 e 4 mil nós.

**3+1: não corresponde a um corte fixo nesses tamanhos.** A constante implícita c_4 vale 0,009, 0,017 e 0,029 em 1, 2 e 4 mil nós. A entropia cresce como N^0,58 a 0,68 (lei de área: N^0,50), com a região interna pequena demais para o corte agir de fato.

## O que já era conhecido

Que o corte de 1+1 corresponde a guardar ~√N modos, motivado pelo comprimento de onda mínimo do grão (tese de Nomaan X, arXiv:2105.07241; Belenchia e outros). Nas fontes lidas não encontrei a identificação desse número com a maior anticadeia, nem a largura proposta como regra de corte em qualquer dimensão. A busca foi limitada e não prova ineditismo. Segunda busca (18/11): Surya, X e Yazdi (arXiv:2008.07697) já motivaram o corte pela ideia de que o número de modos deve ser proporcional ao volume espacial de uma hipersuperfície de Cauchy, mas estimaram esse volume pelo contínuo, e em de Sitter o valor ficou grande demais; a maior anticadeia já é conhecida como o análogo de Cauchy (Belenchia e outros 2017; Yazdi 2022). Medir a largura da própria teia (Dilworth) e usá-la como número de corte não apareceu. Avaliação: provavelmente inédito como procedimento, mas muito próximo de ideias publicadas; o teste decisivo é de Sitter.

## Limites

- Peso das conclusões em 2+1 e 3+1 limitado pelo tamanho das teias (até 24 mil e 4 mil nós).
- Em 3+1 a regra não se comporta como um corte de constante fixa; pode ser efeito de tamanho ou um afastamento real.
- Só campo escalar sem massa, espaço plano.

## Como reproduzir

Scripts na pasta [`scripts`](scripts/): `corte_anticadeia.py` (regra em 1+1 e 2+1), `joelho.py` (comparação com o corte de Sorkin–Yazdi), `c_implicito.py` (c_d implícito), `largura_fluxo.py` (largura por fluxo sobre as ligações, idêntica ao emparelhamento e muito mais rápida), `grande2.py` (teias grandes), `analise_kaggle.py` (rodadas de até 24 mil nós).

## Perguntas para quem conhece a área

1. A identificação "modos guardados = maior anticadeia" já aparece em algum trabalho?
2. Qual c_3 e qual c_4 foram usados em arXiv:1712.04227, para comparar com 0,17 e 0,03?
3. Há razão para esperar que a largura deixe de acompanhar o corte certo em 3+1?


## Teste em de Sitter 1+1 (18/11)

Fatia |T| < 1,2, cunha tipo Rindler, 3 rodadas por N (scripts/ds2_anticadeia.py). Sem corte, S cresce como N^1,02 (lei de volume). Com a regra da largura, S = 2,31 / 2,66 / 2,98 / 3,39 para N = 500 / 1000 / 2000 / 3000: crescimento logarítmico, que é a forma da lei de área em 1+1, sem nenhum parâmetro ajustado. Mas a inclinação contra ln N é 0,57, contra 1/6 = 0,167 esperado para duas pontas: a regra guarda modos demais, o mesmo defeito que Surya, X e Yazdi acharam na estimativa pela fatia espacial. Em de Sitter, a regra acerta a forma e erra o coeficiente.
