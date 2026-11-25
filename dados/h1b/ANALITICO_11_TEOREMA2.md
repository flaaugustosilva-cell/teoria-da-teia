# Teorema 2: a forma assintótica exata do resíduo das ordens de altura ≤ 2

Data: 25/11/2026. Conjectura registrada antes da prova: `CONJECTURA_RESIDUO.md` (commit 5a66aae). Conferência numérica das peças em valores **novos** de θ: `scripts/h1b_teorema2_confere.py` → `teorema2_confere.txt`. Tabela: `teorema2_tabela.txt`.

**Status: (D) demonstrado.** O resultado é mais forte que a conjectura C-R: não precisa da hipótese de k\* único.

## Notação

- **Parâmetros:** θ ∈ (2π/3, 4π/3), w = e^{−iθ}, y = 1 + w e |y| = 2|cos(θ/2)| < 1.
- **Soma exata:** S_n = e^{−iθn}·a_n = Σ das ordens rotuladas de altura ≤ 2 de w^{N₀}.
- **Fórmula já demonstrada:** S_n = Σ_k T_k, com T_k = C(n, k)(y^k − 1)^{n−k}.
- **Taxas:** ρ_k = |1 − y^k| e ρ\* = max_{k≥1} ρ_k. A* é o conjunto dos k que atingem o máximo, e k̂ = max A\*.

## Enunciado

**Teorema 2.** Para θ ∈ (2π/3, 4π/3), θ ≠ π:

1. ρ\* > 1, e A\* é finito.
2. S_n / (2·T_{k̂}) → 1 quando n → ∞. A convergência é exponencial se A\* = {k̂}, e pelo menos como 1/n se houver empate.
3. Portanto |a_n| = 2·C(n, k̂)·ρ\*^{n−k̂}·(1 + o(1)) e lim (1/n) ln|a_n| = ln ρ\*.
4. ρ\* < 2. A taxa real de crescimento é estritamente menor que a cota 3ⁿ do Teorema 1.

## Prova

**Lema A (fórmula dupla).**

- **Enunciado:** S_n = Σ_{b,t ≥ 0, b+t ≤ n} M(b,t), com M(b,t) = n!/(b!·t!·r!)·(−1)^r·y^{bt} e r = n − b − t.
- **Prova:** a função geradora exponencial de S_n é Σ_k (x^k/k!)·e^{x(y^k − 1)} = e^{−x}·Σ_k (x^k/k!)·e^{x y^k}. Expanda e^{x y^k} = Σ_t (x y^k)^t / t! e tire o coeficiente de xⁿ/n!. ∎

**Lema B (linhas e colunas).**

- **Enunciado:** para b fixo, Σ_t M(b,t) = T_b. Para t fixo, Σ_b M(b,t) = T_t.
- **Prova:** Σ_t M(b,t) = C(n,b)·Σ_t C(n−b, t)(−1)^{n−b−t}(y^b)^t = C(n,b)(y^b − 1)^{n−b}, pelo binômio. A segunda vem da simetria M(b,t) = M(t,b). ∎

**Lema C (decomposição exata).**

- **Enunciado:** para todo K ≥ 0,

  S_n = 2·Σ_{k=0}^{K} T_k − D_K + R_K,

  em que D_K = Σ_{b,t ≤ K} M(b,t) e R_K = Σ_{b,t > K} M(b,t).
- **Prova:** some as linhas b ≤ K (Lema B). As linhas b > K se dividem em duas partes:
  - a parte com t ≤ K, que é igual a Σ_{t≤K} T_t − D_K (Lema B, colunas);
  - a parte com t > K, que é R_K. ∎

**Lema D (cotas).** Como |y| < 1:

- **Cota de D_K:** n!/(b!t!r!) ≤ n^{b+t}, então |D_K| ≤ (K+1)²·n^{2K}, polinomial em n.
- **Cota de R_K:**
  - se b, t ≥ K+1, então bt ≥ (K+1)·max(b,t) ≥ (K+1)(b+t)/2;
  - logo |y|^{bt} ≤ q^{b+t}, com q = |y|^{(K+1)/2};
  - então |R_K| ≤ Σ_{todos b,t} n!/(b!t!r!)·q^b q^t = (1 + 2q)ⁿ. ∎

**Lema E (as taxas).**

