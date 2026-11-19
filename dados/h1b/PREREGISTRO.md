# H1, segunda etapa — pré-registro (A → E → B → C)

Flavio Augusto da Silva · registrado em 19/11/2026, 15:55 (Brasília), antes de qualquer rodada desta etapa.
O horário do commit no GitHub é a prova do registro. Nada aqui muda depois de ver resultados.

## Decisões do autor (19/11/2026, 15:52)

1. **Definição de teia boa para H1:** todas as teias que cabem em Minkowski 3+1, com altura ≥ 3, com peso 1/|Aut| (a mesma convenção do E1: soma rotulada dividida por n!). A contagem não rotulada (peso 1) não se compara com o E1.
2. **O sorteio** (teias típicas de um diamante) é um **substituto experimental**, com interpretação própria. φ_sorteio não será chamada de aproximação de φ_n sem uma relação demonstrada entre as duas distribuições.
3. **Ordem:** A → E → B → C. Nada de teias ruins de três camadas nesta etapa.
4. **Nenhuma confirmação de H1 baseada só em números finitos.**

## Níveis de conclusão

| Resultado | O que autoriza concluir |
| --- | --- |
| Evidência numérica | O comportamento observado é compatível com uma hipótese |
| Mecanismo matemático demonstrado | O comportamento decorre de propriedades demonstradas do modelo |
| Extrapolação assintótica demonstrada | O resultado vale para n arbitrariamente grande, sob hipóteses explicitadas |

Nada nesta etapa pode chegar ao terceiro nível só com números.

## A — Formalização do estimador (entregue com este registro)

Seja p_n(C) a probabilidade de o sorteio de n pontos no diamante 3+1, condicionado a altura ≥ 3, dar a teia não rotulada C. Seja w(C) = 1/|Aut(C)| e W_n = Σ_C w(C) sobre todas as teias boas.

- φ_sorteio,n(θ) = Σ_C p_n(C)·e^(iθB(C));  φ_n(θ) = Σ_C w(C)·e^(iθB(C)) / W_n.
- **Sem viés (demonstrado):** com M sorteios independentes, φ̂ = (1/M)·Σ_j e^(iθB_j) tem E[φ̂] = φ_sorteio,n(θ), por linearidade. E|φ̂ − φ_sorteio|² = (1 − |φ_sorteio|²)/M.
- **O módulo é enviesado (demonstrado):** E|φ̂|² = |φ_sorteio|² + (1 − |φ_sorteio|²)/M. Por isso Γ = |φ̂| "para" em ~1/√M. O estimador sem viés de |φ_sorteio|² é Q = (M·|φ̂|² − 1)/(M − 1). Todas as etapas abaixo usam Q, com erro por jackknife em 50 blocos.
- **Distância até o objeto de H1 (exata):** Δ_n(θ) = φ_sorteio,n(θ) − φ_n(θ) = Σ_C [p_n(C) − w(C)/W_n]·e^(iθB(C)). Então |Δ_n| ≤ Σ_C |p_n(C) − w(C)/W_n|, que é a distância de variação total entre as duas medidas e pode chegar a 2. Não há cota útil sem conhecer p_n, e p_n não é calculável. Só a entrega B mede Δ_n, e só para n pequeno.

## E — Origem do crescimento de B (roda primeiro)

**Pergunta central:** o crescimento de B vem de um modo global cuja distribuição força o cancelamento rápido das fases, ou é só uma correlação global que não decide esse cancelamento?

**Base matemática (hipótese de trabalho, não resultado):** se a distribuição de B se escrever como P_n(B) ≈ g((B − média)/n)/n, com g suave e independente de n, então |φ_n(θ)| ≈ |Σ_k ĝ(n(θ + 2πk))| mais correções de estrutura fina. Nesse caso, o decaimento é decidido pela suavidade de g, não pela variância. Uma g gaussiana dá e^(−cn²) (H1 cai). Uma g analítica só numa faixa dá e^(−cn) (H1 passa). Uma g com saltos dá ~1/n (H1 passa).

**Dados novos:** diamante 3+1, semente **20261121** (nunca usada). n = 10, 20, 40, 80, 160, com M = 1.000.000 (n ≤ 40), 200.000 (n = 80) e 50.000 (n = 160). Mesma ação de sempre (Benincasa–Dowker 4D, ε = 1).

**E1 — existe um modo global?** Regressão linear de B em observáveis globais fixados agora: número de pares relacionados R, R², altura h (maior cadeia), número de minimais e número de maximais. N₀..N₃ não entram, porque compõem B.
- "Modo global identificado" se R² da regressão ≥ 0,90 em n = 40, 80 e 160.
- "Resíduo local" se a variância do resíduo crescer com expoente ≤ 1,2 em n (ajuste de log Var contra log n, n de 10 a 160). Caso contrário, "modo global incompleto".

