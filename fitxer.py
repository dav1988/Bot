
def personal():

	arxiu= open ('personal.txt', 'r')
	linies= arxiu.readlines()
	nobre_linies=len(linies)
	llista=[]
	paraula=""
	diccionari={}
	for i in linies:
		llista.append(i)

	for x in range(0,len(llista)):
		for i in llista[x]:
			if i != " " and i !="\n":
				paraula=paraula+i
			elif i == " ":
				clau=paraula
				paraula=""	
			else:
				diccionari[clau]=paraula
				paraula=""		
				x=x+1
	return diccionari

def id_users(iduser,personal):
	iduser= str(iduser)
	if iduser in personal:
		if personal[iduser] != 'None':
			return personal[iduser]
		else:
			return iduser
	else:
		return iduser
