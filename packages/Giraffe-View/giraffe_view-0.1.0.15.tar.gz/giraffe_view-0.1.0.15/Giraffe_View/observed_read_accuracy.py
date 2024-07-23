import pysam
import re
from os import system 
from Giraffe_View.function import *
import multiprocessing

def data_process(sample_ID, data_type, data_path, ref, threads=10):
    # Define the commands as a list of strings to avoid issues with spaces
    # in file names or command arguments
    # path =  os.getcwd()

    output = "Giraffe_Results/2_Observed_quality/" + str(sample_ID) + ".bam"
    
    if data_type == "ONT":
        cmd1 = ["minimap2", "-ax", "map-ont", "-o", "Giraffe_Results/2_Observed_quality/tmp.sam", "--MD", \
        "--secondary=no", "-L", "-t", str(threads), ref, data_path]

    elif data_type == "ONT_RNA":
        cmd1 = ["minimap2", "-ax", "splice", "-uf", "-k14", "-o", "Giraffe_Results/2_Observed_quality/tmp.sam", "--MD", \
        "--secondary=no", "-L", "-t", str(threads), ref, data_path]

    elif data_type == "Pacbio":
        cmd1 = ["minimap2", "-ax", "map-pb", "-o", "Giraffe_Results/2_Observed_quality/tmp.sam", "--MD", \
        "--secondary=no", "-L", "-t", str(threads), ref, data_path]

    else:
        error_with_color("Please check your data type!!! [ONT, Pacbio, ONT_RNA]")

    cmd2 = ["samtools", "view", "-bS", "-F4", "-@", str(threads), "-o", "Giraffe_Results/2_Observed_quality/tmp.bam", "Giraffe_Results/2_Observed_quality/tmp.sam"]
    cmd3 = ["samtools", "sort", "-@", str(threads), "-o", output, "Giraffe_Results/2_Observed_quality/tmp.bam"]
    cmd4 = ["samtools", "index", "-@", str(threads), output]
    cmd5 = ["rm", "-rf", "Giraffe_Results/2_Observed_quality/tmp.bam", "Giraffe_Results/2_Observed_quality/tmp.sam"]

    # Run each command and check the return code
    for i, cmd in enumerate([cmd1, cmd2, cmd3, cmd4, cmd5]):
        try:
            subprocess.run(cmd, check=True)
            # print("Command {} succeeded".format(i + 1))
        except subprocess.CalledProcessError as e:
            print("Command {} failed with error code {}".format(i + 1, e.returncode))
            print(e.output)
            # Raise an exception to indicate that processing failed
            raise Exception("Data processing failed")

def identify_match(cigar):
    """
    Identifies the number of matching bases in a read from its CIGAR string.
    """
    cigar_mat = re.findall(r"\d+M", cigar)
    base_num_mat = sum(int(i[:-1]) for i in cigar_mat)
    return base_num_mat

def identify_insertion(cigar):
    """
    Identifies the number of inserted bases in a read from its CIGAR string.
    """
    cigar_ins = re.findall(r"\d+I", cigar)
    base_num_ins = sum(int(i[:-1]) for i in cigar_ins)
    return base_num_ins

def identify_deletion(cigar):
    """
    Identifies the number of deleted bases in a read from its CIGAR string.
    """
    cigar_del = re.findall(r"\d+D", cigar)
    base_num_del = sum(int(i[:-1]) for i in cigar_del)
    return base_num_del

def identify_substitution(md):
    """
    Identifies the number of substitutions in a read from its MD tag.
    """
    return len(re.findall(r"\d+[ATCG]", md))

def merge_results_observed_acc():
    with open("Giraffe_Results/2_Observed_quality/header", "a") as ff:
        ff.write("ID\tIns\tDel\tSub\tMat\tIden\tAcc\tGroup\n")
    ff.close()

    system("cat Giraffe_Results/2_Observed_quality/header \
        Giraffe_Results/2_Observed_quality/*_primary_* \
        Giraffe_Results/2_Observed_quality/*_supplementary.total.txt > \
        Giraffe_Results/2_Observed_quality/Observed_information.txt")
    
    system("rm Giraffe_Results/2_Observed_quality/*_primary_* \
        Giraffe_Results/2_Observed_quality/header \
        Giraffe_Results/2_Observed_quality/*_supplementary.total.txt")

