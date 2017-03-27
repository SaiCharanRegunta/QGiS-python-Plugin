file=open("Important_Places.tsv","r")
file.readline()
Places=[]
for line in file:
	line=line.split(" ")
	Places.append(line[0])
Places=list(set(Places))
#print Places
file=open("IN.csv","r")
outputfile=open("Imp_Places_LatLon.csv","w")
for line in file:
	line=line.split(",")
	if line[2] in Places:
		outputfile.write(line[2]+","+line[3]+","+line[9]+","+line[10]+"\n")

