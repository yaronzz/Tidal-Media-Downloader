#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spanish.py
@Time    :   2020/08/21
@Author  :   JavierSC
@Version :   1.0
@Contact :   
@Desc    :   
'''

class LangSpanish(object):
    SETTING = "AJUSTES"
    VALUE = "VALORES"
    SETTING_DOWNLOAD_PATH = "Ruta de descarga"
    SETTING_ONLY_M4A = "Convertir mp4 a m4a"
    SETTING_ADD_EXPLICIT_TAG = "Añadir tag de 'Contenido explícito'"
    SETTING_ADD_HYPHEN = "Agregar guión"
    SETTING_ADD_YEAR = "Agregar año en la carpeta del álbum"
    SETTING_USE_TRACK_NUM = "Agregar número de la pista"
    SETTING_AUDIO_QUALITY = "Calidad de audio"
    SETTING_VIDEO_QUALITY = "Calidad de video"
    SETTING_CHECK_EXIST = "Verificar si existe"
    SETTING_ARTIST_BEFORE_TITLE = "Nombre del artista en el título de la pista"
    SETTING_ALBUMID_BEFORE_FOLDER = "Añadir id de la carpeta del álbum"
    SETTING_INCLUDE_EP = "Incluir single&ep"
    SETTING_SAVE_COVERS = "Guardar covers"
    SETTING_LANGUAGE = "Idioma"
    SETTING_USE_PLAYLIST_FOLDER = "Use playlist folder"
    SETTING_MULITHREAD_DOWNLOAD = "Mulit thread download"
    SETTING_ALBUM_FOLDER_FORMAT = "Album folder format"
    SETTING_TRACK_FILE_FORMAT = "Track file format"

    CHOICE = "SELECCÍON"
    FUNCTION = "FUNCION"
    CHOICE_ENTER = "Ingresar"
    CHOICE_ENTER_URLID = "Ingresar 'Url/ID':"
    CHOICE_EXIT = "Salir"
    CHOICE_LOGIN = "Login"
    CHOICE_SETTINGS = "Ajustes"
    CHOICE_SET_ACCESS_TOKEN = "Establecer AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Descargar por Url o ID"

    PRINT_ERR = "[ERR]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[EXITO]"

    PRINT_ENTER_CHOICE = "Ingresar Seleccíon:"
    PRINT_LATEST_VERSION = "Ultima versión:"
    PRINT_USERNAME = "nombre de usuario:"
    PRINT_PASSWORD = "contraseña:"
    
    CHANGE_START_SETTINGS = "Iniciar ajustes('0'-Volver,'1'-Si):"
    CHANGE_DOWNLOAD_PATH = "Ruta de descarga('0' not modify):"
    CHANGE_AUDIO_QUALITY = "Calidad de audio('0'-Normal,'1'-High,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "Calidad de video('0'-1080,'1'-720,'2'-480,'3'-360):"
    CHANGE_ONLYM4A = "Convertir mp4 a m4a('0'-No,'1'-Si):"
    CHANGE_ADD_EXPLICIT_TAG = "Agregar tag de contenido explícito a los nombres de archivo('0'-No,'1'-Si):"
    CHANGE_ADD_HYPHEN = "Usar guiones en lugar de espacios en el nombre de los archivos('0'-No,'1'-Si):"
    CHANGE_ADD_YEAR = "Agregar año a el nombre de las carpetas del álbum('0'-No,'1'-Si):"
    CHANGE_USE_TRACK_NUM = "Agregar número de la pista('0'-No,'1'-Si):"
    CHANGE_CHECK_EXIST = "Verificar si el el archivo existe antes de descargar la pista('0'-No,'1'-Si):"
    CHANGE_ARTIST_BEFORE_TITLE = "Añadir el nombre del artista en el título de la pista('0'-No,'1'-Si):"
    CHANGE_INCLUDE_EP = "Incluir singles y EPs al descargar el albun del artista('0'-No,'1'-Si):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Añadir id de la carpeta del álbum('0'-No,'1'-Si):"
    CHANGE_SAVE_COVERS = "Guardar covers('0'-No,'1'-Si):"
    CHANGE_LANGUAGE = "Seleccione el idioma"
    CHANGE_ALBUM_FOLDER_FORMAT = "Album folder format('0' not modify):"
    CHANGE_TRACK_FILE_FORMAT = "Track file format('0' not modify):"

    MSG_INVAILD_ACCESSTOKEN = "AccessToken invalido! Por favor reinicie"
    MSG_PATH_ERR = "La ruta no es correcta!"
    MSG_INPUT_ERR = "Error de entrada!"

    MODEL_ALBUM_PROPERTY = "PROPIEDAD-DE-ÁLBUM"
    MODEL_TRACK_PROPERTY = "PROPIEDAD-DE-PISTA"
    MODEL_VIDEO_PROPERTY = "PROPIEDAD-DE-VIDEO"
    MODEL_ARTIST_PROPERTY = "PROPIEDAD-DE-ARTISTA"
    MODEL_PLAYLIST_PROPERTY = "PROPIEDAD-DE-PLAYLIST"

    MODEL_TITLE = 'Titulo'
    MODEL_TRACK_NUMBER = 'Numero de pista'
    MODEL_VIDEO_NUMBER = 'Numero de video'
    MODEL_RELEASE_DATE = 'Fecha de lanzamiento'
    MODEL_VERSION = 'Versión'
    MODEL_EXPLICIT = 'Explícito'
    MODEL_ALBUM = 'Álbum'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Nombre'
    MODEL_TYPE = 'Tipo'
