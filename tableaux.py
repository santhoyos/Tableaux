"""
Código de Tableaux realizado por Sofía Carrerá y Santiago Hoyos

"""
#-*-coding: utf-8-*-
from random import choice
##############################################################################
# Variables globales
##############################################################################

# Crea los conectivos
conectivos = ['Y', 'O', '>', '=']
# Crea las letras minúsculas a-z
letrasProposicionales = [chr(x) for x in range(97, 123)]
# inicializa la lista de interpretaciones
listaInterpsVerdaderas = []
# inicializa la lista de hojas
listaHojas = []

##############################################################################
# Definición de objeto tree y funciones de árboles
##############################################################################

class Tree(object):
	def __init__(self, label, left, right):
		self.left = left
		self.right = right
		self.label = label

def Inorder(f):
    # Imprime una formula como cadena dada una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: string de la formula
	if f.right == None:
		return f.label
	elif f.label == '-':
		return f.label + Inorder(f.right)
	else:
		return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def String2Tree(A):
	# Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
	# Input: - A, lista de caracteres con una formula escrita en notacion polaca inversa
	#        - letrasProposicionales, lista de letras proposicionales
	#        - conectivos, lista de conectivos
	# Output: formula como tree
	pila = []
	for c in A:
		# print("Examinando " + str(c))
		if c in letrasProposicionales:
			# print(u"El símbolo es letra proposicional")
			pila.append(Tree(c, None, None))
		elif c == '-':
			# print("Negamos")
			formulaAux = Tree(c, None, pila[-1])
			del pila[-1]
			pila.append(formulaAux)
		elif c in conectivos:
			# print("Unimos mediante conectivo")
			formulaAux = Tree(c, pila[-1], pila[-2])
			del pila[-1]
			del pila[-1]
			pila.append(formulaAux)
		else:
			print(u"Hay un problema: el símbolo " + str(c) + " no se reconoce")
	return pila[-1]

def Inorder2Tree(A):
	if len(A) == 1:
		return Tree(A[0], None, None)
	elif A[0] == '-':
		return Tree(A[0], None, Inorder2Tree(A[1:]))
	elif A[0] == "(":
		counter = 0 #Contador de parentesis
		for i in range(1, len(A)):
			if A[i] == "(":
				counter += 1
			elif A[i] == ")":
				counter -=1
			elif (A[i] in ['Y', 'O', '>', '=']) and (counter == 0):
				return Tree(A[i], Inorder2Tree(A[1:i]), Inorder2Tree(A[i + 1:-1]))
	else:
		return -1

##############################################################################
# Definición de funciones de tableaux
##############################################################################

def imprime_hoja(H):
	cadena = "{"
	primero = True
	for f in H:
		if primero == True:
			primero = False
		else:
			cadena += ", "
		cadena += Inorder(f)
	return cadena + "}"

def imprime_listaHojas(L):
	for h in L:
		print(imprime_hoja(h))

def complemento(l):
	# Esta función devuelve el complemento de un literal
	# Input: l, un literal
	# Output: x, un literal
    if es_literal(l) == True:
        if l.right == None:
            return Tree("-", None, l)
        elif l.label == "-":
            x = l.right
            return x
    else:
        return l
    pass

def par_complementario(l):
	# Esta función determina si una lista de solo literales
	# contiene un par complementario
	# Input: l, una lista de literales
	# Output: True/False
    pares = []
    for x in l:
        y = complemento(x)
        pares.append(y)
    # pares.append(complemento(x for x in l))
    for x in l:
        for y in pares:
            if Inorder(x) == Inorder(y):
                return True
    return False
    pass

def es_literal(f):
	# Esta función determina si el árbol f es un literal
	# Input: f, una fórmula como árbol
	# Output: True/False
	if f.right == None:
		return True
	elif f.label == "-":
            x = f.right
            if x.label == "-": 
                return False
            else: 
                return es_literal(f.right)
	elif f.label in conectivos:
		return False
	pass

