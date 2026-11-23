# Análise 10: κ ao trocar um ponto do quociente por um módulo de 2 elementos

Data: 23/11/2026. Script: `scripts/h1b_modulo2.py`. Saída: `modulo2.txt`. População: todas as ordens, θ = π.

Os níveis estão marcados assim:

- **(D)** demonstrado;
- **(V)** verificado exatamente;
- **(O)** observação.

Nenhuma conjectura foi registrada.

**Correção:** na mensagem anterior falei em "seis módulos de 2 ou 3 elementos". O certo são **7** tipos (não rotulados): 2 de tamanho 2 (cadeia e anticadeia) e 5 de tamanho 3. Não havia restrição escondida; foi erro de contagem.

## 1. Fator local condicionado à posição (D)

Parto da fórmula de `ANALITICO_9.md` para P = Q[M₁…M_k] e junto os termos em que aparecem as estatísticas do módulo Mᵢ: m, D, X (máximos), U, s, e e = [|Mᵢ| = 1]. O resultado é

  κ(P) = s(Mᵢ)·(−1)^{α·m + β·D + γ·X + δ·U + ε·e} · R,

em que R não depende de Mᵢ.

**Os coeficientes** (mod 2) dependem só da posição de qᵢ em Q e dos módulos vizinhos. Quando os outros módulos são pontos (m = X = e = 1, D = U = 0), eles ficam assim:

- **α** = (coberturas abaixo de qᵢ) + (pontos j com exatamente um ponto entre j e qᵢ, abaixo) + [qᵢ tem exatamente um ponto abaixo];
- **β** = (coberturas abaixo) + [qᵢ é mínimo];
- **γ** = (coberturas acima) + (pontos com exatamente um ponto entre, acima) + [qᵢ tem exatamente um ponto acima];
- **δ** = (coberturas acima) + [qᵢ é máximo];
- **ε** = (pares j < qᵢ < l em que qᵢ é o único ponto entre eles) + #{j : qᵢ é o único abaixo de j} + #{j : qᵢ é o único acima de j}.

**De onde vem cada termo.** Cada termo vem de uma das duas regras de pares cruzados do `ANALITICO_9.md`, ou das fórmulas de D(P) e U(P):

- coberturas: X·m + U·m + X·D;
- par com um único ponto unitário no meio: X·m;
- "exatamente um ponto unitário abaixo ou acima": entra em D ou em U.

**Consequência.** Trocar o ponto qᵢ por um módulo M multiplica κ por ρᵢ(M) = −w_c(M)·(−1)^{α+γ+ε}, em que w_c(M) = s(M)(−1)^{c·σ(M)} e c = (α, β, γ, δ). Somando sobre todos os módulos de tamanho t, aparece o **caráter Â_t[c] de todas as ordens de tamanho t**. O caráter local c **muda de posição para posição**.

**Módulos de 2 elementos:**

- **anticadeia** (1 rotulagem; s = +1, estado par): ρ = −(−1)^{α+γ+ε};
- **cadeia** (2 rotulagens; s = −1, estado (1,1,1,1)): ρ = (−1)^{β+δ+ε} para cada rotulagem.

## 2. Verificação (V)

A parte "exatamente um módulo de 2 elementos, o resto pontos" da raiz prima de κ em n é prevista pela fórmula

  (n!/2)·Σ_{Q estritamente prima com k = n−1} (1/|Aut Q|)·κ(Q)·Σᵢ ρᵢ.

A previsão coincide exatamente com a contagem direta nos dados, **separadamente para cadeia e para anticadeia**, em todo n de 5 a 10.

| n | anticadeia | cadeia | total | sinal em relação a (−1)^n |
| --- | --- | --- | --- | --- |
| 5 | 0 | −480 | −480 | + |
| 6 | +1.800 | −2.160 | −360 | **−** |
| 7 | −93.240 | −5.040 | −98.280 | + |
| 8 | +1.646.400 | +389.760 | +2.036.160 | + |
| 9 | −108.017.280 | +33.626.880 | −74.390.400 | + |
| 10 | +5.151.988.800 | −1.363.219.200 | +3.788.769.600 | + |

## 3. Quando a substituição troca o sinal (D)

Somando cadeia (com peso 2) e anticadeia, o fator líquido sobre κ(Q) numa posição é:

| β+δ+ε mod 2 | α+γ+ε mod 2 | fator líquido | efeito |
| --- | --- | --- | --- |
| 0 | 0 | +1 | não troca |
| 0 | 1 | +3 | não troca |
| 1 | 0 | −3 | troca |
| 1 | 1 | −1 | troca |

**A paridade de β + δ + ε decide** se a substituição troca o sinal, porque a cadeia entra com duas rotulagens. Em termos de Q:

  β + δ + ε = (coberturas abaixo + coberturas acima) + [mínimo] + [máximo] + (pares em que qᵢ é o único ponto do meio) + (vizinhos que têm qᵢ como único ponto abaixo ou acima).

**A regra não se reduz a um fator que dependa só do módulo.** A mesma cadeia, ou a mesma anticadeia, troca o sinal em algumas posições e não em outras. A sua precaução estava certa.

## 4. De onde vem o sinal do total (O)

As posições dos quatro tipos aparecem em números parecidos. Em n = 10 são 94.349, 71.160, 83.990 e 77.435 posições.

O sinal do total resulta de como κ(Q) se distribui entre os tipos. Em n = 10:

| tipo | soma de κ(Q) ponderada | × fator líquido | contribuição |
| --- | --- | --- | --- |
| (0,0) | −2,36×10⁹ | +1 | −2,36×10⁹ |
| (0,1) | +6,6×10⁸ | +3 | +1,99×10⁹ |
| (1,0) | −1,57×10⁹ | −3 | +4,71×10⁹ |
| (1,1) | +5,6×10⁸ | −1 | −5,6×10⁸ |

O total é +3,79×10⁹. Ele acompanha (−1)^n porque as posições que trocam o sinal com fator 3 pesam mais. Isso depende de **como o sinal de κ(Q) se correlaciona com o tipo da posição**, o que **não está explicado**.

Em n = 6 a transmissão **falha**: o total é −360, contra o padrão.

## 5. Respostas às cinco etapas pedidas

1. **Cadeia** (D, V): fator (−1)^{β+δ+ε} por rotulagem, com 2 rotulagens.
2. **Anticadeia** (D, V): fator −(−1)^{α+γ+ε}.
3. **Comparação:** a cadeia lê a paridade de β + δ + ε e a anticadeia a de α + γ + ε. As duas compartilham ε, a parte que depende de q ser o único ponto do meio ou o único vizinho.
4. **O que de Q é necessário:** as coberturas acima e abaixo, ser mínimo ou máximo, os pontos a distância 2 com um único ponto no meio, ter exatamente um ponto abaixo ou acima, e o número de vizinhos para os quais qᵢ é o único ponto abaixo ou acima. **Isso basta** quando os outros módulos são pontos. Quando não são, entram também as estatísticas dos módulos vizinhos, pela fórmula geral do item 1.
5. **Tamanho 3:** ainda não, conforme a sequência combinada.

**Qual propriedade estrutural faz a transmissão acontecer:** o fator líquido troca o sinal quando a paridade de β + δ + ε é ímpar.

**Quando deixa de acontecer:**

- em cada posição em que essa paridade é par;
- no total, quando o peso de κ(Q) nessas posições prevalece, como em n = 6.
