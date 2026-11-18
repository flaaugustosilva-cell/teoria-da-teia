# Quantas vibrações cabem num pedaço de espaço-tempo?

Flavio Augusto da Silva · estudante de Licenciatura em Ciências da Natureza (Faculdade SESI-SP de Educação, em curso) · 18/11/2026

Versão em linguagem simples da nota [NOTA_ANTICADEIA.md](NOTA_ANTICADEIA.md). As contas foram feitas com a ajuda de um assistente de IA (Claude) e ainda não foram revisadas por especialistas.

## O cenário

Uma das ideias para unir a relatividade e a física quântica diz que o espaço-tempo não é liso: ele é feito de "grãos", pontos ligados por relações de antes e depois, como uma teia. Na física isso se chama teoria dos conjuntos causais.

Numa teia assim dá para colocar um campo, por exemplo algo parecido com a luz, e medir quanta informação uma região compartilha com o resto. Essa medida se chama entropia de emaranhamento.

## O problema

A física de buracos negros indica que essa entropia deveria crescer com a **área** da borda da região. Feita a conta direto na teia, porém, ela cresce com o **volume**: dá informação demais.

A explicação é que a teia permite vibrações mais finas do que os próprios grãos, e essas vibrações não são físicas. Os pesquisadores resolvem isso cortando as vibrações mais finas. A questão é onde cortar:
- num espaço-tempo de 2 dimensões (uma de espaço e uma de tempo), existe uma fórmula para o corte;
- em 3 e 4 dimensões, o ponto de corte é escolhido olhando os gráficos, "a olho".

## A ideia

Contar quantas vibrações são reais olhando só para a teia, sem escolher nada à mão. A regra proposta é:

> **Contam tantas vibrações quantos grãos tem a maior "camada" da região, isto é, o maior grupo de grãos em que nenhum vem antes ou depois de outro.**

Os matemáticos chamam essa camada de **maior anticadeia**. Ela funciona como um retrato do espaço num instante: são grãos que estão "lado a lado".

## O que os testes mostraram

**Em 2 dimensões, a regra acerta.** Ela guarda praticamente o mesmo número de vibrações que a fórmula usada pelos pesquisadores:

| Grãos na teia | Pela regra | Pela fórmula dos pesquisadores |
| --- | --- | --- |
| 1000 | 58 | 62 |
| 2000 | 82 | 88 |
| 4000 | 122 | 125 |

Isso não é sorte. Os dois números crescem como 2 × √(número de grãos). No caso da camada, isso vem de um teorema de matemática de 1977, sobre ordenar números ao acaso. Com a regra, a entropia passa a crescer do jeito que a teoria prevê.

**Em 3 dimensões, chega perto, mas não decide.** Com teias de até 4 mil grãos, a entropia cresce quase como a área. Com até 24 mil grãos, rodados num computador gratuito na nuvem, os dados servem tanto para "cresce como a área" quanto para "cresce um pouco mais rápido". Para decidir seriam necessárias teias muito maiores.

**Em 4 dimensões (o nosso espaço-tempo), ainda não funciona como esperado.** As teias que deu para simular são pequenas demais para o teste valer.

## O que é novo e o que não é

Já se sabia que, em 2 dimensões, o corte guarda "da ordem de √N" vibrações. O que parece novo é dizer exatamente quantas, a maior camada, e usar isso como regra em qualquer dimensão, sem ajustar nada. Não encontrei isso publicado, mas a busca foi limitada e pode já existir.

## Por que isso importa

Se a regra se confirmar, ela mostra que o número de "graus de liberdade" de um pedaço de espaço-tempo pode ser lido direto na estrutura dos grãos, sem nenhum número escolhido de fora. É uma peça pequena, mas está no caminho de explicar a entropia dos buracos negros a partir de algo mais fundamental.

## Para reproduzir

Os programas estão na pasta [`scripts`](scripts/) deste repositório. Basta ter Python com `numpy` e `scipy` instalados.
