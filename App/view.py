"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from prettytable import PrettyTable
assert cf
import datetime
from datetime import date
import time


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def print5Avistamientos(avistamientos):
    """
    Imprime la información del autor seleccionado
    """
    if avistamientos == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif avistamientos:
        print("\n")
        print('5 primeras obras cargadas')
        primeros5 = lt.subList(avistamientos,1,5)
        x = PrettyTable(["Fecha", "Ciudad", 'Estado','Pais','Forma','Duracion (Segundos)','Duracion (Horas)','Comentarios','Fecha (Posteo)','Latitud','Longitud'])
        x._max_width = {"Fecha" : 10, "Ciudad" : 10,"Estado" : 10, "Pais" : 10,"Forma" : 10,"Duracion (Segundos)" : 10,"Duracion (Horas)" : 10,"Comentarios" : 10,"Fecha (Posteo)" : 10,"Latitud" : 10,"Longitud" : 10}
        for primeros in lt.iterator(primeros5):
            x.add_row([primeros['datetime'], primeros['city'], primeros['state'],primeros['country'],primeros['shape'],primeros['duration (seconds)'],primeros['duration (hours/min)'],primeros['comments']+'\n',primeros['date posted'],primeros['latitude'],primeros['longitude']])
        print(x)
        print("\n")
        print('5 ultimas obras cargadas')
        ultimos5 = lt.subList(avistamientos,(int(lt.size(avistamientos))-4),5)
        y = PrettyTable(["Fecha", "Ciudad", 'Estado','Pais','Forma','Duracion (Segundos)','Duracion (Horas)','Comentarios','Fecha (Posteo)','Latitud','Longitud'])
        y._max_width = {"Fecha" : 10, "Ciudad" : 10,"Estado" : 10, "Pais" : 10,"Forma" : 10,"Duracion (Segundos)" : 10,"Duracion (Horas)" : 10,"Comentarios" : 10,"Fecha (Posteo)" : 10,"Latitud" : 10,"Longitud" : 10}
        for ultimos in lt.iterator(ultimos5):
            y.add_row([ultimos['datetime'], ultimos['city'], ultimos['state'],ultimos['country'],ultimos['shape'],ultimos['duration (seconds)'],ultimos['duration (hours/min)'],ultimos['comments']+'\n',ultimos['date posted'],ultimos['latitude'],ultimos['longitude']])
        print(y)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_avistamientos(author):
    """
    Imprime la información del autor seleccionado
    """
    if author:
        print("\n")
        x = PrettyTable(["Fecha", "Ciudad", 'Pais','Duracion (Segundos)','Forma'])
        x._max_width = {"Fecha" : 20, "Ciudad" : 20,"Pais" : 20, "Duracion (Segundos)" : 20,"Forma" : 20}
        for artistas in lt.iterator(author):
            x.add_row([artistas['datetime']+'\n', artistas['city'],artistas['country'],artistas['duration (seconds)'],artistas['shape']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_ciudadesorden(author):
    """
    Imprime la información del autor seleccionado
    """
    if author:
        print("\n")
        x = PrettyTable(["Ciudad", "Cantidad"])
        x._max_width = {"Ciudad" : 20, "Cantidad" : 20}
        for artistas in lt.iterator(author):
            x.add_row([artistas['NombreCiudad']+'\n', lt.size(artistas['ListaAvistamientos'])])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_duracionorden(author):
    """
    Imprime la información del autor seleccionado
    """
    if author:
        print("\n")
        x = PrettyTable(["Duracion", "Cantidad"])
        x._max_width = {"Duracion" : 20, "Cantidad" : 20}
        for artistas in lt.iterator(author):
            x.add_row([str(artistas['duracion'])+'\n', artistas['cantidad']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_FechaAntiguasyCantidad(author):
    """
    Imprime la información del autor seleccionado
    """
    if author:
        print("\n")
        x = PrettyTable(["Fecha", "Cantidad"])
        x._max_width = {"Fecha" : 20, "Cantidad" : 20}
        for artistas in lt.iterator(author):
            x.add_row([str(artistas['Fecha'])+'\n', artistas['cantidad']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_avistamientosconlatitudylongitud(author):
    """
    Imprime la información del autor seleccionado
    """
    if author:
        print("\n")
        x = PrettyTable(["Fecha", "Ciudad", 'Pais','Duracion (Segundos)','Forma','Latitud','Longitud'])
        x._max_width = {"Fecha" : 20, "Ciudad" : 20,"Pais" : 20, "Duracion (Segundos)" : 20,"Forma" : 20,"Latitud" : 20,"Longitud" : 20}
        for artistas in lt.iterator(author):
            x.add_row([artistas['datetime']+'\n', artistas['city'],artistas['country'],artistas['duration (seconds)'],artistas['shape'],str(round(float(artistas['latitude']),2)),str(round(float(artistas['longitude']),2))])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')


def printMenu():
    print("Bienvenido")
    print("1- Crear el catalogo")
    print("2- Cargar información en el catálogo")
    print("3- Avistamientos por ciudad y rango de duracion")
    print("4- Contar los avistamientos por duracion")
    print("5- Contar los avistamientos por fecha")
    print("6- Contar los avistamientos por area")
    print("0- Salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando....\n")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        controller.loadData(cont)
        ciudades_orden = controller.sortCantidades(om.valueSet(cont['IndiceCiudad']))
        print('Avistamientos cargados: ' + str(lt.size(cont['avistamientos'])))
        print5Avistamientos(cont['avistamientos'])

    elif int(inputs[0]) == 3:
        ciudad = input("Escriba la ciudad que quiere consultar: ")
        start_time = time.process_time()
        respuesta = controller.primer_req(cont,ciudad,ciudades_orden)
        print(('*'*90) + ('\n') +"El total de ciudades donde se reportaron avistamientos es de: "+ ' ' + str(respuesta[0])+ '\n')
        print(('*'*90) + ('\n') +"Este es el Top 5 de ciudades con mas avistamientos: : "+ '\n')
        print_ciudadesorden(respuesta[4])
        print(('*'*90) + ('\n') +"El total de avistamientos reportados en la ciudad consultada es de: : "+ ' ' + str(respuesta[1])+ '\n')
        print(('*'*90) + ('\n') +"Estos son los primeros 3 avistamientos de la ciudad: : "+ '\n')
        print_avistamientos(respuesta[2])
        print(('*'*90) + ('\n') +"Estos son los ultimos 3 avistamientos de la ciudad: : "+ '\n')
        print_avistamientos(respuesta[3])
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)

    elif int(inputs[0]) == 4:
        duracion_inicial = float(input("Escriba la duracion inicial que desea buscar: "))
        duracion_final = float(input("Escriba la duracion final que desea buscar: "))
        start_time = time.process_time()
        respuesta = controller.segundo_req(cont,duracion_inicial,duracion_final)
        print(('*'*90) + ('\n') +"El total de duraciones diferentes es de: "+ ' ' + str(lt.size(om.keySet(cont['IndiceDuracionseg'])))+ '\n')
        print(('*'*90) + ('\n') +"Estas son el Top 5 de duracion mas largas: "+ '\n')
        print_duracionorden(respuesta[4])
        print(('*'*90) + ('\n') +"El total de avistamientos en el rango es de: "+ ' ' + str(respuesta[0])+ '\n')
        print(('*'*90) + ('\n') +"Estos son los primeros 3 avistamientos en el rango: : "+ '\n')
        print_avistamientos(respuesta[2])
        print(('*'*90) + ('\n') +"Estos son los ultimos 3 avistamientos en el rango: : "+ '\n')
        print_avistamientos(respuesta[3])
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)

    elif int(inputs[0]) == 5:
        fecha_inicial = (input("Escriba la fecha inicial que desea buscar: "))
        fecha_final = (input("Escriba la fecha final que desea buscar: "))
        fecha_inicial = datetime.datetime.strptime(fecha_inicial, '%Y-%m-%d').date()
        fecha_final = datetime.datetime.strptime(fecha_final, '%Y-%m-%d').date()
        start_time = time.process_time()
        respuesta = controller.cuarto_req(cont,fecha_inicial,fecha_final)
        print(('*'*90) + ('\n') +"El total de diferentes fechas es de: "+ ' ' + str(respuesta[0])+ '\n')
        print(('*'*90) + ('\n') +"Estas son el Top 5 de fechas mas antiguas: "+ '\n')
        print_FechaAntiguasyCantidad(respuesta[1])
        print(('*'*90) + ('\n') +"El total de avistamientos en el rango es de: "+ ' ' + str(respuesta[2])+ '\n')
        print(('*'*90) + ('\n') +"Estos son los primeros 3 avistamientos en el rango: : "+ '\n')
        print_avistamientos(respuesta[3])
        print(('*'*90) + ('\n') +"Estos son los ultimos 3 avistamientos en el rango: : "+ '\n')
        print_avistamientos(respuesta[4])
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)

    elif int(inputs[0]) == 6:
        longitud_inicial = float(input("Escriba la longitud inicial que desea buscar: "))
        longitud_final = float(input("Escriba la longitud final que desea buscar: "))
        latitud_inicial = float(input("Escriba la latitud inicial que desea buscar: "))
        latitud_final = float(input("Escriba la latitud final que desea buscar: "))
        start_time = time.process_time()
        respuesta = controller.quinto_req(cont,longitud_inicial,longitud_final,latitud_inicial,latitud_final)
        print(('*'*90) + ('\n') +"El total de avistamientos en el rango es de: "+ ' ' + str(respuesta[0])+ '\n')
        print(('*'*90) + ('\n') +"Estos son los primeros 5 avistamientos en el rango: : "+ '\n')
        print_avistamientosconlatitudylongitud(respuesta[1])
        print(('*'*90) + ('\n') +"Estos son los ultimos 5 avistamientos en el rango: : "+ '\n')
        print_avistamientosconlatitudylongitud(respuesta[2])
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)

    else:
        sys.exit(0)
sys.exit(0)
