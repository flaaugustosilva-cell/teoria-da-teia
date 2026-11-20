# Resultados: modelo gaussiano de rede (pré-registro `PREREGISTRO_MODELO_REDE.md`, commit 7581d06)

Data: 20/11/2026. Todos os resultados abaixo são da **população oficial** (n = 5 a 10, altura ≥ 3, todas incorporáveis em 3+1, peso 1/|Aut|). A população auxiliar (n = 11) não entrou neste teste.

Ordem seguida, como registrada:

1. validação sintética;
2. P3;
3. P1 e P2.

O script não mudou entre o registro e a execução (sha256 `8d0c31b7…a0b`). Saídas brutas: `modelo_rede/valida.txt`, `p3.txt`, `p1p2.txt`, `modelo_rede_p3.json` e `modelo_rede_p1p2.json`.

## Vereditos

| Previsão | Veredito (n = 9 e 10) | Natureza |
| --- | --- | --- |
| P3a: posição dos picos, 51 controles | **SUCESSO** (43/51 e 42/51 ok; limiar 41/51) | potencialmente independente |
| P3b: magnitude, 51 controles | **FALHA** (0/51 ok e 51/51 falha, nos dois n) | potencialmente independente |
| P1: posição de θ\* | **SUCESSO** (diferença de 0,0033 nos dois n; limiar 0,005) | motivada pelos dados |
| P2: módulo de 𝒵 na janela | **FALHA** (erro log₁₀ mediano de 4,3 e 5,9; limiar de falha 1) | motivada pelos dados |

Pela interpretação fixada antes (seção 5 do registro), este é o caso **"P3a com sucesso e P3b falhando"**:

- **As posições** das ressonâncias são explicadas pela aritmética de c junto com a covariância das contagens.
- **As magnitudes não são.** Elas dependem de estrutura além dos dois primeiros momentos.
- **Consequência:** o modelo sozinho **não** serve de caminho para uma cota inferior de |𝒵_boa|.

## Validações

- **Implementação** (dados sintéticos, repetida depois do registro): erro máximo de 9,3×10⁻¹⁵, contra o limite de 10⁻¹⁰. As contagens foram conferidas em cadeia e anticadeia.
- **Dados:** o B recalculado a partir de (N₀, …, N₃) bateu com o B armazenado em **todas** as classes de n = 5 a 10. Os valores de W coincidem com os publicados (28,25; 164,417; 1171,03; 10551,5; 121989; 1,81818×10⁶).
- **Degenerescência:** nenhum n foi degenerado. Os autovalores de Σ são:
  - n = 5: 0,079; 0,28; 0,67; 0,82;
  - n = 9: 0,70; 1,46; 2,47; 3,69;
  - n = 10: 0,93; 1,87; 3,02; 4,62.
- **Normalização D − 1:**
  - n = 5: +0,21. O efeito de rede é forte, e por isso a normalização não podia ser suposta igual a 1;
  - n = 6: −6,2×10⁻⁴;
  - n = 7: −2,7×10⁻⁴;
  - n = 8: −1,4×10⁻⁶;
  - n = 9: 7×10⁻⁹;
  - n = 10: 1×10⁻¹¹.
- **Truncamento:** a maior variação entre L = 50 e L = 70 foi de 3,4×10⁻¹⁰, abaixo do limite de 10⁻³. Nenhum vetor foi não testável.
- **Erro numérico das somas exatas:** no máximo 459 valores distintos de B′, o que dá erro relativo ≤ 5×10⁻¹⁴, abaixo do piso de 10⁻¹².

## P3: controles artificiais (rodou primeiro)

Número de controles com classificação "ok", de 51, no modelo completo e no modelo descritivo com Σ diagonal:

| n | posição ok (completo) | posição falha | magnitude ok | magnitude falha | posição ok (diagonal) |
| --- | --- | --- | --- | --- | --- |
| 5 | 50 | 0 | 18 | 0 | 49 |
| 6 | 47 | 0 | 0 | 1 | 48 |
| 7 | 44 | 2 | 0 | 46 | 42 |
| 8 | 43 | 2 | 0 | 51 | 39 |
| 9 | **43** | 5 | **0** | **51** | 39 |
| 10 | **42** | 5 | **0** | **51** | 38 |

**Por família, em n = 10, modelo completo, posição ok:**

- A (permutações): 23/23;
- B (sorteados): 12/20;
- C (vizinhos de c): 7/8.

Os erros de posição se concentram nos vetores sorteados.

**Margem de P3a:** o sucesso é **estreito**. A fração de acertos é 0,84 em n = 9 e 0,82 em n = 10, contra o limiar de 0,80, e ela cai com n (0,98, 0,92, 0,86, 0,84, 0,84, 0,82).

**Papel da covariância:**

- O modelo diagonal acerta menos posições: 0,76 e 0,75, o que é inconclusivo pelos mesmos critérios.
- A covariância melhora a previsão das posições de forma real, mas **modesta**: 4 vetores a mais em 51.
- Grande parte da posição das ressonâncias já vem da teoria dos números (θc′ perto de 2πℤ⁴).

**Onde a magnitude falha (descritivo):**

- **O pico mais alto é bem previsto.** A mediana de log₁₀(pico do modelo/pico observado) fica entre −0,03 e 0,00 em todos os n. Para o c original em n = 10, o observado é 0,158 em θ = 0,7418 e o modelo dá 0,138 em θ = 0,7453.
- **Longe dos picos, o modelo erra por várias ordens de grandeza.** A mediana do erro log₁₀ na região fina vale 0,33, 0,70, 1,25, 1,88, 2,70 e 3,65 para n = 5 a 10, com percentil 90 (mediana entre os controles) de 7,4 em n = 10.
- **O modelo fica abaixo do observado.** O pico do modelo é menor que o observado em 49 dos 51 controles em n = 10.
- **O erro cresce com n.** Os vales verdadeiros decaem muito mais devagar do que a gaussiana prevê.

