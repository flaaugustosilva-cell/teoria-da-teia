# Consolidação de E (E2) — pré-registro

Flavio Augusto da Silva · registrado em 20/11/2026, antes de gerar qualquer dado desta etapa. O horário do commit é a prova.
Item 3 da ordem do autor ([`DECISOES_H1STAR.md`](DECISOES_H1STAR.md)): entender o mecanismo de cancelamento **no conjunto do sorteio**.

## Escopo

Tudo aqui é sobre o sorteio (diamante 3+1, altura ≥ 3), que a entrega B mostrou ser um objeto diferente do de H1*. **Nenhum resultado desta etapa é evidência sobre H1*.** O nível máximo é evidência numérica sobre o sorteio.

## O que se testa

Os três achados exploratórios de E ([`RESULTADOS_E.md`](RESULTADOS_E.md)), agora com dados novos e critérios fixados antes:

- **T1, colapso em u.** A fase depende só de u = σ_n·θ, em que σ_n é o desvio de B no tamanho n?
- **T2, núcleo gaussiano.** Para u ≤ 1, |φ|² ≈ e^(−u²)?
- **T3, cauda não gaussiana.** Para u ≥ 2, |φ|² fica claramente acima de e^(−u²)?
- **T4, origem da variância.** A variância de B vem de N₁ e N₂?

## Dados

- Diamante 3+1, condicionado a altura ≥ 3, semente nova **20261124**. O sorteio é o mesmo de E (`sorteia` de `scripts/h1_robustez.py`, ordenação no tempo, ação de Benincasa–Dowker 4D com ε = 1).
- n = 10, 20, 40, 80, 160 com M = 1.000.000, 1.000.000, 1.000.000, 200.000 e 50.000 sorteios (os mesmos de E).
- Guardam-se, por teia válida, N₀, N₁, N₂, N₃ e B. Cada tamanho é gravado em disco ao terminar.

## Grade de ângulos

u = 0,1; 0,2; …; 4,0 (40 valores). Para cada n, θ = u/σ̂_n, em que σ̂_n é o desvio de B calculado nos próprios dados. Essa é uma transformação fixada agora, não uma escolha feita depois de ver as fases. A grade é a mesma em u para todos os n, então as comparações de T1 são diretas, sem interpolação.

## Estimador e erro

Q = (|S|²/N − 1)/(N − 1), sem viés para |φ|². Erro = o maior entre o jackknife em 50 blocos e √2/N (lição da entrega C: perto de zero, o jackknife subestima). "Resolvido" se Q > 4·erro. Para ln Q, o erro é erro/Q.

## Critérios

- **T1:** compara-se ln Q entre todos os pares de n = 20, 40, 80, 160, no mesmo u, onde os dois estão resolvidos. Confirmado se ≥ 80% das comparações ficarem dentro de 3 erros combinados. Com menos de 10 comparações, inconclusivo.
- **T2:** pontos resolvidos com u ≤ 1, todos os n. Confirmado se ≥ 80% tiverem |Q − e^(−u²)| ≤ 3·erro.
- **T3:** pontos resolvidos com u ≥ 2, todos os n. Confirmado se ≥ 80% tiverem Q − e^(−u²) > 3·erro. Com menos de 5 pontos, inconclusivo.
- **T4:** com B = n − N₀ + 9N₁ − 16N₂ + 8N₃, a parte de N₁ e N₂ é V₁₂ = 81·Var(N₁) + 256·Var(N₂) − 288·Cov(N₁, N₂). Confirmado se V₁₂/Var(B) ≥ 0,80 em n = 40, 80 e 160. Também se reporta a decomposição completa.

Cada teste tem veredito próprio: **confirmado**, **não confirmado** ou **inconclusivo**. Reporta-se tudo, inclusive os pontos não resolvidos e os resultados desfavoráveis.

## Já visto antes deste registro

Os dados e a análise exploratória de E (semente 20261121), que motivaram T1 a T4. Nenhum dado com a semente 20261124 existe neste momento.
