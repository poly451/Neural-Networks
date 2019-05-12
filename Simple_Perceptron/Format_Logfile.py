import sys
"""
This is where I doodle. Everything gets tranfered over to the main program,
SimplePerceptron.py
"""
input_file = "logfile.txt"
# output_file = "formatted_logfile.txt"
print_debug = False
# mylist = []

# formated_data = []

def print_list(mylist, listname):
    print("{}:".format(listname))
    for item in mylist:
        print("{}".format(item))

def format_file(logfile, logfile_formatted):
    list_of_floats = []
    list_segments = []
    with open(logfile, "r") as f:
        mylist = f.readlines()
    mylist = [i.strip() for i in mylist]

    # break the data up into sections
    for line in mylist:
        line = line.split()
        # print(line)
        # print(len(line))
        if len(line) < 2:
            list_segments.append(list_of_floats)
            list_of_floats = []
            # print("accessed")
        else:
            list_of_floats.append(line)

    # break the data up into four lists, x1, y1, x2, y2
    print(len(list_segments))
    output_array = []
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    temp_x1 = []
    temp_y1 = []
    temp_x2 = []
    temp_y2 = []

    for line in list_segments:
        print("\n{}\n".format(line))
        temp_x1 = []
        temp_y1 = []
        temp_x2 = []
        temp_y2 = []
        for item in line:
            if int(item[2]) == 0:
                temp_x1.append(item[0])
                temp_y1.append(item[1])
            elif int(item[2]) != 0:
                temp_x2.append(item[0])
                temp_y2.append(item[1])
            print(item)
        x1.append(temp_x1)
        y1.append(temp_y1)
        x2.append(temp_x2)
        y2.append(temp_y2)

    print_list(x1, "x1")
    print_list(y1, "y1")
    print_list(x2, "x2")
    print_list(y2, "y2")

    x1string = ""
    for list1 in x1:
        for list2 in list1:
            x1string = "{} {}".format(x1string, list2)
        x1string += "\n"
    # -----------------------------------------------------
    y1string = ""
    for list1 in y1:
        for list2 in list1:
            y1string = "{} {}".format(y1string, list2)
        y1string += "\n"
    # -----------------------------------------------------
    x2string = ""
    for list1 in x2:
        for list2 in list1:
            x2string = "{} {}".format(x2string, list2)
        x2string += "\n"
    # -----------------------------------------------------
    y2string = ""
    for list1 in y2:
        for list2 in list1:
            y2string = "{} {}".format(y2string, list2)
        y2string += "\n"
    # -----------------------------------------------------

    with open(logfile_formatted, "w") as f:
        f.write(x1string)
        f.write("=\n")
        f.write(y1string)
        f.write("=\n")
        f.write(x2string)
        f.write("=\n")
        f.write(y2string)

def read_data_from_file(filepath):
    print_debug = False
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    with open(filepath, "r") as f:
        filelines = f.readlines()
    filelines = [i.strip() for i in filelines]
    number_of_filelines = len(filelines)
    if print_debug: print("number of filelines: {} - 3: {}".format(len(filelines), len(filelines) - 3))
    number_of_filelines = number_of_filelines - 3
    iterations_per_segment = int(number_of_filelines / 4)
    x = []
    y = []
    mybegin = 0
    myend = iterations_per_segment
    for i in range(mybegin, myend):
        if print_debug: print("{} in range({} to {})".format(i, mybegin, myend))
        x1.append(filelines[i])
    if print_debug: print("---------------------------------------------------")
    # need to remove the divider
    mybegin = iterations_per_segment+1
    myend = (iterations_per_segment*2)+1
    for i in range(mybegin, myend):
        if print_debug: print("{} in range({} to {})".format(i, mybegin, myend))
        y1.append(filelines[i])
    if print_debug: print("---------------------------------------------------")
    # again, need to remove the divider
    mybegin = (iterations_per_segment * 2) + 2
    myend = (iterations_per_segment * 3) + 2
    for i in range(mybegin, myend):
        if print_debug: print("{} in range({} to {})".format(i, mybegin, myend))
        x2.append(filelines[i])
    if print_debug: print("---------------------------------------------------")
    mybegin = (iterations_per_segment * 3) + 3
    myend = (iterations_per_segment * 4) + 3
    for i in range(mybegin, myend):
        if print_debug: print("{} in range({} to {})".format(i, mybegin, myend))
        y2.append(filelines[i])

    if print_debug: [print(i) for i in x1]
    if print_debug: print("---")
    if print_debug: [print(i) for i in y1]
    if print_debug: print("---")
    if print_debug: [print(i) for i in x2]
    if print_debug: print("---")
    if print_debug: [print(i) for i in y2]
    return x1, y1, x2, y2

