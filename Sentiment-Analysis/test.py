import csv
import json 
import string

index = 0
dictionary_ult = {}        
with open ("ACCT1101.txt") as f:
    for line in f:
        # print(line[0:-2:])
        js = json.loads(line[:-2:])
        for key in js:
            if (key == "content"):
                dictionary_ult[index] = js[key]
                index += 1
        # print(js)
        # break
print(dictionary_ult)

#write to a file/txt 

# with open("readme.txt","w") as f1:
#     # f1.write("Content\n")
#     for key in dictionary_ult:
#         if (dictionary_ult[key] != None):
#             # f1.write(key,"\t")
#             f1.write(dictionary_ult[key])
#             # f1.write("]\n")
#             f1.write("]\n")
        # print(key)

    # f1.write("}")
    
with open("readme2.csv","w") as f2:
    writer = csv.writer(f2)
    for key in dictionary_ult:
        if (dictionary_ult[key] != None):
            text = dictionary_ult[key]
            text = str(text)
            text = text.translate(str.maketrans('','',string.punctuation))
            data = {text}
            writer.writerow(data)

f.close()
    # f1.close()
f2.close()
    