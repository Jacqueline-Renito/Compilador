from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from io import open
from tkinter import ttk
import re
from tkinter import font
from os import remove, system

compilado=False
root = Tk()
root.geometry("1350x700")
root.config(bg="#154360",  relief="sunken", borderwidth=5)
root.title("Compilador R++")



#---------Diseño del frame 1
frame1=Frame(root, width=900, height=400)
frame1.config(bg="#5F6A6A",relief="raised", borderwidth=5)
frame1.grid(row=0, column=0, padx=12, pady=12)


#---------Diseño del frame 2
frame2=Frame(root, width=550, height=350)
frame2.config(bg="#5F6A6A",relief="raised", borderwidth=5)
frame2.place(x=790,y=25)


#---------Diseño del frame 3
frame3=Frame(root, width=1342, height=200)
frame3.config(bg="#5F6A6A",relief="raised", borderwidth=5)
frame3.place(x=11,y=455)



#-------------DECLARACION DE LAS VARIABLES
archivo = ""
palabras_reservadas = ['program', 'if', 'else', 'fi','do', 'until', 'while', 'read', 'write', 'float', 'int', 'bool', 'not', 'and', 'or',"+", "-", "*", "/","^", "<", "<=", ">", ">=", "==", "!=", "=", ";", ",", "(",")","{","}"]
idx="1.0"
operadores_reservados=["+", "-", "*", "/","^", "<", "<=", ">", ">=", "==", "!=", "=", ";", ",", "(",")","{","}"]



#FUNCIONES

#Funcion para abrir archivos
def abrirarchivo():
	compilado=False
	global archivo
	try:
		archivo = filedialog.askopenfile(title="Abrir Archivo",mode ="r+", initialdir="'C:\'", filetypes=(("Archivos de Texto","*.txt"),("Todos los archivos","*.*")))
		entryCodigo.delete(1.0, END)
		entryCodigo2.config(state=NORMAL)
		entryCodigo2.delete(1.0, END)
		entryCodigo2.config(state=DISABLED)
		entryErrores.config(state=NORMAL)
		entryErrores.delete(1.0, END)
		entryErrores.config(state=DISABLED)
		lineas=""
		for linea in archivo:
			lineas=lineas+linea
	
		entryCodigo.insert(1.0, lineas[:])
		print("Se abrio el archivo")
		print("Ruta del archivo: ",archivo.name)
		print("Ruta del archivo: ",archivo.name)
		espacio2()
	except:
		messagebox.showwarning("Archivo","No se abrio ningun archivo")
#Funcion para guardar como archivo
def guardarcomo():
	global archivo
	try:
		archivo = filedialog.asksaveasfile(mode='w+', defaultextension=".txt")
		archivo.write(entryCodigo.get(1.0, END))
		archivo.close()
		print("Archivo guardado como:")
		print("En la ruta: ", archivo.name)
	except:
		messagebox.showwarning("Archivo","Archivo no guardado")	

#Funcion para guardar archivo
def guardar():
	global archivo
	try:
		if(archivo!="" or archivo!=" "):
			archivo = open(archivo.name,"w")
			archivo.seek(0)
			archivo.write(entryCodigo.get(1.0, END))
			print("Archivo guardado")
			print("Se guardo en la ruta:", archivo.name)
			archivo.close()
	except:
		guardarcomo()


#Funcion para cerrar archivo
def cerrar():
	compilado=False
	try:
		global archivo
		archivo.close()
		archivo=""
		entryCodigo.delete(1.0, END)
		entryCodigo2.config(state=NORMAL)
		entryCodigo2.delete(1.0, END)
		entryCodigo2.config(state=DISABLED)
		print("Archivo Cerrado")
	except:
		messagebox.showinfo("Archivo","No se ha abierto ningún archivo")	
#Funcion para copiar
def copiar():
    entryCodigo.event_generate("<<Copy>>")
#Funcion para copiar
def seleccionartodo():
    entryCodigo.event_generate("<<SelectAll>>")
#Funcion para cortar
def cortar():
        entryCodigo.event_generate("<<Cut>>")
#Funcion para pegar 	
def pegar():
    entryCodigo.event_generate("<<Paste>>")
#Funcion para deshacer 	
def deshacer():
	entryCodigo.edit_undo()
#Funcion para rehacer 	
def rehacer():
	try:
		entryCodigo.edit_redo()
	except:
		messagebox.showinfo("Rehacer","Nada que rehacer")
#Funcion para colorear palabras 
def espacio(event):  
	global palabras_reservadas
	global operadores_reservados

	for i in palabras_reservadas:
		idx = '1.0'
		while idx:
			idx = entryCodigo.search(i, idx, nocase=1, stopindex=END) 
			aux = entryCodigo.index('insert') 
			if idx:
				lastidx = '%s+%dc' % (idx,len(i))
				entryCodigo.tag_add("tag",idx, lastidx)
				entryCodigo.tag_configure("tag", foreground="red")
				idx = lastidx