**E2 — como o modo se distribui?** Para X = (B − média)/desvio: assimetria e curtose em excesso, com intervalos de 95% por bootstrap; caudas em |X| > 3 e > 4 contra a gaussiana; distância de Kolmogorov–Smirnov entre n = 80 e n = 160. "Compatível com gaussiana" se, em n = 160, |assimetria| < 0,1 e |curtose em excesso| < 0,2. Os momentos são só indícios, porque o decaimento depende da suavidade de g e não dos momentos. A decisão fica com E3.

**E3 — o decaimento da fase (decisivo).**
- Ângulos pequenos: θ = 0,01; 0,02; 0,03; 0,045; 0,06; 0,08; 0,10; 0,13; 0,16; 0,20; 0,25; 0,32.
- **Colapso:** se |φ| depender só de ω = nθ, as curvas de n = 40, 80 e 160 se sobrepõem. "Colapso aceito" se ≥ 80% das comparações nos ω em comum (interpolação linear em ln Q) ficarem dentro de 3 erros combinados.
- **Forma de ĝ:** com os pontos de n = 40, 80 e 160 em que Q > 4 erros, ajustam-se três modelos para ln|φ| = ½·ln Q em função de ω: gaussiano (a − sω²), exponencial (a − bω) e potência (a − c·ln ω). "Decisivo" se o melhor modelo tiver AIC pelo menos 10 menor que o segundo; senão, inconclusivo.
- **Estrutura fina:** em θ_efetivo = 0,5; 0,75 e 1,0 (n = 10, 20, 40), compara-se o Q medido com a previsão do colapso, |ĝ(n·θ_efetivo)|², usando o ĝ ajustado; a soma dos termos com k ≠ 0 entra como incerteza de modelo. "Estrutura fina desprezível" se ≥ 80% dos pontos válidos concordarem dentro de 3 erros. Os ângulos da janela (2,339; 3,099; 2,125) são só reportados.

**Veredito de E** (nível: evidência numérica, nunca demonstração):
- **E-a, cancelamento rápido sustentado no substituto:** modo global identificado, colapso aceito, gaussiano decisivo e estrutura fina desprezível. Leitura: H1 em risco forte no substituto.
- **E-b, decaimento lento sustentado no substituto:** colapso aceito, com exponencial ou potência decisivo. Leitura: substituto compatível com H1.
- **E-c, inconclusivo:** qualquer outro caso.

Ressalva fixada agora: mesmo E-a ou E-b extrapolam ĝ de ω ≲ 5 (onde se mede) até ω ≈ 300 (a janela em n = 160). Essa extrapolação é uma hipótese de modelo. Só uma derivação analítica da suavidade de g levaria ao segundo nível.

## B — φ_n exato para n pequeno (depois de E)

- n = 5, 6 e 7 obrigatórios; n = 8 se a enumeração terminar em menos de 6 horas (critério de viabilidade, que não depende das fases).
- Enumeração: todas as ordens rotuladas naturalmente; soma rotulada pela identidade Σ_rotuladas f = Σ_naturais f · n!/e(P), em que e(P) é o número de extensões lineares; altura ≥ 3.
- Caber em 3+1: para cada teia não rotulada, busca de coordenadas (até 200 recomeços aleatórios). O certificado é conferido em aritmética racional exata, depois de arredondar para 6 casas: relacionados são do tipo tempo e futuros; não relacionados são do tipo espaço. Sem certificado = "não certificada"; reporta-se φ_n só com as certificadas e a cota |φ_n − φ_cert| ≤ 2·W(não certificadas)/W_n.
- Comparação: φ_n contra φ_sorteio (10⁷ sorteios, semente 20261123) nos mesmos n e nos ângulos de E3 e da janela. Reporta-se Δ_n. A contagem não rotulada (peso 1) entra só como verificação.

## C — Mapa de |φ_sorteio| na janela (por último)

- 21 ângulos igualmente espaçados em θ = 2β ∈ [2π/3, 4π/3], com as pontas incluídas.
- n = 6, 8, 10, 12 com M = 10⁸; n = 14, 16, 20, 24 com M = 10⁷. Semente 20261122.
- Q com intervalos por jackknife. Serve para testar as previsões de E e não demonstra H1 para n = 160.

## O que já foi visto antes deste registro

Médias e desvios de B (E1 e primeira etapa de H1); Γ em x = 0,832 e x = 9 com as sementes 20261119, 20261120 e 7777. Em x = 0,832 (θ = 0,045), essas rodadas preferiram decaimento quadrático em n. Por isso a escolha do modelo em E3 usa só a semente nova, e o ângulo 0,045 está na grade junto com outros onze. Nenhum dado com a semente 20261121, 20261122 ou 20261123 existe neste momento.
