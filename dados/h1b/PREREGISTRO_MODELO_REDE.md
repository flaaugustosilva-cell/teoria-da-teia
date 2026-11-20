# Pré-registro: modelo gaussiano de rede para a estrutura fina de 𝒵(θ)

Data: 20/11/2026. Este documento foi publicado **antes** de qualquer cálculo do modelo sobre os dados das teias.

Antes deste registro só foram feitas duas coisas, e nenhuma delas usa as teias:

- o teste da implementação em distribuições sintéticas (seção 2.6);
- o sorteio da família B de controles, que é feito só com uma semente fixa (seção 4.1).

Script de análise, fixado neste commit: `scripts/h1b_modelo_rede.py`, sha256 `8d0c31b743dc5870ac672163b232c5aab2f11ff390c31b1f43116188acc32a0b`.

## 0. Status do que está sendo testado

- O modelo é uma **hipótese explicativa**, não um resultado.
- A estabilidade de θ\* (de 0,740 a 0,742 para n = 5 a 10) é uma **observação exploratória**, registrada em `EXPLORATORIO_ESTRUTURA_FINA.md`. Ainda não sabemos se ela vem da aritmética dos coeficientes da ação ou de alguma propriedade combinatória das teias.
- As duas explicações não se excluem. O modelo afirma que a estrutura fina é fixada pela aritmética de c **junto com** a média e a covariância das contagens. Média e covariância já são propriedades combinatórias das teias, só que de segunda ordem. Um acerto do modelo diria que **basta a informação de segunda ordem**, não que a combinatória é irrelevante.
- Mesmo que o modelo funcione, isso **não demonstra que a distribuição das contagens é gaussiana**. Demonstra no máximo que uma gaussiana discreta com os momentos observados explica aspectos importantes da transformada. A origem dessa distribuição continua sendo uma questão matemática aberta.

## 1. Pergunta principal

A distribuição de N = (N₀, N₁, N₂, N₃) pode ser aproximada por uma gaussiana discreta em ℤ⁴ cuja transformada explica a estrutura fina de 𝒵(θ)?

Aqui N_k é o número de pares x < y com exatamente k elementos estritamente entre eles.

## 2. Modelo matemático

### 2.1 Notação

- c = (−1, 9, −16, 8), de modo que B = n + c·N.
- ρ(N) é a soma de 1/|Aut| sobre as classes com vetor de contagens N.
- W = Σ_N ρ(N).
- φ(θ) = 𝒵(θ)/W = e^{iθn} χ(θc), em que χ(t) = Σ_N ρ(N) e^{i t·N} / W, com t ∈ ℝ⁴.
- Convenção da transformada: e^{+i t·N}. Como m percorre todo o ℤ⁴, que é simétrico, o sinal de 2πm não importa.

### 2.2 Gaussiana discreta e normalização

A gaussiana discreta com parâmetros (μ, Σ) é

  g(N) = exp(−½ (N−μ)ᵀ Σ⁻¹ (N−μ)) / Ξ, para N ∈ ℤ⁴,

em que Ξ normaliza a soma sobre a rede. Pela fórmula de soma de Poisson,

  Σ_{N∈ℤ⁴} exp(−½ (N−μ)ᵀ Σ⁻¹ (N−μ)) e^{i t·N} = (2π)² (det Σ)^{1/2} Σ_{m∈ℤ⁴} F(t − 2πm),

com F(u) = exp(i u·μ − ½ uᵀ Σ u). Dividindo pelo mesmo resultado em t = 0, a constante (2π)²(det Σ)^{1/2} se cancela e fica

  χ_mod(t) = Σ_m F(t − 2πm) / D,  D = Σ_m F(−2πm) = Σ_m cos(2π m·μ) exp(−2π² mᵀΣm).

O denominador D é real e **não é suposto igual a 1**: ele é calculado e relatado para cada n.

A previsão do modelo é φ_mod(θ) = e^{iθn} χ_mod(θc).

### 2.3 Parâmetros

- μ e Σ são a média e a covariância empíricas de N, com peso 1/|Aut|, na população oficial de cada n, **separadamente**.
- **Nenhum ajuste.** Os parâmetros de uma gaussiana discreta não coincidem exatamente com os momentos dela. A diferença é da ordem dos termos m ≠ 0 de D. Mesmo assim, usamos os momentos empíricos diretamente como parâmetros, porque reajustá-los seria uma escolha livre. D − 1 é relatado.

