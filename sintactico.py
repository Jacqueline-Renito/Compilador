import re
import codecs
import os
import sys
from io import open
from tkinter.constants import FALSE
        
textoarchsin=['']
class Elemento:
    def __init__(self,token, lexema,linea):
        self.token=token
        self.lexema=lexema
        self.linea=linea
class Pila:
     def __init__(self):
         self.items = []
     def vaciar(self):
         self.items=[]
     def incluir(self, item):
         self.items.append(item)


def inicio():
    global pila
    regla=['T_PROGRAM','T_LLAVEI']
    band=False
    if(len(pila.items)==len(regla)):
        if (pila.items[0].token == regla[0] and pila.items[1].token == regla[1] ):
            return True
        else: 
            return False
    else:
        band=False
    return band
def declaracion():
    global pila
    bandtipo=False
    regla=['T_INT','T_FLOAT','T_BOOL']
    regla2=['T_ID','T_COMA','T_PCOMA']
    for i in range(0,len(regla)):
        if(pila.items[0].token==regla[i]):
            bandtipo=True
            break
        else:
            bandtipo=False
    if(bandtipo):
        bandcoma=False
        bandid=False
        for i in range (1,len(pila.items)):
            for j in range(0,len(regla2)):
                if(pila.items[i].token==regla2[j]):
                    if(pila.items[i].token=='T_COMA' and not(bandcoma)):
                        bandcoma=True
                        bandid=False
                    elif(pila.items[i].token=='T_PCOMA' and not(bandcoma)):
                        return True
                    elif(pila.items[i].token=='T_ID' and not(bandid)):
                        bandcoma=False
                        bandid=True
                    elif((pila.items[i].token=='T_COMA' and bandcoma) or(pila.items[i].token=='T_ID' and bandid)):
                        return False
                    break
        return False
    else:
        return False
def sent_read(auxiliarpila):
    global pila
    regla=['T_READ','T_ID','T_PCOMA']
    if(len(auxiliarpila.items)!=len(regla)):
        return False
    for i in range(0,len(regla)):
        if(auxiliarpila.items[i].token!=regla[i]):
            return False
    return True
def sent_ifanidado(auxiliarpila):
    global contadorifanidado
    global ifbandanidado
    auxpila=Pila()
    regla=['T_IF','T_PARENI','T_PAREND','T_THEN','T_LLAVEI','T_LLAVED','T_FI']
    
    contador=1
    bandtermino=False
    if(len(auxiliarpila.items)>1):
        if(auxiliarpila.items[0].token==regla[0] and auxiliarpila.items[1].token==regla[1]):
            
            for i in range(2,len(auxiliarpila.items)):
                if(auxiliarpila.items[i].token==regla[1]):
                    contador+=1
                    auxpila.incluir(auxiliarpila.items[i])
                elif(auxiliarpila.items[i].token==regla[2]and contador!=1):
                    contador-=1
                    auxpila.incluir(auxiliarpila.items[i])
                elif(auxiliarpila.items[i].token==regla[2]):
                    contador-=1
                else:
                    auxpila.incluir(auxiliarpila.items[i])
                if(contador==0):
                    #enviar a bterm
                    
                    bandtermino=True
                    break
            if(bandtermino):
                #print('len auxpila if')
                #print(len(auxpila.items))
                sintaxisif=sent_bexpresion(auxpila)
                if(sintaxisif and (len(pila.items)>=len(auxpila.items)+4)):
                    #aqui se revisara todo lo demas como el then y lo que resta
                    #textoarchsin.append('IF-Condicion:\n\tLexema\t\t\tLinea\t\t\tToken\n')
                    #for i in range(0,len(auxpila.items)+3):
                       #textoarchsin.append('\t'+pila.items[i].lexema+'\t\t\t'+pila.items[i].linea+'\t\t\t'+pila.items[i].token+'\n')
                    #print('aqui quedo')
                    if(auxiliarpila.items[len(auxpila.items)+3].token=='T_THEN'):
                        auxpila2=Pila()
                        
                        for i in range(len(auxpila.items)+4,len(auxiliarpila.items)):
                            auxpila2.incluir(auxiliarpila.items[i])
                        print('ver bloque')
                        for i in range(0,len(auxpila2.items)):
                            print(auxpila2.items[i].token) 
                        valor=sent_bloque(auxpila2) 
                        if(valor):
                            ifbandanidado=True
                            print('esto es un if anidado')
                            return True
                            print('final if')
                            if(pila.items[len(pila.items)-1].token=='T_FI' and contadorif==0):
                                #print(contadorif)
                                print('tknfi entre final')
                                return True
                            pila3=Pila()
                            print('aqui checo if')
                            print(len(auxpila.items))
                            print(len(auxpila2.items))
                            for i in range(len(auxpila.items)+len(auxpila2.items)+3,len(pila.items)):
                                pila3.incluir(pila.items[i])
                                print(pila.items[i].token)
                            if(not(sent_bloque(pila3))):
                                print('esto no es bloque')
                                return False 
                            else:
                                return True
                        else:
                            #print('bloque no')
                            
                            return False
                    else:
                        
                        return False
                    print('si es un if')
                    print(textoarchsin)
                    #return True
                else:
                    return False
