import fuzzy;
import jellyfish;

"""
double metaphone:
-----------------
	(Primary Key = Primary Key)   = Strongest Match
	(Secondary Key = Primary Key) = Normal Match
	(Primary Key = Secondary Key) = Normal Match
"""

global dm
dm = fuzzy.DMetaphone()

global conf
conf = {"dist":"get_closest_jaro","phon":"get_close_dmeta"}
#conf["dist"] = "get_closest_jaro_winkler"

global comp_map
comp_map = {}

comp_list = ["get_closest_jaro","get_closest_jaro_winkler","get_closest_hamming","get_closest_damerau_levenshtein","get_closest_levenshtein","get_close_dmeta"]

def get_closest_match(needle,haystack):
	global conf
	global comp_map
	res = None
	mm,hs = comp_map[conf["phon"]](needle,haystack)
	ml = len(mm)
	# Get best jaro dist for all strings if no phonetic matches, else get best jaro dist for the phonetic matches.
	if(ml > 0):
		res = comp_map[conf["dist"]](needle,mm)
	else:
		res = comp_map[conf["dist"]](needle,haystack)
	return res

def get_close_dmeta(needle,haystack,get_all=False):
	global dm
	res = None
	targ,ls = (needle,haystack)
	mm = []
	mm2 = []
	rz = dm(needle)
	if(rz[1] == None):
		del rz[1]
	has_strong = False
	for x in haystack:
		tz = dm(x)
		if(tz[1] == None):
			del tz[1]
		if(tz[0] == rz[0]): # strong match
			mm.append(x)
			has_strong = True
		elif((not has_strong)and(((len(tz) > 1)and(tz[1] == rz[0]))or((len(rz) > 1)and(tz[0] == rz[1])))):
			mm2.append(x)
	if((not has_strong) and (not get_all)):
		mm = mm2
	elif(get_all):
		for m in mm2:
			mm.append(m)
	return (mm,has_strong)

def get_closest_jaro(needle,haystack):
	closest = None
	for x in haystack:
		if(closest == None):
			closest = (x,jellyfish.jaro_distance(needle,x))
		else:
			temp = (x,jellyfish.jaro_distance(needle,x))
			if(temp[1] > closest[1]):
				closest = temp
	if(closest == None):
		return None
	return closest[0]

def get_closest_jaro_winkler(needle,haystack):
	closest = None
	for x in haystack:
		if(closest == None):
			closest = (x,jellyfish.jaro_winkler(needle,x))
		else:
			temp = (x,jellyfish.jaro_winkler(needle,x))
			if(temp[1] > closest[1]):
				closest = temp
	if(closest == None):
		return None
	return closest[0]

def get_closest_hamming(needle,haystack):
	closest = None
	for x in haystack:
		if(closest == None):
			closest = (x,jellyfish.hamming_distance(needle,x))
		else:
			temp = (x,jellyfish.hamming_distance(needle,x))
			if(temp[1] < closest[1]):
				closest = temp
	if(closest == None):
		return None
	return closest[0]

def get_closest_damerau_levenshtein(needle,haystack):
	closest = None
	for x in haystack:
		if(closest == None):
			closest = (x,jellyfish.damerau_levenshtein_distance(needle,x))
		else:
			temp = (x,jellyfish.damerau_levenshtein_distance(needle,x))
			if(temp[1] < closest[1]):
				closest = temp
	if(closest == None):
		return None
	return closest[0]

def get_closest_levenshtein(needle,haystack):
	closest = None
	for x in haystack:
		if(closest == None):
			closest = (x,jellyfish.levenshtein_distance(needle,x))
		else:
			temp = (x,jellyfish.levenshtein_distance(needle,x))
			if(temp[1] < closest[1]):
				closest = temp
	if(closest == None):
		return None
	return closest[0]

for x in comp_list:
	exec("global comp_list;\nglobal comp_map;\ncomp_map[\""+str(x)+"\"] = "+str(x)+";\n")

if __name__ == "__main__":
	print(str(get_closest_match("test",["targ","alpha","charlie","tactile","tactics","extreme","variable","excellent"])))