### 2.4 Truncamento da soma sobre m

- Entram todos os m com ½ uᵀΣu ≤ L, em que u = θc − 2πm e L = 50.
- A enumeração é completa por construção:
  - escreve-se m = round(θc/2π) + K;
  - cada coordenada de K fica limitada por ⌈√(2L (Σ⁻¹)_jj)/(2π)⌉ + 1;
  - descartam-se os K com (2π)² λ_min (|K| − 1)² > 2L, que não podem cumprir a condição para nenhum resto em [−½, ½]⁴.
- **Verificação:** tudo é repetido com L = 70. O relatório traz a maior variação relativa nos pontos em que |φ_mod| ≥ 10⁻¹².
- **Regra:** se essa variação passar de 10⁻³ para algum vetor, o vetor é classificado como "não testável (truncamento)". Ele continua contando no denominador.

### 2.5 Degenerescência

Se Σ for singular, a soma de rede não converge na direção nula. As regras são:

- se λ_min(Σ) < 10⁻⁶ λ_max(Σ), o modelo é declarado **indefinido** naquele n;
- se o conjunto de deslocamentos candidatos passar de 5×10⁶, o modelo é declarado **não computável** naquele n;
- nos dois casos, todas as previsões são **inconclusivas** naquele n.

Os autovalores de Σ são relatados para cada n.

### 2.6 Contínuo × discreto e erro numérico

- A fórmula da seção 2.2 é **exata** para a gaussiana discreta, sem aproximação contínua.
- Há só duas aproximações:
  - (a) ρ ≈ gaussiana discreta, que é justamente a hipótese testada;
  - (b) o truncamento da seção 2.4, que é controlado.
- **Somas exatas:**
  - são agregadas por valor de B′ = n + c′·N, com pesos inteiros L = n!/|Aut|, que são exatos;
  - são avaliadas em precisão dupla;
  - o erro relativo a W fica abaixo de (K + 2)·1,1×10⁻¹⁶, em que K é o número de valores distintos de B′ (relatado). Com K ≤ 1500, isso dá ≤ 2×10⁻¹³, abaixo do piso de 10⁻¹² usado nas métricas.
- **Teste da implementação**, feito em dados sintéticos antes deste registro:
  - a distribuição sintética é exatamente uma gaussiana discreta, com autovalores (0,6; 1,5; 3; 5) e (0,15; 0,4; 2; 6), este último com efeitos de rede fortes;
  - foram testados quatro vetores c;
  - o maior erro |exato − modelo| foi de 9×10⁻¹⁵, contra o limite exigido de 10⁻¹⁰;
  - as contagens N foram conferidas na cadeia de 5 elementos e na anticadeia.
- **Validação dos dados**, que é condição para continuar:
  - o B recalculado a partir de N tem de ser igual ao B armazenado em **todas** as classes, senão a execução aborta;
  - o W de cada n tem de coincidir com o publicado.

## 3. Populações

- **Oficial**, a única usada aqui:
  - n = 5 a 10;
  - teias de altura ≥ 3, incorporáveis em Minkowski 3+1 (para n ≤ 10, todas as classes de altura ≥ 3 são incorporáveis, como já certificado);
  - peso 1/|Aut(C)|.
- **Auxiliar (n = 11): não entra neste teste.** Os dados de n = 11 guardam apenas (B, altura, conexidade), não N₀ a N₃. Gerá-los seria um cálculo novo, fora deste registro. Um teste auxiliar futuro precisaria de um pré-registro próprio e seria relatado separado.
- Não se junta nenhuma série em uma curva única. Cada n tem os seus próprios μ e Σ, e os critérios são aplicados em n = 9 e em n = 10 separadamente. Os tamanhos n = 5 a 8 são relatados de forma descritiva.

## 4. Previsões e critérios

**Elementos comuns:**

- Grade: 3601 pontos igualmente espaçados em [0, π], a mesma da exploração. Como B é inteiro, |φ(2π − θ)| = |φ(θ)|, então [0, π] cobre tudo, e a janela [2π/3, 4π/3] equivale a [2π/3, π].
- Piso: f = 10⁻¹² (relativo a W).
- Erro logarítmico: e(θ) = |log₁₀ max(|φ_mod|, f) − log₁₀ max(|φ_obs|, f)|.
- **Regra de combinação**, igual para todas as previsões:
  - SUCESSO se o critério de sucesso vale em n = 9 **e** em n = 10;
  - FALHA se o critério de falha vale em n = 9 **e** em n = 10;
  - INCONCLUSIVO em qualquer outro caso, inclusive quando os dois tamanhos discordam.