def sent_if():
    global pila
    global textoarchsin
    global contadorif
    global ifband
    auxpila=Pila()
    regla=['T_IF','T_PARENI','T_PAREND','T_THEN','T_LLAVEI','T_LLAVED','T_FI']
    contador=1
    bandtermino=False
    if(len(pila.items)>1):
        if(pila.items[0].token==regla[0] and pila.items[1].token==regla[1]):
            
            for i in range(2,len(pila.items)):
                if(pila.items[i].token==regla[1]):
                    contador+=1
                    auxpila.incluir(pila.items[i])
                elif(pila.items[i].token==regla[2]and contador!=1):
                    contador-=1
                    auxpila.incluir(pila.items[i])
                elif(pila.items[i].token==regla[2]):
                    contador-=1
                else:
                    auxpila.incluir(pila.items[i])
                if(contador==0):
                    #enviar a bterm
                    
                    bandtermino=True
                    break
            if(bandtermino):
                #print('len auxpila if')
                #print(len(auxpila.items))
                sintaxisif=sent_bexpresion(auxpila)
                if(sintaxisif and (len(pila.items)>=len(auxpila.items)+4)):
                    #aqui se revisara todo lo demas como el then y lo que resta
                    #textoarchsin.append('IF-Condicion:\n\tLexema\t\t\tLinea\t\t\tToken\n')
                    #for i in range(0,len(auxpila.items)+3):
                       #textoarchsin.append('\t'+pila.items[i].lexema+'\t\t\t'+pila.items[i].linea+'\t\t\t'+pila.items[i].token+'\n')
                    #print('aqui quedo')
                    if(pila.items[len(auxpila.items)+3].token=='T_THEN'):
                        auxpila2=Pila()
                        
                        for i in range(len(auxpila.items)+4,len(pila.items)):
                            auxpila2.incluir(pila.items[i]) 
                        valor=sent_bloque(auxpila2) 
                        if(valor):
                            
                            ifband=True
                            return True
                            print('final if')
                            if(pila.items[len(pila.items)-1].token=='T_FI' and contadorif==0):
                                #print(contadorif)
                                print('tknfi entre final')
                                return True
                            pila3=Pila()
                            print('aqui checo if')
                            print(len(auxpila.items))
                            print(len(auxpila2.items))
                            for i in range(len(auxpila.items)+len(auxpila2.items)+3,len(pila.items)):
                                pila3.incluir(pila.items[i])
                                print(pila.items[i].token)
                            if(not(sent_bloque(pila3))):
                                print('esto no es bloque')
                                return False 
                            else:
                                return True
                        else:
                            #print('bloque no')
                            
                            return False
                    else:
                        
                        return False
                    print('si es un if')
                    print(textoarchsin)
                    #return True
                else:
                    return False
