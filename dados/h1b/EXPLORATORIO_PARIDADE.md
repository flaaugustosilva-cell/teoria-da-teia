# Exploração (fora de registro): origem do desequilíbrio de paridade no centro da janela

Data: 20/11/2026. Isto é exploração. Nada aqui é teste, e os padrões encontrados só podem virar conjecturas, cada uma com registro próprio antes de qualquer teste. Script: `scripts/h1b_paridade_explora.py`. Saída completa: `exploratorio_paridade.txt`.

**População:** oficial, n = 5 a 10, altura ≥ 3, todas incorporáveis em 3+1. Onde aparece "todas as ordens", a população é outra, que inclui altura ≤ 2, e isso vai sempre indicado.

## 0. Como o problema dos pesos foi tratado: nível rotulado

Cada classe C corresponde a L = n!/|Aut(C)| ordens **rotuladas** (com os elementos numerados de 1 a n), e todas elas têm o mesmo sinal s = (−1)^B. Então

  n!·𝒵(π) = T = Σ_C L·s = Σ sobre as ordens rotuladas de (−1)^B,

e nessa soma cada ordem rotulada pesa exatamente 1. Isso resolve a objeção dos pesos desiguais:

- uma involução que inverte o sinal, definida sobre as ordens **rotuladas**, cancela exatamente os pares que forma;
- as ordens que ficam sem par dão o saldo **exato**;
- se a transformação comutar com a troca de rótulos, ela leva automaticamente classes em classes com o mesmo |Aut|;
- se não comutar, ela só faz sentido no nível rotulado, e o cancelamento continua exato lá.

Todas as somas abaixo são inteiras e exatas.

## 1. Primeiro fato: as teias ruins saem exatamente

A soma rotulada de (−1)^B sobre as ordens de altura ≤ 2 vale **−1 para todo n**. Foi conferido de n = 1 a 10, e é o que dá a fórmula fechada Z_rot com y = 0 em θ = π.

| n | todas as ordens | ruins (altura ≤ 2) | boas (T = n!·𝒵(π)) |
| --- | --- | --- | --- |
| 5 | +169 | −1 | +170 |
| 6 | −10.261 | −1 | −10.260 |
| 7 | −17.739 | −1 | −17.738 |
| 8 | −2.181.341 | −1 | −2.181.340 |
| 9 | −27.904.687 | −1 | −27.904.686 |
| 10 | −2.494.684.501 | −1 | −2.494.684.500 |

**Consequência para n ≤ 10.** Nessa faixa, todas as ordens de altura ≥ 3 cabem em 3+1. Por isso, ali, C2 é **equivalente** a uma afirmação sem nenhuma condição de altura:

  Σ sobre todas as ordens rotuladas em n elementos de (−1)^B < −1.

**Atenção para n ≥ 11.** A população oficial passa a ser "as incorporáveis", e essa equivalência deixa de valer automaticamente. Chamo a versão sem altura de **C2′**: é uma afirmação puramente combinatória sobre todas as ordens. Ela coincide com C2 para n ≤ 10 e, em n = 11, com a população auxiliar.

**Fórmula exponencial.** Como N₀, N₁ e n somam sobre as componentes conexas, vale exatamente que a série de todas as ordens é a exponencial da série das conexas. Isso foi conferido de n = 1 a 10.

## 2. Pergunta 1: o que distingue as paridades?

**Viés por estrato em n = 10**, isto é, a soma com sinal dividida pelo peso do estrato:

- **Número de minimais:** todos os estratos relevantes têm o mesmo sinal e viés parecido:
  - 1 minimal: −5,4×10⁻⁴;
  - 2: −4,7×10⁻⁴;
  - 3: −4,5×10⁻⁴;
  - 4: −6,0×10⁻⁵;
  - 5: −1,6×10⁻⁴.

  Isso é uma **diferença pequena e sistemática** entre populações enormes, como você antecipou. O saldo não vem de algumas teias atípicas.
- **Altura:**
  - a altura 3 tem sinal oposto (+2,0×10⁻⁴);
  - a altura 5 carrega 87% do saldo;
  - as alturas altas têm viés grande, mas pouco peso (a cadeia, de altura 10, tem viés −1).
- **Componentes:**
  - as conexas carregam 126% do saldo;
  - as de 2 componentes carregam −33%, com sinal oposto.
- **|Aut|:** os dois estratos são negativos.
- **Gêmeos:**
  - as ordens **sem** gêmeos incomparáveis carregam 151%;
  - as **com** gêmeos carregam −51%, com sinal oposto.

**Decomposição modular.** Toda ordem é, de um único jeito, uma das três coisas:

- **paralela**: união disjunta de partes;
- **série**: soma ordinal, isto é, uma parte inteira abaixo da outra;
- **de raiz modular prima** (chamada "prima" na primeira versão deste arquivo): o grafo de comparabilidade e o de incomparabilidade são ambos conexos. Equivale a ser obtida por substituição de módulos quaisquer dentro de uma ordem prima (uma ordem sem módulos não triviais). **Não** é o mesmo que "ordem sem módulos não triviais".

