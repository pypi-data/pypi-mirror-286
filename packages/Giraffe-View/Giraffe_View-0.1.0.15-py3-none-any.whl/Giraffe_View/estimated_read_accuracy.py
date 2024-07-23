from os import system 
import numpy as np
import math
import multiprocessing
import gzip

def GC_content(string):
    read = str(string).upper()
    length = len(read)
    c = read.count("C")
    g = read.count("G")
    GC = (c+g)/length
    return[length, GC]

def Qvalue_to_accuracy(string):
    error_list = []
    for base_value in string:
        ascii_value = ord(base_value) - 33
        error_proporation = math.pow(10, (-1) * int(ascii_value) / 10)
        error_list.append(error_proporation)
    error_mean = np.mean(error_list)
    return [1 - error_mean, error_mean, (-10) * math.log10(error_mean)]

def process_chunk(chunk):
    results = []
    for line in chunk:
        read_id, sequence, quality = line
        GC = GC_content(sequence)
        quality = Qvalue_to_accuracy(quality)
        results.append([read_id, quality[0], quality[1], quality[2], GC[0], GC[1]])
    return results

def calculate_estimated_accuracy(input_type, input_file, num_processes, chunk_size=1000):
    pool = multiprocessing.Pool(processes=num_processes)
    results = []
    whether_compressed = ""


    # judge whether input file is compressed (.gz) or not
    if input_file.endswith('.gz'):
    	open_func = gzip.open
    	whether_compressed = "yes"

    else:
    	open_func = open
    	whether_compressed = "no"

    with open_func(input_file, "r") as input_file:
        count = 1
        chunk = []
        for line in input_file:
        	line = line.strip()

        	if whether_compressed == "yes":
        		line = line.decode('ascii')

        	if count % 4 == 1:
        		read_id = line.split(" ")[0]
        	elif count % 4 == 2:
        		sequence = line
        	elif count % 4 == 0:
        		chunk.append((read_id, sequence, line))

        	count += 1

        	if len(chunk) == chunk_size:
        		results.append(pool.apply_async(process_chunk, (chunk,)))
        		chunk = []
        
        if len(chunk) > 0:
            results.append(pool.apply_async(process_chunk, (chunk,)))
    pool.close()
    pool.join()
    input_file.close()

    file = "Giraffe_Results/1_Estimated_quality/" + str(input_type) + ".tmp"
    with open(file, "w") as output_file:
            for result in results:
                for line in result.get():
                    message = f"{line[0]}\t{line[1]:.4f}\t{line[2]:.4f}\t{line[3]:.4f}"
                    message += f"\t{line[4]}\t{line[5]:.4f}\t{input_type}"
                    output_file.write(message + "\n")
    output_file.close()
    output_file.close()

def calculate_estimated_accuracy_slow(input_type, input_file, num_processes, chunk_size=1000):
    pool = multiprocessing.Pool(processes=num_processes)
    results = []
    whether_compressed = ""
    output_file = "Giraffe_Results/1_Estimated_quality/" + str(input_type) + ".tmp"

    # Determine whether the input file is compressed (.gz) or not
    if input_file.endswith('.gz'):
        open_func = gzip.open
        whether_compressed = "yes"
    else:
        open_func = open
        whether_compressed = "no"

    with open_func(input_file, "r") as input_file_handle, open(output_file, "w") as output_file_handle:
        count = 1
        chunk = []
        for line in input_file_handle:
            line = line.strip()

            if whether_compressed == "yes":
                line = line.decode('ascii')

            if count % 4 == 1:
                read_id = line.split(" ")[0]
            elif count % 4 == 2:
                sequence = line
            elif count % 4 == 0:
                chunk.append((read_id, sequence, line))

            count += 1

            if len(chunk) == chunk_size:
                result = pool.apply_async(process_chunk, (chunk,))
                for line in result.get():
                    message = f"{line[0]}\t{line[1]:.4f}\t{line[2]:.4f}\t{line[3]:.4f}"
                    message += f"\t{line[4]}\t{line[5]:.4f}\t{input_type}"
                    output_file_handle.write(message + "\n")
                chunk = []

        if len(chunk) > 0:
            result = pool.apply_async(process_chunk, (chunk,))
            for line in result.get():
                message = f"{line[0]}\t{line[1]:.4f}\t{line[2]:.4f}\t{line[3]:.4f}"
                message += f"\t{line[4]}\t{line[5]:.4f}\t{input_type}"
                output_file_handle.write(message + "\n")

    pool.close()
    pool.join()

def merge_results():
    with open("Giraffe_Results/1_Estimated_quality/header", "a") as ff:
        ff.write("ReadID\tAccuracy\tError\tQ_value\tLength\tGC_content\tGroup\n")
    ff.close()
    system("cat Giraffe_Results/1_Estimated_quality/header \
        Giraffe_Results/1_Estimated_quality/*tmp > \
        Giraffe_Results/1_Estimated_quality/Estimated_information.txt")
    system("rm Giraffe_Results/1_Estimated_quality/*tmp Giraffe_Results/1_Estimated_quality/header")
