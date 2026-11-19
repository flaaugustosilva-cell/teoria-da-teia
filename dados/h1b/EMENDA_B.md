# Emenda ao pré-registro — entrega B

Registrada em 19/11/2026 (Brasília), antes de qualquer cálculo da entrega B. O horário do commit é a prova. Corrige e detalha a seção B de [`PREREGISTRO.md`](PREREGISTRO.md); o resto do registro não muda.

## 1. Correção da cota (observação do autor, 19/11, 16:00)

O registro original dizia |φ_n − φ_cert| ≤ 2·W(não certificadas)/W_n. Isso usa no denominador um W_n que não é conhecido. Como B enumera **todas** as ordens, o peso total das não certificadas, W_nc, é conhecido exatamente. A cota correta é:

|φ_n − φ_cert| ≤ 2·W_nc / W_cert

Demonstração: seja U ⊆ (não certificadas) o subconjunto que de fato cabe em 3+1, com peso W_U ≤ W_nc e soma S_U, em que |S_U| ≤ W_U. Então φ_n = (S_cert + S_U)/(W_cert + W_U), e |φ_n − φ_cert| = |S_U − φ_cert·W_U|/(W_cert + W_U) ≤ 2·W_U/(W_cert + W_U) ≤ 2·W_nc/W_cert.

## 2. Classificação

Uma teia sem certificado é **não certificada**, nunca "não cabe em 3+1". Duzentas tentativas sem sucesso não provam nada sobre a existência de uma representação.

## 3. Detalhes de implementação fixados agora

- **Enumeração:** ordens rotuladas naturalmente (i antes de j implica i < j), geradas acrescentando o elemento k com um conjunto de antecessores fechado para baixo. Cada ordem natural sai uma única vez.
- **Peso 1/|Aut|:** cada classe não rotulada C tem e(C)/|Aut(C)| rotulações naturais, onde e é o número de extensões lineares. Daí, Σ_rotuladas f = n!·Σ_naturais f/e(P). Logo W_n = Σ_naturais 1/e(P) e 𝒵 = Σ_naturais e^(iθB)/e(P), somando só as de altura ≥ 3.
- **Classes não rotuladas** (para os certificados e para a verificação com peso 1): forma canônica por refinamento de invariantes (antecessores, sucessores e invariantes dos vizinhos), seguida de permutações só dentro dos empates, tomando a menor matriz em ordem lexicográfica.
- **Certificado de caber em 3+1:** minimização (L-BFGS) de uma penalidade quadrática com folga δ = 0,05. Para cada par relacionado i < j: Δt > 0 e Δt² − |Δx|² ≥ δ; para cada par não relacionado: |Δx|² − Δt² ≥ δ. São até 200 recomeços aleatórios por classe. As coordenadas encontradas são arredondadas para 6 casas e conferidas em aritmética racional exata (frações): todo par relacionado tem de ser do tipo tempo e futuro, e todo par não relacionado tem de ser do tipo espaço. Só isso conta como certificado.
- **Validações obrigatórias, antes de usar qualquer fase:** número de ordens naturais (OEIS A006455: 40, 357, 4.824, 96.428, 2.800.472 para n = 4 a 8); número de classes não rotuladas (A000112: 16, 63, 318, 2.045, 16.999); e Σ_naturais 1/e(P) = (ordens rotuladas)/n! (A001035: 219, 4.231, 130.023, 6.129.859, 431.723.379), com igualdade exata em frações. Se alguma falhar, B para e o erro é reportado.
- **n = 8:** tentado só se a enumeração, os certificados e a soma de n = 5 a 7 terminarem e a estimativa para n = 8 ficar abaixo de 6 horas. É um critério de tempo, não de fase.
- **Sorteio para comparação:** diamante 3+1, semente 20261123, 10⁷ sorteios por n, condicionado a altura ≥ 3. Estimativa complexa φ̂ com erro, e Q com jackknife em 50 blocos.
- **Ângulos:** os 12 ângulos pequenos de E3 e os três da janela (2β para x = 6, 7 e 8).
- **O que se reporta:** φ_n (complexo) e |φ_n|² exatos (somente certificadas); a cota da seção 1; φ_sorteio com erro; Δ_n = φ_sorteio − φ_n e o seu tamanho em erros. A versão com peso 1 por classe entra só como verificação. O sorteio é um substituto e não será chamado de aproximação de φ_n; Δ_n mede a diferença, e nada além disso.
