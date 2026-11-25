# Conjectura do resíduo (registrada em 25/11/2026, antes de qualquer tentativa de prova)

Aprovada pelo autor em 25/11/2026 ("siga"). Origem: `EXPLORATORIO_RESIDUO_ASSINTOTICO.md`. Os dados que a inspiraram foram n = 40 a 640 em θ = 2,114; 2,2; 2,3; 2,4; 2,5; 2,7; 2,9; 3,05. **Eles não servem para validá-la.**

## Notação

- **y e w:** y = 1 + e^{−iθ}, e w = e^{−iθ}. Na janela aberta θ ∈ (2π/3, 4π/3), |y| = 2|cos(θ/2)| < 1.
- **Soma exata:** S_n = e^{−iθn}·a_n = Σ sobre as ordens rotuladas de altura ≤ 2 de w^{N₀}.
- **Termos:** T_k = C(n, k)·(y^k − 1)^{n−k}, a soma das ordens com exatamente k minimais.
- **Taxas:** ρ_k = |1 − y^k|, e ρ\* = max_{k ≥ 1} ρ_k.

## Enunciado (C-R)

Seja θ ∈ (2π/3, 4π/3), θ ≠ π, e suponha que o máximo ρ\* seja atingido num único k = k\*. Então

  S_n / (2·T_{k\*}) → 1 quando n → ∞.

## Versão fraca (C-R′), sem a hipótese de k\* único

lim sup (1/n) ln|S_n| = ln ρ\*.

## O que contaria como refutação

- uma prova de que a razão não tende a 1 para algum θ que satisfaça as hipóteses;
- ou um cálculo exato, com precisão conferida, em valores de θ **novos** e n grandes, mostrando a razão afastando-se de 1 de forma persistente.

## O que fica fora

- θ = π, onde todos os ρ_k = 1 e a_n = −1;
- as bordas θ = 2π/3 e 4π/3, onde |y| = 1;
- as ordens de altura ≥ 3.
