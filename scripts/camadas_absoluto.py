"""Complemento do passo 2: o que importa e |Z| em si (negativo = suprimida em termos absolutos),
nao so em relacao a contagem. Valor = ln|Z| / n^2. Teias de altura <= 2, soma exata.
Uso: python camadas_absoluto.py"""
import mpmath as mp, numpy as np
from camadas_variaveis import lnZ, F
mp.mp.dps = 400
ns = (40, 80, 120)
print('   l     alfa    ' + '   '.join(f'n={n:3d}' for n in ns))
for l in np.round(np.concatenate([[0.832], np.arange(5.4, 8.41, 0.2), np.arange(11.0, 13.01, 0.25)]), 3):
    b = np.sqrt(2/3)*(l/F)**2
    v = [float(lnZ(n, b)/n**2) for n in ns]
    print(f' {l:5.2f}  {0.5/l**2:.5f}  ' + '  '.join(f'{x:+8.4f}' for x in v) + ('   SUPRIMIDA' if max(v) < 0 else ''), flush=True)