def busquedafinif(auxpila):
    global contadorif
    if(auxpila.items[0].token=='T_FI'):
        return True
    elif(auxpila.items[0].token=='T_ELSE'):
        pila2=Pila()
        print('endif')
        for i in range(1,len(auxpila.items)):
            pila2.incluir(auxpila.items[i])
        if(len(pila2.items)>=2):
            print('es bloque?')
            if(sent_bloque(pila2)):
                print('checo pila 2')
                return False
            else:
                print('contadorif'+str(contadorif))
                if(pila2.items[len(pila2.items)-1].token=='T_FI' and pila2.items[len(pila2.items)-2].token=='T_LLAVED'):
                    #contadorif-=1
                    print('contadorif'+str(contadorif))
                    return True
                else:
                    return False
        else:
            return False    
def sent_bloque(pilabloque):
    if(len(pilabloque.items)>0):
        if(pilabloque.items[0].token=='T_LLAVEI' and pilabloque.items[len(pilabloque.items)-1].token=='T_LLAVED'):
            
            auxpila2=Pila()
            for i in range (1,len(pilabloque.items)-1):
              auxpila2.incluir(pilabloque.items[i])
              #print('bloquepilasin bracket')
              #print(pilabloque.items[i].token)
            #   print(auxpila.items[i].token)
            contadorbracket=0
            for i in range(0,len(auxpila2.items)):
                if(auxpila2.items[i].token=='T_LLAVEI'):
                    contadorbracket+=1
                elif(auxpila2.items[i].token=='T_LLAVED'):
                    contadorbracket-=1
            if(contadorbracket!=0):
                return False
            if(sent_listsent(auxpila2)):
                return True
            else:
               return False    
        else:
            return False
    else:
        return False
def sent_listsent(auxpila):
    if(len(auxpila.items)>0):
        if(sentencias(auxpila)):
            print('sentlist') 
            return True
        else:
            return False
def sent_bexpresion(auxpila):
    if(len(auxpila.items)==1):
        if(sent_notfactor(auxpila,True)):
            return True
        else:
            return False
    else:
        if(len(auxpila.items)>2):
            bandop=False
            auxpila2=Pila()
            regla=['T_OR','T_AND']
            cont=0
            bandopdoble=False
            for i in range(0,len(auxpila.items)):
                if(auxpila.items[i].token==regla[0] or auxpila.items[i].token==regla[1]):
                    bandopdoble=True
                    continue
                else:
                    bandopdoble=False
                if(bandopdoble):
                    print('em 309')
                    error()
                    return False
                
            for i in range(0,len(auxpila.items)):
                if(auxpila.items[i].token==regla[0] or auxpila.items[i].token==regla[1]):
                    bandop=not(bandop)
                    cont+=1
                else:                        
                    auxpila2.incluir(auxpila.items[i])
                if(bandop and len(auxpila2.items)!=0):
                    #for j in range(0,len(auxpila2.items)):
                        #print(auxpila2.items[j].lexema)
                    if(sent_notfactor(auxpila2,False)):
                        auxpila2.vaciar()
                        bandop=False
                        pass
                    else:
                        return False   
                    #break
            if(len(auxpila2.items)!=0):
                
                if(sent_notfactor(auxpila2,False)):
                    
                    return True
                else:
                    return False
        elif(sent_notfactor(auxpila,False)):
            return True
        else:
            return False
def sent_notfactor(auxpila,unchar):
    if(unchar):
        if(sent_bfactor(auxpila.items[0],True)):
        
            return True
        else:
            return False
    else:
        bandnot=False
        if(auxpila.items[0].token=='T_NOT'):
            auxpila3=Pila()
            for i in range (1,len(auxpila.items)):
                auxpila3.incluir(auxpila.items[i])
            if(sent_bfactor(auxpila3,False)):
                return True
            else:
                return False
        else:
            auxpila2=Pila()
            for i in range(0,len(auxpila.items)):
                if(auxpila.items[i].token=='T_NOT'):
                    bandnot=True
                else:
                    auxpila2.incluir(auxpila.items[i])
                #aqui va cuando sea distinto de una expresion booleana de un if not x==y
            if(sent_bfactor(auxpila2,False)):
                return True
            else:
                return False
