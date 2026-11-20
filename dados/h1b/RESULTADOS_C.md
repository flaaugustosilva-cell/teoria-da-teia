# H1, segunda etapa — entrega C: resultados (descritivos)

Flavio Augusto da Silva · rodado de 19/11/2026, 23:59, a 20/11/2026, ~02:10 (Brasília), depois do registro [`DECISOES_H1STAR.md`](DECISOES_H1STAR.md) (commit e5dc0ea). Parâmetros de [`PREREGISTRO.md`](PREREGISTRO.md), seção C, sem mudança.

**Interpretação restrita:** C descreve só o conjunto produzido pelo sorteio. A entrega B mostrou que ele é diferente do objeto de H1*. Por isso **nada aqui é evidência a favor ou contra H1***. Não há ajuste de modelo nem veredito, como foi registrado.

## Resultado

Tabela completa em `h1b_C_relatorio.txt` e `h1b_C_resultados.csv`.

| n | Teias válidas | Pontos resolvidos (Q > 4 erros) | Faixa de Q na janela |
| --- | --- | --- | --- |
| 6 | 4.310.611 | 21/21 | 6,2 × 10⁻⁴ a 2,5 × 10⁻³ |
| 8 | 9.996.950 | 21/21 | 4,9 × 10⁻⁵ a 2,7 × 10⁻⁴ |
| 10 | 17.694.616 | 21/21 | 2,8 × 10⁻⁶ a 1,7 × 10⁻⁵ |
| 12 | 26.763.733 | 2/21 | até ~1,4 × 10⁻⁶; maioria compatível com zero |
| 14, 16, 20, 24 | 3,7 a 7,8 milhões | 0/21 | todos compatíveis com zero |

- Na janela, Q cai cerca de 10 vezes a cada 2 elementos de n = 6 a n = 10 (descritivo; não foi ajustado nenhum modelo).
- Os 21 ângulos formam pares simétricos em torno de θ = π (|φ(θ)| = |φ(2π − θ)|, porque B é inteiro), então são 11 ângulos independentes. Os valores dos pares coincidem, o que confere a conta.
- Q pode sair negativo quando o valor verdadeiro é ~0; isso é esperado de um estimador sem viés.

## Problema de método encontrado (reportado, sem mudar a tabela)

O erro do jackknife fica abaixo do erro teórico esperado perto de zero (~1/N a √2/N) em 7, 6, 6 e 11 dos 21 pontos de n = 14, 16, 20 e 24. Isso explica o único ponto com Q mais de 3 erros abaixo de zero (n = 14, θ = π: −2,7 × 10⁻⁷ ± 6 × 10⁻⁸). Usando o maior entre o erro do jackknife e √2/N, a contagem de pontos resolvidos não muda (21, 21, 21, 2, 0, 0, 0, 0). Os intervalos de 95% dos pontos não resolvidos de n ≥ 14 devem ser lidos com esse erro maior (`h1b_C_nota_erro.txt`).

## Execução

O ambiente na nuvem reiniciou durante n = 10 e n = 12. Os dois tamanhos foram refeitos desde o início, com a mesma semente. O script passou a gravar o estado exato do gerador a cada bloco, para poder retomar. Conferi que a retomada reproduz a mesma sequência e que o primeiro bloco de n = 6 sai idêntico ao gravado antes do reinício. Nenhum parâmetro mudou.

## Como reproduzir

```
cd scripts
python h1b_C_sorteio.py 6 8 10 12 14 16 20 24
python h1b_C_analise.py
```
