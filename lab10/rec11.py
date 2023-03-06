# Rec 11
f = open('features.cav')
alltext = f.read()
f.close()

with open('features.cav') as f:
    oneline = f.readline()
    for line in f:
        print(line)

painting_features = {}
with open('features.cav') as f:
    headers = f.readline().strip().lower().split(',')
    for line in f:
        vals = line.strip().split(',')
        this_feature = {headers[ix] for ix, val in enumerate(vals)
                        if val == True}
    painting_features[vals[0]] = this_feature # add k-v pair into dict

count = 0
for i in painting_features.values():
    if 'tree' in i:
        count += 1

sum('tree' in i for i in painting_features.values())

feature_count = {}
for h in headers[1:]:
    feature_count[h] = sum(h in i for i in painting_features.values())