#Funcion para colorear el archivo que se abra
def espacio2():  
	global palabras_reservadas
	global operadores_reservados

	for i in palabras_reservadas:
		idx = '1.0'
		while idx:
			idx = entryCodigo.search(i, idx, nocase=1, stopindex=END) 
			aux = entryCodigo.index('insert') 
			if idx:
				lastidx = '%s+%dc' % (idx,len(i))
				entryCodigo.tag_add("tag",idx, lastidx)
				entryCodigo.tag_configure("tag", foreground="red")
				idx = lastidx

#Funcion Compilar
def compilar():
	global compilado
	global archivo
	if archivo!='':
		guardar()
		try:
			remove('lexico.txt')
		except:
			pass
		ruta = '"'+archivo.name+'"'
		system("python3 lexico.py "+ruta)
		bandcompil=False
		contenido=''
		while(bandcompil!=True):
			try:
				
				lex=open('lexico.txt', 'r')
				err=open('errores.txt', 'r')
				contenido = lex.read()
				contenido2 = err.read()
			except:
				bandcompil=False
			if(contenido==''):
				bandcompil=False
			else:
				bandcompil=True
		#imprimiendo contenido
		entryCodigo2.config(state=NORMAL)
		entryErrores.config(state=NORMAL)
		entryCodigo2.delete(1.0, END)
		entryErrores.delete(1.0, END)
		tabla='TOKEN \t\tLEXEMA\t\t#LINEA \n----------------------------------------\n'
		entryCodigo2.insert(1.0, tabla)
		entryErrores.insert(1.0, tabla)
		lexico=""
		for linea in contenido:
			lexico+=linea
		entryCodigo2.insert(3.0, lexico[:])
		errores=""
		for lin in contenido2:
			errores+=lin
		entryErrores.insert(3.0, errores[:])
		entryErrores.config(state=DISABLED)
		compilado=True
		lex.close()
		err.close()
	else:
		messagebox.showwarning("Archivo no guardado","Favor de guardar el archivo.")
#Funcion Sintactico
def sintactico():
    global compilado
    if compilado:
        system("python3 sintactico.py lexico.txt")
        # Leer el resultado del análisis sintáctico desde el archivo sintactico.txt
        try:
            with open('sintactico.txt', 'r', encoding="utf-8") as sint_file:
                sint_content = sint_file.read()
            with open('errorsintactico.txt', 'r') as errsint_file:
                errsint_content = errsint_file.read()
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo sintactico.txt o errorsintactico.txt no se encontró.")
            return
        entryCodigo2.config(state=NORMAL)
        entryErrores.config(state=NORMAL)
        entryCodigo2.delete(1.0, END)
        entryErrores.delete(1.0, END)
        sintacticotxt = ""
        for linea in sint_content:
            sintacticotxt += linea
        entryCodigo2.insert(3.0, sintacticotxt[:])
        errores = ""
        for lin in errsint_content:
            errores += lin
        entryErrores.insert(3.0, errores[:])
        entryErrores.config(state=DISABLED)
        entryCodigo2.config(state=DISABLED)
    else:
        messagebox.showwarning("Alerta", "Primero compilar")

	
def lexico():
	global compilado
	if compilado:
		contenido=''
		try:
				
				lex=open('lexico.txt', 'r')
				err=open('errores.txt', 'r')
				contenido = lex.read()
				contenido2 = err.read()
		except:
			messagebox.showwarning("Alerta", "No se pudo abrir archivo.")
		entryCodigo2.config(state=NORMAL)
		entryErrores.config(state=NORMAL)
		entryCodigo2.delete(1.0, END)
		entryErrores.delete(1.0, END)
		tabla='TOKEN \t\tLEXEMA\t\t#LINEA \n----------------------------------------\n'
		entryCodigo2.insert(1.0, tabla)
		entryErrores.insert(1.0, tabla)
		lexico=""
		for linea in contenido:
			lexico+=linea
		entryCodigo2.insert(3.0, lexico[:])
		errores=""
		for lin in contenido2:
			errores+=lin
		entryErrores.insert(3.0, errores[:])
		entryErrores.config(state=DISABLED)
		compilado=True
		lex.close()
		err.close()
	else:
		messagebox.showwarning("Alerta", "Compilar primero")

