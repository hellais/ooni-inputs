#!/bin/bash

workdir=$(mktemp -d)

wget http://www.iaui.gov.lv/images/Blokesana/Block_domain.pdf -O "$workdir/list.pdf" > /dev/null
pdftotext -layout -nopgbrk "$workdir/list.pdf" "$workdir/list.txt"
grep -P -o '^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}' "$workdir/list.txt"

rm -rf "$workdir"
