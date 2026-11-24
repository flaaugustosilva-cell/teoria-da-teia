"""PREREGISTRO_D11.md: analise congelada do teste de coerencia dimensional em n = 11 (todas as ordens).
Uso: python h1b_D11_analise.py N PASTA_PARTES NUMERO_DE_PARTES [PASTA_N11AUX] [SAIDA_JSON]
 - Le as partes 0..P-1 em ordem; concatena as classes nessa ordem (a ordem importa para os sorteios).
 - Validacoes (n = 11): total de classes 46749427; soma com sinal de cada parte = parte auxiliar; ruins (altura <= 2) = -1.
 - Primaria: R_3 = coerencia da faixa 2,5-3,5 / mediana de 20 controles (semente 20261125, faixas 0, 1, 2 nessa ordem).
 - Sensibilidade: 200 controles para a faixa 2,5-3,5 (semente 20261126).
 - Secundarias: razoes das faixas 0 e 1; indice I; |Z|^2/sum|Z_g|^2; p -> mu; particao por perfil (semente 20261127)."""
import sys, json, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_dimensao import faixa, NOMES
from h1b_decoerencia import razoes_controle, analisa, TH_JANELA
from h1b_dimensao_piloto import diamante, camadas, perfil

def grupos_perfil_armazenado(N, R, h, n, rng, M=4000):
    refs = {}
    for nome, g in (('d=2', lambda: diamante(n, 2, rng)), ('d=3', lambda: diamante(n, 3, rng)),
                    ('d=4', lambda: diamante(n, 4, rng)), ('camadas', lambda: camadas(n, rng, True))):
        V = []
        for _ in range(M):
            Nn, R4, hh = perfil(g()); V.append(np.r_[Nn, R4, hh] / np.r_[[math.comb(n, 2)] * 5, n])
        refs[nome] = np.array(V)
    sd = np.vstack(list(refs.values())).std(0) + 1e-9; cen = [v.mean(0) / sd for v in refs.values()]
    R4 = R.astype(np.int64) - N.astype(np.int64).sum(1)
    V = np.c_[N.astype(float), R4, h] / np.r_[[math.comb(n, 2)] * 5, n] / sd
    dist = np.full(len(R), np.inf); g = np.zeros(len(R), int)
    for k, c in enumerate(cen):
        dk = ((V - c) ** 2).sum(1); m = dk < dist; dist[m] = dk[m]; g[m] = k
    return g, list(refs)

def main():
    n, pasta, partes = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
    aux = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != '-' else None
    saida = sys.argv[5] if len(sys.argv) > 5 else None
    D = [np.load(f'{pasta}/h1b_D11_n{n}_parte{x}.npz') for x in range(partes)]
    B = np.concatenate([d['B'] for d in D]).astype(np.int64); A = np.concatenate([d['aut'] for d in D])
    N = np.concatenate([d['N'] for d in D]); R = np.concatenate([d['R'] for d in D]); h = np.concatenate([d['h'] for d in D])
    fat = math.factorial(n); L = fat // A; s = np.where(B % 2 == 0, 1, -1)
    val = dict(classes=int(len(B)), T_todas=int((L * s).sum()), ruins=int((L * s)[h <= 2].sum()))
    print(f'Validacao: classes {val["classes"]}; soma com sinal {val["T_todas"]:+d}; ruins (altura <= 2) {val["ruins"]:+d}')
    ok = val['ruins'] == -1
    if aux:
        for x, d in enumerate(D):
            a = np.load(f'{aux}/h1b_N11_n11_parte{x}.npz')
            Taux = sum(int(p) * (1 if b % 2 == 0 else -1) for (b, h3, c), p in zip(a['chaves'], a['peso']))
            Lx = fat // d['aut']; sx = np.where(d['B'] % 2 == 0, 1, -1)
            okx = (int((Lx * sx).sum()) == Taux) and (len(d['B']) == int(a['total_classes'])); ok &= okx
            if not okx: print(f'  parte {x} DIFERE da parte auxiliar')
        ok &= val['classes'] == 46749427 and val['T_todas'] == -40491236963
    print(f'Validacoes obrigatorias: {"OK" if ok else "FALHARAM -> resultado INCONCLUSIVO"}')
    w = 1.0 / A; r = R.astype(float) / math.comb(n, 2); g = faixa(r)
    # ---- primaria ----
    prim = razoes_controle(B, w, g, np.random.default_rng(20261125), sorteios=20, faixas=(0, 1, 2))
    R3 = prim[2][2]
    if not ok: veredito = 'INCONCLUSIVO'
    elif R3 > 6.0: veredito = 'CONFIRMA o criterio pre-registrado (R_3 > 6,0)'
    elif R3 > 1.0: veredito = 'EXCESSO sobre o controle, mas NAO confirma a previsao mais forte (1 < R_3 <= 6,0)'
    else: veredito = 'NAO confirma nem o excesso sobre o controle (R_3 <= 1)'
    print(f'\nPRIMARIA: R_3({n}) = {R3:.3f} (referencia R_3(10) = 6.044) -> {veredito}')
    for k, v in prim.items():
        print(f'  {NOMES[k]}: real {v[0]:.4e}; controles mediana {np.median(v[1]):.4e} [{min(v[1]):.3e}, {max(v[1]):.3e}]; razao {v[2]:.3f}')
    # ---- sensibilidade ----
    sens = razoes_controle(B, w, g, np.random.default_rng(20261126), sorteios=200, faixas=(2,))
    cs = np.array(sens[2][1])
    print(f'\nSENSIBILIDADE (200 controles, faixa 2,5-3,5): razao {sens[2][2]:.3f}; controles: mediana {np.median(cs):.3e}, '
          f'percentis 2,5% e 97,5% {np.percentile(cs, 2.5):.3e} e {np.percentile(cs, 97.5):.3e}, maximo {cs.max():.3e}; '
          f'real/maximo = {sens[2][0]/cs.max():.2f}')
    # ---- secundarias ----
    sec = {}
    for rot, gg, nomes in (('Myrheim-Meyer', g, NOMES),) + ((('perfil de intervalos',) + grupos_perfil_armazenado(N, R, h, n, np.random.default_rng(20261127))),):
        p, mu, I, coer = analisa(B, w, gg, nomes, TH_JANELA)
        print(f'\nSECUNDARIA, particao {rot}: indice I mediana {np.median(I):.2f} [min {I.min():.2f}, max {I.max():.2f}]; '
              f'|Z|^2/soma|Z_g|^2 mediana {np.median(coer):.2e}')
        for k, nm in enumerate(nomes):
            print(f'   {nm:9s}: p {p[k]:.4f} -> mu mediana {np.median(mu[:, k]):.4f} [{mu[:, k].min():.4f}, {mu[:, k].max():.4f}]')
        sec[rot] = dict(p=p.tolist(), mu_mediana=np.median(mu, 0).tolist(), I_mediana=float(np.median(I)), coer_mediana=float(np.median(coer)))
    if saida:
        json.dump(dict(validacao=val, validacoes_ok=bool(ok), R3=R3, veredito=veredito,
                       primaria={NOMES[k]: dict(real=v[0], controles=v[1], razao=v[2]) for k, v in prim.items()},
                       sensibilidade=dict(real=sens[2][0], controles=sens[2][1], razao=sens[2][2]), secundarias=sec),
                  open(saida, 'w'), indent=1)

if __name__ == '__main__':
    main()
