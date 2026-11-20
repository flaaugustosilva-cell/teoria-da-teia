# Investigação auxiliar: teias ruins contra todas as outras ordens em n = 11 — pré-registro

Flavio Augusto da Silva · registrado em 20/11/2026 (Brasília), antes de qualquer cálculo de n = 11. O horário do commit é a prova.

## Estatuto (decisão do autor, 20/11, 14:57)

- **A definição oficial não muda:** "teia boa" continua sendo ordem de altura ≥ 3 que cabe em Minkowski 3+1 (opção 1).
- **Esta é uma investigação auxiliar (opção 2), com pergunta própria:** as teias ruins (altura ≤ 2) pesam menos que **todas as outras ordens** (altura ≥ 3, caibam ou não em 3+1)? Esse conjunto é chamado aqui de "não ruins".
- Para n ≤ 10, "não ruins" e "boas" coincidem (toda ordem de altura ≥ 3 cabe em 3+1 até n = 10). Em n = 11, podem diferir. **Nenhum resultado desta investigação demonstra H1\* ou C1 para a definição oficial em n = 11.** Somar ordens que não cabem em 3+1 pode aumentar ou diminuir o módulo da soma.

## Perguntas (todas em n = 11, peso 1/|Aut|, ação de Benincasa–Dowker 4D, ε = 1)

- **A1 (centro da janela, β = π/2):** com T_11 = Σ_{ordens rotuladas} (−1)^(N₀+N₁) e T_11(ruim) = +1 (Teorema 1′), vale |T_11(não ruim)| > 3¹¹ = 177.147?
- **A2 (janela inteira):** |𝒵_não-ruim(β)| > 3¹¹/11! = 0,004439 para todo β da janela? Esse é o análogo de C1.
- **A3 (janela inteira):** R_aux = |𝒵_ruim|/|𝒵_não-ruim| < 1 para todo β da janela? Esse é o análogo de H1\*.

Antes deste registro, só se conhecem n ≤ 10, em que as três valem desde n = 6.

## Método

- **Geração:** `genposetg 11 t m x 20`, x = 0, …, 19 (mesmo executável, sha256 `ea9e6303…`). Cada parte é processada direto da saída do gerador, sem arquivo intermediário, e o resultado de cada parte é gravado. Uma parte já gravada não é refeita.
- **Por classe:** fecho transitivo, conferência de ordem parcial, |Aut| (mesmo código de `h1b_N_classes.py`), B, altura e conexidade (grafo de comparabilidade conexo).
- **Guarda-se só o agregado exato,** em inteiros: para cada (B, altura ≤ 2 ou ≥ 3, conexa ou não), a soma de 11!/|Aut| e o número de classes.
- **Janela:** o mesmo método rigoroso de `h1b_N_analise.py` (subdivisão adaptativa com cota da derivada; mínimos pontuais conferidos em 60 dígitos).

## Validações (antes de qualquer resposta a A1, A2 ou A3)

1. Número de classes = 46.749.427 (A000112).
2. Σ 11!/|Aut| = 1.396.281.677.105.899 (A001035), igualdade exata.
3. Σ 11!/|Aut| sobre as classes conexas = 1.320.327.172.853.172 (A001927), igualdade exata.
4. Toda saída é ordem parcial.
5. Lado ruim: T_11(ruim) = +1 (Teorema 1′ no centro) e soma das ruins igual à fórmula exata do E1 em três ângulos (diferença < 10⁻⁶ em ln|Z|).

Se alguma falhar, o cálculo para e o erro é reportado.

## Interrupção

Se o processamento passar de 8 horas, ele para. As perguntas A1 a A3 não são respondidas com dados parciais, porque as somas exigem todas as partes.

## Relato

Resultado de A1, A2 e A3 (cada uma: vale, falha ou não decidida), com a ressalva de estatuto acima em destaque. Como descrição, também a estrutura de W_b em n = 11 (as perguntas da linha principal: suporte, suavidade, paridade, quase-zeros), sem valor de teste.
