"""PREREGISTRO_D11.md, recuperacao tecnica (24/11/2026): a execucao unica de h1b_D11_analise.py foi interrompida por falta de
memoria (OOM) DEPOIS de imprimir a primaria e a sensibilidade, e ANTES das secundarias e do JSON.
Este script: (1) refaz os controles com as MESMAS funcoes e sementes (calculo determinista) e exige que os valores
coincidam com os impressos na execucao unica; (2) guarda todos os controles; (3) faz as secundarias com pouca memoria.
Uso: python h1b_D11_secundarias.py PASTA_PARTES SAIDA_JSON"""
import sys, json, math, gc, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_dimensao import faixa, NOMES
from h1b_decoerencia import razoes_controle, analisa, TH_JANELA
from h1b_dimensao_piloto import diamante, camadas, perfil

IMPRESSO = {'R3': '8.055', 'sens': '8.608', 'real': ['2.6066e-03', '4.1178e-04', '5.6589e-03']}

def main():
    pasta, saida = sys.argv[1], sys.argv[2]; n = 11
    D = [np.load(f'{pasta}/h1b_D11_n{n}_parte{x}.npz') for x in range(20)]
    B = np.concatenate([d['B'] for d in D]).astype(np.int64); w = 1.0 / np.concatenate([d['aut'] for d in D])
    R = np.concatenate([d['R'] for d in D]); g = faixa(R.astype(float) / math.comb(n, 2)); del D; gc.collect()
    prim = razoes_controle(B, w, g, np.random.default_rng(20261125), sorteios=20, faixas=(0, 1, 2))
    sens = razoes_controle(B, w, g, np.random.default_rng(20261126), sorteios=200, faixas=(2,))
    confere = (f'{prim[2][2]:.3f}' == IMPRESSO['R3'] and f'{sens[2][2]:.3f}' == IMPRESSO['sens']
               and [f'{prim[k][0]:.4e}' for k in (0, 1, 2)] == IMPRESSO['real'])
    print(f'Recalculo determinista confere com a execucao unica: {confere} (R_3 = {prim[2][2]:.4f}, sensibilidade = {sens[2][2]:.4f})')
    if not confere: raise SystemExit('NAO CONFERE: nada e gravado')
    sec = {}
    p, mu, I, coer = analisa(B, w, g, NOMES, TH_JANELA)
    sec['Myrheim-Meyer'] = (NOMES, p, mu, I, coer)
    # particao por perfil, em blocos (mesmos centroides: semente 20261127, mesma ordem de sorteio)
    rng = np.random.default_rng(20261127); refs = {}
    for nome, fn in (('d=2', lambda: diamante(n, 2, rng)), ('d=3', lambda: diamante(n, 3, rng)),
                     ('d=4', lambda: diamante(n, 4, rng)), ('camadas', lambda: camadas(n, rng, True))):
        V = []
        for _ in range(4000):
            Nn, R4, hh = perfil(fn()); V.append(np.r_[Nn, R4, hh] / np.r_[[math.comb(n, 2)] * 5, n])
        refs[nome] = np.array(V)
    sd = np.vstack(list(refs.values())).std(0) + 1e-9; cen = [v.mean(0) / sd for v in refs.values()]
    gp = np.zeros(len(B), np.int8); escala = np.r_[[math.comb(n, 2)] * 5, n] * sd
    for x in range(20):
        d = np.load(f'{pasta}/h1b_D11_n{n}_parte{x}.npz'); ini = sum(len(np.load(f'{pasta}/h1b_D11_n{n}_parte{j}.npz')['B']) for j in range(x)) if x else 0
        N = d['N'].astype(float); R4 = d['R'].astype(float) - N.sum(1)
        V = np.c_[N, R4, d['h'].astype(float)] / escala
        dist = np.stack([((V - c) ** 2).sum(1) for c in cen], 1); gp[ini:ini + len(V)] = dist.argmin(1); del V, dist, N, R4
    p, mu, I, coer = analisa(B, w, gp, list(refs), TH_JANELA)
    sec['perfil de intervalos'] = (list(refs), p, mu, I, coer)
    out = {}
    for rot, (nomes, p, mu, I, coer) in sec.items():
        print(f'\nSECUNDARIA, particao {rot}: indice I mediana {np.median(I):.2f} [min {I.min():.2f}, max {I.max():.2f}]; '
              f'|Z|^2/soma|Z_g|^2 mediana {np.median(coer):.2e}')
        for k, nm in enumerate(nomes):
            print(f'   {nm:9s}: p {p[k]:.4f} -> mu mediana {np.median(mu[:, k]):.4f} [{mu[:, k].min():.4f}, {mu[:, k].max():.4f}]')
        out[rot] = dict(nomes=nomes, p=p.tolist(), mu_mediana=np.median(mu, 0).tolist(), mu_min=mu.min(0).tolist(), mu_max=mu.max(0).tolist(),
                        I_mediana=float(np.median(I)), I_min=float(I.min()), I_max=float(I.max()), coer_mediana=float(np.median(coer)))
    json.dump(dict(R3=prim[2][2], veredito='CONFIRMA o criterio pre-registrado (R_3 > 6,0)', recalculo_confere=confere,
                   primaria={NOMES[k]: dict(real=v[0], controles=v[1], razao=v[2]) for k, v in prim.items()},
                   sensibilidade=dict(real=sens[2][0], controles=sens[2][1], razao=sens[2][2]), secundarias=out),
              open(saida, 'w'), indent=1)
    print('\nJSON gravado:', saida)

if __name__ == '__main__':
    main()
