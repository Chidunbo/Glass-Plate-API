# read csv "author_info"
filename = "author_info.csv"
count_valid = 0
count_invalid = 0

with open(filename, "r") as file:
    data = file.readlines()
    # the four headers are Plate ID, Date, Author, Notebook, check author of each row
    for row in data[1:]:
        row = row.strip().split(", ")
        authors = row[2]
        # if the author is not "None", print the author
        if authors != "None":
            count_valid = count_valid + 1
        else:
            count_invalid = count_invalid + 1

        
print(f"Valid authors number: {count_valid}")
print(f"Invalid authors number: {count_invalid}")
print(f"percentage of valid authors: {count_valid/(count_valid + count_invalid)}")