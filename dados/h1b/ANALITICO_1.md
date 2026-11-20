# Item 5 — argumento analítico para H1\*, parte 1

Flavio Augusto da Silva · 20/11/2026 (Brasília). Registrado antes de qualquer dado de n = 9 e 10.

## Teorema 1 (supressão das teias ruins na janela) — demonstrado

**Enunciado.** Para todo n ≥ 1 e todo β na janela 1 fechada (π/3 ≤ β ≤ 2π/3), com a ação de Benincasa–Dowker 4D (ε = 1) e peso 1/|Aut|:

|𝒵_ruim(n, β)| ≤ 3ⁿ / n!

Portanto ln|𝒵_ruim| ≤ n·ln 3 − ln n! = −n·ln n + O(n), que tende a −∞.

**Demonstração.** Uma teia rotulada de altura ≤ 2 fica determinada, de modo único, pelo conjunto A de seus elementos minimais (a = |A| ≥ 1) e, para cada um dos n − a elementos restantes, por um subconjunto **não vazio** de A abaixo dele. Todas as relações são ligações, então B = n − L. Com μ = 2β e y = 1 + e^(−iμ):

Z_rot = e^(iμn) · Σ_a C(n, a) · (y^a − 1)^(n−a)

(esta é a fórmula de `scripts/camadas_variaveis.py`, conferida por força bruta em n = 4 e 5 e pela enumeração completa em n ≤ 8). Agora |y| = |1 + e^(−iμ)| = 2|cos β| ≤ 1 exatamente quando π/3 ≤ β ≤ 2π/3. Nesse caso |y^a − 1| ≤ |y|^a + 1 ≤ 2, então |Z_rot| ≤ Σ_a C(n, a)·2^(n−a) = 3ⁿ. Dividindo por n!: |𝒵_ruim| ≤ 3ⁿ/n!. ∎

**Por que o termo ruim é tão suprimido (pergunta 1 do autor).** Fora da janela, |y| > 1, e o fator y^a cresce sem limite: a soma acompanha a contagem, ~2^(n²/4), e é isso que dá o termo n². Dentro da janela, cada elemento não minimal contribui com no máximo 2 em módulo, qualquer que seja o número de ligações. O crescimento cai de e^(cn²) para no máximo 3ⁿ. A janela é exatamente a condição |1 + e^(−2iβ)| ≤ 1, isto é, a soma das fases de "ligar ou não ligar" um par ter módulo ≤ 1.

**Conferência com os números.** Nos 12 casos do E1 (n = 40 a 160; x = 6, 7, 8), L fica abaixo da cota (por exemplo, n = 160, x = 7: L = −648,4 contra a cota −479,7). Para n = 5 a 8, o máximo de |𝒵_ruim| na janela (0,504 / 0,316 / 0,167 / 0,071) fica abaixo de 3ⁿ/n! (2,025 / 1,013 / 0,434 / 0,163). Uma cota mais fina, dependente de β: |Z_rot| ≤ Σ_a C(n, a)(1 + q^a)^(n−a), com q = 2|cos β|.

**Corolário (condição suficiente para H1\*), demonstrado.** Se |𝒵_boa(n, β)| > 3ⁿ/n! para todo β da janela, então H1\* vale nesse n. Em termos de φ_n: basta |φ_n| > 3ⁿ/(n!·W_n). A exigência sobre as teias boas fica muito mais fraca que H1 (|𝒵_boa| ≥ 1): o limiar 3ⁿ/n! tende a zero mais rápido que qualquer exponencial.

## Pergunta 2 do autor: a cota mínima suficiente para o termo bom

É o corolário acima. Ele é suficiente, mas **não necessário**: em n = 5, |𝒵_boa| desce a 0,252, abaixo de 3⁵/5! = 2,025, e mesmo assim H1\* vale (R ≤ 0,570), porque o |𝒵_ruim| real (0,504) é bem menor que a cota.

## Pergunta 3 do autor: dá para demonstrar sem extrapolar?

O lado ruim está resolvido de forma analítica e para todo n (Teorema 1). Falta uma **cota inferior** para |𝒵_boa| na janela. Esse é o obstáculo de verdade: T4 (seção 16) mostrou que pesos positivos não impedem cancelamento total, então a cota precisa vir da estrutura das teias que cabem em 3+1. Hoje não há demonstração. As linhas de ataque, a explorar depois, são: (i) achar uma subclasse de teias boas com soma calculável e dominante; (ii) entender como a soma se decompõe pelos minimais, como foi feito para as ruins; (iii) estudar se existe um análogo da condição |y| ≤ 1 para as teias boas.

## Conjectura C1 — registrada agora, testada de forma prospectiva em n = 9 e 10

**Enunciado.** Para n ≥ 6 e todo β na janela 1: |𝒵_boa(n, β)| > 3ⁿ/n!.

- **Situação antes do teste:** vale em n = 6, 7, 8 (mínimos 1,797 / 2,581 / 0,539 contra 1,013 / 0,434 / 0,163); falha em n = 5 (0,252 contra 2,025), e por isso o enunciado começa em n = 6. Essa escolha foi feita olhando n = 5 a 8; os testes que contam são n = 9 e 10, ainda não calculados.
- **Previsões:** mínimo de |𝒵_boa| na janela > 3⁹/9! = 0,0542 em n = 9 e > 3¹⁰/10! = 0,0163 em n = 10. Se isso falhar em algum dos dois, C1 está refutada nesse n. H1\* ainda pode valer, mas teria de ser verificada diretamente.
- **O que C1 é e o que não é:** uma conjectura sobre n finito, testada em dois tamanhos. Mesmo confirmada, não demonstra nada para n grande.
