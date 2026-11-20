"""phi_n exato em n = 9 e 10 (PREREGISTRO_N9N10.md) - certificados de que cada classe de altura >= 3 cabe em 3+1.
Primeira passada: metodo da entrega B (delta = 0,05, ate 200 recomecos). Segunda passada, so para as nao certificadas:
delta = 0,01, ate 2000 recomecos. Coordenadas arredondadas para 6 casas e conferidas em fracoes.
Uso: python h1b_N_cert.py n trabalhador total_trabalhadores  ->  h1b_N_cert_n{n}_t{k}.npz (gravado a cada 20.000 classes)
estado: 0 nao tentada, 1 certificada na 1a passada, 2 certificada na 2a, -1 sem certificado apos a 1a, -2 sem certificado apos a 2a."""
import sys, os, time, numpy as np
import h1b_B_exato as BX

def roda(n, k, K):
    d = np.load(f'h1b_N_n{n}.npz'); P = d['pred']; h = d['h']
    idx = np.where(h >= 3)[0][k::K]; arq = f'h1b_N_cert_n{n}_t{k}.npz'
    if os.path.exists(arq):
        s = np.load(arq); est = s['estado']; tent = s['tentativas']; coords = s['coords']
    else:
        est = np.zeros(len(idx), np.int8); tent = np.zeros(len(idx), np.int32); coords = np.full((len(idx), 4*n), np.nan, np.float64)
    def grava():
        np.savez(arq + '.tmp.npz', indices=idx, estado=est, tentativas=tent, coords=coords); os.replace(arq + '.tmp.npz', arq)
    t0 = time.time()
    for passada, delta, recom, alvo, ok_, falha in ((1, 0.05, 200, 0, 1, -1), (2, 0.01, 2000, -1, 2, -2)):
        BX.DELTA = delta; BX.RECOMECOS = recom; rng = np.random.default_rng([20261123, 777, n, k, passada])
        feitos = 0
        for j in np.where(est == alvo)[0]:
            C = ((P[idx[j]] >> np.arange(n)[:, None]) & 1).astype(bool)
            X, t = BX.certifica(C, rng); tent[j] += t
            if X is not None: est[j] = ok_; coords[j] = [float(v) for linha in X for v in linha]
            else: est[j] = falha
            feitos += 1
            if feitos % 20_000 == 0:
                grava(); print(f'  n={n} t{k} passada {passada}: {feitos}, {time.time()-t0:.0f}s', flush=True)
        grava()
        print(f'n={n} t{k}: fim da passada {passada}; certificadas {int((est > 0).sum())}, sem certificado {int((est < 0).sum())}, '
              f'nao tentadas {int((est == 0).sum())}; {time.time()-t0:.0f}s', flush=True)

if __name__ == '__main__':
    roda(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
