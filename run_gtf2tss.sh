#!/bin/bash
python gtf2tss.py --gtf "gencode.v28.primary_assembly.annotation.gtf" --outfile "gencode.v28.tss.bed" --flanking 5000
