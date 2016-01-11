import os

os.mkdir('check in/B111')


poi_list = []
f = open("txt/check_in_list.txt", "r")
for line in f:
    poi_list.append(line[:-1])
f.close()

for poi_id in poi_list:
    document_path = 'check in/'+poi_id[:8]
    if os.path.isdir(document_path):
        continue
    else:
        os.mkdir(document_path)