- **Fatos:** ρ_0 = 0, e T_0 = 0 para n ≥ 1. ρ_1 = |w| = 1. ρ_2 = |1 − (1+w)²| = |2 + w| = √(5 + 4 cos θ), que é > 1 para θ ≠ π. E ρ_k → 1 quando k → ∞, porque |y| < 1.
- **Consequência:** ρ\* ≥ ρ_2 > 1, e o máximo é atingido num conjunto finito A\*.
- **Cota superior:** para k ≥ 2, ρ_k ≤ 1 + |y|^k ≤ 1 + |y|² < 2. ∎

**Fim da prova.**

1. **Escolha de K:** tome K ≥ k̂ com 1 + 2|y|^{(K+1)/2} < ρ\*. Isso é possível porque |y| < 1 e ρ\* > 1.
2. **Separação dos termos:** pelo Lema C, S_n = 2·T_{k̂} + E_n, com

   E_n = 2·Σ_{k ∈ A\*, k < k̂} T_k + 2·Σ_{k ≤ K, k ∉ A\*} T_k − D_K + R_K.

3. **Cada parte de E_n é pequena perto de T_{k̂}.** Note que |T_{k̂}| = C(n, k̂)·ρ\*^{n−k̂}.
   - **Empates (k ∈ A\*, k < k̂):** |T_k / T_{k̂}| = [C(n,k)/C(n,k̂)]·ρ\*^{k̂−k} = O(n^{k−k̂}) = O(1/n).
   - **Fora do máximo (k ∉ A\*, k ≤ K):** com ρ′ = max dessas taxas < ρ\*, a razão é O(n^K (ρ′/ρ\*)ⁿ), que vai a zero exponencialmente.
   - **D_K:** é polinomial, e ρ\*ⁿ cresce exponencialmente.
   - **R_K:** a razão é O((1 + 2q)ⁿ / ρ\*ⁿ), que vai a zero exponencialmente pela escolha de K.
4. **Conclusão:** E_n / T_{k̂} → 0, o que prova o item 2. Os itens 3 e 4 seguem dos Lemas E e da Stirling elementar (1/n)ln C(n, k̂) → 0. ∎

## Conferências (V; não fazem parte da prova)

Feitas em θ = 2,25; 2,6; 2,8; 3,3; 3,9, todos **novos** (3,9 está do lado θ > π), com n = 30, 60, 120 e 240.

- **Lema A e Lema C:** erro relativo ≤ 10⁻⁶⁸.
- **Lema B (linha 2):** erro ≤ 10⁻⁷⁴.
- **Cota de R_K:** respeitada em todos os 20 casos.
- **A razão S/(2T_{k̂}) em n = 240:**

| θ | razão |
| --- | --- |
| 2,25 | 1,0000037 |
| 2,6 | 1,0 (erro 10⁻¹¹) |
| 2,8 | 1,0000002 |
| 3,3 | 0,953 (perto do centro, onde a convergência é lenta) |
| 3,9 | 1,0003 |

## A forma do resíduo ao longo da janela

| θ | k̂ | ρ\* | ln ρ\* |
| --- | --- | --- | --- |
| 2,112 | 3 | 1,955 | 0,670 |
| 2,234 | 3 | 1,665 | 0,510 |
| 2,304 | 2 | 1,524 | 0,422 |
| 2,513 | 2 | 1,328 | 0,284 |
| 2,792 | 2 | 1,114 | 0,108 |
| 3,072 | 2 | 1,005 | 0,005 |

- **De θ ≈ 2,30 até π (e, pelo espelho, de π até ≈ 3,98):** k̂ = 2 e ρ\* = √(5 + 4 cos θ).
- **Mais perto das bordas:** k̂ = 3 na grade testada.

## O que o teorema diz e o que não diz (O)

- **Diz:** a soma exata das teias ruins de altura ≤ 2 é, para n grande, o dobro da soma das ordens com k̂ (2 ou 3) minimais. O dobro corresponde às ordens com k̂ minimais e às com k̂ maximais. Essa soma cresce como n^{k̂}·ρ\*ⁿ.
- **Corrige a imagem anterior:** o resíduo não vem das camadas equilibradas (a sela da literatura). Vem do canto das camadas mais desiguais.
- **Barra para o H1\*:** no nível rotulado, as teias boas precisam superar 2·C(n, k̂)·ρ\*ⁿ (com ρ\* < 2), e não 3ⁿ. Dividindo por n!, como no 𝒵, o resíduo vale ~ρ\*ⁿ/n!.
- **Não diz:**
  - nada sobre θ = π (onde a_n = −1) nem sobre as bordas (|y| = 1, onde a cota de R_K não serve);
  - nada sobre as ordens ruins de altura ≥ 3;
  - nada sobre se as teias boas superam essa barra.
