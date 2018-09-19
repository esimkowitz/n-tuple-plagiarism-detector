import re

def read_string_to_word_list(line):
    """Takes in a string of text and returns a list of the words in the text."""
    regex = r"[a-zA-Z]+"
    words_in_text = []
    # Finds all the words in the text
    matches = re.findall(regex, line)
    # Iterate through all the words in the line and add them to the list
    for word in matches:
        # We want the list of words to be case-sensitive
        words_in_text.append(word.lower())
    return words_in_text

class NTupleAlgorithm:
    """ A class representing an N-tuple comparison algorithm."""
    def __init__(self, n):
        """ NTupleAlgorithm constructor """
        self.n = n
    
    def compare(self, input1, input2):
        """ Takes in two lists of items. Returns a number between `0` and `1` \
        representing the confidence that the two lists are similar. Assumes that \
        the two lists contain the same number of items."""
        # Get the N-size tuples for the two input lists.
        input1_n_tuples = NTupleInput(input1, self.n)
        input2_n_tuples = NTupleInput(input2, self.n)
        num_matches = 0
        # Iterate through the N-size tuples for the first input. If the tuple matches one in 
        # the second input, take note by incrementing our counter of the number of matches.
        for tuple in input1_n_tuples:
            if input2_n_tuples.match(tuple):
                num_matches += 1
        # Return the percentage of matching tuples to total tuples in the first input list.
        return float(num_matches)/float(len(input1_n_tuples)) 

        
class NTupleInput:
    """A helper class for NTupleAlgorithm which breaks down lists of items \
    into tuples of size N."""
    def __init__(self, input_list, n):
        """NTupleInput constructor.
        
        Expects a list of inputs in `input_list` and a N size for the tuples in `n`."""
        # Create a HashMap to store the N-size tuples
        self.tuple_map = {}
        curr_window = []

        # Iterate through the list of items using a moving window of size N
        for item in input_list:
            # Add a new item to the window
            curr_window.append(item)
            # If the window is of size N, we can add it to our HashMap.
            if len(curr_window) == n:
                self.tuple_map[tuple(curr_window)] = 1
                # Popping off the first element ensures that the window doesn't get too large.
                curr_window.pop(0)

    def __iter__(self):
        """The Iterator operator for the NTupleInput class."""
        # We want to iterate over the list of tuples, which is stored in the metadata of the HashMap.
        # While this could be stored in a second list, using the pre-existing metadata from the HashMap
        # saves on memory usage.
        return iter(self.tuple_map.keys())
    
    def __len__(self):
        """The Length opereator for the NTupleInput class."""
        # Returns the number of objects in the HashMap.
        return len(self.tuple_map)

    def match(self, tuple):
        """Checks if the input tuple matches any in the object."""
        # To do this, we just check if the tuple exists in the HashMap
        return tuple in self.tuple_map

class GeneralWordListGenerator:
    """A helper class which generates generalized lists of words using a provided list of synonyms"""
    def __init__(self, synonyms_list):
        """GeneralWordListGenerator constructor
        
        Takes in a list where each item is a tuple containing words that are synonyms of each other."""
        self.synonyms_dict = self.generate_synonym_to_tuple_dict(synonyms_list)
    
    @staticmethod
    def read_file_to_tuple_list(file):
        """Reads in a file and outputs a list, where each item in the list is a \
        tuple of the words in a line in the file."""
        tuple_list = []
        # Read in the first line of the file
        curr_line = file.readline()
        while curr_line != "":
            # Break up the text of a line by word
            words_in_line = read_string_to_word_list(curr_line)
            # Append the tuple of words to the list of tuples
            tuple_list.append(tuple(words_in_line))
            # Read in the next line
            curr_line = file.readline()
        return tuple_list

    @staticmethod
    def generate_synonym_to_tuple_dict(synonym_list):
        """Takes in a list where each element is a tuple of words that are synonyms of \
        each other. Returns a dictionary matching each word to its corresponding tuple \
        of synonyms."""
        synonym_to_tuple_dict = {}
        # Iterate through the list of tuples
        for synonym_tuple in synonym_list:
            # Iterate through the tuple and add each word to the dictionary
            for word in synonym_tuple:
                # The word should be the key and the synonym tuple should be the value. We want
                # it such that if we indexed the dictionary for two different words which are
                # synonyms of each other, they will return the same value.
                synonym_to_tuple_dict[word] = synonym_tuple
        return synonym_to_tuple_dict

    def generate_word_list(self, string):
        """Takes in a string representing an input text. Returns a list representing a \
        generalized version of the text, where words with synonyms are represented \
        as the tuple of all the synonyms and words without synonyms are represented as \
        strings of just the word. """
        # Read in the string and get the list of the words in the string
        words_in_line = read_string_to_word_list(string)
        general_word_list = []
        # Iterate through the words in the list
        for word in words_in_line:
            # If the word has synonyms from the list of synonyms provided in the constructor method,
            # append the generalized tuple of the synonyms of the word. Otherwise, append the word
            # itself.
            if word in self.synonyms_dict:
                general_word_list.append(self.synonyms_dict[word])
            else:
                general_word_list.append(word)
        return general_word_list
