# Cota inferior para |𝒵_boa| — primeira exploração (fora de registro)

Flavio Augusto da Silva · 20/11/2026 (Brasília). Exploratório: nenhum critério foi fixado antes, e nada aqui é teste de hipótese.

## Pergunta

Alguma subclasse de teias boas domina 𝒵_boa na janela, de modo que uma cota inferior para ela bastasse?

## Método

Decomposição exata de 𝒵_boa (n = 5 a 10, peso 1/|Aut|, 4.001 ângulos na janela) por altura e por número de elementos minimais. Para cada ângulo, compara-se |𝒵_boa| com a soma dos módulos das partes: o valor 1 significa nenhum cancelamento entre as partes. Código: `scripts/h1b_N_decomposicao.py`; saída: `n9n10/exploratorio_decomposicao.txt`.

## Resultado

| n | min \|𝒵_boa\| | Sobra por altura (mediana / mínimo) | Sobra por minimais (mediana / mínimo) |
| --- | --- | --- | --- |
| 5 | 0,252 | 0,61 / 0,122 | 0,92 / 0,415 |
| 6 | 1,797 | 0,57 / 0,097 | 0,89 / 0,230 |
| 7 | 2,581 | 0,58 / 0,205 | 0,83 / 0,102 |
| 8 | 0,616 | 0,50 / 0,006 | 0,70 / 0,009 |
| 9 | 23,41 | 0,57 / 0,089 | 0,80 / 0,069 |
| 10 | 151,4 | 0,62 / 0,035 | 0,81 / 0,090 |

- Nenhuma altura e nenhum número de minimais domina: as partes maiores ficam em torno de 30% a 40% da soma dos módulos.
- **Os mínimos de |𝒵_boa| vêm de cancelamento entre as partes.** Em n = 8, no ponto de mínimo, as partes por altura (3 a 8) têm módulos 10,7 / 36,5 / 45,4 / 5,5 / 4,0 / 1, e somadas dão 0,62.
- A parte de altura n (só a cadeia) tem módulo exatamente 1 em todo n.

## O que isso diz sobre a estratégia

Uma cota inferior para uma subclasse não basta: as demais podem cancelar até ~99% da soma dos módulos em certos ângulos (n = 8). Uma demonstração de C1, ou de H1\*, para todo n precisa controlar esse cancelamento **entre** classes, que é uma propriedade global da soma. Nenhuma propriedade desse tipo foi identificada.
