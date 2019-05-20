import os

class PostCodeOptimizer:
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    input_filename = ""
    output_filename = ""
    input_file = ""
    output_file = ""

    postal_dictionary = ""
    candidate_range_start = 0

    def postal_dictionary_creator(self, input_filename):
        self.input_filename = input_filename
        self.output_filename = input_filename.replace('.txt', '_optimized.txt')
        self.input_file = os.path.join(self.scriptdir, input_filename)
        self.output_file = os.path.join(self.scriptdir, self.output_filename)
        self.file = open(self.input_file, 'r')

        lineList = self.file.read().rstrip().split(',')
        lineList = [int(i) for i in lineList]
        return dict(enumerate(lineList))


    def postal_range_finder(self, postalDictionary):
        print("Processing dictionary: " + str(postalDictionary))
        print("Length of dictionary: " + str(len(postalDictionary)))
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
        print("Printed these objects to file: " + str(processed_list))
        output_string = ",".join([str(x) for x in processed_list])
        return output_string