#---------Declaracion del menu
barraMenu = Menu(root)
root.config(menu=barraMenu, width=300, height=300)
#-----------Declaracion de las Ventanas del menu
archivoMenu=Menu(barraMenu, tearoff=0)
editarMenu=Menu(barraMenu, tearoff=0)
formatoMenu=Menu(barraMenu, tearoff=0)
compilarMenu=Menu(barraMenu, tearoff=0)
ayudaMenu=Menu(barraMenu, tearoff=0)
#-----------Ventanas del menu
barraMenu.add_cascade(label="Archivo", menu=archivoMenu)
barraMenu.add_cascade(label="Editar", menu=editarMenu)
barraMenu.add_cascade(label="Formato", menu=formatoMenu)
barraMenu.add_cascade(label="Compilar", menu=ayudaMenu)
barraMenu.add_cascade(label="Ayuda")
#-----------Ventanas del archivomenu
archivoMenu.add_command(label="Abrir", command= abrirarchivo)
archivoMenu.add_separator()
archivoMenu.add_command(label="Guardar", command =  guardar, underline=0, accelerator="Ctrl+S")
archivoMenu.add_command(label="Guardar Como...", command= guardarcomo)
archivoMenu.add_separator()
archivoMenu.add_command(label="Cerrar", command = cerrar)

#-----------Ventanas del editarmenu
editarMenu.add_command(label="Copiar", command = copiar, accelerator="Ctrl+C")
editarMenu.add_command(label="Pegar", command = pegar, accelerator="Ctrl+V")
editarMenu.add_command(label="Seleccionar Todo", command = seleccionartodo, accelerator="Ctrl+A")
editarMenu.add_separator()
editarMenu.add_command(label="Cortar", command = cortar, accelerator="Ctrl+X")
editarMenu.add_separator()
editarMenu.add_command(label="Rehacer" , command = rehacer, accelerator="Ctrl+Y")
editarMenu.add_command(label="Deshacer", command = deshacer, accelerator="Ctrl+Z")
#------------Ventanas del compilarmenu
ayudaMenu.add_command(label="Compilar", command = compilar)
#-----------Declaracion del escritor de codigo 
#---labelCodigo=Label(frame1, text="Código a compilar", width=20, height=2, borderwidth=4, relief="sunken", bg="#D7DBDD")
#--labelCodigo.grid(row=0, column=1, padx=10, pady=10)

entryCodigo=Text(frame1, width=90, height=20, undo=True)
entryCodigo.grid(row=1, column=1, padx=10, pady=10)

scrollVert= Scrollbar(frame1, command=entryCodigo.yview)
scrollVert.grid(row=1, column=2, sticky="nsw", padx=0, pady=8)

entryCodigo.config(yscrollcommand=scrollVert.set)

#-----------------------ELEMENTOS FRAME 2
entryCodigo2=Text(frame2, width=63,state=DISABLED,wrap="none", height=22)
entryCodigo2.grid(row=1, column=0, padx=10, pady=10)

scrollVert= Scrollbar(frame2, command=entryCodigo2.yview)
scrollVert.grid(row=1, column=1, sticky="nsw", padx=0, pady=2)
scrollHor= Scrollbar(frame2, command=entryCodigo2.xview, orient="horizontal")
scrollHor.grid(row=20, column=0, padx=2,sticky="ew", pady=0)

entryCodigo2.config(xscrollcommand=scrollHor.set)
entryCodigo2.config(yscrollcommand=scrollVert.set)


#----------------------BOTONES FRAME 2
botonLexico=Button(root, text="Lexico", width=7, relief="raised", borderwidth=5, command=lexico)
botonLexico.place(x=800,y=12)
botonSintactico=Button(root, text="Sintactico", width=9, relief="raised", borderwidth=5, command=sintactico)
botonSintactico.place(x=860,y=12)
botonSemantico=Button(root, text="Semantico", width=9, relief="raised", borderwidth=5)
botonSemantico.place(x=934,y=12)
botonCodIntermedio=Button(root, text="Codigo Intermedio", width=20, relief="raised", borderwidth=5)
botonCodIntermedio.place(x=1008,y=12)

#----------------------BOTONES FRAME 3
botonLexico=Button(root, text="Error", width=10, relief="raised", borderwidth=5)
botonLexico.place(x=25, y=433)
botonSintactico=Button(root, text="Resultados", width=12, relief="raised", borderwidth=5)
botonSintactico.place(x=108,y=433)

entryErrores=Text(frame3, width=160, height=10)
entryErrores.grid(row=0, column=1, padx=10, pady=10)

scrollVert= Scrollbar(frame3, command=entryErrores.yview)
scrollVert.grid(row=0, column=2, sticky="nsw", padx=0, pady=8)

entryErrores.config(yscrollcommand=scrollVert.set)


entryCodigo.bind("<space>", espacio)
entryCodigo.bind("<Return>", espacio)

root.bind('<Control-s>', lambda event: guardar())
root.mainloop()
