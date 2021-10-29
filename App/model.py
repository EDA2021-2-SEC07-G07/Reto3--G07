"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
import datetime
from datetime import date

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalogo():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    catalog = {'avistamientos': None}

    catalog['avistamientos'] = lt.newList('SINGLE_LINKED', compareAvistamientos)
    catalog['IndiceCiudad'] = om.newMap(omaptype='BST',
                                      comparefunction=compareCiudad)
    catalog['IndiceDuracionseg'] = om.newMap(omaptype='BST',
                                      comparefunction=compareCiudad)
    catalog['IndiceFecha'] = om.newMap(omaptype='BST',
                                      comparefunction=compareCiudad)
    catalog['IndiceLongitud'] = om.newMap(omaptype='BST',
                                      comparefunction=compareCiudad)

    return catalog

# Funciones para agregar informacion al catalogo

def addAvistamiento(catalog, avistamiento):
    """
    """
    lt.addLast(catalog['avistamientos'], avistamiento)
    updateIndiceCiudad(catalog['IndiceCiudad'], avistamiento)
    updateIndiceDuracion(catalog['IndiceDuracionseg'], avistamiento)
    updateIndiceFecha(catalog['IndiceFecha'], avistamiento)
    updateIndiceLongitud(catalog['IndiceLongitud'], avistamiento)
    return catalog

def updateIndiceCiudad(map, avistamiento):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    ciudad = avistamiento['city']
    entry = om.get(map, ciudad)
    if entry is None:
        datentry = newDataEntry(avistamiento)
        om.put(map, ciudad, datentry)
    else:
        datentry = me.getValue(entry)
    addFechaIndex(datentry, avistamiento)
    return map

def updateIndiceDuracion(map, avistamiento):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    tiempo = float(avistamiento['duration (seconds)'])
    entry = om.get(map, tiempo)
    if entry is None:
        datentry = newDataEntryDuracionseg(avistamiento)
        om.put(map, tiempo, datentry)
    else:
        datentry = me.getValue(entry)
    addFechaIndexDuracionseg(datentry, avistamiento)
    return map

def updateIndiceFecha(map, avistamiento):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    tiempo = (datetime.datetime.strptime(avistamiento['datetime'], '%Y-%m-%d %H:%M:%S')).date()
    entry = om.get(map, tiempo)
    if entry is None:
        datentry = newDataEntryDuracionseg(avistamiento)
        om.put(map, tiempo, datentry)
    else:
        datentry = me.getValue(entry)
    addFechaIndexsubFecha(datentry, avistamiento)
    return map

def updateIndiceLongitud(map, avistamiento):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    tiempo = round(float(avistamiento['longitude']),2)
    entry = om.get(map, tiempo)
    if entry is None:
        datentry = newDataEntryLatitud(avistamiento)
        om.put(map, tiempo, datentry)
    else:
        datentry = me.getValue(entry)
    addLatitudIndex(datentry, avistamiento)
    return map

def addFechaIndexDuracionseg(datentry, avistamiento):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['ListaAvistamientos']
    lt.addLast(lst, avistamiento)
    offenseIndex = datentry['FechaIndice']
    fecha_avistamiento = avistamiento['city'] + avistamiento['country']
    offentry = om.get(offenseIndex, fecha_avistamiento)
    if (offentry is None):
        entry = newOffenseEntryDuracionseg(fecha_avistamiento, avistamiento)
        lt.addLast(entry['ListaAvistamientosporFecha'], avistamiento)
        om.put(offenseIndex, fecha_avistamiento, entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['ListaAvistamientosporFecha'], avistamiento)
    return datentry

def addFechaIndexsubFecha(datentry, avistamiento):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['ListaAvistamientos']
    lt.addLast(lst, avistamiento)
    offenseIndex = datentry['FechaIndice']
    fecha_avistamiento = avistamiento['datetime']
    offentry = om.get(offenseIndex, fecha_avistamiento)
    if (offentry is None):
        entry = newOffenseEntryDuracionseg(fecha_avistamiento, avistamiento)
        lt.addLast(entry['ListaAvistamientosporFecha'], avistamiento)
        om.put(offenseIndex, fecha_avistamiento, entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['ListaAvistamientosporFecha'], avistamiento)
    return datentry