def sent_write(auxpila):
    regla=['T_WRITE','T_PCOMA']
    auxpila2=Pila()
    if(auxpila.items[0].token==regla[0]):
        for i in range(1,len(auxpila.items)):
            if(auxpila.items[i].token!=regla[1]):
                auxpila2.incluir(auxpila.items[i])
            else:
                if(sent_bexpresion(auxpila2)):
                    return True
                else:
                    return False
        return False
    else:
        return False
def sent_asignacion(auxpila):
    regla=['T_ID','T_ASIGN','T_PCOMA']
    auxpila2=Pila()
    if(len(auxpila.items)<2):
        return False
    if(auxpila.items[0].token==regla[0] and auxpila.items[1].token==regla[1]):
        for i in range(2,len(auxpila.items)):
            if(auxpila.items[i].token!=regla[2]):
                auxpila2.incluir(auxpila.items[i])
            else:
                if(sent_bexpresion(auxpila2)):
                    return True
                else:
                    return False
        return False
    else:
        return False  
def sent_bfactor(auxpila,unchar):
    regla=['T_TRUE','T_FALSE']
    if(unchar):
        for i in range(0,len(regla)):
            if(auxpila.token==regla[i]):
                return True
        auxpila2=Pila()
        auxpila2.incluir(auxpila)
        if(sent_relacion(auxpila2)):
            return True
        else:
            return False
    else:
        if(sent_relacion(auxpila)):
            return True
        else:
            return False
def sent_relacion(auxpila):
    regla=['T_IGUAL','T_NOIGUAL','T_MENQ','T_MENI','T_MAYQ','T_MAYI']
    auxpila2=Pila()
    band=False
    for i in range(0,len(auxpila.items)):
        for j in range(0,len(regla)):
            if(auxpila.items[i].token==regla[j]):
                band=True
                break
        if(not(band)):
            auxpila2.incluir(auxpila.items[i])
        band=False
    if(sent_expresion(auxpila2)):
        return True
    else:
        return False
def sent_expresion(auxpila):
    regla=['T_MAS','T_MENOS','T_DIVID','T_POR']
    cont=0
    bandop=False
    auxpila2=Pila()
    for i in range(0,len(auxpila.items)):
        for j in range(0,len(regla)):
            if(auxpila.items[i].token==regla[j]):
                bandop=True
                break
        if(not(bandop)):
            auxpila2.incluir(auxpila.items[i])
        else:
            bandop=False
    if(sent_factor(auxpila2)):
        return True
    else:
        return False
def sent_while(auxiliarpila):
    auxpila=Pila()
    regla=['T_WHILE','T_PARENI','T_PAREND','T_LLAVEI','T_LLAVED']
    contador=1
    bandtermino=False
    if(len(auxiliarpila.items)>1):
        if(auxiliarpila.items[0].token==regla[0] and auxiliarpila.items[1].token==regla[1]):
            for i in range(2,len(auxiliarpila.items)):
                if(auxiliarpila.items[i].token==regla[1]):
                    contador+=1
                    auxpila.incluir(auxiliarpila.items[i])
                elif(auxiliarpila.items[i].token==regla[2]and contador!=1):
                    contador-=1
                    auxpila.incluir(auxiliarpila.items[i])
                elif(auxiliarpila.items[i].token==regla[2]):
                    contador-=1
                else:
                    auxpila.incluir(auxiliarpila.items[i])
                if(contador==0):
                    #enviar a bterm
                    
                    bandtermino=True
                    break
            if(bandtermino):
                #print('len auxpila if')
                #print(len(auxpila.items))
                sintaxisif=sent_bexpresion(auxpila)
                if(sintaxisif and (len(pila.items)>=len(auxpila.items)+3)):
                    auxpila2=Pila()
                        
                    for i in range(len(auxpila.items)+3,len(auxiliarpila.items)):
                        auxpila2.incluir(auxiliarpila.items[i])
                    print('ver bloque while')
                    for i in range(0,len(auxpila2.items)):
                        print(auxpila2.items[i].token) 
                    valor=sent_bloque(auxpila2) 
                    if(valor):
                        print('esto es while')
                        return True
                            
                    else:                       
                        return False
                else:
                    return False
