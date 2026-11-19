"""H1, segunda etapa, entrega B - soma exata de phi_n e comparacao com o sorteio (EMENDA_B.md).
Le h1b_B_n{n}.npz e h1b_B_sorteio_n{n}.npz. Uso: python h1b_B_compara.py 5 6 7 8  ->  h1b_B_resultados.json
phi_n = sum_{naturais, altura>=3, certificadas} e^{i theta B}/e(P) / W_cert   (peso 1/|Aut|; ver EMENDA_B.md)
Cota: |phi_n - phi_cert| <= 2 W_nc / W_cert.  Verificacao: peso 1 por classe.
Descritivo extra (nao registrado): distancia de variacao total entre as distribuicoes de B das duas medidas."""
import sys, json, math, numpy as np
from e1_comum import beta_de
TH = (0.01, 0.02, 0.03, 0.045, 0.06, 0.08, 0.10, 0.13, 0.16, 0.20, 0.25, 0.32)
JAN = {'x=6': 2*beta_de(6.0), 'x=7': 2*beta_de(7.0), 'x=8': 2*beta_de(8.0)}
ANG = [(str(t), t) for t in TH] + list(JAN.items()); G = 50
out = {}
for n in map(int, sys.argv[1:]):
    d = np.load(f'h1b_B_n{n}.npz'); s = np.load(f'h1b_B_sorteio_n{n}.npz')
    B, h, e, cl, cert = d['B'], d['h'], d['e'].astype(float), d['classe'], d['certificada']
    boa = h >= 3; c_ok = cert[cl] & boa; c_nc = (~cert[cl]) & boa
    w = 1/e; Wc = w[c_ok].sum(); Wnc = w[c_nc].sum(); cota = 2*Wnc/Wc
    rep = {}; [rep.setdefault(c, i) for i, c in enumerate(cl)]
    Bcl = np.array([B[rep[c]] for c in sorted(rep) if cert[c] and h[rep[c]] >= 3])
    Bs = s['B'].astype(float); N = len(Bs); blocos = np.array_split(np.arange(N), G)
    # distribuicoes de B (descritivo)
    vals = np.union1d(np.unique(B[c_ok]), np.unique(Bs))
    pe = np.array([w[c_ok][B[c_ok] == v].sum() for v in vals])/Wc; ps = np.array([np.mean(Bs == v) for v in vals])
    tv = 0.5*np.abs(pe - ps).sum()
    res = dict(W_cert=Wc, W_nc=Wnc, cota=cota, classes_boas_cert=len(Bcl), sorteios_validos=N, descartadas=int(s['descartadas']),
               TV_B=tv, media_B_exata=float((pe*vals).sum()), media_B_sorteio=float(Bs.mean()), angulos={})
    print(f'\nn={n}: W_cert = {Wc:.6f}, W_nc = {Wnc} (cota {cota}), classes boas certificadas {len(Bcl)}, sorteios validos {N}')
    print(f'  media de B: exata (1/|Aut|) {res["media_B_exata"]:.3f}, sorteio {res["media_B_sorteio"]:.3f}; TV entre as distribuicoes de B = {tv:.3f}')
    print('  angulo   |phi_n|^2 exato   |phi_classes|^2   Q sorteio (+- ep)        |Delta| em erros   Re/Im phi_n            Re/Im sorteio')
    for nome, th in ANG:
        phin = np.sum(w[c_ok]*np.exp(1j*th*B[c_ok]))/Wc; phic = np.mean(np.exp(1j*th*Bcl))
        z = np.exp(1j*th*Bs); m = z.mean(); ep = math.sqrt(max(1 - abs(m)**2, 0)/N)
        sb = np.array([z[b].sum() for b in blocos]); nb = np.array([len(b) for b in blocos]); S = sb.sum()
        Q = (abs(S)**2/N - 1)/(N - 1); Sk = S - sb; Nk = N - nb; Qk = (np.abs(Sk)**2/Nk - 1)/(Nk - 1)
        epQ = math.sqrt((G - 1)/G*np.sum((Qk - Qk.mean())**2)); dz = abs(m - phin)/ep
        res['angulos'][nome] = dict(theta=th, phi_n=[phin.real, phin.imag], mod2_exato=abs(phin)**2, mod2_classes=abs(phic)**2,
                                    phi_sorteio=[m.real, m.imag], ep_sorteio=ep, Q=Q, ep_Q=epQ, Delta=abs(m - phin), Delta_em_erros=dz)
        print(f'  {nome:6s}  {abs(phin)**2:14.6e}  {abs(phic)**2:14.6e}  {Q:12.4e} +- {epQ:.1e}  {dz:12.1f}       '
              f'{phin.real:+.4f}{phin.imag:+.4f}i   {m.real:+.4f}{m.imag:+.4f}i')
    out[n] = res
json.dump(out, open('h1b_B_resultados.json', 'w'), indent=1)