Soma com sinal por tipo, **todas as ordens**:

| n | paralelo | série | raiz prima |
| --- | --- | --- | --- |
| 5 | +29 | +260 | **−120** |
| 6 | −599 | −6.782 | **−2.880** |
| 7 | +62.705 | +27.916 | **−108.360** |
| 8 | +958.273 | −1.359.990 | **−1.779.624** |
| 9 | +26.869.253 | +9.873.636 | **−64.647.576** |
| 10 | +670.248.361 | −587.673.902 | **−2.577.258.960** |

- **As ordens de raiz prima têm sinal negativo em todo n de 5 a 10.** As partes paralela e série trocam de sinal conforme n.
- Na população oficial (só altura ≥ 3), a parte de raiz prima vale 0, −1.800, −99.120, −1.685.040, −63.556.416 e −2.563.084.440. Ela é negativa a partir de n = 6 e carrega 103% do saldo em n = 10.
- As ordens de raiz prima são a **maior parte** do peso: 79% em n = 10. Isso de novo indica um viés sistemático em uma população enorme (−4,9×10⁻⁴), e não teias atípicas.
- ~~As ordens primas não têm gêmeos, porque gêmeos são módulos de tamanho 2. Isso explica por que as ordens sem gêmeos carregam o saldo.~~ **Errado** (ver Errata).

## 3. Pergunta 2 (primeira sondagem): o toggle de gêmeos

**A transformação.** Tome dois gêmeos incomparáveis x e y, isto é, elementos com o mesmo conjunto abaixo D e o mesmo conjunto acima U. A transformação faz x < y. Fiz a conta à mão:

- a mudança em N₀ + N₁ é 1 − #{d ∈ D com exatamente 1 elemento entre d e x} − #{u ∈ U com exatamente 1 elemento entre x e u};
- a paridade só troca quando esse número de "vizinhos a distância 2" é par;
- os minimais diminuem em 1 quando o par é minimal (D vazio);
- no nível rotulado, cada par não ordenado {x, y} corresponde a **duas** ordens (x < y ou y < x). A relação entre os pesos é controlada, mas é de 1 para 2, não de 1 para 1.

**Resultado:** o toggle troca a paridade em apenas cerca de 54% dos pares (0,454; 0,516; 0,540; 0,546; 0,545; 0,541 para n = 5 a 10). Ele **não** é uma transformação que inverte o sinal, e quase não organiza o cancelamento. Fica registrado como resultado negativo.

**Altura:** pelo item 1, a altura sai exatamente do problema para n ≤ 10. Por isso não estudei como as transformações mudam a altura.

## 4. Pergunta 3 (resíduo): ainda não atacada

O que a exploração sugere, **sem** que isso seja conjectura registrada:

**(a)** O sinal parece estar nas ordens **de raiz prima**. Uma possível conjectura futura seria: "a soma rotulada de (−1)^B sobre as ordens de raiz prima em n elementos é negativa para todo n ≥ 5". Ela foi inspirada por estes dados, então só poderia ser testada de forma independente em n ≥ 11, com todas as ordens, ou demonstrada.

**(b)** As partes paralela e série são determinadas por ordens menores:

- a paralela, exatamente pela fórmula exponencial;
- a série, pela soma ordinal P ⊕ Q. Os pares que cruzam de P para Q têm exatamente |acima_P(p)| + |abaixo_Q(q)| elementos entre si. Então o sinal de P ⊕ Q é s(P)·s(Q) vezes um fator que depende só de quatro números: os máximos de P, os elementos de P com exatamente um elemento acima, os mínimos de Q e os elementos de Q com exatamente um elemento abaixo.

Isso sugere uma recursão exata, refinada por essas estatísticas, em que o problema todo se reduz às ordens de raiz prima. A identidade da série é **verificável** (é um teorema a conferir, não uma conjectura a testar) nos dados de n ≤ 10.

## 5. Alcance

| Resultado | Situação |
| --- | --- |
| C2 no centro (W_ímpar > W_par) | conjectura; n ≤ 10 é o que a inspirou |
| Cota inferior no centro | não atacada |
| H1\* em toda a janela | provada só para n = 5 a 10 (por computador); a prova no centro não a implicaria |

Não consegui consultar a OEIS para ver se a sequência +169, −10.261, −17.739, −2.181.341, … é conhecida: o site bloqueia o acesso automático.

## Errata (20/11/2026, depois da revisão do Flavio)

1. **Terminologia.** O que o script chama de "primo" (comparabilidade conexa **e** incomparabilidade conexa) é uma ordem **de raiz modular prima**. Uma ordem assim pode conter módulos substituídos que não são primos. O nome foi trocado no texto. O script não muda: a classificação é a mesma.
2. **Afirmação errada.** Escrevi que "as ordens primas não têm gêmeos". Isso vale para ordens **sem módulos não triviais**, mas **não** para as de raiz prima: um par de gêmeos pode ser um dos módulos substituídos. A afirmação está riscada acima. A observação de que as ordens sem gêmeos carregam 151% do saldo continua valendo como dado, mas fica sem a explicação que eu tinha dado.