def sent_factor(auxpila):
    regla=['T_PARENI','T_PAREND','T_NUM','T_ID']
    band=False
    for i in range(0,len(auxpila.items)):
        for j in range(0,len(regla)):
            if(auxpila.items[i].token==regla[j]):
                band=True
                break
        if(not(band)):
            print('em 505')
            error()
            return False 
        band=False 
    return True      
def sent_do(auxpila):
    regla=['T_DO', 'T_PCOMA']
    if(len(auxpila.items)>3):
        if(auxpila.items[0].token==regla[0]):
            auxpila2=Pila()
            for i in range(1, len(auxpila.items)):
                auxpila2.incluir(auxpila.items[i])
            if(sent_bloque(auxpila2)):
                return True
            else:
                print('no es bloque')
                return False
        else:
            print('no lleva do')
            return False
    else:
        return False
def sent_until(auxpila):
    if(len(auxpila.items)>4):
        if(auxpila.items[0].token=='T_UNTIL' and auxpila.items[1].token=='T_PARENI'):
            auxpila2=Pila()
            for i in range(2, len(auxpila.items)-1):
                auxpila2.incluir(auxpila.items[i])
            if(sent_bexpresion(auxpila2)):
                if(auxpila.items[len(auxpila.items)-1].token=='T_PCOMA'):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def sentencias(pila2):     
    global textoarchsin
    global pila
    global ifbandanidado    
    band='incompleto'
    bsent=False
    bdo=False
    auxiliarmayorpila=Pila()
    for i in range(0,len(pila.items)):
        auxiliarmayorpila.incluir(pila.items[i])
    pila.vaciar()
    
    longitud=len(pila2.items)-1
    z=0
    while z<=longitud:

        if(len(pila2.items)>0):
            pila.incluir(pila2.items[z])
            print('añade - a pila bloque')
            print(pila2.items[z].token)
            if(inicio()):
                return False
            elif(declaracion()):
                print('esto es una declaracion')
                bsent=True
                pila.vaciar()
            elif(sent_read(pila)):
                print('esto es un read')
                bsent=True    
                pila.vaciar()
            elif(sent_write(pila)):
                print('esto es un write')
                bsent=True
                pila.vaciar()
            elif(sent_asignacion(pila)):
                print('esto es una asignacion')
                bsent=True
                pila.vaciar()
            elif(sent_ifanidado(pila)):
                
                print('si es if anidado if sentecias')
                bsent=True
            elif(sent_do(pila)):
                print('esto es un do')
                bsent=True
                bdo=True
            elif(sent_until(pila) and bdo==True):
                
                bsent=True
            elif(sent_ifanidado(pila)):
                
                bsent=True
                pila.vaciar()
            elif(busquedafinif(pila) and ifbandanidado):
                pila.vaciar()
                bsent=True
                print('llegue if final')
        else:
            return False
        z+=1    
    print('comparo esto')
    for i in range(0,len(pila.items)):
        print(pila.items[i].token)
    pila.vaciar()
    for i in range(0,len(auxiliarmayorpila.items)):
        pila.incluir(auxiliarmayorpila.items[i])
    print('pilotamax')
    for i in range(0,len(pila.items)):
        print(pila.items[i].token)
    print('acabe este pedote')
    if(bsent):
        return True
    if(contadorif!=1):
        print('em 628')
        error()
        return False
    else:
        return False      
