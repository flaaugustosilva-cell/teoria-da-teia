"""H1, segunda etapa, entrega C (PREREGISTRO.md secao C + DECISOES_H1STAR.md): mapa de |phi_sorteio| na janela.
Diamante 3+1, condicionado a altura >= 3, semente 20261122. Guarda o histograma de B em 50 blocos contiguos.
Uso (de dentro de scripts): python h1b_C_sorteio.py 6 8 ...   ->  h1b_C_n{n}.npz
Retomada: ao fim de cada bloco grava h1b_C_n{n}_parcial.npz com o histograma e o estado exato do gerador;
se o processo for interrompido, rodar de novo continua do ultimo bloco, com a mesma sequencia de sorteios.
Interpretacao restrita: estuda so o conjunto do sorteio; nao e evidencia sobre H1*."""
import sys, os, time, json, numpy as np
from h1_robustez import lote
M = {6: 10**8, 8: 10**8, 10: 10**8, 12: 10**8, 14: 10**7, 16: 10**7, 20: 10**7, 24: 10**7}
SEMENTE = 20261122; LOTE = 20_000; G = 50; OFF = 6000; TAM = 2*OFF + 1
for n in map(int, sys.argv[1:]):
    if os.path.exists(f'h1b_C_n{n}.npz'): print(f'n={n}: ja concluido', flush=True); continue
    rng = np.random.default_rng([SEMENTE, 4, n]); nl = M[n] // LOTE; por_bloco = nl // G
    hist = np.zeros((G, TAM), np.int64); desc = 0; k0 = 0; parc = f'h1b_C_n{n}_parcial.npz'
    if os.path.exists(parc):
        p = np.load(parc); hist = p['hist']; desc = int(p['desc']); k0 = int(p['k'])
        rng.bit_generator.state = json.loads(str(p['estado'])); print(f'  n={n}: retomando do lote {k0}', flush=True)
    t0 = time.time()
    for k in range(k0, nl):
        B, _, d = lote(LOTE, n, 4, rng, False); desc += d
        assert B.min() > -OFF and B.max() < OFF, 'B fora da faixa do histograma'
        hist[k // por_bloco] += np.bincount(B + OFF, minlength=TAM)
        if (k + 1) % por_bloco == 0:
            np.savez(parc + '.tmp.npz', hist=hist, desc=desc, k=k + 1, estado=json.dumps(rng.bit_generator.state))
            os.replace(parc + '.tmp.npz', parc)
            print(f'  n={n}: bloco {(k + 1)//por_bloco}/{G}, {time.time()-t0:.0f}s', flush=True)
    np.savez_compressed(f'h1b_C_n{n}.npz', hist=hist, offset=OFF, sorteios=M[n], descartadas=desc)
    if os.path.exists(parc): os.remove(parc)
    print(f'n={n}: sorteios {M[n]}, validas {hist.sum()}, descartadas {desc}', flush=True)
