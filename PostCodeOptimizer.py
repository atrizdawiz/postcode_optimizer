import os

class PostCodeOptimizer:
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    input_file = ""
    output_file = ""

    def __init__(self, input_filename):
        output_filename = input_filename.replace('.txt', '_optimized.txt')
        self.input_file = os.path.join(self.scriptdir, input_filename)
        self.output_file = os.path.join(self.scriptdir, output_filename)

    candidate_range_start = 0

    def postal_dictionary_creator(self):
        file = open(self.input_file, 'r')
        lineList = file.read().rstrip().split(',')
        lineList = [int(i) for i in lineList]
        return dict(enumerate(lineList))


    def postal_range_finder(self, postalDictionary):
        print("Processing input...")
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
        output_string = ",".join([str(x) for x in processed_list])
        print("Printed these objects to file: " + output_string)
        return output_string
