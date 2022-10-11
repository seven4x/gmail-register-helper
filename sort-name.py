

checked_name = {line.strip() for line in open('names.txt', 'r')}
sorted_name = sorted(checked_name, key=len)
f = open('names-sorted.txt', 'w')
for name in sorted_name:
    f.write(name+"\n")
f.close()
