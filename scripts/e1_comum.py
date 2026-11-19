"""E1 (pre-registrado em 19/11/2026 02:24): funcoes comuns.
Uso: de dentro da pasta scripts: python e1_validacao.py ; python e1_rodada.py ; python e1_diagnostico.py
(as saidas sao gravadas na pasta atual; as do autor estao em dados/e1/).
Acao de Benincasa-Dowker 4D, eps = 1: S/hbar = 2*beta*B, B = n - N0 + 9 N1 - 16 N2 + 8 N3,
beta = raiz(2/3) * x^2 / (8 pi), x = l / l_P (l_P = raiz(G hbar)).
Teias ruins: soma exata de scripts/camadas_variaveis.py (importada sem modificacao)."""
import os, sys, numpy as np
REPO = os.environ.get('REPO_SCRIPTS', os.path.dirname(os.path.abspath(__file__)))   # pasta scripts/
sys.path.insert(0, REPO)
import mpmath as mp
from camadas_variaveis import lnZ          # funcao original do repositorio

C_ACAO = np.sqrt(2/3); F = np.sqrt(8*np.pi)
def beta_de(x): return C_ACAO*(x/F)**2

def contagens(C):
    """C: matriz booleana n x n, C[i,j] = i antes de j. Devolve N0..N3 e se a altura e >= 3."""
    Ci = C.astype(np.float32); K = Ci @ Ci          # K[i,j] = elementos estritamente entre i e j
    Kr = np.rint(K).astype(np.int32)
    N = [int(np.sum(C & (Kr == m))) for m in range(4)]
    altura3 = bool(np.any(C & (Kr > 0)))
    return N, altura3

def B_de(n, N): return n - N[0] + 9*N[1] - 16*N[2] + 8*N[3]

def sorteia_diamante(n, rng):
    """n pontos uniformes no diamante causal |t| + r <= 1 em 3+1."""
    pts = np.empty((0, 4))
    while len(pts) < n:
        p = rng.uniform(-1, 1, (4*n, 4))
        ok = np.abs(p[:, 0]) + np.sqrt((p[:, 1:]**2).sum(1)) <= 1
        pts = np.vstack([pts, p[ok]])
    return pts[:n]

def causal(p):
    dt = p[None, :, 0] - p[:, None, 0]; dr2 = ((p[None, :, 1:] - p[:, None, 1:])**2).sum(2)
    return (dt > 0) & (dt*dt > dr2)

def tem_gemeos(C):
    """Dois elementos com o mesmo passado e o mesmo futuro (automorfismo de troca)."""
    assin = np.concatenate([C, C.T], 1)
    return len({r.tobytes() for r in assin}) < C.shape[0]

def lnZ_ruim(n, x, dps=400):
    mp.mp.dps = dps
    return float(lnZ(n, beta_de(x)))