def observed_accuracy_worker(bam_file, sample_ID, chromosome):
    output_1 = f"Giraffe_Results/2_Observed_quality/{sample_ID}_primary_{chromosome}.txt"
    output_2 = f"Giraffe_Results/2_Observed_quality/{sample_ID}_supplementary_{chromosome}.txt"
    bamfile= pysam.AlignmentFile(bam_file, 'rb')

    with open(output_1, "w") as pri_f:
    	with open(output_2, "w") as sup_f:
    		for read in bamfile.fetch(chromosome):
    			# filter the unmapped reads
    			if read.flag == 4:
    				continue
    			else:
    				read_ID = read.query_name
    				read_cigar = read.cigarstring
    				read_md = read.get_tag("MD")

    				# count the number of matched and mismatched base
    				Ins = identify_insertion(read_cigar)
    				Del = identify_deletion(read_cigar)
    				Sub = identify_substitution(read_md)
    				Mat = identify_match(read_cigar) - Sub
    				
    				# check the presence of supplementary reads
    				if read.has_tag("SA"):
    					sup_f.write(f"{read_ID}\t{Ins}\t{Del}\t{Sub}\t{Mat}\t{sample_ID}\n")
    				else:
    					# calculate the observed accuracy and identification
    					total = Ins + Del + Sub + Mat
    					Acc = Mat / total if total > 0 else 0
    					Iden = Mat / (Mat + Sub) if (Mat + Sub) > 0 else 0
    					pri_f.write(f"{read_ID}\t{Ins}\t{Del}\t{Sub}\t{Mat}\t{Iden:.4f}\t{Acc:.4f}\t{sample_ID}\n")	
    pri_f.close()
    sup_f.close()
    bamfile.close()

def run_observed_accuracy(input_bamfile, sample_ID, num_processes=10):
    bamfile = pysam.AlignmentFile(input_bamfile, "rb")
    chromosomes = bamfile.references

    with multiprocessing.Pool(processes=num_processes) as pool:
        jobs = []
        for chromosome in chromosomes:
            jobs.append(pool.apply_async(observed_accuracy_worker, (input_bamfile, sample_ID, chromosome)))

        for job in jobs:
            job.get()

def supplementary_read_processing(sample_ID):
    total = {}

    with open("Giraffe_Results/2_Observed_quality/giraffe_supplementary.temp.txt", "r") as ff:
        for line in ff.readlines():
            line = line.rstrip("\n")
            data = line.split("\t")

            read_ID = str(data[0])
            Ins = int(data[1])
            Del = int(data[2])
            Sub = int(data[3])
            Mat = int(data[4])
            sample_ID = str(data[5])

            if read_ID not in total:
                total[read_ID] = {}
                total[read_ID]["Ins"] = Ins
                total[read_ID]["Del"] = Del
                total[read_ID]["Sub"] = Sub
                total[read_ID]["Mat"] = Mat
                total[read_ID]["sample"] = sample_ID
            else:
                total[read_ID]["Ins"] += Ins
                total[read_ID]["Del"] += Del
                total[read_ID]["Sub"] += Sub
                total[read_ID]["Mat"] += Mat
    ff.close()

    output = f"Giraffe_Results/2_Observed_quality/{sample_ID}_supplementary.total.txt"
    with open(output, "w") as ff:
        for read_key, read_data in total.items():
            read_ID = read_key
            Ins = read_data["Ins"]
            Del = read_data["Del"]
            Sub = read_data["Sub"]
            Mat = read_data["Mat"]
            sample_ID = read_data["sample"]

            All = Ins + Del + Sub + Mat
            Acc = Mat / All if All > 0 else 0
            Iden = Mat / (Mat + Sub) if (Mat + Sub) > 0 else 0
            ff.write(f"{read_ID}\t{Ins}\t{Del}\t{Sub}\t{Mat}\t{Iden:.4f}\t{Acc:.4f}\t{sample_ID}\n")
    ff.close()

