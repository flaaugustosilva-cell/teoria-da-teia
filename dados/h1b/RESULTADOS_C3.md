# Resultados: conjectura C3 em n = 11 (pré-registro `PREREGISTRO_C3.md`, commit af58027)

Data: 20/11/2026. O comando foi rodado uma vez, exatamente como registrado:

`python h1b_soma_ordinal.py c3 n9n10 dados/h1b/n11aux`

O script não mudou desde o registro (sha256 `f1b09058…5552`). Saída: `resultado_c3.txt`.

## Validações obrigatórias

- Total de classes nas 20 partes: 46.749.427, que é A000112(11). **Ok.**
- Soma das ordens ruins (altura ≤ 2): −1, como manda a fórmula fechada. **Ok.**

## Resultado (todas as ordens, n = 11; rota R1)

| Quantidade | Valor exato |
| --- | --- |
| T_todas(11) | −40.491.236.963 |
| Par₁₁ (paralelo, pela recursão) | +34.819.420.745 |
| Ser₁₁ (série, pela recursão) | +1.787.428.412 |
| **Prim₁₁ = T_todas − Par − Ser** | **−77.098.086.120** |

**Veredito de C3 em n = 11: SUCESSO** (Prim₁₁ < 0).

## Força do teste (seção 4 do registro)

O registro declarou que o teste só teria força de verdade se Par₁₁ + Ser₁₁ fosse grande e positivo. Foi o caso: Par₁₁ + Ser₁₁ = +3,66×10¹⁰, cerca de 90% de |T_todas(11)|.

- Para C3 falhar, bastaria que Prim₁₁ ficasse acima de −7,7×10¹⁰. Ou seja, o sinal negativo do total **não** forçava o resultado.
- A parte de raiz prima vale 1,90 vezes o total. Ela precisa superar uma parte paralela positiva e grande.

## O que isto estabelece e o que não estabelece

- **Estabelece:** C3 vale em n = 11, fora dos dados que a inspiraram (n = 4 a 10). O valor é exato e depende de duas coisas: a identidade demonstrada em `ANALITICO_3.md` e as partes de n = 11 já publicadas.
- **Não estabelece:**
  - C3 para todo n;
  - C2 oficial em n = 11 (a população oficial, a das incorporáveis, não foi determinada);
  - nada sobre H1\* fora de θ = π.
- **Observação descritiva:** em n = 11, a parte paralela é positiva e grande. Isso mostra por que a redução às ordens de raiz prima **não** basta, sozinha, para C2′: seria preciso controlar o tamanho relativo das partes.

## Pendente

**Rota R2:** a confirmação independente, gerando de novo as ordens de n = 11 e somando diretamente as de raiz prima (cerca de 2 horas). Ainda não foi executada. Se ela discordar de R1, o veredito fica suspenso e o erro é relatado.