def addFechaIndex(datentry, avistamiento):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['ListaAvistamientos']
    lt.addLast(lst, avistamiento)
    offenseIndex = datentry['FechaIndice']
    fecha_avistamiento = avistamiento['datetime']
    fecha_avistamiento = datetime.datetime.strptime(fecha_avistamiento, '%Y-%m-%d %H:%M:%S')
    offentry = om.get(offenseIndex, fecha_avistamiento.date())
    if (offentry is None):
        entry = newOffenseEntry(fecha_avistamiento.date(), avistamiento)
        lt.addLast(entry['ListaAvistamientosporFecha'], avistamiento)
        om.put(offenseIndex, fecha_avistamiento.date(), entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['ListaAvistamientosporFecha'], avistamiento)
    return datentry

def addLatitudIndex(datentry, avistamiento):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['ListaAvistamientos']
    lt.addLast(lst, avistamiento)
    offenseIndex = datentry['LatitudIndice']
    latitud = round(float(avistamiento['latitude']),2)
    offentry = om.get(offenseIndex, latitud)
    if (offentry is None):
        entry = newOffenseEntryLatitud(latitud, avistamiento)
        lt.addLast(entry['ListaAvistamientosporFecha'], avistamiento)
        om.put(offenseIndex, latitud, entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['ListaAvistamientosporFecha'], avistamiento)
    return datentry

# Funciones para creacion de datos

def newDataEntry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'FechaIndice': None, 'ListaAvistamientos': None, 'NombreCiudad': None}
    entry['ListaAvistamientos'] = lt.newList('SINGLE_LINKED', compareCiudad)
    entry['FechaIndice'] = om.newMap(omaptype='BST',
                                      comparefunction=compareCiudad)
    entry['NombreCiudad'] = crime['city']      
    return entry

def newDataEntryDuracionseg(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'FechaIndice': None, 'ListaAvistamientos': None}
    entry['ListaAvistamientos'] = lt.newList('SINGLE_LINKED', compareCiudad)
    entry['FechaIndice'] = om.newMap(omaptype='BST',
                                      comparefunction=compareCiudad)
    return entry

def newDataEntryLatitud(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'LatitudIndice': None, 'ListaAvistamientos': None}
    entry['ListaAvistamientos'] = lt.newList('SINGLE_LINKED', compareCiudad)
    entry['LatitudIndice'] = om.newMap(omaptype='BST',
                                      comparefunction=compareCiudad)
    return entry

def newOffenseEntry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'Fecha': None, 'ListaAvistamientosporFecha': None}
    ofentry['Fecha'] = offensegrp
    ofentry['ListaAvistamientosporFecha'] = lt.newList('SINGLELINKED', compareCiudad)
    return ofentry

def newOffenseEntryLatitud(Latitud, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'Latitud': None, 'ListaAvistamientosporFecha': None}
    ofentry['Latitud'] = Latitud
    ofentry['ListaAvistamientosporFecha'] = lt.newList('SINGLELINKED', compareCiudad)
    return ofentry

def newOffenseEntryDuracionseg(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'Fecha': None, 'ListaAvistamientosporFecha': None}
    ofentry['Fecha'] = offensegrp
    ofentry['ListaAvistamientosporFecha'] = lt.newList('SINGLELINKED', compareCiudad)
    return ofentry

def DuracionMasLargas(duracion,cantidad):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'duracion': None, 'cantidad': None}
    ofentry['duracion'] = duracion
    ofentry['cantidad'] = cantidad
    return ofentry

