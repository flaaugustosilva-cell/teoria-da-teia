# Análise 6: somas torcidas e pontos isolados (centro da janela, todas as ordens)

Data: 21/11/2026. A identidade principal foi proposta pelo Flavio. Script: `scripts/h1b_torcidas.py`. Saída: `torcidas.txt`.

Os níveis estão marcados assim:

- **(D)** demonstrado;
- **(V)** verificado exatamente, com inteiros, para n = 0 a 10;
- **(O)** observação.

Nenhuma conjectura foi registrada.

## 1. Definições

Com s(P) = (−1)^{n+N₀+N₁} e as estatísticas de borda m, D, M e U de `ANALITICO_3.md`:

- **torção inferior:** τ_n = Σ_P s(P)(−1)^{m+D}. A superior é igual, por dualidade;
- **torção dupla:** ω_n = Σ_P s(P)(−1)^{m+D+M+U}. É ela que entra na soma das ordens com menor **e** maior elemento;
- **sem pontos isolados:** τ⁽⁰⁾ e ω⁽⁰⁾ são as mesmas somas restritas às ordens sem pontos isolados.

**Convenções:**

- a ordem vazia contribui com 1, o que dá τ⁽⁰⁾₀ = ω⁽⁰⁾₀ = 1;
- τ⁽⁰⁾₁ = ω⁽⁰⁾₁ = 0, porque o único ponto é isolado.

## 2. Identidades (D, com V para n = 0 a 10)

**Decomposição única.** Toda ordem rotulada se escreve, de um único jeito, como P = R ⊔ I, em que I é o conjunto dos seus pontos isolados e R é o resto.

- R não tem pontos isolados. Um elemento incomparável a todos os de R também é incomparável aos de I, e então seria isolado em P.
- Escolher os j rótulos de I pode ser feito de C(n, j) formas.

**Efeito de cada ponto isolado:**

- s troca de sinal, porque n aumenta e N₀ e N₁ não mudam;
- m e M aumentam 1, porque o ponto é ao mesmo tempo mínimo e máximo;
- D e U não mudam.

**Consequências:**

- **Peso torcido:** s·(−1)^{m+D} fica **invariante**. Logo

  τ\_n = Σ\_j C(n, j) τ⁽⁰⁾\_{n−j}, e a inversa é τ⁽⁰⁾\_n = Σ\_j (−1)^j C(n, j) τ\_{n−j}.

  Em séries geradoras exponenciais, τ = e^{x}·τ⁽⁰⁾.
- **Peso duplamente torcido:** s·(−1)^{m+D+M+U} **troca** de sinal, porque o fator recebe (−1)^{1+1+1}. Logo

  ω\_n = Σ\_j (−1)^j C(n, j) ω⁽⁰⁾\_{n−j}, ou seja, ω = e^{−x}·ω⁽⁰⁾.

  É a mesma regra que vale para a e b.
- **Fórmula exponencial:** como o peso torcido é multiplicativo na união disjunta, τ = exp(τ das conexas). Isso também foi verificado (V).

**Consequência estrutural:** a parte de um ponto E_n de `ANALITICO_5.md` fica inteiramente escrita por meio das ordens sem pontos isolados:

- E_iso por meio de b = a⁽⁰⁾;
- E_ext por meio de τ⁽⁰⁾ (para S_⊥ e S_⊤) e de ω⁽⁰⁾ (para S_⊥⊤).

## 3. Sinal (V e O)

| n | τ_n | τ⁽⁰⁾_n | τ⁽⁰⁾ paralela | τ⁽⁰⁾ série | τ⁽⁰⁾ raiz prima |
| --- | --- | --- | --- | --- | --- |
| 2 | −1 | −2 | 0 | −2 | 0 |
| 3 | +1 | +6 | 0 | +6 | 0 |
| 4 | −53 | −66 | +12 | −102 | +24 |
| 5 | +741 | +1.030 | −120 | +910 | +240 |
| 6 | −849 | −6.130 | +2.580 | −2.350 | −6.360 |
| 7 | +113.737 | +137.158 | −62.160 | +191.758 | +7.560 |
| 8 | −35.405 | −1.014.370 | +1.003.100 | −720.342 | −1.297.128 |
| 9 | +24.052.333 | +28.636.998 | −27.124.776 | +64.822.686 | −9.060.912 |
| 10 | −456.228.137 | −712.369.458 | +555.442.020 | −2.405.612.238 | +1.137.800.760 |

A parte paralela aqui é a das ordens sem pontos isolados. As partes série e raiz prima são conexas e não têm pontos isolados para n ≥ 2.

**A alternância já está em τ⁽⁰⁾ (V, n = 2 a 10).** τ⁽⁰⁾_n·(−1)^{n+1} > 0, então ela **não** é criada pela recombinação binomial.

**A recombinação produz cancelamentos fortes (V)** nos n pares. A parcela dos pontos isolados vale 6,2 vezes |τ₆| e 27,6 vezes |τ₈|, com sinal oposto ao de τ⁽⁰⁾. Em n = 8, τ⁽⁰⁾ = −1.014.370, mas τ = −35.405. Era a cautela que você tinha levantado.

**Onde está a alternância dentro de τ⁽⁰⁾ (O):**

- a **parte série torcida** alterna com sinal (−1)^{n+1} em **todo** n de 2 a 10;
- a parte paralela torcida alterna com o sinal oposto, (−1)^n;
- a parte de **raiz prima** torcida é **irregular**: ela é negativa em n = 9 e positiva em n = 10, contra o padrão.

## 4. Magnitude (V)

| n | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- |
| \|τ_{n−1}\|/\|Prim_{n−1}\| | 6,18 | 0,30 | 1,05 | 0,02 | 0,37 |

A razão é irregular. **Não** há relação quantitativa útil entre τ e Prim: τ é uma informação nova, não uma reescrita de Prim.

## 5. Respostas aos critérios da etapa

1. **A identidade vale para todo n, por demonstração?** Sim (item 2), tanto para τ quanto para ω, com as convenções de fronteira explícitas.
2. **Os valores coincidem exatamente?** Sim, de n = 0 a 10, nas duas direções da inversão e na fórmula exponencial.
3. **A alternância fica explicada pelas ordens sem pontos isolados?** Só em parte.
   - Ela já existe em τ⁽⁰⁾.
   - Dentro de τ⁽⁰⁾, quem a carrega é a parte série torcida.
   - A parte prima torcida é irregular, e a alternância de τ⁽⁰⁾ resulta de a parte série dominar as outras.
   - **Explicar** por que a parte série torcida alterna continua em aberto.
4. **Há relação quantitativa útil com Prim_n?** Não, por ora. τ é apenas uma nova descrição.

## 6. Observação estrutural (D)

A entrada livre de cada tamanho **não** é só o número Prim_n. É o vetor de **16 somas refinadas** Prim_n[σ], com σ = (m, D, M, U) mod 2.

- As somas não torcidas, as torcidas τ e as duplamente torcidas ω são três dos 16 "caracteres" desse vetor, isto é, as combinações Σ_σ Prim_n[σ](−1)^{χ·σ}.
- A soma ordinal mistura esses caracteres: por exemplo, {⊥} ⊕ P transforma o peso torcido de P em s(P)(−1)^{D(P)}, que é outro caráter.

Por isso, controlar o sinal no centro exige entender os 16 caracteres das ordens de raiz prima, e não um só número por tamanho. Os dados até n = 10 mostram que eles são irregulares entre si.
