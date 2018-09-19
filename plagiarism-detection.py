import argparse
import re
import json

from ntuple import GeneralWordListGenerator, NTupleAlgorithm

def main(synonymsFile, file1, file2, n):
    """ The main method for the Plagiarism Detection program. The instructions were vague about \
    what to do when there were multiple lines in the input files, I've assumed here that the confidence \
    value should reflect the entire file. If there are multiple lines, they'll be treated the same as one \
    line. """
    # Read in the contents of the synonyms file into a list of tuples, where each
    # tuple contains words that are synonyms of each other.
    synonyms = GeneralWordListGenerator.read_file_to_tuple_list(args.synonymsFile)
    # Construct our word list generator, which will take strings representing text
    # and return a generalized form of the text, where each word with a synonym from
    # the synonyms file is represented as a tuple of its synonyms. See the `generate_word_list`
    # method in the `GeneralWordListGenerator` for more details.
    word_list_generator = GeneralWordListGenerator(synonyms)
    # Read in all the lines from the two input files. Here, we ignore lines. Each file will be read
    # as one long string.
    file1_string = file1.read()
    file2_string = file2.read()
    # Generate generalized lists of words for the lines in the two files.
    file1_general_word_list = word_list_generator.generate_word_list(file1_string)
    file2_general_word_list = word_list_generator.generate_word_list(file2_string)
    
    # Initialize our N-tuple comparison algorithm, passing it the size N for the tuples.
    n_tuple_alg = NTupleAlgorithm(n)
    # If the lists of words are the same length, run the N-tuple comparison algorithm and 
    # return the confidence value
    if len(file1_general_word_list) == len(file2_general_word_list):
        return n_tuple_alg.compare(file1_general_word_list, file2_general_word_list)
    else:
        return -1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detect plagiarism in two input files \
                    using an N-tuple comparison algorithm fed by a list of synonyms.')
    parser.add_argument('synonymsFile', metavar='SYNONYMS', type=argparse.FileType('r'),
                    help='A path to a file containing a list of synonyms')
    parser.add_argument('file1', metavar='FILE_1', type=argparse.FileType('r'),
                    help='A path to the first input file')
    parser.add_argument('file2', metavar='FILE_2', type=argparse.FileType('r'),
                    help='A path to the second input file')
    parser.add_argument('-n', metavar='N', type=int, default=3,
                        help='The tuple size for the N-tuple comparison algorithm')
    args=parser.parse_args()
    print("{0}%".format(main(args.synonymsFile, args.file1, args.file2, args.n) * 100))
