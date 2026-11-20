# φ_n exato em n = 9 e n = 10 — pré-registro

Flavio Augusto da Silva · registrado em 20/11/2026 (Brasília), antes de compilar o gerador e de qualquer cálculo. O horário do commit é a prova.
Decisão do autor (20/11, 03:39): caminho (b), com o `genposetg` do nauty, e item 5 em paralelo ([`ANALITICO_1.md`](ANALITICO_1.md)).

## Pergunta central

A partir de qual tamanho aparecem teias de altura ≥ 3 que não cabem em Minkowski 3+1? Para n ≤ 8, todas cabem (entrega B). Secundárias: H1* em n = 9 e 10, e o teste prospectivo da conjectura C1.

## 1. Procedência e compilação do gerador

- **Fonte:** pacote pynauty 2.8.8.1 (sdist do PyPI), que traz o nauty 2.8.8. Hash do pacote baixado: `454d3b0e605d649d13478afb090daef4a152f15c4a337a391fe69fded7e683f2`, idêntico ao publicado pelo PyPI (envio de 06/06/2024). `genposetg.c` ("poset generator version 1.0, October 8, 2022"), sha256 `b75e2f78a8d74454109d989bee54edefabc9df0fe5f5cb08aee6806226db1fe1`.
- **Compilação:** gcc 13.3.0, numa pasta isolada fora do repositório (`/home/claude/ferramentas`), sem instalar nada no sistema e sem sudo. São registrados o comando exato e o sha256 do executável gerado.
- **Se o ambiente bloquear a compilação ou a execução:** pare e registre a limitação. Nada de contornar o bloqueio, mudar políticas ou buscar executáveis prontos de fora. A autorização do autor para o experimento não substitui a autorização técnica do ambiente.

## 2. Validação do gerador (antes de qualquer cálculo de H1*)

1. **Contagem de classes** produzidas pelo `genposetg`, n = 1 a 10, contra A000112: 1, 2, 5, 16, 63, 318, 2.045, 16.999, 183.231, 2.567.284.
2. **Cada saída é uma ordem parcial:** irreflexiva, antissimétrica e transitiva (depois do fecho transitivo, se o formato der só as coberturas). Uma única falha interrompe.
3. **Automorfismos:** |Aut| de cada classe, calculado pelo nosso código (permutações que preservam a ordem, com refinamento por invariantes). Identidade obrigatória: Σ_classes n!/|Aut| = número de ordens rotuladas (A001035): 1, 3, 19, 219, 4.231, 130.023, 6.129.859, 431.723.379, 44.511.042.511, 6.611.065.248.783, com igualdade exata em inteiros.
4. **Concordância com a entrega B:** para n = 5 a 8, a distribuição W(B) por classe (peso 1/|Aut|), separada em altura ≥ 3 e ≤ 2, tem de ser idêntica, em frações, à da enumeração natural.

Se qualquer validação falhar, o cálculo para e o erro é reportado.

## 3. Cálculo

- Por classe: B (ação de Benincasa–Dowker 4D, ε = 1), altura e |Aut|. 𝒵 = Σ_classes e^(iθB)/|Aut|.
- **Certificados (caber em 3+1):** mesmo método da entrega B (L-BFGS, folga δ = 0,05, até 200 recomeços, coordenadas arredondadas para 6 casas e conferidas em frações). As classes sem certificado na primeira passada passam por uma **segunda passada fixada agora:** até 2.000 recomeços, com δ = 0,01.
- **Lado ruim:** soma exata pela fórmula do E1 (Teorema 1) e, como conferência, pela soma das classes de altura ≤ 2.
- **H1* na janela inteira:** mesmo método rigoroso de `h1b_B_rigor.py`. Se houver classes não certificadas (peso W_nc), usa-se |𝒵_boa| ≥ |𝒵_cert| − W_nc. Se essa cota não for positiva, H1* fica "não decidida" naquele n.
- **C1:** previsto mínimo de |𝒵_boa| > 3⁹/9! = 0,0542 (n = 9) e > 3¹⁰/10! = 0,0163 (n = 10). Se houver classes não certificadas, C1 é avaliada com a mesma cota.

## 4. Como as classes serão relatadas (exigência do autor)

1. Total de classes não rotuladas geradas.
2. Classes de altura ≥ 3.
3. Classes com certificado positivo de que cabem em 3+1 (primeira e segunda passada, separadas).
4. Classes sem certificado. **Nunca serão chamadas de "não cabem em 3+1".**
5. Classes demonstradas como não embutíveis. **Nesta etapa não existe método de prova de impossibilidade.** Esta categoria será reportada como 0 por falta de método, não por falta de casos. Se houver classes sem certificado, elas serão listadas (forma e B) para trabalho futuro.

## 5. Armazenamento e interrupção segura

- Saída do gerador gravada em arquivo antes do processamento; processamento em partes de 100.000 classes, com gravação ao fim de cada parte e retomada automática.
- Certificados gravados a cada 20.000 classes, com retomada.
- **Limite de tempo:** se a primeira passada de certificados de n = 10 passar de 10 horas, o cálculo para e reporta o que foi feito, com as classes não tentadas em categoria própria (nem certificadas, nem sem certificado).
- Os arquivos finais vão para `dados/h1b/n9n10/`.

## 6. O que estes resultados podem e não podem dizer

São resultados finitos, em n = 9 e n = 10. Se aparecer uma classe sem certificado, isso é um **candidato** à mudança de composição, não uma prova. Se todas forem certificadas, isso diz só que a mudança, se existe, vem depois de n = 10. Nenhum resultado aqui é extrapolação assintótica.
