#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spanish.py
@Time    :   2021/09/15
@Author  :   Frikilinux & JavierSC
@Version :   2.2
@Contact :
@Desc    :
'''


class LangSpanish(object):
    SETTING = "AJUSTES"
    VALUE = "VALORES"
    SETTING_DOWNLOAD_PATH = "Ruta de descarga"
    SETTING_ONLY_M4A = "Convertir mp4 a m4a"
    SETTING_ADD_EXPLICIT_TAG = "Agregar etiqueta de 'Contenido explícito'"
    SETTING_ADD_HYPHEN = "Agregar guión"
    SETTING_ADD_YEAR = "Agregar año en la carpeta del álbum"
    SETTING_USE_TRACK_NUM = "Agregar número de la pista"
    SETTING_AUDIO_QUALITY = "Calidad de audio"
    SETTING_VIDEO_QUALITY = "Calidad de video"
    SETTING_CHECK_EXIST = "Verificar si existe"
    SETTING_ARTIST_BEFORE_TITLE = "Nombre del artista en el título de la pista"
    SETTING_ALBUMID_BEFORE_FOLDER = "Añadir ID de la carpeta del álbum"
    SETTING_INCLUDE_EP = "Incluir sencillos y EPs"
    SETTING_SAVE_COVERS = "Guardar carátulas"
    SETTING_LANGUAGE = "Idioma"
    SETTING_USE_PLAYLIST_FOLDER = "Usar directorio de la lista de reproducción"
    SETTING_MULITHREAD_DOWNLOAD = "Descarga Multi-hilo"
    SETTING_ALBUM_FOLDER_FORMAT = "Formato del nombre de carpeta del álbum"
    SETTING_TRACK_FILE_FORMAT = "Formato del nombre de archivo de la pista"
    SETTING_SHOW_PROGRESS = "Mostrar progreso"
    SETTING_SHOW_TRACKIFNO = "Mostrar información de pista"
    SETTING_SAVE_ALBUMINFO = "Guardar AlbumInfo.txt"
    SETTING_ADD_LYRICS = "Añadir letras"
    SETTING_LYRICS_SERVER_PROXY = "Proxy del servidor de letras"
    SETTING_PATH = "Ruta de ajustes"
    SETTINGS_ADD_LRC_FILE = "Añadir letras cronometradas (archivo .lrc)"
    SETTING_APIKEY = "APIKey support"
    SETTING_ADD_TYPE_FOLDER = "Add Type-Folder"

    CHOICE = "SELECCIÓN"
    FUNCTION = "FUNCIÓN"
    CHOICE_ENTER = "Ingresar"
    CHOICE_ENTER_URLID = "Ingresar 'Url/ID':"
    CHOICE_EXIT = "Salir"
    CHOICE_LOGIN = "Verificar el token de acceso"
    CHOICE_SETTINGS = "Ajustes"
    CHOICE_SET_ACCESS_TOKEN = "Establecer AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Descargar por Url o ID"
    CHOICE_LOGOUT = "Cerrar sesión"
    CHOICE_APIKEY = "Select APIKey"

    PRINT_ERR = "[ERROR]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[ÉXITO]"

    PRINT_ENTER_CHOICE = "Ingresar Selección:"
    PRINT_LATEST_VERSION = "Última versión:"
    # PRINT_USERNAME = "nombre de usuario:"
    # PRINT_PASSWORD = "contraseña:"

    CHANGE_START_SETTINGS = "¿Iniciar ajustes? ('0'-Volver,'1'-Sí):"
    CHANGE_DOWNLOAD_PATH = "Ruta de descarga ('0' No modificar):"
    CHANGE_AUDIO_QUALITY = "Calidad de audio ('0'-Normal,'1'-High,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "Calidad de video (1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "¿Convertir mp4 a m4a? ('0'-No,'1'-Sí):"
    CHANGE_ADD_EXPLICIT_TAG = "¿Agregar etiqueta de contenido explícito a los nombres de archivo? ('0'-No,'1'-Sí):"
    CHANGE_ADD_HYPHEN = "¿Usar guiones en lugar de espacios en el nombre de los archivos? ('0'-No,'1'-Sí):"
    CHANGE_ADD_YEAR = "¿Agregar año a el nombre de las carpetas del álbum? ('0'-No,'1'-Sí):"
    CHANGE_USE_TRACK_NUM = "¿Agregar número de la pista? ('0'-No,'1'-Sí):"
    CHANGE_CHECK_EXIST = "¿Verificar si el archivo existe antes de descargar la pista? ('0'-No,'1'-Sí):"
    CHANGE_ARTIST_BEFORE_TITLE = "¿Añadir el nombre del artista en el título de la pista? ('0'-No,'1'-Sí):"
    CHANGE_INCLUDE_EP = "¿Incluir Sencillos y EPs al descargar el álbum del artista? ('0'-No,'1'-Sí):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "¿Añadir ID de la carpeta del álbum? ('0'-No,'1'-Sí):"
    CHANGE_SAVE_COVERS = "¿Guardar carátulas?('0'-No,'1'-Sí):"
    CHANGE_LANGUAGE = "Seleccione el idioma"
    CHANGE_ALBUM_FOLDER_FORMAT = "Formato del nombre de carpeta del álbum ('0' No modificar):"
    CHANGE_TRACK_FILE_FORMAT = "Formato del nombre de archivo de la pista ('0' No modificar):"
    CHANGE_SHOW_PROGRESS = "¿Mostrar progreso? ('0'-No,'1'-Sí):"
    CHANGE_SHOW_TRACKINFO = "¿Mostrar información de pista?('0'-No,'1'-Sí):"
    CHANGE_SAVE_ALBUM_INFO = "¿Guardar AlbumInfo.txt?('0'-No,'1'-Sí):"
    CHANGE_ADD_LYRICS = "¿Añadir letras?('0'-No,'1'-Sí):"
    CHANGE_LYRICS_SERVER_PROXY = "¿Proxy del servidor de letras?('0' no modificar):"
    CHANGE_ADD_LRC_FILE = "¿Añadir letras cronometradas en un archivo .lrc? ('0'-No,'1'-Sí):"
    CHANGE_ADD_TYPE_FOLDER = "Add Type-Folder,eg Album/Video/Playlist('0'-No,'1'-Yes):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Iniciando sesión..."
    AUTH_LOGIN_CODE = "Su código para autorizar la sesión es {}"
    AUTH_NEXT_STEP = "Diríjase a {} en los próximos {} para completar la autorización."
    AUTH_WAITING = "Esperando la autorización..."
    AUTH_TIMEOUT = "Se superó el tiempo de espera."

    MSG_VALID_ACCESSTOKEN = "Token de acceso válido por {}."
    MSG_INVAILD_ACCESSTOKEN = "El token de acceso ha expirado. Tratando de renovarlo."
    MSG_PATH_ERR = "¡La ruta no es correcta!"
    MSG_INPUT_ERR = "¡Error de entrada!"

    MODEL_ALBUM_PROPERTY = "PROPIEDAD-DE-ÁLBUM"
    MODEL_TRACK_PROPERTY = "PROPIEDAD-DE-PISTA"
    MODEL_VIDEO_PROPERTY = "PROPIEDAD-DE-VIDEO"
    MODEL_ARTIST_PROPERTY = "PROPIEDAD-DE-ARTISTA"
    MODEL_PLAYLIST_PROPERTY = "PROPIEDAD-DE-PLAYLIST"

    MODEL_TITLE = 'Título'
    MODEL_TRACK_NUMBER = 'Numero de pistas'
    MODEL_VIDEO_NUMBER = 'Numero de videos'
    MODEL_RELEASE_DATE = 'Fecha de lanzamiento'
    MODEL_VERSION = 'Versión'
    MODEL_EXPLICIT = 'Explícito'
    MODEL_ALBUM = 'Álbum'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Nombre'
    MODEL_TYPE = 'Tipo'
