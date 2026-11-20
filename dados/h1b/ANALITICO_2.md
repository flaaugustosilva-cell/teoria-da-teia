# Item 5 — argumento analítico para H1\*, parte 2

Flavio Augusto da Silva · 20/11/2026 (Brasília). Escrito durante o cálculo de n = 10, sem usar resultados de n = 9 ou 10.

## Teorema 1′ (cota fina, dependente de β) — demonstrado

**Enunciado.** Com q = 2|cos β| ≤ 1 (janela 1 fechada) e T(q) = Σ_{a=1..n} C(n, a)·[(1 + q^a)^(n−a) − 1]:

1 − T(q) ≤ |Z_rot,ruim| ≤ 1 + T(q)

Portanto |𝒵_ruim| ≤ (1 + T(q))/n!. Em β = π/2 (q = 0), T = 0 e |Z_rot,ruim| = 1 exatamente.

**Observação (do autor, 20/11/2026).** A cota inferior 1 − T(q) só informa algo quando T(q) < 1, ou seja, perto do centro da janela (q pequeno, n não muito grande). Quando T(q) ≥ 1, ela é trivial. A parte usada para H1\* é a cota superior.

**Demonstração.** Da fórmula do Teorema 1, Z_rot = e^(iμn)·Σ_{a≥1} C(n, a)·(y^a − 1)^(n−a), com |y| = q. Expandindo (y^a − 1)^(n−a) = Σ_k C(n−a, k)·y^(ak)·(−1)^(n−a−k), os termos com k = 0 somam Σ_{a≥1} C(n, a)(−1)^(n−a) = (1 − 1)ⁿ − (−1)ⁿ = −(−1)ⁿ, que tem módulo 1. Os demais têm módulo ≤ Σ_a C(n, a)·Σ_{k≥1} C(n−a, k)·q^(ak) = T(q). Pela desigualdade triangular, nos dois sentidos, sai o enunciado. ∎

**O mecanismo, em palavras.** Sem nenhuma ligação ativa, as teias ruins se cancelam exatamente pela identidade binomial (1 − 1)ⁿ = 0, que é um cancelamento entre os tamanhos possíveis do conjunto dos minimais. O que sobra vem das ligações, e cada ligação carrega o fator q = 2|cos β| = |1 + e^(−2iβ)|. Dentro da janela, q ≤ 1; no centro, q = 0. O tamanho da soma das teias ruins é controlado só por q.

**Conferência com os números exatos do E1** (ln|Z_rot,ruim|, exato contra cota):

| x | n = 40 | n = 80 | n = 120 | n = 160 |
| --- | --- | --- | --- | --- |
| 6 (q = 0,781) | 24,0 / 27,2 | 40,7 / 50,7 | 57,1 / 74,2 | 73,8 / 97,6 |
| 7 (q = 0,042) | 4,5 / 5,6 | 6,1 / 8,2 | 6,8 / 10,4 | 7,1 / 12,3 |
| 8 (q = 0,974) | 37,9 / 39,8 | 70,3 / 73,0 | 97,4 / 101,3 | 120,4 / 126,4 |

A cota fica a poucas unidades do valor exato. Ela explica a forma dos números do E1: perto do centro da janela (x = 7), a soma ruim quase não cresce com n.

**Consequência.** Para q < 1 fixo, o termo a = 1 domina: T(q) ≈ n·(1 + q)^(n−1), então ln|𝒵_ruim| ≤ (n − 1)·ln(1 + q) + ln n + O(1) − ln n!. Uma condição suficiente para H1\*, mais fraca que a de C1 e já demonstrada do lado ruim, é: |𝒵_boa(n, β)| > (1 + T(q))/n!.

## O que continua faltando

O lado ruim está resolvido para todo n e todo β da janela. O lado bom não tem cota inferior demonstrada. Esse é o único obstáculo para transformar H1\* em teorema. A pergunta precisa é: as teias de altura ≥ 3 que cabem em 3+1 têm alguma estrutura que impeça a soma de cancelar abaixo de (1 + T(q))/n!? Hoje não há resposta.
