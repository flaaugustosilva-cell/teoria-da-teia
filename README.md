# Teoria da Teia — Estado atual

Atualizado em 17/11/2026 · Flavio

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
3. **As janelas de supressão com três camadas.** Falta saber se valem para as teias mais comuns, com a ação completa.
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

Cuidados: os nats por molécula mudam entre as duas regiões; poucas realizações; 3+1 não testado. A escala usada (N^((d−1)/d)) já existe na literatura com coeficiente escolhido à mão (Surya, X e Yazdi, arXiv:2008.07697); fixá-lo pela maior anticadeia pode ser próprio.

**Próximo passo:** explicar a diferença entre as regiões (correção de curvatura da borda) e testar em 3+1, que decide a hipótese das espécies.

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
