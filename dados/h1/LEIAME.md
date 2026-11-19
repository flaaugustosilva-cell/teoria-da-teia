# H1 — A soma das teias boas pode ficar menor que o peso de uma teia?

Flavio Augusto da Silva · 19/11/2026 · teste numérico pré-registrado por volta das 13:45 (Brasília), antes de rodar

H1 é a hipótese de que a soma das teias boas, por teia não rotulada, vale pelo menos 1. O E1 ([`../e1/LEIAME.md`](../e1/LEIAME.md)) depende dela.

## Análise matemática

- **T1 (exato).** Agrupando as teias boas pelo valor inteiro de B, com θ = 2β: 𝒵_boa(θ) = Σ_B W_n(B)·e^(iθB) = W_n·φ_n(θ), com W_n(B) ≥ 0. H1 equivale a |φ_n(θ)| ≥ 1/W_n. O E1 só precisa de |φ_n| > e^L/W_n (hipótese H1*).
- **T2 (cotas; citações de memória, não conferidas).** n!/(2e²) ≤ W_n ≤ (2e(n−1))^(4n)/n!. A cota inferior vem das ordens de dimensão 2 (permutações simples, Albert, Atkinson e Klazar 2003); a superior, do teorema de Warren. Daí: H1 vale se a fase média decair mais devagar que e^(−n·ln n); o E1 só cai se ela decair mais rápido que cerca de e^(−2n·ln n). Limiar de H1 em n = 160: ln|φ_n| > −652,8.
- **T3 (exato, Parseval).** A média de |𝒵_boa|² sobre θ é Σ_B W_n(B)² ≥ W_n²/K_n, com K_n ≤ 17n(n−1) + n + 1. Na média sobre β, H1 vale com folga enorme; num β específico, nada está garantido.
- **T4 (contraexemplo, exato).** As teias ruins de camadas cheias têm pesos positivos e mesmo assim somam zero em β = π/2 (x = 6,953, dentro da janela 1). As de camadas livres somam exatamente |Z| = 1 nesse ponto. Positividade e contagem não demonstram H1.

## Teste numérico pré-registrado

- **Medida:** Γ = |média de e^(iθB)| em teias sorteadas em diamantes de 1+1, 2+1 e 3+1 (todas cabem em 3+1), com a ação 4D de sempre (ε = 1). É um substituto de |φ_n|: o sorteio não dá o peso 1/|Aut| de todas as teias boas.
- **Parâmetros:** n = 6, 8, 10, 12, 14, 16, 20, 24, 28, 32; M = 1.000.000 por n; sementes 20261120 e 7777 (3+1) e 20261120 (1+1 e 2+1); x = 6, 7, 8 e controles 0,832 e 9.
- **Ajuste:** só pontos acima de 4 erros padrão; mínimo de 4 pontos; modelos −γn, −γ·n·ln n e −κn², extrapolados até n = 160.

## Resultado

- **Dentro da janela: inconclusivo nos 12 casos.** Γ cai abaixo do ruído (~0,001) já em n = 8 a 10, e sobram 1 ou 2 pontos válidos. Em n = 32 só existe a cota superior Γ < 0,004, que não ajuda H1.
- **Sementes:** concordam (maior desvio de 1,45 erros combinados).
- **Automorfismos:** o peso 1/|Aut| muda Γ além de 3 erros onde Γ é mensurável. A medida escolhida importa.
- **Alerta (fora do veredito):** no controle x = 9 (ângulo efetivo de 1,02 rad), 4 pontos válidos; o modelo quadrático ajusta bem, com κ = 0,032, acima do κ crítico de 0,0255. Extrapolado até n = 160, cruza o limiar de H1 (−816 contra −652,8).
- **Falha de desenho reconhecida:** com M = 10⁶, o teste só enxerga Γ acima de ~0,004, e dentro da janela Γ fica abaixo disso a partir de n ≈ 10.

## Conclusão

Não foi encontrada propriedade das teias boas que garanta H1, e a análise mostra que ela teria de ser específica (T4). H1 continua em aberto (classe D). Pela regra pré-registrada, o E1 continua classe B, mas o único indício numérico (x = 9) aponta contra H1. Próximo passo: amostragem por importância em B, para medir fases médias de e^(−30) ou menores, e um mapa de Γ em função do ângulo.

## Como reproduzir

```
cd scripts
python h1_robustez.py 4 20261120 peso
python h1_robustez.py 4 7777
python h1_robustez.py 3 20261120
python h1_robustez.py 2 20261120
python h1_ajuste.py
```

Cada rodada de 3+1 leva cerca de 5 minutos. Os histogramas gerados (`h1_hist_*.npz`) devem sair idênticos aos desta pasta. `h1_ajuste.py` grava `h1_resultados.csv` e `h1_ajustes.csv` e imprime o resumo (`h1_resumo.txt`).

Nota: a primeira rodada do caso `4 20261120 peso` não guardava a soma dos pesos ao quadrado, necessária para o erro de Γ com peso. O script foi completado e esse caso foi rodado de novo com a mesma semente; as teias saíram idênticas. Nenhum parâmetro foi alterado.
