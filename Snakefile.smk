configfile: "config.yaml"

from os.path import join as pjoin

INPUT = config["inf"]
WDIR = config["wdir"]
HTSLIBDIR = config["htslibdir"]


rule all:
   input:
     pjoin(WDIR, "output-{n}.fa"),
     pjoin(WDIR, "moni-out.thrbv.ms"),
     pjoin(WDIR, "bwa-out.bwt"),
     pjoin(WDIR, "pingpong-out.bin")

rule create_subfile:
    input:
        INPUT
    output:
        pjoin(WDIR, "output-{n}.fa")
    params:
        n = "{n}"
    shell:
        "python bioinformatica.py {input} {params.n} {wildcards.n} > {output.fa}"

rule moni_index:
    input:
        pjoin(WDIR, "output-{n}.fa")
    output:
        pjoin(WDIR, "moni-out.thrbv.ms")
    params:
        bench = pjoin(WDIR, "moni-bench.txt")
    shell:
        " \time -v -o {params.bench} moni build -r {input} -o {output} -f"

rule bwa_index:
    input:
        pjoin(WDIR, "output-{n}.fa")
    output:
        pjoin(WDIR, "bwa-out.bwt")
    params:
        bench = pjoin(WDIR, "bwa-beanch.txt")
    shell:
        " \time -v -o {params.bench} bwa index -a bwtsw {input.fa} > {output.bwt} "

rule pingpong_index:
    input:
        HTSLIBDIR,
        pjoin(WDIR, "output-{n}.fa")
    output:
        pjoin(WDIR, "pingpong-out.bin")
    params:
        bench = pjoin(WDIR, "pingpong-bench.txt")
    shell:
        "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{input}",
        " \time -v -o {params.bench} PingPong index --fastq {input.fa} --index {output.bin}"
