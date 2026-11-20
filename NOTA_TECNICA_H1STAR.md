# Supressão de teias de duas camadas na Teoria da Teia: o que está demonstrado e o que está em aberto

**Flavio Augusto da Silva**
Estudante de Licenciatura em Ciências da Natureza, Faculdade SESI-SP de Educação
Nota técnica · 20 de novembro de 2026 · repositório `flaaugustosilva-cell/teoria-da-teia`

## Resumo

Na Teoria da Teia, as teias "ruins" de duas camadas precisam pesar menos que as teias "boas" na soma quântica, e isso deve valer dentro de uma janela do grão (5,7 ≤ ℓ/l_P ≤ 8,0). Esta nota separa o que foi demonstrado do que não foi.

- **Demonstrado para todo n:** dentro da janela, a soma das teias ruins por teia não rotulada é no máximo 3ⁿ/n! (Teorema 1), com uma versão mais fina que depende do ângulo (Teorema 1′).
- **Demonstrado para n = 5 a 10, com ajuda do computador:**
  - toda teia de altura ≥ 3 cabe em Minkowski 3+1;
  - a soma das teias ruins é menor que a das boas em toda a janela (hipótese H1\*);
  - para n = 6 a 10, a soma das teias boas supera 3ⁿ/n! (conjectura C1).
- **Em aberto:** uma cota inferior para a soma das teias boas, válida para todo n. A exploração dos dados mostra que o obstáculo é o cancelamento entre classes de teias.

## 1. Definições

- **Ação.** Benincasa–Dowker em 4D, versão local (ε = 1): S/ħ = 2β·B, com B = n − N₀ + 9N₁ − 16N₂ + 8N₃, em que N_k é o número de intervalos com k elementos dentro e β = √(2/3)·(ℓ/l_p)², l_p = √(8πGħ).
- **Janela 1.** π/3 ≤ β ≤ 2π/3, equivalente a 5,677 ≤ ℓ/l_P ≤ 8,029, com l_P = √(Għ).
- **Teias ruins:** ordens parciais de altura ≤ 2 (maior cadeia com até 2 elementos). **Teias boas:** ordens de altura ≥ 3 que cabem em Minkowski 3+1.
- **Peso.** Soma rotulada dividida por n!, o que equivale a pesar cada teia não rotulada C por 1/|Aut(C)|:
  𝒵_classe(n, β) = Σ_{C na classe} e^(2iβB(C)) / |Aut(C)|.
- **Hipóteses.**
  - **H1:** |𝒵_boa| ≥ 1 em toda a janela. Condição suficiente proposta antes; **refutada** (seção 3).
  - **H1\*:** R_n(β) = |𝒵_ruim| / |𝒵_boa| < 1 em toda a janela. É o que o argumento de supressão precisa.
  - **C1:** |𝒵_boa| > 3ⁿ/n! em toda a janela, para n ≥ 6. Conjectura; pelo Teorema 1, implica H1\*.

## 2. Resultados analíticos gerais

**Teorema 1.** Para todo n ≥ 1 e todo β na janela fechada, |𝒵_ruim(n, β)| ≤ 3ⁿ/n!.

*Demonstração.* Uma teia rotulada de altura ≤ 2 é determinada pelo conjunto A de seus minimais (|A| = a ≥ 1) e, para cada um dos outros n − a elementos, por um subconjunto não vazio de A abaixo dele. Todas as relações são ligações, então B = n − L. Com μ = 2β e y = 1 + e^(−iμ), a soma rotulada é Z_rot = e^(iμn)·Σ_{a=1..n} C(n, a)·(y^a − 1)^(n−a). Na janela, |y| = 2|cos β| ≤ 1, logo |y^a − 1| ≤ 2 e |Z_rot| ≤ Σ_a C(n, a)·2^(n−a) = 3ⁿ. Dividindo por n!, sai o enunciado. ∎

**Teorema 1′.** Com q = 2|cos β| e T(q) = Σ_{a=1..n} C(n, a)·[(1 + q^a)^(n−a) − 1], vale 1 − T(q) ≤ |Z_rot,ruim| ≤ 1 + T(q).

