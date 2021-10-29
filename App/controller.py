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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    catalog = model.newCatalogo()
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    avistamientosfile = cf.data_dir + 'Ufo/UFOS-utf8-large.csv'
    input_file = csv.DictReader(open(avistamientosfile, encoding="utf-8"),
                                delimiter=",")
    for avistamiento in input_file:
        model.addAvistamiento(catalog, avistamiento)
    return catalog

# Funciones de ordenamiento

def sortCantidades(catalog):
    """
    Ordena los artistas por nacimiento
    """
    orden = model.sortCantidades(catalog)
    return orden

# Funciones de consulta sobre el catálogo

# Funciones de Requerimientos

def primer_req(catalogo,ciudad,ciudades_orden):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    avistamientos = model.primer_req(catalogo, ciudad,ciudades_orden)
    return avistamientos

def segundo_req(catalog, duracion_inicial, duracion_final):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    avistamientos = model.segundo_req(catalog, duracion_inicial, duracion_final)
    return avistamientos

def cuarto_req(catalog, fecha_inicial, fecha_final):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    avistamientos = model.cuarto_req(catalog, fecha_inicial, fecha_final)
    return avistamientos

def quinto_req(catalog, longitud_inicial, longitud_final,latitud_inicial,latitud_final):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    avistamientos = model.quinto_req(catalog, longitud_inicial, longitud_final,latitud_inicial,latitud_final)
    return avistamientos
