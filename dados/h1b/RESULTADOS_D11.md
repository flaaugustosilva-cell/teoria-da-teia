# Resultados: teste de coerência dimensional em n = 11 (pré-registro `PREREGISTRO_D11.md`, commit 3067e69)

Data: 24/11/2026. A população é a de **todas as ordens** com n = 11. Ela não foi misturada com a população oficial.

## Execução

- **Geração.** As 20 partes foram geradas do zero com o genposetg registrado, de 01:52 a 04:03, em dois processos. Tempos em `D11_tempos.txt`; dados por classe em `d11/` (hashes em `D11_partes_sha256.txt`).
- **Análise.** `h1b_D11_analise.py` foi rodado **uma única vez**, com os mesmos hashes do registro. Saída: `resultado_D11.txt`.

**Validações obrigatórias: todas OK.**

- classes: 46.749.427;
- soma com sinal: −40.491.236.963;
- soma das ruins: −1;
- as 20 partes conferem com as partes auxiliares publicadas.

## Resultado primário

| faixa de Myrheim–Meyer | coerência real | mediana dos 20 controles [mín., máx.] | razão |
| --- | --- | --- | --- |
| d < 1,5 | 2,607×10⁻³ | 1,343×10⁻³ [1,08; 1,72]×10⁻³ | 1,94 |
| 1,5 a 2,5 | 4,118×10⁻⁴ | 1,614×10⁻⁴ [1,45; 1,74]×10⁻⁴ | 2,55 |
| **2,5 a 3,5** | **5,659×10⁻³** | **7,025×10⁻⁴ [5,20; 10,04]×10⁻⁴** | **8,06** |

**R₃(11) = 8,055 > 6,0: CONFIRMA o critério pré-registrado.**

Pela regra de leitura fixada antes, isso **confirma o critério para n = 11, mas não demonstra crescimento assintótico.** A sequência fica R₃ = 2,82, 3,57, 6,04 e 8,06 para n = 8 a 11.

A margem sobre o critério (8,06 contra 6,0) é bem maior que a incerteza de alguns por cento declarada antes.

## Sensibilidade (200 controles, semente 20261126)

- Razão: **8,61**.
- Controles: mediana 6,57×10⁻⁴; percentis de 2,5% e 97,5% iguais a 4,71×10⁻⁴ e 8,86×10⁻⁴; máximo 9,60×10⁻⁴.
- O valor real (5,66×10⁻³) é **5,9 vezes o maior dos 200 controles**.

## Desvio técnico declarado

A execução única foi **interrompida por falta de memória** (registro do sistema: "Memory cgroup out of memory", processo python encerrado). Isso aconteceu **depois** de calcular e imprimir a primária e a sensibilidade, e **antes** das secundárias e do JSON com todos os controles.

Para recuperar o que faltava, escrevi `scripts/h1b_D11_secundarias.py`:

- ele refaz os controles com as **mesmas funções e sementes**;
- é um cálculo determinista, e o script exige que os números coincidam com os impressos antes de gravar qualquer coisa. **Coincidiram:** R₃ = 8,0552 e sensibilidade = 8,6080, com os mesmos valores reais;
- depois ele faz as secundárias com pouca memória: a classificação por perfil é feita em blocos, com os mesmos centroides e a mesma semente 20261127.

Esse desvio **não** muda o veredito, que veio da execução única. O JSON completo, com todos os controles, está em `resultado_D11.json`. A saída das secundárias está em `resultado_D11_secundarias.txt`.

## Secundárias (não mudam o veredito)

**Partição de Myrheim–Meyer.**

- Índice de decoerência I: mediana 1,08 [0,27; 1,70].
- |𝒵|²/Σ|Z_g|²: mediana 0,135.

| faixa | p (peso clássico) | μ (distribuição das contribuições diagonais; não é probabilidade): mediana [mín., máx.] |
| --- | --- | --- |
| d < 1,5 | 0,0096 | 0,0028 [0,0001; 0,080] |
| 1,5 a 2,5 | 0,9488 | 0,5025 [0,107; 0,988] |
| **2,5 a 3,5** | **0,0416** | **0,4950 [0,012; 0,886]** |
| 3,5 a 4,5 | 0,0000 | 0,0000 |

**Partição por perfil de intervalos.**

- I: mediana 1,68 [1,03; 2,03].
- |𝒵|²/Σ|Z_g|²: mediana 0,0043.

| grupo | p | μ: mediana [mín., máx.] |
| --- | --- | --- |
| d = 2 | 0,744 | 0,101 [0,0001; 0,598] |
| **d = 3** | **0,057** | **0,489 [0,041; 0,820]** |
| d = 4 | 0,0000 | 0,0000 |
| camadas | 0,199 | 0,430 [0,046; 0,663] |

**Leitura das secundárias:**

- As duas partições contam a mesma história: a classe de cerca de 3 dimensões tem de 4% a 6% do peso clássico e cerca de 49% das contribuições diagonais.
- As classes continuam interferindo fortemente (I ≥ 0,27 em toda a janela). A dimensão **não** se comporta como propriedade clássica decoerente da soma de histórias.
- O grupo de 4 dimensões continua praticamente vazio em n = 11.

## O que isto responde

| Pergunta (item 7 do registro) | Resposta |
| --- | --- |
| Persistência (R₃ > 1)? | Sim: 8,06, e 5,9 vezes o maior de 200 controles. |
| Crescimento (R₃ > 6,0)? | Sim, para n = 11: a previsão mais forte foi confirmada. |
| Seleção física de dimensionalidade? | **Não respondida.** Um excesso de coerência numa classe definida por um estimador não mostra que o espaço-tempo emergente seja 3 ou 3+1. |

**Questão aberta (registrada antes):** o excesso vem da geometria dos intervalos, da distribuição de B dentro da classe, ou de uma correlação entre as duas? Também falta entender por que a classe de 3 dimensões, e não a de 4, que não tem membros nestes tamanhos.
