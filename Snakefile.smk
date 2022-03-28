configfile: "config.yaml"

from os.path import join as pjoin

INPUT = config["inf"]
WDIR = config["wdir"]

Ns = range(20)

rule all:
   input:
     pjoin(WDIR, "final-out.fa")

rule create_subfile:
    input:
        INPUT
    output:
        pjoin(WDIR, "output-{n}.fa")
    params:
        n = "{n}"
    shell:
        "python bioinformatica.py {input} {params.n} {wildcards.n} > {output.fa}"

rule create_file:
    input:
        expand(pjoin(WDIR, "output-{n}.fa"), n = Ns)
    output:
        pjoin(WDIR, "final-out.fa")
    shell:
        ""
rule moni_index:
    input:
        pjoin(WDIR, "final-out.fa")
    output:
        pjoin(WDIR, "moni-out.txt")
    shell:
        "moni build -r {input} -o {output} -f"

rule bwa_index:
    input:
        pjoin(WDIR, "final-out.fa")
    output:
        pjoin(WDIR, "bwa-out.txt")
    shell:
        "bwa index -a bwtsw {input.fa} > {output} "

rule pingpong_index:
    input:
        pjoin(WDIR, "final-out.fa")
    output:
        pjoin(WDIR, "pingpong-out.txt")
    shell:
        "PingPong index --binary --fasta {input.fa} --index {output}"
