import errno
import os
import re

class PostCodeOptimizer:
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = ""
    output_file_path = ""
    input_read = ""
    written_output = ""
    is_input_valid = ""
    input_file_size = ""
    output_file_size = ""

    def __init__(self, input_filename):
        output_filename = input_filename.replace('.txt', '_optimized.txt')
        self.input_file_path = os.path.join(self.scriptdir, input_filename)
        self.input_file_size = self.input_file_path.__sizeof__()
        self.output_file_path = os.path.join(self.scriptdir, output_filename)
        self.validate_input(self.input_file_path)
        # When a postCodeOptimizer object is instantiated it will get the postal_code dictionary belonging to that input path
        # It also sets the input_read
        postcode_dictionary = self.postal_dictionary_creator()
        self.input_file_size = self.input_read.__sizeof__()
        self.postal_range_finder(postcode_dictionary) # We also get the output list, which sets the written_output variable


    def read_file_to_list(self, file_path):
        file = open(file_path, 'r')
        lineList = file.read()
        self.input_read = lineList
        file.close()
        return lineList

    def cleanup_input_list(self, en_lista):
        lineListNoWhiteSpace = re.sub(r'\s+', '', en_lista).split(',')
        lineListNoWhiteSpace = list(set(lineListNoWhiteSpace))  # removes any duplicate postcodes
        lineListNoWhiteSpace.sort()
        return lineListNoWhiteSpace

    def postal_dictionary_creator(self):
        if(self.is_input_valid):
            lineList = self.read_file_to_list(self.input_file_path)
            lineListNoWhiteSpace = self.cleanup_input_list(lineList)
            lineListNoWhiteSpace = [int(i) for i in lineListNoWhiteSpace]
            return dict(enumerate(lineListNoWhiteSpace))
        else:
            return dict(enumerate([]))

    def validate_input(self, file):
        not_allowed = re.compile(r'[^\d| | ,]')
        try:
            with open(file) as f:
                for line in f:
                    if re.search(not_allowed, line):
                        self.is_input_valid = False
                        return False
                    else:
                        self.is_input_valid = True
                        return True
        except IOError as x:
            if x.errno == errno.ENOENT:
                print(file, '- does not exist')
                return False
            elif x.errno == errno.EACCES:
                print(file, '- cannot be read')
                return False
            else:
                print(file, '- some other error')
                return False


    def postal_range_finder(self, postalDictionary):
        processed_list = []
        temp_list = []
        for key, value in postalDictionary.items():
            # We have yet another successor
            if key < len(postalDictionary)-1:
                postcode_comparison = postalDictionary[key + 1] - postalDictionary[key]
                if postcode_comparison == 1:
                    temp_list.append(postalDictionary[key])
                    temp_list.append(postalDictionary[key+1])
                else:
                    if len(temp_list) == 0:
                        processed_list.append(str(value))
                    elif len(temp_list)>1:
                        processed_list.append(str(min(temp_list)) + '-' + str(max(temp_list)))
                        temp_list.clear()
                    elif len(temp_list)==1:
                        processed_list.append(temp_list[0])
            else:
                #last postcode
                if len(temp_list)>0:
                    if value-max(temp_list) == 0:
                        processed_list.append(str(min(temp_list)) + '-' + str(value))
                    else:
                        processed_list.append(str(value))
                else:
                    processed_list.append(str(value))
        processed_list.sort()
        output_string = ",".join([str(x) for x in processed_list])
        self.written_output = output_string
        self.output_file_size = self.__sizeof__()
        return output_string
