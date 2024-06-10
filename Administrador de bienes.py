import csv
import os
import ctypes
import sys

def obtenertecla():
    produccion=True
    tecla=''
    if (produccion):

        tecla=keypressed()
    else:
        tecla=input("\n\nPrograma en fase de desarrollo, recuerda Escribir 'Enter', 'Escape' o 'Espacio' segun necesites => ")
        print(tecla.upper)
    return tecla
def cls():
    if os.name == "posix":
        # Linux y macOS
       os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        # Windows
       os.system ("cls")
def maximiza():
    if os.name == "posix":
        # Linux y macOS
        os.system('printf "\033[8;50;120t"')  # Cambia los valores según el tamaño deseado
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        # Windows
        os.system('mode con: cols=120 lines=50')  # Configura el tamaño de la consola
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        SW_MAXIMIZE = 3

        hWnd = kernel32.GetConsoleWindow()
        if hWnd:
            user32.ShowWindow(hWnd, SW_MAXIMIZE)
def findx(d):
    if d=='1':
        x="Encontrado"
    else:
        x="No encontrado"
    return x
def printLinea():
    print("|------|-------------|--------------------------------|---------------------------------|-------------------------------------------|")
def lineaDatos(a,b,c,d,e):
    print("|{:^6}|{:^13}|{:^32}|{:^33}|{:^43}|".format(a,b,c,d,e))
    printLinea()
def enterescape(cadena):
    print(cadena)
    tecla=""
    while True:
        tecla=obtenertecla()
        if tecla == "Enter" or tecla == "Escape":
            break
def actualizar():
    global lista
    nuevo = open("resources\\temp.csv","w")
    for linea in lista:
        cadena=','.join(linea)
        nuevo.write(cadena+"\n")
    nuevo.close()
    if os.path.isfile("resources\\dataBackup.csv"):
        os.remove("resources\\dataBackup.csv")
    os.rename("resources\\data.csv","resources\\dataBackup.csv")
    os.rename("resources\\temp.csv","resources\\data.csv")
    lista.clear()
    file= open("resources\\data.csv",'r')
    entrada=csv.reader(file)
    lista=list(entrada) 
    file.close()
def getsep(x,comentarios,indice):
    separador='|'
    for n in range(len(lista[indice])):
        if(n==0 or n==2 or n==7 or n==10):
            for m in range(len(lista[indice][n])):
                if (n==10):
                    for k in range(len(x)):
                        separador+='-'
                    break
                elif (n==0 or n==2 or n==7):
                    separador+='-'
            separador+='|'
    for l in range(len(lista[indice][8])):
        separador+='-'
    separador+='|'
    for k in range(len(comentarios)):
        separador+='-'
    separador+='|'
    return separador
def busqueda(a):
    global lista
    c=[]
    for x in range(len(lista)):
        if a==lista[x][0]:
            return x,True
        elif a in lista[x][0]:
            c.append(lista[x])
    if len(c)!=0:
        return 1,coincidenciamultiple(c)
    return 0,False
def coincidenciamultiple(coincidencias):
    a=''
    lineas=0
    print ("Se encontraron las siguientes coincidencias\n")
    printLinea()
    for linea in coincidencias:
        if (lineas!=0 and lineas%13==0 and linea[1]=='1'):
            print("\npresione Espacio para mostrar mas o Escape para salir...")
            a=obtenertecla()
            if a=="Escape":
                break
            elif a=="Espacio":
                a=''
                x=''
                x=findx(linea[10])
                printLinea()
                if(linea[1]=='1'):
                    lineaDatos(linea[0],x, linea[2], linea[8],linea[9])
                    #printLinea()
                    lineas+=1
        else:
            x=''
            x=findx(linea[10])
            if(linea[1]=='1'):
                lineaDatos(linea[0],x, linea[2], linea[8],linea[9])
                #printLinea()
                lineas+=1
    if a!="Escape":
        a=enterescape("\npresione enter o escape para salir...")
        a=''
    return False
