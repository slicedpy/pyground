import os
  
def run_directory_count():
    path = 'C:/Users/Tiffanee C. Lang/Desktop/keep'
    
    unique_ext = []

    keep_count = 0
    for (dirpath, dirnames, filenames) in os.walk(path):
        for flname in filenames:
            ext = os.path.splitext(flname.upper())[1]
            if [ext,0] not in unique_ext:
                unique_ext.append([ext,0])
        

    for (dirpath, dirnames, filenames) in os.walk(path):
        for flname in filenames:
            for each in unique_ext:
                if each[0] == os.path.splitext(flname.upper())[1]:
                    each[1] += 1

    for each in unique_ext:
        print each[0] + "," + str(each[1])      


run_directory_count()
