"""Verificacao independente e exata dos certificados de n = 9 e 10, em aritmetica inteira.
As coordenadas certificadas tem 6 casas decimais; multiplicadas por 10^6 sao inteiros exatos (int64).
Para cada par: relacionado (i antes de j) exige dt > 0 e dt^2 - |dx|^2 > 0; nao relacionado exige dt^2 - |dx|^2 < 0.
Uso: python h1b_N_verifica.py n  ->  grava h1b_N_cert_n{n}_inteiros.npz (indices, estado, tentativas, coordenadas x 10^6)"""
import sys, glob, hashlib, numpy as np
n = int(sys.argv[1]); d = np.load(f'h1b_N_n{n}.npz'); P = d['pred']
idx, est, tent, X = [], [], [], []
for f in sorted(glob.glob(f'h1b_N_cert_n{n}_t[0-9].npz')):
    s = np.load(f); idx.append(s['indices']); est.append(s['estado']); tent.append(s['tentativas']); X.append(s['coords'])
idx = np.concatenate(idx); est = np.concatenate(est); tent = np.concatenate(tent); X = np.concatenate(X)
o = np.argsort(idx); idx, est, tent, X = idx[o], est[o], tent[o], X[o]
cert = est > 0
Xi = np.rint(X[cert]*1e6).astype(np.int64).reshape(-1, n, 4)
assert np.allclose(Xi/1e6, X[cert].reshape(-1, n, 4), atol=1e-12, rtol=0), 'coordenadas nao sao de 6 casas'
I, J = np.triu_indices(n, 1); ok = np.ones(len(Xi), bool)
for a in range(0, len(Xi), 200_000):
    Y = Xi[a:a+200_000]; Pp = P[idx[cert][a:a+200_000]]
    rel = ((Pp[:, J] >> I[None, :]) & 1).astype(bool)          # i antes de j (ordem natural: so i < j)
    D = Y[:, J, :] - Y[:, I, :]; dt = D[..., 0]; s2 = dt*dt - (D[..., 1:]**2).sum(-1)
    bom = np.where(rel, (dt > 0) & (s2 > 0), s2 < 0)
    ok[a:a+200_000] = bom.all(1)
print(f'n={n}: {int(cert.sum())} certificados conferidos em inteiros exatos; todos validos: {bool(ok.all())}; invalidos: {int((~ok).sum())}')
h = hashlib.sha256(Xi.tobytes()).hexdigest(); print(f'   sha256 das coordenadas inteiras: {h}')
np.savez_compressed(f'h1b_N_cert_n{n}_inteiros.npz', indices=idx, estado=est, tentativas=tent, coords_micro=Xi.reshape(len(Xi), -1).astype(np.int32), sha256=h)
