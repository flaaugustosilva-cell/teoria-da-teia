# Exploratório: de onde vem o resíduo e^{cn} das ordens de altura ≤ 2

Data: 25/11/2026. Script: `scripts/h1b_residuo_assintotico.py`. Saída: `residuo_assintotico.txt`.

**Status:** exploração, **não** é teste pré-registrado e **não** é conjectura registrada. Nada aqui foi usado para ajustar parâmetros. Se o resultado da seção 3 for virar enunciado, ele precisa de aprovação antes, como as outras conjecturas.

Os níveis estão marcados assim:

- **(D)** demonstrado;
- **(V)** verificado numericamente com alta precisão, sem prova;
- **(O)** observação ou leitura.

## 1. A pergunta

A soma exata rotulada das ordens de altura ≤ 2 é a_n = e^{iθn}·S_n, com

  S_n = Σ_a T_a, T_a = C(n, a)·(y^a − 1)^{n−a}, y = 1 + e^{−iθ}.

Dentro da janela, |a_n| cresce como e^{cn} (`COMPARACAO_LITERATURA.md`, seção 3). Quais ordens produzem esse crescimento?

## 2. O que cada termo conta (D)

- **T_a é a soma com fase das ordens com exatamente a elementos minimais.**
- **Prova:** escolha o conjunto A dos minimais (C(n,a) jeitos). Numa ordem de altura ≤ 2, cada um dos outros n − a elementos fica acima de um subconjunto **não vazio** de A, e de nada mais. A soma das fases e^{−iθ|S|} sobre os subconjuntos não vazios S de A dá y^a − 1. Os elementos são independentes, o que dá a potência n − a.
- **Espelho:** a inversão da ordem (trocar ≺ por ≻) não muda N₀. Para altura ≤ 2, B = n − N₀ não muda. Então a soma das ordens com exatamente k **maximais** é igual a T_k.

## 3. O resultado numérico (V)

**Conferência da precisão:** em θ = π, a_n = −1 exato para n = 40, 160, 320 e 640 (resíduo ≤ 10⁻⁵⁹). Uma primeira rodada com precisão fixa deu lixo em n = 320, foi descartada e está registrada aqui. A precisão agora é de 0,7n + 40 dígitos.

**O observado:** S_n / (2·T_{k\*}) → 1, em que k\* é o valor de k que maximiza ρ_k = |1 − y^k|.

| θ | k\* | ρ_{k\*} | S/(2T_{k\*}) em n = 160 | em n = 320 | em n = 640 |
| --- | --- | --- | --- | --- | --- |
| 2,2 | 3 | 1,741 | 1,0 (erro 7×10⁻⁷) | 1,0 (6×10⁻¹²) | 1,0 (9×10⁻²²) |
| 2,3 | 3 | 1,5286 | 0,974 | 1,0013 | 1,0022 |
| 2,4 | 2 | 1,432 | 1,0038 | 0,999999 | 1,0 (9×10⁻¹⁵) |
| 2,5 | 2 | 1,340 | 1,00001 | 1,0 (10⁻¹³) | 1,0 (7×10⁻²⁶) |
| 2,7 | 2 | 1,176 | 1,0 (10⁻⁶) | 1,0 (6×10⁻¹⁴) | 1,0 (2×10⁻²⁹) |
| 2,9 | 2 | 1,056 | 0,990 | 1,00004 | 1,0 (4×10⁻¹²) |
| 3,05 | 2 | 1,008 | 0,27 | 0,62 | 0,93 |
| 2,114 | 3 | 1,950 | 10⁷ (longe) | −128 (longe) | 0,9997 |

**Onde converge devagar:**

- **Perto da borda (θ = 2,114):** |y| ≈ 0,98, então muitos k têm ρ_k parecidos. A convergência só aparece em n = 640.
- **Em θ = 2,3:** os dois maiores ρ estão quase empatados (1,5286 e 1,528). A razão oscila perto de 1.
- **Perto do centro (θ = 3,05):** ρ_2 ≈ 1, e os fatores polinomiais competem. A convergência é lenta.

**O que se lê daí:**

- **Taxa de crescimento:** (1/n) ln|a_n| → ln ρ_{k\*}, devagar, porque C(n, k\*) é polinomial em n. Para k\* = 2, ρ = √(5 + 4 cos θ).
- **No centro θ = π:** todos os ρ_k valem 1 e a_n = −1. É o caso degenerado.
- **Comparação com o Teorema 1 (|a_n| ≤ 3ⁿ):** pela observação, o crescimento real é no máximo da ordem de n^{k\*}·ρⁿ, com ρ ≤ 1 + |y|² ≤ 2 na janela. **Isso não está provado:** faltaria uma cota para o resto (as ordens com pelo menos k\* + 1 minimais e maximais). **Atualização (25/11): agora está provado.** Ver `ANALITICO_11_TEOREMA2.md`.

## 4. Leitura (O)

- **O resíduo vem de um canto de entropia desprezível.** São as ordens com 2 ou 3 elementos numa camada e todo o resto na outra. A sela de Loomis–Carlip olha o canto oposto, das camadas equilibradas.
- **Por que essas ordens não se cancelam:** cada elemento de cima escolhe um subconjunto não vazio de só k\* elementos de baixo. Há poucas escolhas, então quase não há interferência, e |y^{k\*} − 1| > 1.
- **Consequência para o H1\*:** a barra que as teias boas precisam superar (no nível rotulado) é da ordem de 2·C(n, k\*)·ρⁿ, e não de 3ⁿ.
- **Cuidado:** isto vale só para as ordens de altura ≤ 2. As outras ordens ruins (altura ≥ 3 não imersíveis) não entram aqui.