def modificar():
    global lista
    cls()
    print ("\nBusqueda de Articulos\n")
    articulo=input("\n\tIngrese el articulo: ")
    if len(articulo)>0:
        indice,encontrado=busqueda(articulo)
        if encontrado:
            while True:
                cls()
                x=''
                if lista[indice][10]=='1':
                    x="Encontrado"
                else:
                    x="No encontrado"
                separador=getsep(x,lista[indice][9],indice)
                print ("\nBusqueda de Articulos\n\n")
                print ("\tEncargado del articulo: "+lista[indice][11]+"\n")
                print("\t"+separador)
                print("\t|{}|{}|{}|{}|{}|{}|".format( lista[indice][0], lista[indice][2], lista[indice][7],x,lista[indice][8],lista[indice][9]))
                print("\t"+separador)
                print ("\n\t\t1. Marcar como encontrado")
                print ("\t\t2. Marcar como no encontrado")
                print ("\t\t3. Agregar observacion")
                print ("\t\t4. Eliminar observacion")
                print ("\t\t5. Cambio de lugar fisico")
                print ("\t\t6. Marcar como 'EN MANTENIMIENTO'")
                print ("\t\t7. Marcar como 'REPARADO'")
                print ("\t\t8. Marcar como 'BAJA'")
                print ("\t\t9. Marcar como 'SE QUEDA EN DIDEPA'")
                print ("\t\t0. Desmarcar 'SE QUEDA EN DIDEPA'")
                print ("\t\tEscape => Regresar")
                opcion=obtenertecla()
                if opcion=="Escape":
                    break
                elif opcion.isdigit():
                    opcion=int(opcion)
                    if opcion==1:
                        lista[indice][10]='1'
                        actualizar()
                    elif opcion==2:
                        lista[indice][10]='0'
                        actualizar()
                    elif opcion==3:
                        if lista[indice][9]=='S/O':
                            comentario=input("\n\t\t\tEscriba la observacion (Nota: use ';' en lugar de ','): ")
                            if len(comentario)>0:
                                lista[indice][9]=comentario.upper()
                                actualizar()
                        else:
                            comentario=input("\n\t\t\tEscriba la observacion (Nota: use ';' en lugar de ','): ")
                            if len(comentario)>0:
                                lista[indice][9]+='; '
                                lista[indice][9]+=comentario.upper()
                                actualizar()
                    elif opcion==4:
                        lista[indice][9]='S/O'
                        actualizar()
                    elif opcion==5:
                        lf(2,indice)
                        actualizar()
                    elif opcion==6:
                        if lista[indice][9]=='S/O':
                            lista[indice][9]="EN MANTENIMIENTO"
                            actualizar()
                        else:
                            lista[indice][9]+='; '
                            lista[indice][9]+="EN MANTENIMIENTO"
                            actualizar()
                    elif opcion==7:
                        if lista[indice][9]=='S/O':
                            lista[indice][9]="REPARADO"
                            actualizar()
                        else:
                            lista[indice][9]+='; '
                            lista[indice][9]+="REPARADO"
                            actualizar()
                    elif opcion==8:
                        if 'BAJA' in lista[indice][9]:
                            pass
                        elif lista[indice][9]=='S/O':
                            lista[indice][9]="BAJA"
                            actualizar()
                        else:
                            lista[indice][9]+='; '
                            lista[indice][9]+="BAJA"
                            actualizar()
                    elif opcion==9:
                        if 'SE QUEDA EN DIDEPA' in lista[indice][9]:
                            pass
                        elif lista[indice][9]=='S/O':
                            lista[indice][9]="SE QUEDA EN DIDEPA"
                            actualizar()
                        else:
                            lista[indice][9]+='; '
                            lista[indice][9]+="SE QUEDA EN DIDEPA"
                            actualizar()
                    elif opcion==0:
                        if 'SE QUEDA EN DIDEPA' in lista[indice][9]:
                            if '; SE QUEDA EN DIDEPA' in lista[indice][9]:
                                lista[indice][9]=lista[indice][9].replace('; SE QUEDA EN DIDEPA','')
                            else:
                                lista[indice][9]=lista[indice][9].replace('SE QUEDA EN DIDEPA','S/O')
                        actualizar()
        elif indice==0:
            cls()
            print ("Busqueda de Articulos\n")
            print("No se encontro el articulo")
            print("\npresione una tecla para salir...")
            a=obtenertecla()
    cls()
