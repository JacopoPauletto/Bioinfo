rule my_fasta_subsample:
    input : 
        "{dataset}\Homo_sapiens.GRCh38.cdna.all.fa.gz"
    output : 
        "{dataset}\transcript.{sample}.fa"
    params:
        "{sample}"
    shell : 
        "python3 bioinformatica.py {input} {output} "