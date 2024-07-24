import argparse
import sys
import os
from .bowtie2_mode import bowtie2, parse_sam
from .kraken2_mode import kraken2, extract
from .fastp import qc
from .build_db import download_taxonomy, add_to_library, build_kraken2_db, build_bowtie2_db

def main():
    hostpurge_parser = argparse.ArgumentParser(
        prog="hostpurge",
        usage="%(prog)s [options] ...",
        description="HostPurge: A tool for purging host sequences from metagenomic data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        
    subparsers = hostpurge_parser.add_subparsers(dest='command', help='Commands')

    # Subparser for the "run" command
    run_parser = subparsers.add_parser('run', help='Run HostPurge with specified mode')
    run_parser.add_argument(
    "--mode", 
    choices=['a', 'b', 'c', 'd'], 
    default='c', 
    help="Mode of operation:\n"
    "a:just run with alignment type\n"
    "b:just run with kmer type\n"
    "c(default):firstly run kmer type then alignment type\n"
    "d:firstly run alignment type then kmer type\n")
    run_parser.add_argument("--alignment_db", dest="alignment_db",help="Path to the alignment database")
    run_parser.add_argument("--kmer_db", dest="kmer_db", help="Path to the kmer database")
    run_parser.add_argument("-i1", dest="input_1", help="Input read file 1 (FASTQ format)")
    run_parser.add_argument("-i2", dest="input_2", help="Input read file 2 (FASTQ format)")
    run_parser.add_argument("-o1", dest="output_1", help="output read file 2 (FASTQ format)")
    run_parser.add_argument("-o2", dest="output_2", help="output read file 2 (FASTQ format)")
    run_parser.add_argument("--taxid", dest="taxid", help="Taxonomy ID of reads to extract (Only for kmer, model b, c, d)")
    run_parser.add_argument("-t", dest="threads", type=int, default=1, help="Number of threads to use (default: 1)")
    # Subparser for the "build-db" command
    build_db_parser = subparsers.add_parser('build-db', help='Build database for kmer or alignment')
    build_db_parser.add_argument("--db-type", choices=['kmer', 'alignment'], help="Type of database to build: kmer or alignment")
    build_db_parser.add_argument("-t", dest="threads", type=int, default=1, help="Number of threads to use (default: 1)")
    build_db_parser.add_argument('--bypass-tax', action='store_true', help='Bypass the download_taxonomy step(required for kmer database)')
    build_db_parser.add_argument("--db-name", dest="db_name", help="DB name of yoursulf(required for kmer database)")
    build_db_parser.add_argument("--add-to-library", dest="reference_genome", help="Please update your FASTA file headers to include the prefix in the following format: >GenomeID|kraken:taxid|39947. For more details, please refer to our GitHub help document.(required for kmer database)")
    build_db_parser.add_argument("--input-fasta", dest="reference_genome", help="Input reference genome FASTA file(required for alignment database)")
    build_db_parser.add_argument("-o", dest="output_prefix", help="Prefix for the output index files(required for alignment database)")
    # Subparser for the "qc" command
    qc_parser = subparsers.add_parser('qc', help='Run qc on input files')
    qc_parser.add_argument("-i1", dest="input_1", help="Input read file 1 (FASTQ format)")
    qc_parser.add_argument("-i2", dest="input_2", help="Input read file 2 (FASTQ format)")
    qc_parser.add_argument("-o1", dest="output_1", help="Output read file 1 (FASTQ format)")
    qc_parser.add_argument("-o2", dest="output_2", help="Output read file 2 (FASTQ format)")
    qc_parser.add_argument("-t", dest="threads", type=int, default=1, help="Number of threads to use (default: 1)")

    combined_help_message = '''
    usage: hostpurge [-h] {run,build-db,qc} ...

    HostPurge: A tool for running metagenome simulations, building databases, and performing quality control.
    Typically, the host decontamination process involves three steps: qc, build-db, and run. If you have already built your database or do not require quality control for your data, you can directly proceed with the run step.

    optional arguments:
      -h, --help         show this help message and exit

    Commands:
      run                Run HostPurge with specified mode
      build-db           Build database for kmer or alignment
      qc                 Run qc to quality control

    Run a specific command for more help:
      hostpurge run -h
      hostpurge build-db -h
      hostpurge qc -h

--------------------------------------

    hostpurge run:
    usage: [-h] --mode {a,b,c,d}
           [-i1 INPUT_1.fq] [-i2 INPUT_2.fq] [-o1 OUTPUT_1.fq] [-o2 OUTPUT_2.fq] [-t THREADS]
           [--alignment_db ALIGNMENT_DB]  # Only for alignment database
           [--kmer_db KMER_DB] [--taxid TAXID]  # Only for kmer database
               
    optional arguments:
      -h, --help                   show this help message and exit
      --mode {a, b, c, d}          Mode of operation:
                                   a: alignment mode
                                   b: kmer mode
                                   c (default): kmer followed by alignment mode
                                   d: alignment followed by kmer mode
      --alignment_db ALIGNMENT_DB  Path to the alignment database
      --kmer_db KMER_DB            Path to the kmer database
      -i1 INPUT_1.fq               Input read file 1 (FASTQ format)
      -i2 INPUT_2.fq               Input read file 2 (FASTQ format)
      -o1 OUTPUT_1.fq              Output read file 1 (FASTQ format)
      -o2 OUTPUT_2.fq              Output read file 2 (FASTQ format)
      --taxid TAXID                Taxonomy ID of reads to extract (Only for kmer, mode b, c, d)
      -t THREADS                   Number of threads to use (default: 1)

--------------------------------------

    hostpurge build-db:
    usage: [-h] [--db-type {kmer, alignment}] [-t THREADS]
           [--db-name DB_NAME] [--add-to-library REFERENCE_GENOME.fasta] # Only for kmer database
           [--bypass-tax]  # Only for kmer database
           [--input-fasta REFERENCE_GENOME.fasta] [-o OUTPUT_PREFIX]  # Only for alignment database

    optional arguments:
      -h, --help                    show this help message and exit
      --db-type {kmer, alignment}   Type of database to build: kmer or alignment
      --bypass-tax                  Bypass the download_taxonomy step. The necessary taxonomy files can                                      be found on our GitHub and downloaded by users.(required for kmer                                        database)
      -t THREADS                    Number of threads to use (default: 1)
      --db-name DB_NAME             DB name of yourself(required for kmer database)
      --add-to-library REFERENCE_GENOME.fasta
                                    Please update your FASTA file headers to include the prefix in the                                       following format: >GenomeID|kraken:taxid|39947. For more details,                                        please refer to our GitHub help document.(required for kmer database)
      --input-fasta REFERENCE_GENOME.fasta
                                    Input reference genome FASTA file (required for alignment database)
      -o OUTPUT_PREFIX              Prefix for the output index files (required for alignment database)

--------------------------------------

    hostpurge qc:
    usage: [-h] [-i1 INPUT_1] [-i2 INPUT_2] [-o1 OUTPUT_1] [-o2 OUTPUT_2]
           [-t THREADS]

    optional arguments:
      -h, --help            show this help message and exit
      -i1 INPUT_1           Input read file 1 (FASTQ format)
      -i2 INPUT_2           Input read file 2 (FASTQ format)
      -o1 OUTPUT_1          Output read file 1 (FASTQ format)
      -o2 OUTPUT_2          Output read file 2 (FASTQ format)
      -t THREADS            Number of threads to use (default: 1)

    '''
    if len(sys.argv) == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print(combined_help_message)
        sys.exit(0)
    args = hostpurge_parser.parse_args()

    if args.command == 'run':
        if args.mode == 'a':
            output_sam = "output.sam"
            bowtie2(args.alignment_db, args.input_1, args.input_2, output_sam, args.threads)
            parse_sam(output_sam, args.output_1, args.output_2)
            os.remove("output.sam")
        elif args.mode == 'b':
            kraken2(args.kmer_db, args.input_1, args.input_2, args.threads)
            extract(args.input_1, args.input_2, args.output_1, args.output_2, args.taxid)
            os.remove("result.report")
            os.remove("result.output")
        elif args.mode == 'c':
            kraken2(args.kmer_db, args.input_1, args.input_2, args.threads)
            output_1 = "temp1.fq"
            output_2 = "temp2.fq"
            extract(args.input_1, args.input_2, output_1, output_2, args.taxid)
            filtered_input_1 = output_1
            filtered_input_2 = output_2
            output_sam = "output.sam"
            bowtie2(args.alignment_db, filtered_input_1, filtered_input_2, output_sam, args.threads)
            parse_sam(output_sam, args.output_1, args.output_2)
            os.remove("temp1.fq")
            os.remove("temp2.fq")
            os.remove("output.sam")
        elif args.mode == 'd':
            output_sam = "output.sam"
            bowtie2(args.alignment_db, args.input_1, args.input_2, output_sam, args.threads)
            filter_1 = "temp1.fq"
            filter_2 = "temp2.fq"
            parse_sam(output_sam, filter_1, filter_2)
            filtered_input_1 = filter_1
            filtered_input_2 = filter_2
            kraken2(args.kmer_db, filtered_input_1, filtered_input_2, args.threads)
            extract(filtered_input_1, filtered_input_2, args.output_1, args.output_2, args.taxid)
            os.remove("temp1.fq")
            os.remove("temp2.fq")
            os.remove("output.sam")

    elif args.command == 'build-db':
        if args.db_type == 'kmer':
            if not args.bypass_tax:
                download_taxonomy(args.db_name, args.threads)
            # Additional command to add FASTA file to the Kraken2 library if provided
            add_to_library(args.db_name, args.reference_genome, args.threads)
            build_kraken2_db(args.db_name, args.threads)
        elif args.db_type == 'alignment':
            build_bowtie2_db(args.reference_genome, args.output_prefix)

    elif args.command == 'qc':
        qc(args.input_1, args.input_2, args.output_1, args.output_2, args.threads)


if __name__ == "__main__":
    main()