def lf(q, indice):
    global lista
    cls()
    if q==1:
        while True:
            cls()
            print ("Mostrar listado\n")
            print ("\tSeleccione el area a mostrar")
            print ("\t1. Sala 1")
            print ("\t2. Sala 2")
            print ("\t3. Sala 2: Rack")
            print ("\t4. Sala 3")
            print ("\t5. Sala Digital")
            print ("\t6. Bodega Sala Digital")
            print ("\t7. Unidad de Informatica")
            print ("\t8. Unidad de Informatica, Biblioteca")            
            print ("\t9. Sala de computo")
            print ("\tA. Bodega Sala de computo")
            print ("\tB. Area biblioteca(DIDEPA)")
            print ("\tC. Planeacion")
            print ("\tD. Auditorio")
            print ("\tE. Direccion")
            print ("\tF. Sala de espera")
            print ("\tG. Rack Colon")
            print ("\tEscape => Cancelar")
            area=obtenertecla()
            if area=="Escape":
                break
            if area.isdigit():
                area=int(area)
                area=area-1
                area=str(area)
            else:
                letras=["a","b","c","d","e","f","g"]
                for x in range(len(letras)):
                    if area==letras[x] or area==letras[x].lower():
                        area=x+9
                        area=str(area)
                        break
            if area.isdigit() and int(area)<17 and int(area)>=0:
                area=int(area)
                cls()
                a=''
                lineas=0
                printLinea()
                for linea in lista:
                    if lineas!=0 and lineas%13==0 and linea[8]==areas[area]:
                        print("\npresione una tecla para mostrar mas o Escape para salir...")
                        a=obtenertecla()
                        if a=="Escape":
                            break
                        a=''
                        x=''
                        x=findx(linea[10])
                        printLinea()
                        if linea[8]==areas[area]:
                            if (linea[9]=="S/O"):
                                comentarios='---'
                            else:
                                comentarios=linea[9]
                            lineaDatos(linea[0],x, linea[2], linea[8],comentarios)
                            #printLinea()
                            lineas+=1
                    else:
                        x=''
                        x=findx(linea[10])
                        if linea[8]==areas[area]:
                            if (linea[9]=="S/O"):
                                comentarios='---'
                            else:
                                comentarios=linea[9]
                            lineaDatos(linea[0],x, linea[2], linea[8],comentarios)
                            #printLinea()
                            lineas+=1
                if a!="Escape":
                    a=enterescape("\npresione enter o escape para salir...")
                    a=''
                    #break
    elif q==2:
        print ("Seleccione el nuevo lugar\n")
        print ("\t1. Sala 1")
        print ("\t2. Sala 2")
        print ("\t3. Sala 2: Rack")
        print ("\t4. Sala 3")
        print ("\t5. Sala Digital")
        print ("\t6. Bodega Sala Digital")
        print ("\t7. Unidad de Informatica")
        print ("\t8. Unidad de Informatica, Biblioteca")            
        print ("\t9. Sala de computo")
        print ("\tA. Bodega Sala de computo")
        print ("\tB. Area biblioteca(DIDEPA)")
        print ("\tC. Planeacion")
        print ("\tD. Auditorio")
        print ("\tE. Direccion")
        print ("\tF. Sala de espera")
        print ("\tG. Rack Colon")
        print ("\tEscape => Cancelar")
        while True:
            area=obtenertecla()
            if area=="Escape":
                break
            if area.isdigit():
                area=int(area)
                area=area-1
                area=str(area)
            else:
                letras=["a","b","c","d","e","f","g"]
                for x in range(len(letras)):
                    if area==letras[x] or area==letras[x].lower():
                        area=x+9
                        area=str(area)
                        break
            
            if area.isdigit() and int(area)<17 and int(area)>=0:
                area=int(area)
                print("\n\t\tLa nueva area sera ",areas[area])
                print("\t\tDesea continuar?")
                print ("\t\tEnter => Aceptar")
                print ("\t\tEscape => Cancelar\n")
                while True:
                    confirm=obtenertecla()
                    if confirm=="Enter":
                        break
                    elif confirm=="Escape":
                        break
                if confirm=="Escape":
                    break
                lista[indice][8]=areas[area]
                if lista[indice][9]=='S/O':
                    lista[indice][9]="SE MOVIO A "
                    lista[indice][9]+= areas[area]
                else:
                    lista[indice][9]+='; '
                    lista[indice][9]+="SE MOVIO A "
                    lista[indice][9]+= areas[area]
                actualizar()
                break
    elif q==3:
        cls()
        if not os.path.isfile("resources\\lista.txt") or os.stat('resources\\lista.txt').st_size == 0:
            print("no se encuentra el archivo llamado lista.txt o esta vacio\ncree un archivo llamado lista.txt unicamente con los numeros de bienes como el sig. ej.\n----------\n44123\n2344\n35634\n----------\nPresione cualquier tecla para cotinuar")
            x=obtenertecla()
        else:
            array=[]
            with open("resources\\lista.txt","r") as archivo:
                for linea in archivo:
                    array.append(linea.strip())
            while True:
                while True:
                    cls()
                    print ("Lista cargada\n\n")
                    print ("Cambio de lugar fisico por lotes\n")
                    print ("\tSeleccione el nuevo lugar\n")
                    print ("\t1. Sala 1")
                    print ("\t2. Sala 2")
                    print ("\t3. Sala 2: Rack")
                    print ("\t4. Sala 3")
                    print ("\t5. Sala Digital")
                    print ("\t6. Bodega Sala Digital")
                    print ("\t7. Unidad de Informatica")
                    print ("\t8. Unidad de Informatica, Biblioteca")            
                    print ("\t9. Sala de computo")
                    print ("\tA. Bodega Sala de computo")
                    print ("\tB. Area biblioteca(DIDEPA)")
                    print ("\tC. Planeacion")
                    print ("\tD. Auditorio")
                    print ("\tE. Direccion")
                    print ("\tF. Sala de espera")
                    print ("\tG. Rack Colon")
                    print ("\tEscape => Cancelar")
                    area=obtenertecla()
                    if area=="Escape":
                        break
                    if area.isdigit():
                        area=int(area)
                        area=area-1
                        area=str(area)
                    else:
                        letras=["a","b","c","d","e","f","g"]
                        for x in range(len(letras)):
                            if area==letras[x] or area==letras[x].lower():
                                area=x+9
                                area=str(area)
                                break
                    if area.isdigit() and int(area)<17 and int(area)>=0:
                        area=int(area)
                        print("\n\n\tATENCION!!\n\n\tLa nueva area para todos los elementos de la lista cargada sera ",areas[area])
                        print("\t\tDesea continuar?")
                        print ("\t\tEnter => Si")
                        print ("\t\tEscape => No\n")
                        while True:
                            confirm=obtenertecla()
                            if confirm=='1' or confirm=="Enter":
                                break
                            elif confirm=='2' or confirm=="Escape":
                                break
                        if confirm=='1' or confirm=="Enter":
                            for item in lista:
                                if item[0] in array:
                                    item[8]=areas[area]
                                    array[array.index(item[0])]='-'
                                    if item[9]=='S/O':
                                        item[9]="SE MOVIO A "
                                        item[9]+= areas[area]
                                    else:
                                        item[9]+='; '
                                        item[9]+="SE MOVIO A "
                                        item[9]+= areas[area]
                            area='Escape'
                            for item2 in array:
                                if item2!='-':
                                    print("No se encontro el articulo: ", item2)
                            actualizar()
                            print("\nSe han realizado los cambios, presione una tecla para continuar\n")
                            x=obtenertecla()
                            break
                if area=="Escape" or confirm=="Escape":
                    break
    cls()
