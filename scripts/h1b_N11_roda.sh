#!/bin/bash
# executor da investigacao auxiliar n = 11: processa as partes indicadas, pulando as ja gravadas
G=${GENPOSETG:-/home/claude/ferramentas/pynauty-2.8.8.1/src/nauty2_8_8/genposetg}   # caminho do executavel compilado (ver n9n10/PROCEDENCIA_GENPOSETG.txt)
export PYTHONPATH=/home/claude/teoria-da-teia/scripts
cd /home/claude/n11
for x in "$@"; do
  [ -f h1b_N11_n11_parte$x.npz ] && { echo "parte $x ja gravada"; continue; }
  $G 11 t q m $x 20 2>/dev/null | python3 /home/claude/teoria-da-teia/scripts/h1b_N11_parte.py 11 $x
done
