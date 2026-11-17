"""Passo 2 (17/11/2026): soma quantica exata sobre TODAS as teias de altura <= 2 (com nome).
Teia de altura <= 2 = conjunto A de minimais + resto B; cada no de B fica acima de >= 1 no de A.
Acao so de ligacoes (em altura 2 todo par relacionado e ligacao): S/hbar = mu*(n - L), mu = 2*beta,
beta = raiz(2/3)*(l/l_p)^2, l_p^2 = 8 pi G hbar.
Z = e^{i mu n} * soma_a C(n,a) * ((1+x)^a - 1)^(n-a),  x = e^{-i mu}  (exata).
Contagem pura (mu = 0): soma_a C(n,a) (2^a - 1)^(n-a).
Mede ln|Z| - ln(contagem) por n^2: negativo e crescente em modulo = supressao.
Uso: python camadas_variaveis.py"""
import mpmath as mp, numpy as np
mp.mp.dps = 400
F = np.sqrt(8*np.pi)
def lnZ(n, beta):
    x = mp.exp(-2j*beta); s = mp.mpf(0)
    for a in range(1, n+1): s += mp.binomial(n, a) * ((1+x)**a - 1)**(n-a)
    return mp.log(abs(s)) if s != 0 else -mp.inf
def lnC(n): return mp.log(sum(mp.binomial(n, a)*(2**a-1)**(n-a) for a in range(1, n+1)))
if __name__ == '__main__':
    print('Varredura do grao l (em l_P = raiz(G hbar)); valor = [ln|Z| - ln(contagem)] / n^2')
    ns = (20, 40, 80); lc = {n: lnC(n) for n in ns}
    print('   l     alfa      ' + '   '.join(f'n={n:3d}' for n in ns) + '   janela da formula simples')
    for l in np.round(np.concatenate([[0.832], np.arange(4.0, 20.01, 0.5)]), 3):
        b = np.sqrt(2/3)*(l/F)**2; jan = abs(np.cos(b)) < 0.5
        v = [float((lnZ(n, b) - lc[n])/n**2) for n in ns]
        print(f' {l:5.2f}  {0.5/l**2:.5f}  ' + '  '.join(f'{x:+7.3f}' for x in v) + ('   dentro' if jan else ''), flush=True)
