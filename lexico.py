import re
import codecs
import os
import sys
from io import open
from numpy.core.defchararray import isalnum, isalpha, isdigit


class Token:
        tipo = ''
        lexema = ''
        linea= ''


reservadas = [
    ['T_PROGRAM','program'],
    ['T_IF','if'],
    ['T_ELSE','else'],
    ['T_FI','fi'], 
    ['T_DO','do'],
    ['T_UNTIL','until'], 
    ['T_WHILE','while'], 
    ['T_READ','read'], 
    ['T_WRITE','write'],
    ['T_FLOAT','float'], 
    ['T_INT','int'],  
    ['T_BOOL','bool'], 
    ['T_NOT','not'],
    ['T_AND','and'], 
    ['T_OR','or'],
    ['T_TRUE','true'],
    ['T_FALSE','false'],
    ['T_THEN','then']   
]

def buscarReservadas(palabra):
    global reservadas
    for plb in reservadas:
        if(palabra==plb[1]):
            return plb[0]
    return ' '
numlin = 1
def isdelim(ch):
    global numlin
    delim=[' ', '\t', '\n']
    if(ch=='\n'):
        numlin+=1
    if(ch in delim):
        if(i>(len(contenido))):
            return False
        return True
    else:
        return False


i = 0
token = Token()
def obttoken(contenido):
    global i
    global numlin
    ch = ''
    global token
    #print(contenido)
    estado = 'IN_START'
    puntoband=0
    igualband=0
    combandbloque=False
    comband=False
    while(estado!='IN_DONE'):
        
        if(estado=='IN_START'):
            ch=contenido[i]
            i+=1
            while(isdelim(ch)):
                if(i==(len(contenido))):
                    i-=1
                ch=contenido[i]
                i+=1
            if (ch.isalpha()):
                estado='IN_ID'
                token.lexema+=ch
            elif (isdigit(ch)):
                estado='IN_NUM'
                token.lexema+=ch
            elif (ch=='('):
                estado='IN_DONE'
                token.tipo='T_PARENI'
                token.lexema+=ch
                token.linea=numlin
            elif (ch==')'):
                estado='IN_DONE'
                token.tipo='T_PAREND'
                token.lexema+=ch
                token.linea=numlin
            elif (ch=='{'):
                estado='IN_DONE'
                token.tipo='T_LLAVEI'
                token.lexema+=ch
                token.linea=numlin
            elif (ch=='}'):
                estado='IN_DONE'
                token.tipo='T_LLAVED'
                token.lexema+=ch
                token.linea=numlin
            elif (ch==';'):
                estado='IN_DONE'
                token.tipo='T_PCOMA'
                token.lexema+=ch
                token.linea=numlin
            elif (ch==','):
                estado='IN_DONE'
                token.tipo='T_COMA'
                token.lexema+=ch
                token.linea=numlin
            elif (ch=='+'):
                estado='IN_DONE'
                token.tipo='T_MAS'
                token.lexema+=ch
                token.linea=numlin
            elif (ch=='-'):
                estado='IN_DONE'
                token.tipo='T_MENOS'
                token.lexema+=ch
                token.linea=numlin
            elif (ch=='^'):
                estado='IN_DONE'
                token.tipo='T_POT'
                token.lexema+=ch
                token.linea=numlin
            elif (ch=='*'):
                estado='IN_DONE'
                token.tipo='T_POR'
                token.lexema+=ch
                token.linea=numlin
            elif (ch=='/'): 
                estado='IN_COM'
                token.lexema+=ch
            elif (ch=='='):
                estado='IN_ASIGN'
                token.lexema+=ch
            elif (ch=='<'):
                estado='IN_OPRMENQ'
                token.lexema+=ch
            elif (ch=='>'):
                estado='IN_OPRMAYQ'
                token.lexema+=ch
            elif (ch=='!' and contenido[i]=='='):
                token.tipo='T_NOIGUAL'
                token.lexema+=ch
                token.lexema+=contenido[i]
                estado='IN_DONE'
                i+=1
                token.linea=numlin
                
            elif (ch=='~' or i==(len(contenido))):
                estado='IN_DONE'
                token.tipo='T_EOF'
                token.lexema+=ch
                i-=1
                token.linea=numlin
            elif ch == '"':
                estado = 'IN_DONE'
                token.tipo = 'T_COMILLAS'
                token.lexema += ch
                token.linea = numlin
            elif ch == '\\':
                estado = 'IN_DONE'
                token.tipo = 'T_BARRAINV'
                token.lexema += ch
                token.linea = numlin   
            else:
                token.tipo='T_ERROR'
                estado='IN_DONE'
                token.lexema+=ch
                token.linea=numlin

        #caso si son varios numeros
        if(estado=='IN_NUM'):
            ch=contenido[i]
            i+=1
            if(ch.isdigit() or ch=='.'): 
                if(ch=='.'):   
                    puntoband+=1
                if(puntoband<=1):
                    estado='IN_NUM'    
                    token.lexema+=ch
                else:
                    estado='IN_DONE'    
                    token.tipo='T_ERROR'
                    token.lexema+=ch
                    token.linea=numlin
            else:
                if(puntoband==1):
                    estado='IN_DONE'
                    token.tipo='T_NUM'
                    token.linea=numlin
                else:
                    estado='IN_DONE'
                    token.tipo='T_NUM'
                    token.linea=numlin
                estado='IN_DONE'
                i-=1
        #caso si tenemos 2 '='
        if(estado=='IN_ASIGN'):
            ch=contenido[i]
            i+=1
            if(ch=='='):
                estado='IN_DONE'
                token.tipo='T_IGUAL'
                token.lexema+=ch
                token.linea=numlin
            else:
                estado='IN_DONE'
                token.tipo='T_ASIGN'
                i-=1
                token.linea=numlin
        #caso '>'
        if(estado=='IN_OPRMAYQ'):
            ch=contenido[i]
            i+=1
            if(ch=='='):
                estado='IN_DONE'
                token.tipo='T_MAYI'
                token.lexema+=ch
                token.linea=numlin
                
            else:
                estado='IN_DONE'
                token.tipo='T_MAYQ' 
                token.linea=numlin
                i-=1
        #caso '<'
        if(estado=='IN_OPRMENQ'):
            ch=contenido[i]
            i+=1
            if(ch=='='):
                estado='IN_DONE'
                token.tipo='T_MENI'
                token.lexema+=ch
                token.linea=numlin
                
            else:
                estado='IN_DONE'
                token.tipo='T_MENQ'
                token.linea=numlin
                i-=1
        #caso ID
        if(estado=='IN_ID'):
            ch=contenido[i]
            i+=1
            if(not( ch.isalnum() or (ch=='_'))):
                tkn=buscarReservadas(token.lexema)
                if(tkn!=' '):
                    token.tipo=tkn
                else:
                    token.tipo="T_ID"
                estado='IN_DONE'
                i-=1
                token.linea=numlin
            else:
                token.lexema+=ch
        if(estado=='IN_COM'):
            ch=contenido[i]
            i+=1
            if(ch!='/' and ch!='*'):
                token.tipo='T_DIVID'
                estado='IN_DONE'
                i-=1
                token.linea=numlin
            else:
                if(ch=='/'):
                    comband=True
                    estado='IN_TERMCOM'
                elif(ch=='*'):
                    combandbloque=True
                    estado='IN_TERMCOM'
                token.lexema+=ch
        if(estado=='IN_TERMCOM'):
            ch=contenido[i]
            i+=1
            if(comband):
                if(ch!='\n' and i!=(len(contenido)-1)):
                    token.lexema+=ch
                else:
                    if(ch!='\n'):
                        token.lexema+=ch
                    token.tipo='T_COM'
                    estado='IN_DONE'  
                    token.linea=numlin
                    numlin+=1 
            if(combandbloque):
                if(ch=='*' and contenido[i]=='/'):
                    token.tipo='T_COM'
                    token.lexema+=ch
                    token.lexema+=contenido[i]
                    estado='IN_DONE'
                    i+=1
                    token.linea=numlin
                else:
                    token.lexema+=ch  
        
        
    return(token)         


            

if(len(sys.argv)==2):
    err=False
    try:
        
        txt = open(sys.argv[1], "r")
        contenido = txt.read()
        contenido+=' ~'
        contenido=list(contenido)
    except IOError:
        print ("No se encontro el archivo.")
        err = True
    if(not (err)):
        lex = open('lexico.txt', 'w')
        err = open('errores.txt', 'w')
        while(i != (len(contenido)-1)):
            token = obttoken(contenido)
            #print('('+token.tipo+','+token.lexema+')')
            if(str(token.tipo)=='T_ERROR'):
                contenido3=str(token.tipo)+'\t\t'+str(token.lexema)+'\t\t'+str(token.linea)+'\n'
                err.write(contenido3)
                token.tipo=''
                token.lexema= ''
            else:
                contenido2=str(token.tipo)+'\t\t'+str(token.lexema)+'\t\t'+str(token.linea)+'\n'
                lex.write(contenido2)
                token.tipo=''
                token.lexema= ''
            
            
        lex.close()
        err.close()  

else:
    print("Error al abrir archivo")

    
    