# def observed_accuracy(bam_file, sample_ID):
#     """
#     Calculates the observed accuracy, insertion, deletion, substitution, match,
#     and identity rates for each read in a BAM file.
#     """
#     quality = {}
#     with open("Giraffe_Results/2_Observed_quality/"+sample_ID+".acc_tmp", "w") as outfile:  
#         bamfile= pysam.AlignmentFile(bam_file, 'rb')
#         for read in bamfile:
#             if read.flag != 4:
#                 read_ID = read.query_name
#                 read_cigar = read.cigarstring
#                 read_md = read.get_tag("MD")

#                 Ins = identify_insertion(read_cigar)
#                 Del = identify_deletion(read_cigar)
#                 Sub = identify_substitution(read_md)
#                 Mat = identify_match(read_cigar) - Sub

#                 if read_ID not in quality.keys():
#                     quality[str(read_ID)] = {}
#                     quality[str(read_ID)]["Ins"] = int(Ins)
#                     quality[str(read_ID)]["Del"] = int(Del)
#                     quality[str(read_ID)]["Sub"] = int(Sub)
#                     quality[str(read_ID)]["Mat"] = int(Mat)
#                 else:
#                     quality[str(read_ID)]["Ins"] += int(Ins)
#                     quality[str(read_ID)]["Del"] += int(Del)
#                     quality[str(read_ID)]["Sub"] += int(Sub)
#                     quality[str(read_ID)]["Mat"] += int(Mat)
#         bamfile.close()

#         for read_key in quality.keys():
#             read_ID = read_key
#             Ins = quality[str(read_key)]["Ins"]
#             Del = quality[str(read_key)]["Del"]
#             Sub = quality[str(read_key)]["Sub"]
#             Mat = quality[str(read_key)]["Mat"]

#             total = Ins + Del + Sub + Mat
#             Acc = Mat / total if total > 0 else 0
#             Iden = Mat / (Mat + Sub) if (Mat + Sub) > 0 else 0
#             outfile.write(f"{read_ID}\t{Ins}\t{Del}\t{Sub}\t{Mat}\t{Iden:.4f}\t{Acc:.4f}\t{sample_ID}\n")
#     outfile.close()


# def supplementary_read_processing(sample_ID):
#   output = f"Giraffe_Results/2_Observed_quality/{sample_ID}_supplementary_total.txt"
#   total = {}
#   with open("Giraffe_Results/2_Observed_quality/giraffe_supplementary_temp.txt", "r") as ff:
#       for l in ff.readlines():
#           l = l.replace("\n", "")
#           l = l.split("\t")

#           read_ID = str(l[0])
#           Ins = int(l[1])
#           Del = int(l[2])
#           Sub = int(l[3])
#           Mat = int(l[4])
#           sample_ID = str(l[5])

#           if read_ID not in total.keys():
#               total[str(read_ID)] = {}
#               total[str(read_ID)]["Ins"] = Ins
#               total[str(read_ID)]["Del"] = Del
#               total[str(read_ID)]["Sub"] = Sub
#               total[str(read_ID)]["Mat"] = Mat
#               total[str(read_ID)]["sample"] = sample_ID
#           else:
#               total[str(read_ID)]["Ins"] += Ins
#               total[str(read_ID)]["Del"] += Del
#               total[str(read_ID)]["Sub"] += Sub
#               total[str(read_ID)]["Mat"] += Mat
#   ff.close()

#     with open(output, "w") as ff:
#         for read_key in total.keys():
#             read_ID = read_key
#             Ins = total[str(read_key)]["Ins"]
#             Del = total[str(read_key)]["Del"]
#             Sub = total[str(read_key)]["Sub"]
#             Mat = total[str(read_key)]["Mat"]
#             sample_ID = total[str(read_key)]["sample"]

#             All = Ins + Del + Sub + Mat
#             Acc = Mat / All if All > 0 else 0
#             Iden = Mat / (Mat + Sub) if (Mat + Sub) > 0 else 0
#             ff.write(f"{read_ID}\t{Ins}\t{Del}\t{Sub}\t{Mat}\t{Iden:.4f}\t{Acc:.4f}\t{sample_ID}\n")
#   ff.close()