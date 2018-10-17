# -*- coding: utf-8 -*-

import sys
import codecs
import glob

att_matrices_folder = "att_matrices/"
files_folder = "../files/"
folders_prefix = "exp"
train_max = 297 
id_suffix = ".id"
different_split = False

def read_matrix(path):
	return [line.strip("\n").split("\t") for line in codecs.open(path,"r","UTF-8")]

def merge_matrices(matrices_list):
	num_lines = len(matrices_list[0])
	num_columns = len(matrices_list[0][0]) #+ 1
	num_matrices = len(matrices_list)
	output = [[0 for i in xrange(num_columns)] for j in xrange(num_lines)]
	output[0] = matrices_list[0][0]
	for line in range(1, num_lines):
		output[line][0] = matrices_list[0][line][0]
		for column in range(1, num_columns):
			for i in range(0, num_matrices):
				if len(matrices_list[i][line]) > 1:
					#print line, column, num_columns, i
					#print matrices_list[i][line]
					output[line][column] += float(matrices_list[i][line][column])
			output[line][column] = str(output[line][column] / num_matrices)
	return output

def write_output(path, matrix):
    output_path = path.replace(".lab", ".avgatt") + ".txt"
    #print output_path
    with codecs.open(output_path, "w", "UTF-8") as outputFile:
        for line in matrix:
            #print line, "\t".join(line)
            try:
                outputFile.write("\t".join(line) + "\n")
            except TypeError:
                pass

def load_files(path_folders, folders):
	files_dict = dict(zip([],[]))
	for folder in folders:
		count = 1
		files_dict[folder] = []
		file_name = "train." + folder[:-1] + id_suffix if different_split else "train" + id_suffix 
		with open(path_folders + files_folder + file_name, "r") as inputFile: #read train
			intern_dict = dict(zip([],[]))
			for line in inputFile:
				intern_dict[line.strip()] = "train."+ str(count)
				count +=1
			file_name = file_name.replace("train","dev")
			with open(path_folders + files_folder + file_name, "r") as inputFile: #read dev
				count = 1
				for line in inputFile:
					intern_dict[line.strip()] = "dev."+ str(count)
					count +=1
			files_dict[folder] = intern_dict
	return files_dict

def get_file_from_index(files_dict, folder, f_id):
	for key in files_dict[folder].keys():
		if files_dict[folder][key] == f_id:
			return key
	print "PROBLEM GETTING KEY FROM DICTIONARY:\nid: " + str(f_id) + " folder: " + folder + "\n"
	sys.exit(1)

def get_index_from_file(files_dict, folder, f_name):
	for key in files_dict[folder].keys():
		if key == f_name:
			return files_dict[folder][key]
	print "PROBLEM GETTING ID FROM DICTIONARY:\nfile: " + f_name + " folder: " + folder + "\n"
	sys.exit(1)

def find_matrices(path_folders, folders, files_dict, file_name):
	matrices = []
	for folder in folders:
		f_id = get_index_from_file(files_dict, folder, file_name)
		#print f_id
		matrix_file = glob.glob(path_folders + folder + att_matrices_folder + f_id +".txt")
		matrix = read_matrix(matrix_file[0])
		matrices.append(matrix)
	if len(matrices) != len(folders):
		print "COULD NOT READ ALL THE MATRICES FOR FILE: " + file_name + "\n"
		sys.exit(1)
	else:
		size = len(matrices[0])
		for i in range(1, len(folders)):
			#print matrices[0][0]
			#print matrices[i][0]
			if len(matrices[i]) != size:
				print "PROBLEM WITH MATRIX SIZE: " + file_name + " folder: " + str(i+1) + "\n"
				sys.exit(1)

	return matrices

def main():
	path_folders = sys.argv[1]
	#list_type = sys.argv[2]#files_list = [line.strip("\n") for line in open(sys.argv[2],"r")]
	output_folder = sys.argv[2]
	rand_num = int(sys.argv[3])
	folders = []
	for i in range(1,rand_num+1):
		folders.append(folders_prefix +str(i)+"/")
	#print folders
	files_dict = load_files(path_folders, folders)
	#print len(files_dict), len(files_dict[folders[0]])
	size = len(files_dict[folders[0]])
	for i in range(1, rand_num):
		if len(files_dict[folders[i]]) != size:
			print "PROBLEM READING THE LISTS (INDEX = " + str(i) + ")\n"
			sys.exit(1)
	for i in range(1, size+1):
		if i > train_max:
			file_i = get_file_from_index(files_dict, folders[0], "dev." + str(i - train_max))
		else:
			file_i = get_file_from_index(files_dict, folders[0], "train." + str(i))
		#print file_i, i
		matrices = find_matrices(path_folders, folders, files_dict, file_i)
		avg_matrix = merge_matrices(matrices)
		write_output(output_folder + file_i, avg_matrix)


if __name__ == '__main__':
	main()