### 4.1 P3: coeficientes artificiais (roda primeiro; é o teste potencialmente independente)

Para cada vetor c′, calcula-se a soma exata φ_obs(θ) = Σ ρ e^{iθ(n + c′·N)}/W nos dados oficiais e compara-se com φ_mod, que usa os mesmos μ e Σ e só troca c por c′. Ninguém olhou essas somas antes.

A **família de controles** está fixada abaixo. Nenhum controle pode ser descartado depois de visto o resultado.

- **Família A** (23 vetores): as permutações dos números (−1, 9, −16, 8) entre N₀ e N₃, exceto a identidade. Preserva exatamente as magnitudes dos coeficientes.
- **Família B** (20 vetores): entradas sorteadas, independentes e uniformes, em {−16, …, 16}, com `numpy.random.default_rng(20261120)` e `rng.integers(-16, 17, size=4)`, um vetor por vez. São rejeitados:
  - o vetor nulo;
  - ±c;
  - ± qualquer vetor das famílias A e C;
  - repetidos (inclusive a menos de sinal).

  Resultado (0 rejeitados): (8, 8, −1, −12), (−3, 11, −14, 3), (8, 5, −1, −3), (−12, 14, 1, −3), (−6, −15, 6, −1), (15, −4, −10, −3), (8, 12, 8, −10), (9, 8, −11, −11), (−6, 12, 15, 10), (14, 7, −3, −16), (11, 10, −8, 15), (−11, 5, −13, 13), (−3, 5, −14, 8), (2, 12, −10, 9), (−9, −10, −16, 13), (−16, 9, −13, −14), (−7, 1, 10, 5), (−9, 16, −1, −7), (−1, −10, 1, −5), (12, 11, 11, 0).
- **Família C** (8 vetores): c ± e_j para j = 0 a 3, isto é, um coeficiente alterado em ±1. Testa se pequenas mudanças deslocam a estrutura do jeito que o modelo prevê.
- O vetor original c é relatado **à parte** e não conta no P3.

**Métricas por vetor:**

- σ′ = √(c′ᵀΣc′).
- A região fina é R = {θ ≥ 8/σ′}. Nela, o termo m = 0 vale no máximo e⁻³².
- A = {θ ∈ R : max(|φ_obs|, |φ_mod|) ≥ f}.
- Picos são máximos locais estritos na grade, no interior de R, com valor ≥ f.
  - θ_obs é a posição do maior pico observado;
  - θ_mod é a posição do maior pico do modelo.
- **Não testável:** quando A é vazio ou quando falta pico em φ_obs ou em φ_mod. Nesse caso o vetor conta como não sucesso e não falha.
- **Posição:**
  - ok se |θ_mod − θ_obs| ≤ 0,01, ou se |φ_obs(θ_mod)| ≥ 0,8 |φ_obs(θ_obs)|;
  - falha se |θ_mod − θ_obs| > 0,05 **e** |φ_obs(θ_mod)| < 0,5 |φ_obs(θ_obs)|;
  - intermediário nos outros casos.
- **Magnitude:**
  - ok se a mediana de e em A for ≤ 0,3 **e** |log₁₀(pico_mod/pico_obs)| ≤ 0,3, isto é, fator 2;
  - falha se a mediana for > 1 **ou** |log₁₀ da razão dos picos| > 1, isto é, uma ordem de grandeza;
  - intermediário nos outros casos.

**Agregação, em cada n ∈ {9, 10}, sobre os 51 controles:**

- sucesso se a fração com "ok" for ≥ 0,8;
- falha se a fração com "falha" for ≥ 0,5;
- inconclusivo nos outros casos.

Isso é feito separadamente para **P3a (posição)** e **P3b (magnitude)**, e combinado pela regra comum.

**Comparação descritiva, sem peso no veredito:**

- o mesmo teste com Σ diagonal, isto é, sem as correlações entre as N_k;
- motivo: em parte, a posição das ressonâncias é fixada pela teoria dos números (θc′ perto de 2πℤ⁴), qualquer que seja Σ;
- regra de leitura: se o modelo diagonal acertar tanto quanto o completo, o papel da covariância **não** fica sustentado.