def format_x1y1x2y2_data_file(inputfile, outputfile):
    with open(inputfile, "r") as f:
        mylist = f.readlines()
    mylist = [i.strip() for i in mylist]
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    num_of_sep = 0
    for item in mylist:
        if num_of_sep == 0:
            x1.append(item)
        elif num_of_sep == 1:
            y1.append(item)
        elif num_of_sep == 2:
            x2.append(item)
        elif num_of_sep == 3:
            y2.append(item)
        if len(item) == 1:
            # print("separater")
            num_of_sep += 1
    x1 = x1[0:-1]
    y1 = y1[0:-1]
    x2 = x2[0:-1]
    if print_debug: [print(i) for i in x1]
    if print_debug: ("--------")
    if print_debug: [print(i) for i in y1]
    if print_debug: print("--------")
    if print_debug: [print(i) for i in x2]
    if print_debug: print("--------")
    if print_debug: [print(i) for i in y2]

    # at this point we have the data read in,
    # now we need to format it x1y1, x2y2
    with open(outputfile, "w") as f:
        for i in range(len(x1)):
            f.writelines(x1[i])
            f.write("\n")
            f.writelines(y1[i])
            f.write("\n")
            f.writelines(x2[i])
            f.write("\n")
            f.writelines(y2[i])
            f.write("\n")
            f.writelines("=\n")

def get_row_from_x1y1x2y2_data_file(inputfile, i):
    if i < 0:
        sys.exit("Error in get_row_from(). i < 0.")
    with open(inputfile, "r") as f:
        mylist = f.readlines()
    mylist = [i.strip() for i in mylist]
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    returnarray = []
    for j in range(0, len(mylist), 5):
        x1 = mylist[j]
        y1 = mylist[j+1]
        x2 = mylist[j+2]
        y2 = mylist[j+3]
        temp = [x1, y1, x2, y2]
        returnarray.append(temp)
    # for item in returnarray:
    #     print(item)
    if i >= len(returnarray):
        return []
    return returnarray[i]

def string_array_to_float_array(string_array):
    # print("--- string_array_to_float_array (begin) ---")
    # print("string_array: {}".format(string_array))
    string_array = string_array.split(' ')
    ret_array = []
    for item in string_array:
        # print(item)
        ret_array.append(float(item))
    return ret_array

def get_all_rows_from_data_file(inputfile):
    with open(inputfile, "r") as f:
        mylist = f.readlines()
    mylist = [i.strip() for i in mylist]
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    returnarray = []
    x1_new = []
    y1_new = []
    x2_new = []
    y2_new = []
    new_array = []
    for j in range(0, len(mylist), 5):
        x1 = mylist[j]
        x1 = string_array_to_float_array(x1)
        y1 = mylist[j+1]
        y1 = string_array_to_float_array(y1)
        x2 = mylist[j+2]
        x2 = string_array_to_float_array(x2)
        y2 = mylist[j+3]
        y2 = string_array_to_float_array(y2)
        temp = [x1, y1, x2, y2]
        returnarray.append(temp)
    return returnarray

def main():
    input_file = "logfile.txt"
    output_file = "formatted_logfile.txt"
    x1y1x2y2_file = "x1y1x2y2_data.txt"
    # format_file(input_file, output_file)
    # read_data_from_file(output_file)
    # format_x1y1x2y2_data_file(output_file, x1y1x2y2_file)
    myrow = get_all_rows_from_data_file(x1y1x2y2_file)
    for item in myrow:
        for item2 in item:
            print("{}\n".format(item2))
        print("-----------------------------")
    # print(myrow[0])
    # print(myrow[1])
    # print(myrow[2])
    # print(myrow[3])

if __name__ == "__main__":
    main()