*Demonstração.* Expandindo (y^a − 1)^(n−a) em potências de y, os termos sem y somam Σ_{a≥1} C(n, a)(−1)^(n−a) = −(−1)ⁿ, que tem módulo 1, pela identidade (1 − 1)ⁿ = 0. Os demais têm módulo total ≤ T(q). ∎

A cota inferior só informa algo quando T(q) < 1. Em β = π/2, q = 0 e |Z_rot| = 1 exatamente.

**Mecanismo.** Fora da janela, |y| > 1, e a soma cresce como a contagem, ~2^(n²/4). Dentro dela, cada elemento não minimal contribui com no máximo 2 em módulo, e o que sobra depois do cancelamento binomial é controlado por q.

**Corolário.** Se |𝒵_boa(n, β)| > 3ⁿ/n! em toda a janela, então H1\* vale nesse n.

**Conferência.** Nos 12 valores exatos do experimento E1 (n = 40 a 160; ℓ/l_P = 6, 7, 8), ln|Z_rot,ruim| fica abaixo da cota do Teorema 1′ por poucas unidades (por exemplo, 120,4 contra 126,4 em ℓ/l_P = 8, n = 160).

## 3. Resultados finitos demonstrados com ajuda do computador (n = 5 a 10)

Esses resultados são demonstrações para os n indicados. Dependem da correção do código, que foi validado contra contagens conhecidas e por caminhos independentes; não dizem nada sobre outros n.

**Gerador e validações.** Para n ≤ 8, enumeração das ordens rotuladas naturalmente. Para n ≤ 10, o `genposetg` do nauty 2.8.8, de pacote com hash conferido. Validações:
- número de classes igual a A000112 até n = 10 (2.567.284);
- Σ n!/|Aut| igual ao número de ordens rotuladas (A001035) até n = 10 (6.611.065.248.783), com igualdade exata;
- os dois caminhos dão as mesmas somas por valor de B, em frações exatas, para n = 5 a 8.

**Embutibilidade.** Toda classe de altura ≥ 3 tem coordenadas em Minkowski 3+1, conferidas em aritmética exata (frações, e de novo em inteiros): 42, 262, 1.881, 16.442, 181.008 e 2.556.518 classes para n = 5 a 10. Nenhuma ficou sem certificado. Portanto, se existir uma teia de altura ≥ 3 que não cabe em 3+1, ela tem pelo menos 11 elementos. Não se sabe se existe.

**H1\*, H1 e C1 em toda a janela.** Grade de 400.001 ângulos e cotas rigorosas entre os pontos, por subdivisão adaptativa com a cota da derivada |d𝒵/dθ| ≤ Σ w|B|. Os mínimos pontuais foram conferidos em 60 dígitos.

| n | Mínimo de \|𝒵_boa\| (ℓ/l_P) | Cota inferior rigorosa | Máximo rigoroso de R | H1\* | H1 (≥ 1) | C1 (limiar 3ⁿ/n!) |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 0,252 (6,27) | 0,233 | 0,570 | demonstrada | falha | falha (2,025); fora do enunciado |
| 6 | 1,797 (7,65) | 1,670 | 0,075 | demonstrada | vale | vale (1,013) |
| 7 | 2,581 (7,84) | 1,530 | 0,041 | demonstrada | vale | vale (0,434) |
| 8 | 0,539 (7,24) | 0,170 | 0,086 | demonstrada | falha | vale (0,163) |
| 9 | 23,41 (7,28) | 0,120 | 0,576 | demonstrada | não decidida | vale (0,0542) |
| 10 | 150,4 (7,34) | 0,193 | 0,395 | demonstrada | não decidida | vale (0,0163) |

- **H1** é refutada como hipótese geral pelos contraexemplos exatos de n = 5 e n = 8. Em n = 9 e 10, a cota rigorosa foi refinada só até decidir C1, por isso H1 fica não decidida, embora os mínimos pontuais estejam bem acima de 1.
- **C1** foi formulada depois de ver n = 5 a 8 (por isso começa em n = 6), e as previsões para n = 9 e 10 foram registradas antes de esses dados existirem. Só n = 9 e 10 são confirmações prospectivas.