def FechaMasAntiguas(Fecha,cantidad):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'Fecha': None, 'cantidad': None}
    ofentry['Fecha'] = Fecha
    ofentry['cantidad'] = cantidad
    return ofentry

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def compareAvistamientos(id1, id2):
    """
    Compara dos avistamientos
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareCiudad(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareCantidades(ciudad1, ciudad2):
    tamaño1 = lt.size(ciudad1['ListaAvistamientos'])
    tamaño2 = lt.size(ciudad2['ListaAvistamientos'])
    return (tamaño1) > (tamaño2)

def compareDuracionRango(artwork1, artwork2):

    if artwork1['datetime'] == '':

        fecha1 = 0
    else: 
        fecha1 = datetime.datetime.strptime(artwork1['datetime'], '%Y-%m-%d %H:%M:%S')

    if artwork2['datetime'] == '':

        fecha2 = 0

    else:
        fecha2 = datetime.datetime.strptime(artwork2['datetime'], '%Y-%m-%d %H:%M:%S')

    return fecha1 < fecha2

def comparefechasintermas(ciudad1, ciudad2):
    fecha1 = ciudad1['Fecha']
    fecha2 = ciudad2['Fecha']
    return (fecha1) < (fecha2)

def comparelatitudinterna(ciudad1, ciudad2):
    fecha1 = ciudad1['Latitud']
    fecha2 = ciudad2['Latitud']
    return (fecha1) < (fecha2)

# Funciones de ordenamiento

def sortCantidades(catalog):

    sorted_list = merge.sort(catalog, compareCantidades)
    return sorted_list

def sortDuracionRango(catalog):

    sorted_list = merge.sort(catalog, compareDuracionRango)
    return sorted_list

def sortFechasMapasinternos(catalog):

    sorted_list = merge.sort(catalog, comparefechasintermas)
    return sorted_list

def sortlatitudinterna(catalog):

    sorted_list = merge.sort(catalog, comparelatitudinterna)
    return sorted_list

# Funciones de Requerimientos

def primer_req(catalogo,ciudad,ciudades_orden):
    total_avistamientos = om.size(catalogo['IndiceCiudad'])
    llavevalor = om.get(catalogo['IndiceCiudad'],ciudad)
    valor = me.getValue(llavevalor)['FechaIndice']
    valores = om.valueSet(valor)
    lista_avistamientos_crudos = me.getValue(llavevalor)['ListaAvistamientos']
    if int(lt.size(lista_avistamientos_crudos)) >= 6:
        lista3primeros = lt.subList(valores,1,3)
        primeros3avistamientos = lt.newList('ARRAY_LIST')
        for c in lt.iterator(lista3primeros):
            for j in lt.iterator(c['ListaAvistamientosporFecha']):
                if int(lt.size(primeros3avistamientos)) < 3:
                    lt.addLast(primeros3avistamientos,j)
        lista3ultimos = lt.subList(valores,int(lt.size(valores))-2,3)
        ultimos3avistamientos = lt.newList('ARRAY_LIST')
        for c in lt.iterator(lista3ultimos):
            for j in lt.iterator(c['ListaAvistamientosporFecha']):
                lt.addLast(ultimos3avistamientos,j)
        lista_final = lt.subList(ultimos3avistamientos,int(lt.size(ultimos3avistamientos))-2,3)
    else:
        primeros3avistamientos = lt.newList('ARRAY_LIST')
        for k in lt.iterator(valores):
            for l in lt.iterator(k['ListaAvistamientosporFecha']):
                lt.addLast(primeros3avistamientos,l)
        lista_final =  primeros3avistamientos
    medida = lt.size(lista_avistamientos_crudos)
    lista5primeros = lt.subList(ciudades_orden,1,5)

    return total_avistamientos,medida,primeros3avistamientos,lista_final,lista5primeros

def segundo_req(catalogo,duracion_inicial,duracion_final):

        maslargas = lt.subList(om.keySet(catalogo['IndiceDuracionseg']),lt.size(om.keySet(catalogo['IndiceDuracionseg']))-4,5)
        final = lt.newList('ARRAY_LIST')
        duracion_top = lt.newList('ARRAY_LIST')
        for k in lt.iterator(maslargas):
            lt.addFirst(final,k)
            valor = me.getValue(om.get(catalogo['IndiceDuracionseg'],k))['ListaAvistamientos']
            ordenduracion = DuracionMasLargas(k,lt.size(valor))
            lt.addFirst(duracion_top,ordenduracion)
        medida = om.size(catalogo['IndiceDuracionseg'])
        llaves = om.keys(catalogo['IndiceDuracionseg'],duracion_inicial,duracion_final)
        total = 0
        avistamientosrango = lt.newList('ARRAY_LIST')
        for c in lt.iterator(llaves):
            llavevalor = om.get(catalogo['IndiceDuracionseg'],c)
            cantidades = me.getValue(llavevalor)['ListaAvistamientos']
            total += int(lt.size(cantidades))
        sublistaprimeros = lt.subList(llaves,1,3)
        for primeros in lt.iterator(sublistaprimeros):
            llave_valor_primeros = om.get(catalogo['IndiceDuracionseg'],primeros)
            mapa = me.getValue(llave_valor_primeros)['FechaIndice']
            for ciudad in lt.iterator(om.keySet(mapa)):
                llavevalorciudad = om.get(mapa,ciudad)
                valorciudad = me.getValue(llavevalorciudad)['ListaAvistamientosporFecha']
                for j in lt.iterator(valorciudad):
                    lt.addLast(avistamientosrango,j)
        sublistaultimos = lt.subList(llaves,lt.size(llaves)-2,3)
        for ultimos in lt.iterator(sublistaultimos):
            llave_valor_primeros = om.get(catalogo['IndiceDuracionseg'],ultimos)
            mapa = me.getValue(llave_valor_primeros)['FechaIndice']
            for ciudad in lt.iterator(om.keySet(mapa)):
                llavevalorciudad = om.get(mapa,ciudad)
                valorciudad = me.getValue(llavevalorciudad)['ListaAvistamientosporFecha']
                for j in lt.iterator(valorciudad):
                    lt.addLast(avistamientosrango,j)
        primeros3finales = lt.subList(avistamientosrango,1,3)
        ultimos3finales = lt.subList(avistamientosrango,lt.size(avistamientosrango)-2,3)
        return total,medida,primeros3finales,ultimos3finales,duracion_top

def cuarto_req(catalogo,fecha_inicial,fecha_final):

    medida = om.size(catalogo['IndiceFecha'])
    mas_antiguas_llaves = lt.subList(om.keySet(catalogo['IndiceFecha']),1,5)
    top5antiguas = lt.newList('ARRAY_LIST')
    for c in lt.iterator(mas_antiguas_llaves):
        llavevalor = om.get(catalogo['IndiceFecha'],c)
        cantidades = me.getValue(llavevalor)['ListaAvistamientos']
        fechaycantidad = FechaMasAntiguas(c,lt.size(cantidades))
        lt.addLast(top5antiguas,fechaycantidad)
    llaves = om.keys(catalogo['IndiceFecha'],fecha_inicial,fecha_final)
    total = 0
    for c in lt.iterator(llaves):
        llavevalor = om.get(catalogo['IndiceFecha'],c)
        cantidades = me.getValue(llavevalor)['ListaAvistamientos']
        total += int(lt.size(cantidades))
    valores = om.values(catalogo['IndiceFecha'],fecha_inicial,fecha_final)
    valores_primeros = lt.subList(valores,1,3)
    listaavistamientosprimeros = lt.newList('ARRAY_LIST')
    for k in lt.iterator(valores_primeros):
        lista = k['ListaAvistamientos']
        for j in lt.iterator(lista):
            lt.addLast(listaavistamientosprimeros,j)
    primeros_orden = sortDuracionRango(listaavistamientosprimeros)
    primero3 = lt.subList(primeros_orden,1,3)
    finales = lt.subList(valores,lt.size(valores)-2,3)
    listaavistamientosultimos = lt.newList('ARRAY_LIST')
    for l in lt.iterator(finales):
        lista = l['ListaAvistamientos']
        for t in lt.iterator(lista):
            lt.addLast(listaavistamientosultimos,t)
    ultimos_orden = sortDuracionRango(listaavistamientosultimos)
    lista_final = lt.subList(ultimos_orden,int(lt.size(ultimos_orden))-2,3)
    return medida,top5antiguas,total,primero3,lista_final

def quinto_req(catalogo,longitud_inicial,longitud_final,latitud_inicial,latitud_final):
    valores = om.values(catalogo['IndiceLongitud'],longitud_inicial,longitud_final)
    final = lt.newList('ARRAY_LIST')
    for c in lt.iterator(valores):
        valores_latitud = om.values(c['LatitudIndice'],latitud_inicial,latitud_final)
        if lt.size(valores_latitud) >= 1:
            for j in lt.iterator(valores_latitud):
                for k in lt.iterator(j['ListaAvistamientosporFecha']):
                    lt.addLast(final,k)
    orden_cronologico = sortDuracionRango(final)
    total = lt.size(orden_cronologico)
    orden = lt.newList('ARRAY_LIST')
    resultados = lt.newList('ARRAY_LIST')
    for c in lt.iterator(valores):
        valores_latitud = om.values(c['LatitudIndice'],latitud_inicial,latitud_final)
        if lt.size(valores_latitud) >= 1:
            for j in lt.iterator(valores_latitud):
                    lt.addLast(orden,j)
    orden_latitud_longitud = sortlatitudinterna(orden)
    primeros5 = lt.subList(orden_latitud_longitud,1,5)
    for k in lt.iterator(primeros5):
        for l in lt.iterator(k['ListaAvistamientosporFecha']):
            lt.addLast(resultados,l)
    ultimos5 = lt.subList(orden_latitud_longitud,lt.size(orden_latitud_longitud)-4,5)
    for k in lt.iterator(ultimos5):
        for l in lt.iterator(k['ListaAvistamientosporFecha']):
            lt.addLast(resultados,l)
    if lt.size(resultados) >= 10:
        primeros = lt.subList(resultados,1,5)
        ultimos = lt.subList(resultados,lt.size(resultados)-4,5)
    else: 
        primeros = resultados
        ultimos = resultados

    return total,primeros,ultimos