def mostrar():
    global areas
    global lista
    while True:
        cls()
        print ("\nMostrar listado\n")
        print ("\t1. Completo\n")
        print ("\t2. Por area\n")
        print ("\t3. Articulos con observaciones\n")
        print ("\t4. Articulos no encontrados\n")
        print ("\t5. Articulos en mantenimiento\n")
        print ("\t6. Articulos para baja\n")
        print ("\tEscape => Regresar\n")
        opcion=obtenertecla()
        cls()
        if opcion=="Escape":
            break
        elif opcion.isdigit():
            opcion=int(opcion)
            lineas=0
            a=''
            if opcion==1:
                a=''
                printLinea()
                for linea in lista:
                    if lineas!=0 and lineas%13==0 and linea[1]=='1':
                        x=''
                        x=findx(linea[10])
                        print("\npresione Espacio para mostrar mas o Escape para salir...")
                        a=obtenertecla()
                        if a=="Escape":
                            break
                        elif a=="Espacio":
                            a=''
                            printLinea()
                            if(linea[1]=='1'):
                                if (linea[9]=="S/O"):
                                    comentarios='-------------------------------------------'
                                else:
                                    comentarios=linea[9]
                                lineaDatos(linea[0],x, linea[2], linea[8],comentarios)
                                #printLinea()
                                lineas+=1
                    else:
                        x=''
                        x=findx(linea[10])
                        if(linea[1]=='1'):
                            if (linea[9]=="S/O"):
                                comentarios='-------------------------------------------'
                            else:
                                comentarios=linea[9]
                            lineaDatos(linea[0],x, linea[2], linea[8],comentarios)
                            #printLinea()
                            lineas+=1
                if a!="Escape":
                    a=enterescape("\npresione enter o escape para salir...")
                    a=''
            elif opcion==2:
                lf(1,0)
            elif opcion==3:
                a=''
                printLinea()
                for linea in lista:
                    if (lineas!=0 and lineas%13==0 and linea[1]=='1' and linea[9]!='S/O'):
                        print("\npresione Espacio para mostrar mas o Escape para salir...")
                        a=obtenertecla()
                        if a=="Escape":
                            break
                        elif a=="Espacio":
                            a=''
                            x=''
                            x=findx(linea[10])
                            printLinea()
                            if(linea[1]=='1' and linea[9]!='S/O'):
                                lineaDatos(linea[0],x, linea[2], linea[8],linea[9])
                                #printLinea()
                                lineas+=1
                    else:
                        x=''
                        x=findx(linea[10])
                        if(linea[1]=='1' and linea[9]!='S/O'):
                            lineaDatos(linea[0],x, linea[2], linea[8],linea[9])
                            #printLinea()
                            lineas+=1
                if a!="Escape":
                    a=enterescape("\npresione enter o escape para salir...")
                    a=''
            elif opcion==4:
                a=''
                printLinea()
                for linea in lista:
                    if lineas!=0 and lineas%13==0 and linea[10]=='0':
                        print("\npresione Espacio para mostrar mas o Escape para salir...")
                        a=obtenertecla()
                        if a=="Escape":
                            break
                        elif a=="Espacio":
                            a=''
                            x=''
                            x=findx(linea[10])
                            printLinea()
                            if(linea[10]=='0'):
                                if (linea[9]=="S/O"):
                                    comentarios='-------------------------------------------'
                                else:
                                    comentarios=linea[9]
                                lineaDatos(linea[0],x, linea[2], linea[8],comentarios)
                                #printLinea()
                                lineas+=1
                    else:
                        x=''
                        x=findx(linea[10])
                        if(linea[10]=='0'):
                            if (linea[9]=="S/O"):
                                comentarios='-------------------------------------------'
                            else:
                                comentarios=linea[9]
                            lineaDatos(linea[0],x, linea[2], linea[8],comentarios)
                            #printLinea()
                            lineas+=1
                if a!="Escape":
                    a=input("\npresione enter para regresar...")
                    a=''
            elif opcion==5:
                a=''
                printLinea()
                for linea in lista:
                    mant=linea[9].count("MANTENIMIENTO")
                    rep=linea[9].count("REPARADO")
                    activo=0
                    activo=mant-rep
                    if (lineas!=0 and lineas%13==0 and linea[1]=='1' and activo>0 and "BAJA" not in linea[9]):
                        print("\npresione Espacio para mostrar mas o Escape para salir...")
                        a=obtenertecla()
                        if a=="Escape":
                            break
                        elif a=="Espacio":
                            a=''
                            x=''
                            x=findx(linea[10])
                            printLinea()
                            if(linea[1]=='1' and activo>0 and "BAJA" not in linea[9]):
                                lineaDatos(linea[0],x, linea[2], linea[8],linea[9])
                                #printLinea()
                                lineas+=1
                    else:
                        x=''
                        x=findx(linea[10])
                        if(linea[1]=='1' and activo>0 and "BAJA" not in linea[9]):
                            lineaDatos(linea[0],x, linea[2], linea[8],linea[9])
                            #printLinea()
                            lineas+=1
                if a!="Escape":
                    a=enterescape("\npresione enter o escape para salir...")
                    a=''
            elif opcion==6:
                a=''
                printLinea()
                for linea in lista:
                    if (lineas!=0 and lineas%13==0 and linea[1]=='1' and "BAJA" in linea[9]):
                        print("\npresione Espacio para mostrar mas o Escape para salir...")
                        a=obtenertecla()
                        if a=="Escape":
                            break
                        elif a=="Espacio":
                            a=''
                            x=''
                            x=findx(linea[10])
                            printLinea()
                            if(linea[1]=='1' and "BAJA" in linea[9]):
                                lineaDatos(linea[0],x, linea[2], linea[8],linea[9])
                                #printLinea()
                                lineas+=1
                    else:
                        x=''
                        x=findx(linea[10])
                        if(linea[1]=='1' and "BAJA" in linea[9]):
                            lineaDatos(linea[0],x, linea[2], linea[8],linea[9])
                            #printLinea()
                            lineas+=1
                if a!="Escape":
                    a=enterescape("\npresione enter o escape para salir...")
                    a=''
    cls()
