"""Checa o metodo aleatorizado numa teia grande: mesma teia, subespaco maior e mais iteracoes.
Se S nao muda, o metodo esta convergido. Uso: python convergencia.py N"""
import sys, numpy as np, grande
N = int(sys.argv[1]); orig = grande.modos_positivos
for folga, pot in ((150, 2), (900, 4)):
    grande.modos_positivos = lambda A, M, rng, f=folga, k=pot: orig(A, M, rng, folga=f, pot=k)
    S = grande.entropia(N, 0.315, np.random.default_rng(4242))
    print(f'N = {N}, folga = {folga}, iteracoes = {pot}: S = {S[0]:.2f}  ({S[4]:.0f} s)', flush=True)
