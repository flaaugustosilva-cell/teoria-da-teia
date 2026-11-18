"""O corte da literatura e a maior anticadeia sao o mesmo numero? (18/11/2026)
Belenchia e outros (1712.04227) cortam o espectro de iDelta "onde ele despenca", escolhendo c_d a olho
em 3D e 4D (valores nao publicados); em 2D o corte e raiz(N)/(4 pi) (Sorkin-Yazdi).
Aqui o "joelho" vira regra fixa, a mesma em toda dimensao: inclinacao local de ln(lambda_k) contra ln(k)
(em janela de fator 1,5 em k); patamar = mediana das inclinacoes para k de 5 a 20; joelho = primeiro k > 20
em que a inclinacao fica 2 vezes mais ingreme que o patamar. Compara com a largura (maior anticadeia).
Green: 2D C/2; 3D 1/(2 pi tau); 4D ligacoes (escala nao muda a contagem).
Uso: python joelho.py"""
import numpy as np
from ssee import sorteia
from largura_fluxo import ligacoes, largura_por_fluxo

def espectro(p, d):
    dt = p[None, :, 0] - p[:, None, 0]; dr2 = ((p[None, :, 1:] - p[:, None, 1:])**2).sum(2)
    C = (dt > 0) & (dt*dt > dr2)
    if d == 2: G = 0.5*C
    elif d == 3: G = np.where(C, 1/(2*np.pi*np.sqrt(np.where(C, dt*dt - dr2, 1.0))), 0.0)
    else:
        Cf = C.astype(np.float32); G = (C & ((Cf @ Cf) == 0)).astype(np.float64)
    del dt, dr2
    l = np.linalg.eigvalsh(1j*(G - G.T)); return np.sort(l[l > 0])[::-1]

def joelho(lam):
    k = np.arange(1, len(lam) + 1); lk, ll = np.log(k), np.log(lam)
    def incl(i):
        j = (k >= k[i]/1.22) & (k <= k[i]*1.22); return np.polyfit(lk[j], ll[j], 1)[0]
    plat = np.median([incl(i) for i in range(4, 20)])
    for i in range(20, len(lam) - 5):
        if incl(i) < 2*plat: return i + 1, plat
    return len(lam), plat

for d, Ns in ((2, (1000, 2000, 4000)), (3, (1000, 2000, 4000)), (4, (1000, 2000, 4000))):
    print(f'--- {d} dimensoes ---')
    for N in Ns:
        res = []
        for s in range(2):
            p = sorteia(N, d, np.random.default_rng(100*N + 10*d + s)); lam = espectro(p, d)
            r, c = ligacoes(p); w = largura_por_fluxo(N, r, c); kj, pl = joelho(lam)
            sy = int(np.sum(lam > np.sqrt(N)/(4*np.pi))) if d == 2 else -1
            res.append((w, kj, pl, sy))
        r = np.array(res, float).mean(0)
        print(f' N = {N}: largura = {r[0]:.0f}  joelho = {r[1]:.0f}  (inclinacao do patamar {r[2]:.2f})  joelho/largura = {r[1]/r[0]:.2f}'
              + (f'  corte de Sorkin-Yazdi guarda {r[3]:.0f}' if d == 2 else ''), flush=True)