def sentencia(element):
    global arbol
    global pila
    global padremayor
    global textoarchsin
    global ifband
    global finalarch
    ifbandanidado=False    
    band='incompleto'
    pila.incluir(element)
    print('meto'+element.token)
    
    if(inicio() and not(ifband)):
        textoarchsin.append('MAIN:\n'+pila.items[0].lexema+'\t\t\t'+pila.items[0].linea+'\t\t\t'+pila.items[0].token+'\n')
        textoarchsin.append(pila.items[1].lexema+'\t\t\t'+pila.items[1].linea+'\t\t\t'+pila.items[1].token+'\n')
        pila.vaciar()
    elif(declaracion()):
        textoarchsin.append('\tDeclaracion:\n\tLexema\t\t\tLinea\t\t\tToken\n')
        for i in range(0,len(pila.items)):
            textoarchsin.append('\t'+pila.items[i].lexema+'\t\t\t'+pila.items[i].linea+'\t\t\t'+pila.items[i].token+'\n')
        pila.vaciar()
    
    elif(sent_if()):
        impresion(pila)
        pila.vaciar()
    elif(sent_while(pila)):
        impresion(pila)
        pila.vaciar()
    elif(sent_do(pila)):
        impresion(pila)
        pila.vaciar()
    elif(sent_until(pila)):
        impresion(pila)
        pila.vaciar()
    elif(busquedafinif(pila) and ifband and contadorif==0):
        impresion(pila)
        pila.vaciar()
    elif(sent_read(pila)):
        textoarchsin.append('\tRead:\n\tLexema\t\t\tLinea\t\t\tToken\n')
        for i in range(0,len(pila.items)):
            textoarchsin.append('\t'+pila.items[i].lexema+'\t\t\t'+pila.items[i].linea+'\t\t\t'+pila.items[i].token+'\n')
        pila.vaciar()
    elif(sent_write(pila)):
        textoarchsin.append('\tWrite:\n\tLexema\t\t\tLinea\t\t\tToken\n')
        for i in range(0,len(pila.items)):
            textoarchsin.append('\t'+pila.items[i].lexema+'\t\t\t'+pila.items[i].linea+'\t\t\t'+pila.items[i].token+'\n')
        pila.vaciar()
    elif(sent_asignacion(pila)):
        textoarchsin.append('\tAsignacion:\n\tLexema\t\t\tLinea\t\t\tToken\n')
        for i in range(0,len(pila.items)):
            textoarchsin.append('\t'+pila.items[i].lexema+'\t\t\t'+pila.items[i].linea+'\t\t\t'+pila.items[i].token+'\n')
        pila.vaciar()
    else:
        return False
def impresion(auxpila):
    contadortabs=1
    tab='\t'
    for i in range(0,len(auxpila.items)):
        if(auxpila.items[i].token=='T_IF'):
            textoarchsin.insert(i+(len(textoarchsin)),(tab*contadortabs)+'\tSENT-IF:\n'+(tab*contadortabs)+'\t\tLexema\t\t\tLinea\t\t\tToken\n')
            contadortabs+=1
        elif(auxpila.items[i].token=='T_DO'):
            textoarchsin.insert(i+(len(textoarchsin)),(tab*contadortabs)+'\tSENT-DO:\n'+(tab*contadortabs)+'\t\tLexema\t\t\tLinea\t\t\tToken\n')
            contadortabs+=1
        elif(auxpila.items[i].token=='T_WHILE'):
            textoarchsin.insert(i+(len(textoarchsin)),(tab*contadortabs)+'SENT-WHILE:\n'+(tab*contadortabs)+'\tLexema\t\t\tLinea\t\t\tToken\n')
        elif(auxpila.items[i].token=='T_READ'):
            textoarchsin.insert(i+(len(textoarchsin)),(tab*contadortabs)+'SENT-READ:\n'+(tab*contadortabs)+'\tLexema\t\t\tLinea\t\t\tToken\n')
        elif(auxpila.items[i].token=='T_ID' and auxpila.items[i+1].token=='T_ASIGN'):
            textoarchsin.insert(i+(len(textoarchsin)),(tab*contadortabs)+'SENT-ASIGN:\n'+(tab*contadortabs)+'\tLexema\t\t\tLinea\t\t\tToken\n')
        elif(auxpila.items[i].token=='T_WRITE'):
            textoarchsin.insert(i+(len(textoarchsin)),(tab*contadortabs)+'SENT-WRITE:\n'+(tab*contadortabs)+'\tLexema\t\t\tLinea\t\t\tToken\n')
        elif(auxpila.items[i].token=='T_UNTIL'):
            textoarchsin.insert(i+1+(len(textoarchsin)),(tab*contadortabs)+'UNTIL:\n'+(tab*contadortabs)+'\tLexema\t\t\tLinea\t\t\tToken\n')
        elif(auxpila.items[i].token=='T_INT' or auxpila.items[i].token=='T_FLOAT' or auxpila.items[i].token=='T_BOOL'):
            textoarchsin.insert(i+(len(textoarchsin)),(tab*contadortabs)+'SENT-Declaracion:\n'+(tab*contadortabs)+'\tLexema\t\t\tLinea\t\t\tToken\n')
        elif(auxpila.items[i].token=='T_LLAVED'):
            contadortabs-=1 
            textoarchsin.insert(i+(len(textoarchsin)),(tab*(contadortabs-1))+'\u2514>')
        elif(auxpila.items[i].token=='T_ELSE' ):        
            textoarchsin.insert(i+(len(textoarchsin)),(tab*contadortabs)+'Sent-Else\n')
            contadortabs+=1
        textoarchsin.append((tab*contadortabs)+'\t'+auxpila.items[i].lexema+'\t\t\t'+auxpila.items[i].linea+'\t\t\t'+auxpila.items[i].token+'\n')