### 4.2 P1: posição do pico θ\* (motivada pelos dados; mede capacidade descritiva)

- θ\*_mod repete exatamente a operação da exploração. É o argmax, para θ > 0,5, de |φ_mod(θ)|·|1 − K̂(θ)|, em que:
  - K̂ é a transformada do mesmo núcleo gaussiano (largura sd/4, suporte ±60);
  - sd = √(cᵀΣc), que é o desvio-padrão de B.
- θ\*_obs são os valores publicados: 0,740 (n = 5, 6, 7), 0,741 (n = 8), 0,742 (n = 9, 10).
- **Critério:**
  - ok se |θ\*_mod − θ\*_obs| ≤ 0,005;
  - falha se a diferença for > 0,02;
  - intermediário nos outros casos.
- **Linha de base:** π/4 = 0,785, que vem da ressonância ingênua 8θ = 2π, fica a 0,043 de θ\*_obs. Isso já é falha pelo critério, então P1 não é satisfeito trivialmente.
- **Descritivo:** a fórmula de um termo θ\*₁ = 2π (cᵀΣm₀)/(cᵀΣc), com m₀ = (0, 1, −2, 1). Ela é o mínimo, em θ, de (θc − 2πm₀)ᵀΣ(θc − 2πm₀). O vetor m₀ foi lido da própria exploração (θc/2π ≈ m₀ em θ ≈ 0,74), por isso é descritiva.

### 4.3 P2: módulo de 𝒵 na janela (motivada pelos dados)

- Pontos da grade com θ ≥ 2π/3 (1201 pontos).
- **Critério:**
  - ok se a mediana de e for ≤ 0,3 **e** o máximo de e for ≤ 1;
  - falha se a mediana for > 1;
  - intermediário nos outros casos.
- **Descritivo:**
  - min|𝒵| observado × min|𝒵| do modelo × a cota dos ruins 3ⁿ/n!;
  - o sinal de 𝒵(π) observado e do modelo para n = 6 a 10.

P1 e P2 **não** são independentes entre si, e nenhuma delas é independente da exploração. Elas não podem ser apresentadas como confirmações.

## 5. Interpretação fixada antes

- **P3a e P3b com sucesso:** em n = 9 e 10, a estrutura fina da função característica de N fica explicada por uma gaussiana de rede com os dois primeiros momentos observados. Isso **não** diz que N é gaussiano, **não** é um resultado assintótico e **não** prova H1\*. O próximo passo seria analítico: estudar como μ e Σ crescem com n.
- **P3a com sucesso e P3b falhando:** as posições das ressonâncias vêm da aritmética mais a covariância, mas as magnitudes dependem de cumulantes de ordem mais alta. O modelo sozinho então não serve de caminho para uma cota inferior de |𝒵_boa|.
- **P3 falhando:** o modelo não explica. P1 e P2 continuam sendo relatadas, mas não podem servir de apoio.
- **O modelo acerta para c e erra nos controles:** isso indica algo específico de c. Fica registrado como observação, e nenhuma conjectura nova sai disso sem registro novo.
- **Em nenhum caso** o resultado valida H1\* ou C1 para n ≥ 11.

## 6. Ordem de execução

1. Publicar este registro (commit).
2. `python h1b_modelo_rede.py valida` (repetido e registrado).
3. `python h1b_modelo_rede.py p3 PASTA SAIDA`, com resultado registrado.
4. Só depois disso, `python h1b_modelo_rede.py p1p2 PASTA SAIDA`.
5. Resultados em `RESULTADOS_MODELO_REDE.md`, incluindo os desfavoráveis, os vetores não testáveis e qualquer problema numérico.

## 7. Limitações

- Os dados são finitos (n ≤ 10), e a aproximação gaussiana pode falhar nas caudas, que é justamente onde está a estrutura fina: perto da ressonância, |φ| fica entre 10⁻³ e 10⁻⁴.
- P1 e P2 dependem uma da outra e foram motivadas pelos dados.
- Nada aqui é validação assintótica.
- Os limiares (fator 2, 0,01 em θ, frações de 0,8 e 0,5) são convenções, fixadas agora.
- Sucesso não implica que a distribuição seja gaussiana.

## 8. Conjectura separada

A conjectura da paridade tem registro próprio em `CONJECTURA_PARIDADE.md`. Ela não é testada aqui.
