# Decisões de 19/11/2026 (23:57): H1\* como hipótese central e execução de C

Flavio Augusto da Silva · registrado antes de qualquer rodada da entrega C. O horário do commit é a prova.

## 1. H1 e H1\*

**H1 (condição suficiente, refutada).** |𝒵_boa(n, x)| ≥ 1 em toda a janela 1. É falsa em n = 5 (mínimo 0,252, em x = 6,27) e em n = 8 (mínimo 0,539, em x = 7,24). São contraexemplos exatos, conferidos em 60 dígitos ([`RESULTADOS_B.md`](RESULTADOS_B.md)). H1 fica documentada assim e não será reformulada para ser salva.

**H1\* (hipótese central do argumento do E1).** Para todo x na janela 1 (π/3 < β < 2π/3):

R_n(x) = |𝒵_ruim(n, x)| / |𝒵_boa(n, x)| < 1

- 𝒵_ruim é a soma de e^(iS) sobre as teias de altura ≤ 2 e 𝒵_boa, sobre as teias de altura ≥ 3 que cabem em Minkowski 3+1. As duas usam peso 1/|Aut| (soma rotulada dividida por n!), ação de Benincasa–Dowker 4D com ε = 1.
- **Estado:** demonstrada para n = 5, 6, 7 e 8, em toda a janela, com cotas rigorosas (razão máxima de 0,570, 0,075, 0,041 e 0,278).
- **Isso é um resultado finito, não uma confirmação assintótica.** Os quatro valores não mostram tendência. O conjunto das teias boas muda de composição com n: para n ≤ 8 ele inclui todas as teias de altura ≥ 3, e para n grande, pela cota de Warren, só uma fração ínfima delas. Nada sobre n grande pode ser lido destes números.
- **Para n = 40 a 160:** |𝒵_ruim| é conhecido exatamente (E1), mas |𝒵_boa| não. H1\* está em aberto nesses tamanhos.

## 2. Entrega C: executada como registrada, com interpretação restrita

Os parâmetros são os de [`PREREGISTRO.md`](PREREGISTRO.md), seção C, sem mudança: 21 ângulos igualmente espaçados em θ = 2β ∈ [2π/3, 4π/3], pontas incluídas; n = 6, 8, 10, 12 com M = 10⁸ e n = 14, 16, 20, 24 com M = 10⁷; semente 20261122.

**Interpretação restrita (decisão do autor):** C estuda só o conjunto produzido pelo sorteio. A entrega B mostrou que esse conjunto é diferente do objeto de H1\* (variação total entre as distribuições de B de 0,45 a 0,57; diferenças de fase de até 790 erros). Portanto C **não** será usada como evidência a favor ou contra H1\*. A pergunta de C é: na janela, como a fase média do sorteio se comporta com n?

**Detalhes de execução fixados agora** (o registro original não os especificava):

- Sorteio igual ao das etapas anteriores: diamante 3+1, condicionado a altura ≥ 3, função `lote` de `scripts/h1_robustez.py`. M conta sorteios, válidos ou não.
- Gerador: `default_rng([20261122, 4, n])`, lotes de 20.000.
- Guarda-se o histograma de B em cada um de 50 blocos contíguos. Q (estimador sem viés de |φ_sorteio|²) e o seu erro saem de jackknife sobre esses 50 blocos.
- Intervalo de 95%: Q ± 1,96·erro. Ponto "resolvido" se Q > 4·erro.
- Como E deu E-c, não há previsão de E a testar. C é só descritivo: não há ajuste de modelo nem veredito. Reporta-se tudo, inclusive os pontos não resolvidos.

## 3. Próximas etapas (ordem do autor)

1. H1\* registrada (este arquivo).
2. C executada como acima.
3. Consolidar E (mecanismo de cancelamento no conjunto sorteado).
4. Planejar a próxima etapa exata (φ_n em n maior), com novo pré-registro e estimativa realista de custo.
5. Buscar um argumento analítico para H1\* em n geral, que não dependa de extrapolar resultados finitos.

C não deve atrasar os itens 4 e 5. As teias ruins de três camadas continuam fora.
