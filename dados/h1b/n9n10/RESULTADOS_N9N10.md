# φ_n exato em n = 9 e n = 10 — resultados

Flavio Augusto da Silva · 20/11/2026, ~03:45–05:20 (Brasília), depois do pré-registro ([`../PREREGISTRO_N9N10.md`](../PREREGISTRO_N9N10.md), commit 5c5f9a8).

## Resposta à pergunta central

**Até n = 10, toda teia de altura ≥ 3 cabe em Minkowski 3+1.** Não há nenhuma classe sem certificado. Se a mudança de composição existe, ela começa depois de n = 10. Isso é um resultado finito; não diz nada sobre onde ela começa nem se começa.

## Gerador e validações (todas passaram antes de qualquer cálculo de H1\*)

- `genposetg` do nauty 2.8.8, de pacote do PyPI com hash conferido, compilado numa pasta isolada; procedência completa em `PROCEDENCIA_GENPOSETG.txt`.
- Classes geradas, n = 1 a 10: 1, 2, 5, 16, 63, 318, 2.045, 16.999, 183.231, 2.567.284 (= A000112).
- Toda saída é ordem parcial (fecho transitivo, antissimetria, irreflexividade): nenhuma falha.
- Σ n!/|Aut| = ordens rotuladas, n = 1 a 10, até 6.611.065.248.783 (= A001035), com |Aut| calculado pelo nosso código.
- W(B) por classe = enumeração natural da entrega B, em frações exatas, para n = 5 a 8 (`valida4.txt`).
- A análise por classes reproduz os valores da entrega B em n = 5 a 8.

## As cinco categorias pedidas

| Categoria | n = 9 | n = 10 |
| --- | --- | --- |
| 1. Classes não rotuladas geradas | 183.231 | 2.567.284 |
| 2. Classes de altura ≥ 3 | 181.008 | 2.556.518 |
| 3. Com certificado (1ª passada / 2ª passada) | 181.008 / 0 | 2.556.518 / 0 |
| 4. Sem certificado | 0 | 0 |
| 5. Demonstradas não embutíveis | 0 (não há método de prova nesta etapa) | 0 (idem) |

Todos os 2.737.526 certificados foram conferidos de novo, de forma independente, com aritmética inteira exata (coordenadas × 10⁶), por `scripts/h1b_N_verifica.py`: nenhum inválido. As coordenadas de n = 9 estão em `h1b_N_cert_n9_inteiros.npz`. As de n = 10 (363 MB) não cabem no GitHub. Publica-se o estado de cada classe (`h1b_N_cert_n10_estado.npz`) e o sha256 das coordenadas (`42421d3f…`); o cálculo é determinístico e pode ser refeito (~80 min em 2 núcleos).

## H1\*, H1 e a conjectura C1 (janela inteira, cotas rigorosas)

| n | W_boa | Mínimo pontual de \|𝒵_boa\| (x) | Cota inferior rigorosa | Máximo rigoroso de R | H1\* | C1 (limiar) |
| --- | --- | --- | --- | --- | --- | --- |
| 9 | 121.989,22 | 23,41 (7,28) | 0,120 | 0,576 | demonstrada | confirmada (0,0542) |
| 10 | 1.818.177,55 | 150,41 (7,34) | 0,193 | 0,395 | demonstrada | confirmada (0,0163) |

- **H1\*** (soma das ruins menor que a das boas, em toda a janela) vale exatamente em n = 9 e 10. Somando a entrega B, vale para n = 5 a 10.
- **C1** foi confirmada nos dois testes prospectivos, fixados antes destes dados ([`../ANALITICO_1.md`](../ANALITICO_1.md)).
- **H1\** (≥ 1) fica "não decidida" pela cota rigorosa, que foi refinada só até decidir C1. Os mínimos pontuais (23,4 e 150,4) estão bem acima de 1. H1 já estava refutada como condição geral (n = 5 e 8).
- A soma das ruins por classes bate com a fórmula exata do Teorema 1 (diferença ≤ 1,2 × 10⁻⁷ em ln|Z|).

Mudança de método fixada antes de ver n = 9 e 10, conferida em n = 5 a 8: o refinamento rigoroso continua até decidir C1 (cota acima do limiar, ou um ponto exato abaixo dele). Isso apertou a cota de R em n = 8 de 0,278 para 0,086.

## Nomenclatura (correção de 20/11/2026, 14:29, a pedido do autor)

Nas versões anteriores dos arquivos em Markdown, o asterisco de "H1\*" era consumido pela formatação em 5 lugares, e "H1\*" aparecia como "H1". Um desses lugares era o resumo deste arquivo. Os asteriscos foram escapados (`H1\*`) em todos os arquivos; o conteúdo não mudou. As três afirmações são distintas:

| Afirmação | Situação |
| --- | --- |
| H1 original: \|𝒵_boa\| ≥ 1 em toda a janela | refutada como hipótese geral (contraexemplos exatos em n = 5 e n = 8); em n = 9 e 10, não decidida pela cota rigorosa (mínimos pontuais de 23,4 e 150,4) |
| H1\*: \|𝒵_ruim\| < \|𝒵_boa\| em toda a janela | demonstrada para n = 5 a 10 (resultado finito) |
| C1: \|𝒵_boa\| > 3ⁿ/n! em toda a janela, n ≥ 6 | confirmada de forma prospectiva em n = 9 e 10; compatível com n = 6 a 8, que foram vistos antes de C1 ser registrada; falha em n = 5, fora do enunciado |

Sobre a transição: o que está demonstrado é que, **se** existir uma classe de altura ≥ 3 que não cabe em 3+1, ela tem pelo menos 11 elementos. Não se sabe se ela existe nem se aparece em n = 11.

## O que estes resultados podem e não podem dizer

São resultados finitos, exatos, em n = 9 e 10. Não mostram tendência que permita extrapolar: o mínimo de |𝒵_boa| foi 0,25 / 1,80 / 2,58 / 0,54 / 23,4 / 150,4 de n = 5 a 10. A pergunta "a partir de que n aparecem teias de altura ≥ 3 que não cabem em 3+1?" continua aberta, e agora se sabe que a resposta é n ≥ 11.

## Como reproduzir

```
# gerador (ver PROCEDENCIA_GENPOSETG.txt)
genposetg 9 t > d6_n9.txt ; genposetg 10 t > d6_n10.txt
cd scripts
python h1b_N_classes.py d6_n9.txt 9 ; python h1b_N_classes.py d6_n10.txt 10
python h1b_N_cert.py 9 0 1 ; python h1b_N_cert.py 10 0 2 & python h1b_N_cert.py 10 1 2
python h1b_N_verifica.py 9 ; python h1b_N_verifica.py 10
python h1b_N_analise.py 9 10
```
