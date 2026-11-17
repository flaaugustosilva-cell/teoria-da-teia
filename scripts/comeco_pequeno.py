"""Reflexao 12: o comeco tem baixa entropia por ser pequeno? (17/11/2026)
Era da radiacao, unidades de Planck (G = hbar = c = k = 1, l_P = raiz(G hbar)).
Horizonte de particulas r = 2t. Entropia da radiacao dentro dele: s = (2 pi^2/45) g T^3, V = 4/3 pi r^3.
Temperatura pela equacao de Friedmann: H = 1/(2t), H^2 = (8 pi/3) rho, rho = (pi^2/30) g T^4.
Entropia maxima (area do horizonte): S_max = pi r^2 (A/4 = 4 pi r^2 / 4).
Na teia: moleculas de horizonte = a4 * rho_teia^(1/2) * A; com o grao l, S_max = A / (4 l^2) so se
 1 nat por molecula e l = 0,83 (a tensao conhecida); aqui uso so a lei de area.
Uso: python comeco_pequeno.py"""
from math import pi
tP = 5.39e-44   # s
def razao(t, g):
    H = 1/(2*t); rho = 3*H*H/(8*pi); T = (30*rho/(pi*pi*g))**0.25
    r = 2*t; Srad = (2*pi**2/45)*g*T**3*(4/3)*pi*r**3; Smax = pi*r*r
    return T, Srad, Smax
print('  tempo            T (Planck)   S radiacao     S maxima      razao')
for nome, ts, g in (('1 tempo de Planck', tP, 106.75), ('1e-36 s', 1e-36, 106.75), ('1e-12 s', 1e-12, 106.75),
                    ('1 s', 1.0, 10.75), ('3 minutos', 180.0, 3.36), ('50 mil anos', 1.6e12, 3.36)):
    T, Sr, Sm = razao(ts/tP, g)
    print(f'  {nome:17s} {T:10.2e}   {Sr:10.2e}   {Sm:10.2e}   {Sr/Sm:10.2e}')
print('Lei: razao cai como t^(-1/2) (S_rad ~ t^(3/2), S_max ~ t^2).')