def no_literales(l):
	# Esta función determina si una lista de fórmulas contiene
	# solo literales
	# Input: l, una lista de fórmulas como árboles
	# Output: None/f, tal que f no es literal
    for f in l:
        if es_literal(f)==True:
            continue
        else:
            # print ("Este no es literal")
            return f
    return None

    pass

def clasificacion(f):
	# clasifica una fórmula como alfa o beta
	# Input: f, una fórmula como árbol
	# Output: string de la clasificación de la formula
    
    if f.label == "O":
            return "2BETA"
    if f.label == ">":
            return "3BETA"
    elif f.label == "Y":
        return "2ALFA"
    elif f.label == "-":
        x = f.right
        if x.label == "-":
            return "1ALFA"
        elif x.label == ">":
            return "4ALFA"
        elif x.label == "O": 
                return "3ALFA"
        elif x.label == "Y":
                return "1BETA"
            
                
        # elif 
    pass

def clasifica_y_extiende(f, h):
	# Extiende listaHojas de acuerdo a la regla respectiva
	# Input: f, una fórmula como árbol
	# 		 h, una hoja (lista de fórmulas como árboles)
	# Output: no tiene output, pues modifica la variable global listaHojas

    global listaHojas

    print("Formula:", Inorder(f))
    print("Hoja:", imprime_hoja(h))

    assert(f in h), "La formula no esta en la lista!"

    clase = clasificacion(f)
    print("Clasificada como:", clase)
    assert(clase != None), "Formula incorrecta " + imprime_hoja(h)

    if clase == '1ALFA':
        aux = [x for x in h if x != f] + [f.right.right]
        listaHojas.remove(h)
        listaHojas.append(aux)
    elif clase == '2ALFA':
        aux = [x for x in h if x != f] + [f.left] + [f.right]
        listaHojas.remove(h)
        listaHojas.append(aux)
    elif clase == "3ALFA":
        aux = [x for x in h if x != f] + [Tree("-", None, f.right.left), Tree("-", None, f.right.right)]
        listaHojas.remove(h)
        listaHojas.append(aux)
    elif clase == "4ALFA":
        aux = [x for x in h if x != f] + [f.right.left, Tree("-", None, f.right.right)]
        listaHojas.remove(h)
        listaHojas.append(aux)
    elif clase == "1BETA":
        auxd = [x for x in h if x != f] + [Tree("-", None, f.right.left)]
        auxi = [x for x in h if x != f] + [Tree("-", None, f.right.right)]
        listaHojas.remove(h)
        listaHojas.append(auxd)      
        listaHojas.append(auxi)
    elif clase == "2BETA":
        auxd = [x for x in h if x != f] + [f.left]
        auxi = [x for x in h if x != f] + [f.right]
        listaHojas.remove(h)
        listaHojas.append(auxd)      
        listaHojas.append(auxi)
    elif clase == "3BETA":
        auxd = [x for x in h if x != f] + [Tree("-", None, f.left)]
        auxi = [x for x in h if x != f] + [f.right]
        listaHojas.remove(h)
        listaHojas.append(auxd)      
        listaHojas.append(auxi)
        # pass
	# Aqui el resto de casos


def Tableaux(f):

	# Algoritmo de creacion de tableau a partir de lista_hojas
	# Imput: - f, una fórmula como string en notación polaca inversa
	# Output: interpretaciones: lista de listas de literales que hacen
	#		 verdadera a f

	global listaHojas
	global listaInterpsVerdaderas

	A = String2Tree(f)
	print(u'La fórmula introducida es:\n', Inorder(A))

	listaHojas = [[A]]

	while (len(listaHojas) > 0):
		h = choice(listaHojas)
		print("Trabajando con hoja:\n", imprime_hoja(h))
		x = no_literales(h)
		if x == None:
			if par_complementario(h):
				listaHojas.remove(h)
			else:
				listaInterpsVerdaderas.append(h)
				listaHojas.remove(h)
		else:
			clasifica_y_extiende(x, h)

	return listaInterpsVerdaderas