def sequedamasivo(opcion):
    cls()
    if not os.path.isfile("resources\\lista.txt") or os.stat('resources\\lista.txt').st_size == 0:
        print("\n\n\tno se encuentra el archivo llamado lista.txt o esta vacio\ncree un archivo llamado lista.txt unicamente con los numeros de bienes como el sig. ej.\n----------\n44123\n2344\n35634\n----------\nPresione cualquier tecla para cotinuar")
        x=obtenertecla()
    else:
        array=[]
        with open("resources\\lista.txt","r") as archivo:
            for linea in archivo:
                array.append(linea.strip())
        if opcion==1:
            print("marcado por lotes para 'quedar en didepa'\n")
            while True:
                print("\n\nATENCION!!\n\nSe realizara un cambio masivo en los articulos de la lista cargada")
                print("Desea continuar?")
                print ("Enter => Si")
                print ("Escape => No\n")
                while True:
                    confirm=obtenertecla()
                    if confirm=="Enter":
                        break
                    elif confirm=="Escape":
                        break
                if confirm=="Enter":
                    for item in lista:
                        if item[0] in array:
                            array[array.index(item[0])]='-'
                            if 'SE QUEDA EN DIDEPA' in item[9]:
                                pass
                            elif item[9]=='S/O':
                                item[9]="SE QUEDA EN DIDEPA"
                            else:
                                item[9]+='; '
                                item[9]+="SE QUEDA EN DIDEPA"
                    break
                else:
                    break
        elif opcion==2:
            print("desmarcado por lotes para 'quedar en didepa'\n")
            while True:
                print("\n\nATENCION!!\n\nSe realizara un cambio masivo en los articulos de la lista cargada")
                print("Desea continuar?")
                print ("Enter => Si")
                print ("Escape => No\n")
                while True:
                    confirm=obtenertecla()
                    if confirm=="Enter":
                        break
                    elif confirm=="Escape":
                        break
                if confirm=="Enter":
                    for item in lista:
                        if item[0] in array:
                            array[array.index(item[0])]='-'
                            if 'SE QUEDA EN DIDEPA' in item[9]:
                                if '; SE QUEDA EN DIDEPA' in item[9]:
                                    item[9]=item[9].replace('; SE QUEDA EN DIDEPA','')
                                else:
                                    item[9]=item[9].replace('SE QUEDA EN DIDEPA','S/O')
                    break
                else:
                    break
        if confirm=="Enter":
            for item2 in array:
                if item2!='-':
                    print("No se encontro el articulo: ", item2)
            actualizar()
            print("\nSe han realizado los cambios, presione una tecla para continuar\n")
            x=obtenertecla()
