# Bioinfo

Trasforma un genoma e un annotazione in un insieme di tracsritti :
```
gffread -w out-transcript.fa -g genome.fa annotation.gtf 
```
Trasforma il sample da FASTA nel rispettivo FASTQ
```
seqtk seq -F '#' sample_1.fa > sample_1.fq
```
Indicizza il trascrittoma (out-transcript.fa)
```
./PingPong index --fastq out-transcript.fa --index test-index.fmd
```
Cerca le stringhe specifiche del sample nell'indice
```
./PingPong search --index test-index.fmd --fastq sample_1.fq --overlap -1 --threads 1
```
Uniscie tutte le specifiche relative ad una read che si sovrappongono creandono una sola 
```
python new_solution.py solution_bath_0.sfs
```
Crea un FASTA contenente tutte porzioni non-specifiche con la loro posizione nelle read
```
python sfs_read.py new_solution_out.sfs sample_1.fq 
```
Scarta tutte le read che contengono una sola non-specifica
```
python discard_singleton non_specific_read.fa
```
Scarta tutte le read con una non-specifica di lunghezza minore di un valore [n]
```
python discard.py disc_singleton_non_spec.fa n 
```
Indicizza il genoma 
```
bwa index genome.fa -p gen
```
Trova i matches delle non-specifiche sull'indice del genoma
```
bwa fastmap gen disc_non_specific.fa > bwa_fastmap_gen.matches
```
Prende il file dei macthes e scarta tutte le read che hanno un solo match e tutte quelle che hanno due o più matches ma che si trovano ad una distanaza inferiore di un valore [n]
```
python SMEM_clear.py bwa_fastmap_gen.matches n 
```
Crea un file SAM relativo ai matches filtrati 
```
python SMEM_read.py bwa_cleared.matches disc_non_specific.fa genome.fa
```
Trasforma il file SAM nel rispettivo file BAM
```
samtools view -bS outFile.sam > outFile.bam
```
Ordina il file BAM
```
samtools sort outFile.bam > outFile.sorted.bam
```
Indicizza il file BAM 
```
samtools index outFile.sorted.bam
```


