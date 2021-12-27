#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   portuguese.py
@Time    :   2020/08/19
@Author  :   BR8N0BL4CK & João 
@Version :   1.0
@Contact :   
@Desc    :   
'''


class LangPortuguese(object):
    SETTING = "Configurações"
    VALUE = "VALOR"
    SETTING_DOWNLOAD_PATH = "Caminho do download"
    SETTING_ONLY_M4A = "Converter mp4 para m4a"
    SETTING_ADD_EXPLICIT_TAG = "Adicionar etiqueta explícito"
    SETTING_ADD_HYPHEN = "Adicionar hífen"
    SETTING_ADD_YEAR = "Adicionar ano antes do nome do álbum na pasta"
    SETTING_USE_TRACK_NUM = "Adicionar Número da Faixa"
    SETTING_AUDIO_QUALITY = "Qualidade Do Áudio"
    SETTING_VIDEO_QUALITY = "Qualidade Do Vídeo"
    SETTING_CHECK_EXIST = "Verificar Existência"
    SETTING_ARTIST_BEFORE_TITLE = "ArtistaNome Antes do Track-Título"
    SETTING_ALBUMID_BEFORE_FOLDER = "Número De Identificação do Álbum antes na Pasta"
    SETTING_INCLUDE_EP = "Incluir Single & EP"
    SETTING_SAVE_COVERS = "Salvar Capas"
    SETTING_LANGUAGE = "idioma"
    SETTING_USE_PLAYLIST_FOLDER = "Use playlist folder"
    SETTING_MULITHREAD_DOWNLOAD = "Multi thread download"
    SETTING_ALBUM_FOLDER_FORMAT = "Album folder format"
    SETTING_TRACK_FILE_FORMAT = "Track file format"
    SETTING_SHOW_PROGRESS = "Show progress"
    SETTING_SHOW_TRACKIFNO = "Show Track Info"
    SETTING_SAVE_ALBUMINFO = "Save AlbumInfo.txt"
    SETTING_ADD_LYRICS = "Add lyrics"
    SETTING_LYRICS_SERVER_PROXY = "Lyrics server proxy"
    SETTING_PATH = "Settings path"
    SETTINGS_ADD_LRC_FILE = "Save timed lyrics (.lrc file)"
    SETTING_APIKEY = "APIKey support"
    SETTING_ADD_TYPE_FOLDER = "Add Type-Folder"

    CHOICE = "ESCOLHER"
    FUNCTION = "FUNÇÃO"
    CHOICE_ENTER = "Entrar"
    CHOICE_ENTER_URLID = "ADICIONAR 'Url/ID':"
    CHOICE_EXIT = "SAIR"
    CHOICE_LOGIN = "Check AccessToken"
    CHOICE_SETTINGS = "Configurações"
    CHOICE_SET_ACCESS_TOKEN = "Adicionar Token de Acesso"
    CHOICE_DOWNLOAD_BY_URL = "Download Por url ou id"
    CHOICE_LOGOUT = "Logout"
    CHOICE_APIKEY = "Select APIKey"

    PRINT_ERR = "[ERRO]"
    PRINT_INFO = "[INFORMAÇÕES]"
    PRINT_SUCCESS = "[SUCESSO]"

    PRINT_ENTER_CHOICE = "Entrar em Escolher:"
    PRINT_LATEST_VERSION = "Última Versão:"
    # PRINT_USERNAME = "Nome De Usuário:"
    # PRINT_PASSWORD = "Senha:"

    CHANGE_START_SETTINGS = "Configurações Iniciais('0'-Retornar,'1'-Sim):"
    CHANGE_DOWNLOAD_PATH = "Caminho do download('0' Não Modificar):"
    CHANGE_AUDIO_QUALITY = "Qualidade De Áudio('0'-Normal,'1'-Alta,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "Qualidade Do Vídeo(1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "Converter mp4 para m4a('0'-Não,'1'-Sim):"
    CHANGE_ADD_EXPLICIT_TAG = "Adicionar Etiqueta Explícito para os nomes dos arquivos('0'-Não,'1'-Sim):"
    CHANGE_ADD_HYPHEN = "Usar hífen em vez de espaços nos nomes dos arquivos('0'-Não,'1'-Sim):"
    CHANGE_ADD_YEAR = "Adicionar Ano aos nomes das pastas dos álbums('0'-Não,'1'-Sim):"
    CHANGE_USE_TRACK_NUM = "Adicionar número da faixa antes do nome do arquivo('0'-Não,'1'-Sim):"
    CHANGE_CHECK_EXIST = "Verificar existência do arquivo antes de baixar a faixa('0'-Não,'1'-Sim):"
    CHANGE_ARTIST_BEFORE_TITLE = "Adicionar o nome do artista antes do título da faixa('0'-Não,'1'-Sim):"
    CHANGE_INCLUDE_EP = "Incluir singles e EPs quando baixar álbums de um artista('0'-Não,'1'-Sim):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Adicionar id antes no nome da pasta do álbum('0'-Não,'1'-Sim):"
    CHANGE_SAVE_COVERS = "Salvar Capas('0'-Não,'1'-Sim):"
    CHANGE_LANGUAGE = "Selecionar idioma"
    CHANGE_ALBUM_FOLDER_FORMAT = "Album folder format('0' not modify):"
    CHANGE_TRACK_FILE_FORMAT = "Track file format('0' not modify):"
    CHANGE_SHOW_PROGRESS = "Show progress('0'-No,'1'-Yes):"
    CHANGE_SHOW_TRACKINFO = "Show track info('0'-No,'1'-Yes):"
    CHANGE_SAVE_ALBUM_INFO = "Save AlbumInfo.txt('0'-No,'1'-Yes):"
    CHANGE_ADD_LYRICS = "Add lyrics('0'-No,'1'-Yes):"
    CHANGE_LYRICS_SERVER_PROXY = "Lyrics server proxy('0' not modify):"
    CHANGE_ADD_LRC_FILE = "Save timed lyrics .lrc file ('0'-No,'1'-Yes):"
    CHANGE_ADD_TYPE_FOLDER = "Add Type-Folder,eg Album/Video/Playlist('0'-No,'1'-Yes):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Starting login process..."
    AUTH_LOGIN_CODE = "Your login code is {}"
    AUTH_NEXT_STEP = "Go to {} within the next {} to complete setup."
    AUTH_WAITING = "Waiting for authorization..."
    AUTH_TIMEOUT = "Operation timed out."

    MSG_VALID_ACCESSTOKEN = "AccessToken good for {}."
    MSG_INVAILD_ACCESSTOKEN = "Expired AccessToken. Attempting to refresh it."
    MSG_PATH_ERR = "Erro no local de salvamento dos arquivos!"
    MSG_INPUT_ERR = "Erro de Entrada!"

    MODEL_ALBUM_PROPERTY = "ÁLBUM-PROPRIEDADE"
    MODEL_TRACK_PROPERTY = "FAIXA-PROPRIEDADE"
    MODEL_VIDEO_PROPERTY = "VÍDEO-PROPRIEDADE"
    MODEL_ARTIST_PROPERTY = "ARTISTA-PROPRIEDADE"
    MODEL_PLAYLIST_PROPERTY = "PLAYLIST-PPROPRIEDADE"

    MODEL_TITLE = 'Título'
    MODEL_TRACK_NUMBER = 'Número Da Faixa'
    MODEL_VIDEO_NUMBER = 'Número Do Vídeo'
    MODEL_RELEASE_DATE = 'Data De Lançamento'
    MODEL_VERSION = 'Versão'
    MODEL_EXPLICIT = 'Explícito'
    MODEL_ALBUM = 'Álbum'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Nome'
    MODEL_TYPE = 'Tipo'