def inicializar(o):
    if o==1:
        print("\n\tEsta accion definira todos los articulos como 'No encontrados', desea continuar?\n")
        print ("\t\tEnter => Aceptar\n")
        print ("\t\tEscape => Cancelar\n")
        while True:
            a=obtenertecla()
            if a=="Enter":
                for linea in lista:
                    if linea[1]=='1':
                        linea[10]='0'
                actualizar()
                cls()
                print("\n\n\tArticulos inicializados")
                a=input("\n\tPresione enter para continuar...")
                break
            elif a=="Escape":
                break
    else:
        print("\n\tEsta accion borrara las observaciones de todos los articulos exceptuando bajas y articulos en mantenimiento, desea continuar?\n")
        print ("\t\tEnter => Aceptar\n")
        print ("\t\tEscape => Cancelar\n")
        while True:
            a=obtenertecla()
            if a=="Enter":
                for linea in lista:
                    if linea[1]=='1':
                        if 'BAJA' in linea[9]:
                            linea[9]='BAJA'
                        elif 'MANTENIMIENTO' in linea[9]:
                            mant=linea[9].count("MANTENIMIENTO")
                            rep=linea[9].count("REPARADO")
                            activo=0
                            activo=mant-rep
                            if activo>0:
                                linea[9]='EN MANTENIMIENTO'
                        else:
                            linea[9]='S/O'
                actualizar()
                cls()
                print("\n\n\tObservaciones borradas")
                a=input("\n\tPresione enter para continuar...")
                break
            elif a=="Escape":
                break
    cls()
