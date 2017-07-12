# word_discovery

In this repository I gather all the files I used during my masters project in the GETALP research group.

# post-processing folder

In this folder are all the files used for post-processing. 

1) duongPostProcessing.py and reverse_duongPostProcessing.py are the files for base and reverse model (respectively) that implement the smoothing technique described in Duong et al. (2016). 

2) soft2HardAlignment.py and reverse_soft2HardAlignment.py are the files for base and reverse model (respectively) that implement the maximum a posteriori approach for hard segmentation. It provides support for the semi-supervised version, by adding a parameters for the dictionary file.

3) reverse_intermediateSegmentation.py only works for unsupervised version of the pipeline. It uses a threshold of trust for the alignments, and only concatenate characters which are over this threshold, creating an intermediate segmentation. This threshold belongs to the closed interval [0,1].

4) reverse_hardSegmentationThreshold.py only works for unsupervised version of the pipeline. It uses a threshold as the script above, but it uses this alignment trust to decide points of possible boundaries, concatenating everything that falls below this threshold. Because of that, by using high threshold values, this technique severely under-segment the input.

# modifications_seq2seq folder

In this folder I include the files I changed in the seq2seq model implemented by Alexandre Bérard and available in https://github.com/eske/seq2seq. I also include a modifications_log.md file, in which I describe the exact changes made.

# visualization folder

The scripts in this folder are used to generate the loss and BLEU score curves, using the output log file generated by the seq2seq model. Execution order:

1) rnnLogFileParser.py receives the training log from the network, and create a .out file.

2) createGraphics.r uses this .out file to generate the graphics.

# HOW TO RUN THE COMPLETE NEURAL WORD DISCOVERY PIPELINE

* **What you need to download:**

1) The LIG encoder-decoder NMT system available at https://github.com/eske/seq2seq.

2) The Mboshi-French corpus already pre-processed, available at https://bitbucket.org/mzboito/mboshi-french-parallel-corpus.

3) This repository.

* **How to setup:**

1) Replace the scripts in seq2seq/translate by the ones available in the folder word_discovery/seq2seq_modifications.

2) Create an experiment folder with the files you wish to use. For unsupervised grapheme setup, use the files corpus.token.train.mb (Mboshi) and corpus.norm.train.fr (French), available at mboshi-french-parallel-corpus/full_corpus/. Also remember of replacing the "train" part by "dev" and also copying the development files. There are no test files available.

3) In your experiment folder, create a .yaml setup file, in which you will put the settings for your neural network. There are two available examples in this repository. The example1.yaml file has layers in both encoder and decoder networks, and example2.yaml has layers only in the encoder network. Remember to replace the path information,  creating a folder to store the model files, that will be created during training.

4) Generate your files vocabulary. 

Command example: python seq2seq/scripts/prepareData.py my_experiment/files/train (my training file without the .fr ending) fr (shared ending for train and dev files) my_experiment/file/ (where the vocabulary file will be stored) --no-tokenize --dev-prefix my_experiment/files/dev (my development file without the .fr ending)

* **How to execute the NMT model:**

1) For training: python3 translate -m my_experiment/setup_file.yaml --train -v (from inside of the seq2seq folder)

2) For generating the alignment files (one for sentence) python3 seq2seq translate -m my_experiment/setup_file.yaml --align my_experiment/files/SOURCE_FILE (same from .yaml file) my_experiment/files/TARGET_FILE --output my_experiments/alignments_folder/

* **How to post-process:**

If you used reverse architecture (words as source), you will use the word_discovery/post-processing/reverse_ files. 

1) Smoothing (optional): duongPostProcessing.py and reverse_duongPostProcessing.py receive a folder (full of alignment files) and another folder to store the new version of these files.

2) Hard Segmentation: soft2HardAlignment.py and reverse_soft2HardAlignment.py receive the the path for the folder with the matrices, the dictionary file (for mboshi, this file is mboshi-french-parallel-corpus/full_corpus/corpus.token.dic100.train.mb.control), a number (0 for semi-supervised, 1 for unsupervised) and the output file name. If you input one, the script will ignore the dictionary file.

* **How to evaluate:**

The file evaluate_segmentation.py receives the gold standard, the generated segmentation, the dictionary file and the output file name. It generates recall, precision and f-score for types and tokens, and also counts the number of words in the most frequent files list (dictionary) that the model was able to discover, the discovered words outside this list, the vocabulary size and number of correct discovered units.