## 4. Resultados numéricos, não demonstrativos

- **E1 (n = 40 a 160).** A soma exata das teias ruins por teia cai de e^(−72) para e^(−648) ou menos dentro da janela; isso agora é explicado pelo Teorema 1. A comparação com as teias boas nesses tamanhos não está feita, porque |𝒵_boa| não é conhecido para n ≥ 11.
- **O sorteio é outro objeto.** Teias sorteadas num diamante de Minkowski não reproduzem a soma ponderada por 1/|Aut|: para n = 5 a 8, as diferenças de fase chegam a 790 erros, e a distância de variação total entre as distribuições de B fica entre 0,45 e 0,57. Os estudos feitos com o sorteio (entregas E, C e E2) descrevem só o sorteio.

## 5. Exploração (sem valor de demonstração)

Decompondo 𝒵_boa por altura e por número de minimais (n = 5 a 10, grade de 4.001 ângulos), nenhuma parte domina. Os mínimos da soma vêm de cancelamento entre as partes: em n = 8, partes com módulos 10,7 / 36,5 / 45,4 / 5,5 / 4,0 / 1 somam 0,62, cerca de 0,6% da soma dos módulos.

Os mínimos dessa exploração são mínimos da grade, não da janela contínua: em n = 8, a grade de 4.001 pontos dá 0,616, e a de 400.001 dá 0,539.

## 6. O problema em aberto

**Pergunta.** Existe uma propriedade da distribuição dos valores de B nas teias que cabem em 3+1 que impeça 𝒵_boa(θ) = Σ_b W_b·e^(iθb) de se aproximar demais de zero dentro da janela? Bastaria |𝒵_boa| > 3ⁿ/n! (ou > (1 + T(q))/n!).

**Por que é difícil.**
1. Pesos positivos não impedem cancelamento total: as próprias teias ruins de camadas cheias somam exatamente zero em β = π/2.
2. O cancelamento acontece entre classes, como mostra a seção 5.
3. Para n ≤ 10, "cabe em 3+1" inclui todas as teias de altura ≥ 3. Para n grande, só uma fração ínfima cabe (cota de Warren, citada de memória). A composição do conjunto muda com n, e os resultados finitos não se extrapolam.
4. Até onde sei, demonstrar que as teias parecidas com espaço-tempo dominam a soma sobre conjuntos causais é uma questão em aberto na própria área. Os trabalhos conhecidos (Loomis e Carlip, 2017, e sucessores) mostram a supressão de classes ruins específicas, não uma cota inferior para as boas. A literatura recente não foi conferida para esta nota.

## 7. Níveis de conclusão

| Nível | Resultado |
| --- | --- |
| Analítico geral | Teoremas 1 e 1′: cota superior para as teias ruins na janela |
| Finito exato | Embutibilidade em 3+1 e H1\* demonstradas de n = 5 a 10 |
| Computacional finito | C1 demonstrada com cotas rigorosas de n = 6 a 10 (prospectiva só em 9 e 10) |
| Numérico | E1 (teias ruins em n = 40 a 160); estudos do sorteio |
| Exploratório | Cancelamento entre classes de alturas e de números de minimais |
| Aberto | Cota inferior geral para a soma das teias boas; H1\* e C1 para todo n |

## Reprodutibilidade

Registros, pré-registros e dados em `dados/e1/`, `dados/h1/` e `dados/h1b/`. Principais commits: `5c5f9a8` (pré-registro de n = 9 e 10), `1624c2d` (resultados de n = 9 e 10 e Teorema 1′), `7c4d9f5` (nomenclatura), `71a9c53` (exploração). Os scripts estão em `scripts/` (`h1b_B_*.py` para n ≤ 8, `h1b_N_*.py` para n ≤ 10). A tabela da seção 3 sai de `h1b_N_analise.py` (`dados/h1b/n9n10/analise_n5a8_refinada.txt` e `h1b_N_relatorio.txt`).
