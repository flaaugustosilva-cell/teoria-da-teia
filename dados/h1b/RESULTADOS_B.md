# H1, segunda etapa — entrega B: resultados

Flavio Augusto da Silva · rodado em 19/11/2026, ~16:15–16:40 (Brasília), depois da emenda ([`EMENDA_B.md`](EMENDA_B.md), commit e91345e).

## Validações (todas passaram, n = 4 a 8)

- Ordens naturais: 40, 357, 4.824, 96.428, 2.800.472 (A006455).
- Classes não rotuladas: 16, 63, 318, 2.045, 16.999 (A000112).
- Σ n!/e(P) = ordens rotuladas: 219, 4.231, 130.023, 6.129.859, 431.723.379 (A001035), igualdade exata em frações.
- A soma das teias ruins da enumeração bate com a fórmula exata do E1 (diferença ≤ 1,4 × 10⁻¹¹ em ln|Z|).

## Certificados

Todas as classes de altura ≥ 3 têm coordenadas em 3+1 conferidas em frações: 42, 262, 1.881 e 16.442 (n = 5 a 8). Não há nenhuma não certificada; logo W_nc = 0, a cota da emenda vale 0, e W_n e φ_n são exatos. n = 8 entrou pelo critério de tempo (~4,5 min).

## Comparação registrada com o sorteio (semente 20261123, 10⁷ sorteios)

O sorteio é um objeto diferente de φ_n. |Δ_n| vai de 1,5 a 790 erros, e a distância de variação total entre as distribuições de B fica entre 0,45 e 0,57 (descritivo). Valores completos em `h1b_B_relatorio.txt` e `h1b_B_resultados.json`. A versão com peso 1 por classe difere da versão com peso 1/|Aut| em até cerca de 5 vezes.

## Extras exatos (não registrados): a janela inteira

| n | Mínimo de \|𝒵_boa\| | H1 (≥ 1 em toda a janela) | Máximo rigoroso de R = \|𝒵_ruim\|/\|𝒵_boa\| | H1* (R < 1) |
| --- | --- | --- | --- | --- |
| 5 | 0,252 (x = 6,27) | falha | 0,570 | demonstrada |
| 6 | 1,797 (≥ 1,670) | demonstrada | 0,075 | demonstrada |
| 7 | 2,581 (≥ 1,530) | demonstrada | 0,041 | demonstrada |
| 8 | 0,539 (x = 7,24) | falha | 0,278 | demonstrada |

Os mínimos foram conferidos em 60 dígitos (mpmath). As cotas rigorosas vêm de subdivisão adaptativa com a cota da derivada (`h1b_B_rigor.py`). `h1b_B_extra.txt` traz uma primeira passada, com grade fixa e cotas mais frouxas.

## Ressalva

Para n ≤ 8, "cabe em 3+1" inclui todas as teias de altura ≥ 3, até as de três camadas. Para n grande, pela cota de Warren, só uma fração ínfima delas cabe em 3+1. A composição das teias boas muda com n, e estes resultados não se extrapolam. O mínimo de |𝒵_boa| e o máximo de R não seguem tendência com n.

## Conclusão

H1, na forma "≥ 1", é falsa em n = 5 e em n = 8 (contraexemplos exatos). H1*, que é o que o E1 precisa, vale exatamente em toda a janela para n = 5 a 8. Nada disso decide n grande.

## Como reproduzir

```
cd scripts
python h1b_B_exato.py 4 5 6 7 8
python h1b_B_sorteio.py 5 6 7 8
python h1b_B_compara.py 5 6 7 8
python h1b_B_rigor.py 5 6 7 8
```
