# Pré-registro: teste de coerência dimensional em n = 11 (todas as ordens)

Data: 24/11/2026. Este documento foi publicado **antes** de gerar as ordens de n = 11 para este teste e antes de calcular qualquer quantidade dimensional em n = 11. O protocolo é o proposto pelo Flavio, com os detalhes técnicos fixados abaixo.

**Natureza do teste.** É a validação independente de uma **observação exploratória** (`EXPLORATORIO_DECOERENCIA.md`). Não há conjectura registrada, e o resultado não é prova de tendência assintótica.

## 1. População

- **Todas** as ordens parciais com n = 11: 46.749.427 classes, peso w = 1/|Aut|. É a população auxiliar.
- **Não** se mistura com a população oficial (altura ≥ 3 e incorporável em 3+1), porque a classificação oficial em n = 11 não está estabelecida.

## 2. Geração e validações obrigatórias

**Geração.**

- Programa: `genposetg 11 t q m x 20`, para x = 0 a 19. É o mesmo executável já registrado (sha256 `ea9e6303ad6c9bae0be3590049a256e941211e1b625f7a88cebb7231495ca72a`).
- Cada parte é processada por `scripts/h1b_D11_parte.py`. Para cada classe, na ordem de saída, ele grava: B (ação de 4 dimensões), |Aut|, N₀ a N₃, R (número de pares comparáveis) e a altura.

**Validações obrigatórias** (`scripts/h1b_D11_analise.py`):

- total de classes = 46.749.427;
- soma com sinal de cada parte = a da parte auxiliar publicada (`n11aux/`);
- soma total = −40.491.236.963;
- soma das ruins (altura ≤ 2) = −1.

Se **qualquer** validação falhar, o resultado é **inconclusivo**.

**Teste do encadeamento,** feito antes deste registro, só em n = 8: a geração reproduz exatamente as classes (B, |Aut|, R e altura) e as coerências calculadas com os dados já existentes.

## 3. Classificação congelada

- r = R / C(11, 2) = R/55.
- Faixa de Myrheim–Meyer pela função `faixa` de `scripts/h1b_dimensao.py`, com os cortes f(1,5), f(2,5), f(3,5) e f(4,5) e f(d) = Γ(d+1)Γ(d/2)/(2Γ(3d/2)).
- A faixa testada é **2,5 ≤ d < 3,5** (índice 2), exatamente como em n = 8 a 10.

## 4. Estatística primária

**Coerência de uma classe.** Para um conjunto de classes A:

  c(A) = mediana, na grade de 241 pontos igualmente espaçados em [2π/3, π], de |Z_A(θ)| / W_A,

com Z_A(θ) = Σ_{P∈A} w·e^{iθB} e W_A = Σ_{P∈A} w.

**Estatística:**

  R₃ = c(faixa 2,5 a 3,5) / mediana dos c dos 20 controles.

**Regra dos controles** (função `razoes_controle` de `scripts/h1b_decoerencia.py`):

- gerador `numpy.random.default_rng(20261125)`;
- faixas processadas na ordem 0, 1, 2, com 20 sorteios cada;
- em cada sorteio, cada classe entra independentemente quando `rng.random(46749427) < q`, com q = W_faixa / W;
- as classes ficam na ordem de concatenação das partes 0 a 19, cada uma na ordem de saída do genposetg.

**Critério de sucesso:** **R₃(11) > 6,0**. É o que testa a afirmação mais forte sugerida pelos dados anteriores, superar o excesso observado em n = 10 (R₃(10) = 6,044, reproduzido com o código congelado).

## 5. Regra de interpretação

| Resultado | Leitura |
| --- | --- |
| R₃ > 6,0 | Confirma o critério pré-registrado para n = 11. **Não** demonstra crescimento assintótico. |
| 1 < R₃ ≤ 6,0 | Há excesso em relação ao controle, mas **não** se confirma a previsão mais forte. |
| R₃ ≤ 1 | Não se confirma nem o excesso em relação ao controle. |
| Falha de geração, validação ou controle | **Inconclusivo.** |

**Incerteza declarada antes.** R₃ tem incerteza de alguns por cento, por vir da mediana de só 20 sorteios. Em n = 8, trocar a semente e a ordem das classes mudou R₃ de 2,817 para 2,905. Um resultado perto de 6,0 deve ser lido com isso em mente. O critério continua sendo o número acima, sem ajuste depois.

## 6. Análises secundárias (fixadas agora; não mudam o veredito)

- **Sensibilidade:** 200 controles para a faixa 2,5 a 3,5, com `default_rng(20261126)`. Serão relatados a razão, os percentis de 2,5% e 97,5% dos controles e real/máximo dos controles.
- **Razões das outras faixas** (0 e 1), do mesmo cálculo primário.
- **Índice de decoerência** I, |𝒵|²/Σ|Z_g|², e a passagem do peso p para μ (distribuição normalizada das contribuições **diagonais**, que **não** é probabilidade nem medida da partição), com mínimo e máximo ao longo da janela.
- **A mesma análise pela partição por perfil de intervalos,** com centroides de 4000 ordens sorteadas por família e `default_rng(20261127)`.
- **Todos os controles** serão guardados integralmente no JSON de saída, não só a mediana.

## 7. O que o teste responde e o que não responde

- **Persistência:** a classe de cerca de 3 dimensões continua mais coerente que os controles (R₃ > 1)?
- **Crescimento:** o excesso supera o de n = 10 (R₃ > 6,0)?
- **Não responde se há seleção física de dimensionalidade.** Mesmo um resultado positivo não mostra que o espaço-tempo emergente seja 3 ou 3+1. Isso exigiria relacionar a coerência a observáveis físicos e a um regime de decoerência apropriado.
- **Questão aberta em paralelo:** um excesso, se existir, vem da geometria dos intervalos, da distribuição de B dentro da classe, ou de uma correlação entre as duas?

## 8. Código fixado neste commit (sha256)

| Arquivo | sha256 |
| --- | --- |
| `scripts/h1b_D11_parte.py` | `b8da1ce559de57d85f97f7714ed13a80dac3d42f75d0858bb02cc605ee069a1f` |
| `scripts/h1b_D11_analise.py` | `8e40ed2459a86404677bbe249963d9e044857664f6db2d1b6e8b763b69e33b32` |
| `scripts/h1b_decoerencia.py` | `fe5a7fbd75200dcdb95f8b1aaf9f046afe95ef29fc99277f664175fab6b37bbb` |
| `scripts/h1b_dimensao.py` | `81e71c16b93a3e846026b3b5d63ceedf3ee16a033f9d1c743927682a9a121764` |
| `scripts/h1b_dimensao_piloto.py` | `d9341b1fc02ec120b005be3ccd43186062d9a75f51b9ca93c7a755df5410467b` |
| `scripts/h1b_modelo_rede.py` | `8d0c31b743dc5870ac672163b232c5aab2f11ff390c31b1f43116188acc32a0b` |
| `scripts/h1b_N_classes.py` | `a062443ab4f900b3d568b6172802f0381b3f81741992a2179ffd55aea56c6e36` |

## 9. Ordem de execução

1. Publicar este registro (commit e push).
2. Gerar as 20 partes de n = 11.
3. Rodar `python h1b_D11_analise.py 11 PASTA 20 dados/h1b/n11aux SAIDA.json` uma única vez.
4. Registrar o resultado em `RESULTADOS_D11.md`, incluindo o que for desfavorável.