def export(i):
    global lista
    try:
        os.mkdir('Export')
    except OSError:
        pass
    else:
        pass
    if i=='1':
        nuevo = open("Export\\Bienes.csv","w")
        for linea in lista:
            nuevo.write(linea[0]+","+linea[2]+","+linea[8]+","+linea[9]+"\n")
        nuevo.close()
        print("\nLista exportada")
        a=input("\nPresione enter para continuar...")
    else:
        nuevo = open("Export\\BienesConObs.csv","w")
        for linea in lista:
            if linea[9]!='S/O':
                nuevo.write(linea[0]+","+linea[2]+","+linea[8]+","+linea[9]+"\n")
        nuevo.close()
        print("\nLista exportada")
        a=input("\nPresione enter para continuar...")
def restaura():
    global lista
    if os.path.isfile("resources\\dataBackup.csv"):
        if os.path.isfile("resources\\data.csv"):
            os.remove("resources\\data.csv")
        os.rename("resources\\dataBackup.csv","resources\\data.csv")
    lista.clear()
    file= open("resources\\data.csv",'r')
    entrada=csv.reader(file)
    lista=list(entrada) 
    file.close()

#programa principal
maximiza()
if sys.platform == 'win32':
    import msvcrt
    def keypressed():
        key = msvcrt.getch()
        if key == b"\x1b": #ESC
            return "Escape"
        elif key ==b"\r":
            return "Enter"
        elif key ==b" ":
            return "Espacio"
        else:
            return key.decode("ANSI")

elif sys.platform == 'linux':
    import termios
    TERMIOS = termios
    def keypressed():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
        new[6][TERMIOS.VMIN] = 1
        new[6][TERMIOS.VTIME] = 0
        termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
        key = None
        try:
            key = os.read(fd, 4)
            if key == b'\x1b':
                key = "Escape"
            elif key ==b'\r':
                key= "Enter"
            elif key ==b' ':
                key= "Espacio"
            else:
                key = key.decode()
        finally:
            termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
        return key
