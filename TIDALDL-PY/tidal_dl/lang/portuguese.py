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
    SETTING_USE_PLAYLIST_FOLDER = "Usar pasta de lista de reprodução"
    SETTING_MULITHREAD_DOWNLOAD = "Download de vários tópicos"
    SETTING_ALBUM_FOLDER_FORMAT = "Formato da pasta do álbum"
    SETTING_PLAYLIST_FOLDER_FORMAT = "Playlist folder format"
    SETTING_TRACK_FILE_FORMAT = "Track file format"
    SETTING_VIDEO_FILE_FORMAT = "Video file format"
    SETTING_SHOW_PROGRESS = "Mostrar progresso"
    SETTING_SHOW_TRACKINFO = "Mostrar informações da faixa"
    SETTING_SAVE_ALBUMINFO = "Salvar AlbumInfo.txt"
    SETTING_DOWNLOAD_VIDEOS = "Download videos"
    SETTING_ADD_LYRICS = "Adicionar Letra da Música"
    SETTING_LYRICS_SERVER_PROXY = "Proxy do servidor de letras"
    SETTING_ADD_LRC_FILE = "Salvar letras cronometradas (.lrc file)"
    SETTING_PATH = "Settings path"
    SETTING_APIKEY = "Suporte APIKey"
    SETTING_ADD_TYPE_FOLDER = "Adicionar tipo de pasta"
    SETTING_DOWNLOAD_DELAY = "Use Download Delay"
    SETTING_LISTENER_ENABLED = "Listener mode enabled"
    SETTING_LISTENER_PORT = "Listener port"
    SETTING_LISTENER_SECRET = "Listener secret"

    CHOICE = "ESCOLHER"
    FUNCTION = "FUNÇÃO"
    CHOICE_ENTER = "Entrar"
    CHOICE_ENTER_URLID = "ADICIONAR 'Url/ID':"
    CHOICE_EXIT = "SAIR"
    CHOICE_LOGIN = "Verificar o token de acesso"
    CHOICE_SETTINGS = "Configurações"
    CHOICE_SET_ACCESS_TOKEN = "Adicionar Token de Acesso"
    CHOICE_DOWNLOAD_BY_URL = "Download Por url ou id"
    CHOICE_LOGOUT = "Logout"
    CHOICE_APIKEY = "Selecione a APIKey"
    CHOICE_PKCE_LOGIN = "Login via PKCE"
    CHOICE_LISTENER = "Start listener mode"

    PRINT_ERR = "[ERRO]"
    PRINT_INFO = "[INFORMAÇÕES]"
    PRINT_SUCCESS = "[SUCESSO]"

    PRINT_ENTER_CHOICE = "Entrar em Escolher:"
    PRINT_LATEST_VERSION = "Última Versão:"
    # PRINT_USERNAME = "Nome De Usuário:"
    # PRINT_PASSWORD = "Senha:"

    CHANGE_START_SETTINGS = "Configurações Iniciais('0'-Retornar,'1'-Sim):"
    CHANGE_DOWNLOAD_PATH = "Caminho do download('0' Não Modificar):"
    CHANGE_AUDIO_QUALITY = "Qualidade De Áudio('0'-Normal,'1'-Alta,'2'-HiFi,'3'-Master,'4'-Max):"
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
    CHANGE_ALBUM_FOLDER_FORMAT = "Formato da pasta do álbum ('0' não modificar)"
    CHANGE_PLAYLIST_FOLDER_FORMAT = "Playlist folder format('0'-not modify,'default'-to set default):"
    CHANGE_TRACK_FILE_FORMAT = "Formato do arquivo de trilha ('0' não modificar):"
    CHANGE_VIDEO_FILE_FORMAT = "Video file format('0'-not modify,'default'-to set default):"
    CHANGE_SHOW_PROGRESS = "Mostrar progresso('0'-Não,'1'-Sim):"
    CHANGE_SHOW_TRACKINFO = "Mostrar informações da faixa('0'-Não,'1'-Sim):"
    CHANGE_SAVE_ALBUM_INFO = "Salvar AlbumInfo.txt('0'-Não,'1'-Sim):"
    CHANGE_DOWNLOAD_VIDEOS = "Download videos (when downloading playlists, albums, mixes)('0'-No,'1'-Yes):"
    CHANGE_ADD_LYRICS = "Adicionar letras('0'-Não,'1'-Sim):"
    CHANGE_LYRICS_SERVER_PROXY = "Proxy do servidor de letras ('0' não modificar):"
    CHANGE_ADD_LRC_FILE = "Salvar arquivo .lrc de letras cronometradas ('0'-Não,'1'-Sim):"
    CHANGE_ADD_TYPE_FOLDER = "Adicionar Tipo de Pasta, por exemplo, Álbum/Vídeo/Lista de Reprodução('0'-Não,'1'-Sim):"
    CHANGE_MULITHREAD_DOWNLOAD = "Multi thread download('0'-No,'1'-Yes):"
    CHANGE_USE_DOWNLOAD_DELAY = "Use Download Delay('0'-No,'1'-Yes):"
    CHANGE_ENABLE_LISTENER = "Enable listener mode('0'-No,'1'-Yes):"
    CHANGE_LISTENER_SECRET = "Listener secret('0'-not modify):"
    CHANGE_LISTENER_PORT = "Listener port('0'-not modify):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Iniciando o processo de login..."
    AUTH_LOGIN_CODE = "Seu código de login é {}"
    AUTH_NEXT_STEP = "Vá para {} no próximo {} para concluir a configuração."
    AUTH_WAITING = "Espera da autorização..."
    AUTH_TIMEOUT = "A operação expirou."

    MSG_VALID_ACCESSTOKEN = "Token de acesso bom por {}."
    MSG_INVALID_ACCESSTOKEN = "Token de acesso expirado. Tentando atualizá-lo."
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