## P1 e P2 (rodaram depois do P3)

| n | θ\*_obs | θ\*_mod | fórmula de um termo | P1 | erro log₁₀ na janela (mediana / máx.) | P2 | min\|𝒵\| obs. | min\|𝒵\| modelo | 3ⁿ/n! | 𝒵(π) obs. | 𝒵(π) modelo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 0,740 | 0,7435 | 0,7391 | ok | 0,59 / 1,93 | interm. | 0,252 | 0,028 | 2,02 | +1,42 | −0,12 |
| 6 | 0,740 | 0,7444 | 0,7433 | ok | 1,20 / 3,51 | falha | 1,80 | 2,3×10⁻³ | 1,01 | −14,25 | −0,085 |
| 7 | 0,740 | 0,7444 | 0,7444 | ok | 2,12 / 4,84 | falha | 2,59 | 5,1×10⁻⁴ | 0,434 | −3,52 | +0,0041 |
| 8 | 0,741 | 0,7453 | 0,7450 | ok | 3,05 / 6,50 | falha | 0,542 | 1,4×10⁻⁵ | 0,163 | −54,1 | +1,7×10⁻⁴ |
| 9 | 0,742 | 0,7453 | 0,7454 | ok | 4,30 / 7,10 | falha | 23,4 | 4,2×10⁻⁵ | 0,054 | −76,9 | +2,1×10⁻⁴ |
| 10 | 0,742 | 0,7453 | 0,7457 | ok | 5,89 / 8,73 | falha | 150 | 2,7×10⁻⁶ | 0,016 | −687 | +5,4×10⁻⁵ |

**P1:**

- Passa nos dois n.
- O modelo fica sempre em torno de 0,745, cerca de 0,003 **acima** do observado. O observado sobe de 0,740 para 0,742 com n, e o modelo não reproduz essa deriva.
- A fórmula de um termo, θ\*₁ = 2π(cᵀΣm₀)/(cᵀΣc), já dá o mesmo valor. Isso mostra que **uma única ressonância** (m₀ = (0, 1, −2, 1), isto é, B ≈ 8(N₁ − 2N₂ + N₃) + (n − N₀ + N₁)) explica o pico.
- Lembrete: P1 foi motivada pelos dados e não conta como confirmação.

**P2:**

- Falha, e por uma margem enorme que cresce com n: em n = 10, o modelo subestima o módulo na janela por um fator de cerca de 10⁶.
- Pior ainda, o modelo **preveria o contrário de H1\***. Ele dá min|𝒵_boa| abaixo da cota dos ruins 3ⁿ/n! para n = 6 a 10, enquanto o observado fica acima dela.
- O modelo também **erra o sinal** de 𝒵(π) para n = 7 a 10.

## O que isto estabelece e o que não estabelece

- **Estabelece**, para n = 5 a 10, população oficial:
  - o "esqueleto" da estrutura fina (onde ficam as ressonâncias e qual é a altura da principal) é bem descrito por uma gaussiana de rede com os dois primeiros momentos;
  - isso vale também para coeficientes que ninguém tinha olhado (P3a).
- **Estabelece também:** a janela física **não** é um fenômeno de segunda ordem. Os valores de |𝒵| na janela, que são exatamente o que decide H1\*, ficam de 10⁴ a 10⁶ vezes acima do que a gaussiana prevê em n = 9 e 10 (mediana do erro na janela), e a discrepância cresce com n. A pergunta "o que impede o cancelamento?" **não** se reduz à covariância das contagens.
- **Não estabelece:**
  - que N seja gaussiano;
  - nada assintótico;
  - nada sobre H1\* ou C1 para n ≥ 11.

## Erros e correções deste registro

**Erro na seção 7 (Limitações) do pré-registro.** Escrevi que perto da ressonância |φ| fica entre 10⁻³ e 10⁻⁴. Isso está **errado**:

- no pico da ressonância, |φ| vale entre 0,16 (n = 10) e 0,72 (n = 5);
- os valores entre 10⁻³ e 10⁻⁴ são os de θ = 0,5, θ = 1,0 e da janela, isto é, os **vales**.

O erro não afeta nenhum critério nem nenhum veredito, porque os critérios não usam essa frase. O pré-registro não foi alterado.

## Próximos passos possíveis (não executados; dependem de decisão)

**1. Exploração "quem carrega os vales".**

- O excesso observado sobre a gaussiana já é enorme no centro da janela, onde 𝒵(π) = W_par − W_ímpar (conjectura C2).
- O modelo diz que esse saldo deveria ser exp(−½π² Var(N₀ + N₁)), que é desprezível.
- O saldo real, portanto, vem de estrutura que não é do volume típico das teias.
- Uma rota analítica natural é uma **involução que troca o sinal**: um emparelhamento entre teias que inverte a paridade de N₀ + N₁. As teias que sobram sem par dariam W_par − W_ímpar exatamente, e isso é uma estratégia de demonstração para C2 e para uma cota inferior no centro da janela.

**2. Correções por cumulantes (Edgeworth).**

- Usariam cumulantes medidos, sem ajuste.
- São pouco promissoras: corrigir um déficit de 10⁶ nas caudas com termos perturbativos raramente funciona.
- Se forem tentadas, precisam de registro próprio.