try:
    os.mkdir('resources')
except OSError:
    pass
else:
    pass



if os.path.isfile("resources\\data.csv"):
    lista=[]
    file= open("resources\\data.csv",'r')
    entrada=csv.reader(file)
    lista=list(entrada)
    file.close()
    kygen=[10, 10, 80, 114, 111, 103, 114, 97, 109, 97, 32, 99, 114, 101, 97, 100, 111, 32, 112, 111, 114, 32, 86, 105, 99, 116, 111, 114, 32, 77, 97, 110, 117, 101, 108, 32, 74, 105, 109, 101, 110, 101, 122, 32, 82, 111, 115, 97, 115, 46, 32, 97, 108, 105, 97, 115, 32, 74, 105, 114, 111]
    areas=["SALA 1","SALA 2","SALA 2 RACK","SALA 3","SALA DIGITAL","BODEGA SALA DIGITAL","UNIDAD DE INFORMATICA","UNIDAD DE INFORMATICA; BIBLIOTECA","SALA DE COMPUTO","BODEGA SALA DE COMPUTO","AREA DE BIBLIOTECA (DIDEPA)","PLANEACION","AUDITORIO","DIRECCION","SALA DE ESPERA","RACK COLON"]
    areasId=["11","9","2","10","12","44","6","98","14","38","30","33","19","16","48","99"]
    while True:
        cls()
        print ("\nAuxiliar para la busqueda de bienes patrimoniales.\n")
        print ("\tQ. Buscar articulos\n")
        print ("\tW. Mostrar listado\n")
        print ("\tE. Exportar listado\n")
        print ("\tR. Restaurar\n")
        print ("\tT. Inicializar articulos (marca todos los articulos como 'No encontrado')\n")
        print ("\tY. Borrar todas las observaciones\n")
        print ("\tU. Acciones por lotes\n")
        print ("\tEscape => Salir")
        opcion=obtenertecla()
        if opcion=='Escape':
            break
        elif opcion.lower()=='q':
            modificar()
        elif opcion.lower()=='w':
            mostrar()
        elif opcion.lower()=='e':
            print ("\n\t\t1. Exportar todo")
            print ("\t\t2. Solo articulos con observaciones")
            while True:
                opcion=obtenertecla()
                if opcion=='1' or opcion=='2':
                    export(opcion)
                    break
                else:
                    break
        elif opcion.lower()=='u':
            while True:
                cls()
                print ("\nAcciones por lotes\n")
                print ("\t(Esta opcion toma los articulos insertados en forma de lista en un archivo llamado 'lista.txt' y aplica los cambos solicitados)\n")
                print ("\ncree un archivo llamado lista.txt unicamente con los numeros de bienes como el sig. ej.\n----------\n44123\n2344\n35634\n----------")
                print ("\t1. Cambio de lugar fisico por lotes\n")
                print ("\t2. marcar como 'se queda en didepa' por lotes\n")
                print ("\t3. desmarcar 'se queda en didepa' por lotes\n")
                print ("\tEscape => Regresar")
                opcion=obtenertecla()
                if opcion=='1':
                    lf(3,0)
                    break
                elif opcion=='2':
                    sequedamasivo(1)
                    break
                elif opcion=='3':
                    sequedamasivo(2)
                    break
                elif opcion=='Escape':
                    break
        elif opcion.lower()=='t':
            inicializar(1)
        elif opcion.lower()=='y':
            inicializar(2)
        elif opcion.lower()=='j':
            cls()
            string = ""
            for num in kygen:
                string = string + chr(num)
            print(str("\t\t"+string))
            opcion=obtenertecla()
        elif opcion.lower()=='r':
            restaura()
            
else:
    try:
        os.mkdir('resources')
    except OSError:
        pass
    else:
        pass
    print("\n\n\tNo se encuentra el archivo de datos")
    opcion=obtenertecla()