def recorrer(texto):
    ncol=0
    bandlex=False
    bandlinea=False
    global ifband
    ifband=False
    global lexemaerror
    token=''
    lexema=''
    global contadorif
    contadorif=0
    contadordo=0
    global linea
    linea=''
    global banderror
    global finalarch
    finalarch=False
    indexif=[]
    while(ncol!=len(texto)-1):
        c=texto[ncol]
        ncol+=1
        if(c=='\t' and not(bandlex) and not(bandlinea)):
            bandlex=True
            ncol+=1
        elif(c=='\t' and bandlex and not(bandlinea)):
            bandlinea=True
            ncol+=1
        elif(c!='\t' and c!='\n'and not(bandlex) and not(bandlinea)):
            token+=c
        elif(c!='\t' and c!='\n' and bandlex and not(bandlinea)):
            lexema+=c
        elif(c!='\t' and c!='\n' and bandlex and bandlinea):
            linea+=c
        else:
            element=Elemento(token,lexema,linea)
            lineaerror=linea
            lexemaerror=lexema
            if(token=='T_IF'):
                contadorif+=1
            elif(token=='T_FI'):
                contadorif-=1
            if(token=='T_DO'):
                contadordo+=1
            elif(token=='T_UNTIL'):
                contadordo-=1
            if(banderror):
                break
            if(token!='T_COM'):
                sentencia(element)
            token=''
            lexema=''
            linea=''
            bandlex=False
            bandlinea=False       
def error():
    global linea
    global banderror
    global lexemaerror
    print('error maximo')
    erroarch=False
    try:
        f=open("errorsintactico.txt","w")
    except IOError:
        print('error en abrir arvhivo errorsintactico')
        erroarch=True
    if(not(erroarch)):
        banderror=True
        f.write("error cerca de la linea "+linea)

if(len(sys.argv)==2):
    global linea
    errorfile=False    
    try:
        f=open(sys.argv[1], "r")
        texto=f.read()
        texto=list(texto)
    except IOError:
        print ("No se encontro el archivo.")
        errorfile=True
    if(not (errorfile)):
        try:
            f2=open("sintactico.txt",'w+', encoding="utf-8") 
            textoarchsin=f2.read()
            textoarchsin=list(textoarchsin)
        except IOError:
            print('error')
        
        padremayor=Elemento('MAIN','','')
        pila=Pila()
        banderror=False
        lineaerror=0
        recorrer(texto)
        if(len(pila.items)>1):
            linea=pila.items[len(pila.items)-1].linea
            print('em 848')
            error()
        elif(len(pila.items)==0):
            try:
                f=open("errorsintactico.txt","w")
            except IOError:
                print('error en abrir arvhivo errorsintactico')
                errorfile=True
            if(not(errorfile)):
                f.write('Error en la linea del cierre programa')
                f.close()
        else:
            textoarchsin.append(pila.items[0].lexema+'\t\t\t'+pila.items[0].linea+'\t\t\t'+pila.items[0].token+'\n')
            for i in range(0,len(textoarchsin)):
                f2.write(textoarchsin[i])
            f2.close()
            try:
                f=open("errorsintactico.txt","w")
            except IOError:
                print('error en abrir arvhivo errorsintactico')
                errorfile=True
            if(not(errorfile)):
                f.write('')
                f.close()
            
else:
    print("Error en abrir archivo")