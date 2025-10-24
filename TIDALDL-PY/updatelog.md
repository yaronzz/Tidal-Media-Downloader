TYPE tidal-dl
USE  pip3 install tidal-dl --upgrade

#### v2025-10-24

- [X] Add DASH manifest parser to support python-tidal dash+xml playback
- [X] Support PKCE login flow with selectable API keys
- [X] Normalise embedded FLAC cover art with ffmpeg/metaflac
- [X] Provide configurable listener mode for remote download triggers

#### v2022-10-31

- [X] Add delay setting by @grzekru

#### v2022-08-29

- [X] Fix #931 

#### v2022-07-06

- [X] Mulithread download

#### v2022-06-23

- [X] remove redundant configuration
- [X] add simple-gui
- [X] optimize code

#### v2022-03-04

- [X] fix "file name contain *"  #844
- [X] Update Vietnamese
- [X] update Hungarian
- [X] Update Ukrainian
- [X] Update Dutch
- [X] fix bug of setting path

#### v2022-02-07

- [X] update api key by 1nikolas

#### v2022-01-21

- [X] update api key by @morguldir
- [X] Fix bug of "ReleaseDate"

#### v2022-01-18

- [X] Gui: search view
- [X] Gui: download view

#### v2022-01-11

- [X] Settings: add type-folder(eg Album/Video/Playlist)
- [X] Album folder format support: {None}

#### v2021-11-30

- [X] Add language:Japanese
- [X] Support select apikey(Different keys support different formats)

#### v2021-11-15

- [X] Add language:Korean
- [X] Update vietnamese
- [X] Additional tags for album path and track name

#### v2021-09-23

- [X] Get lyrics from tidal
- [X] Support mixes

#### v2021-09-10

- [X] Add settings: show track-info
- [X] Fix bug of "Illegal characters in path"

#### v2021-05-31

- [X] Add lyrics

#### v2021-04-30

- [X] Add 'album info.txt'
- [X] Fix bug of download video

#### v2021-04-23

- [X] Show get-quality
- [X] Update language
- [X] Update settings: usePlaylistFolder

#### v2021-03-24

- [X] Fix bug of download video
- [X] Fix bug of 'Command line download'

#### v2021-02-20

- [X] Add log

#### v2020-12-17

- [X] Show DOLBY_ATMOS flag [A]
- [X] Fix bug of "Connection aborted"(Linux platform)
- [X] Fix bug of download failed "stat: path should be string, bytes, os.PathLike or integer, not list"

#### v2020-12-10

- [X] Add feature: set the accessToken manually

#### v2020-12-01

- [X] Fix bug of settings-path
- [X] Ability to download multiple urls at a time.

#### v2020-11-13

- [X] Change settings-file save path: XDG_CONFIG_HOME or HOME
- [X] Fix bug of multiThreadDownload
- [X] Choice: logout

#### v2020-11-09

- [X] New login-method: get the accessToken by opening the link, accessToken good for one week and auto refresh

#### v2020-10-22

- [X] Settings: album folder format、track file format
- [X] Settings: show progress
- [X] Support language: german
- [X] Tag: composer
- [X] Add command opts: username\password\accessToken\quality\resolution

#### v2020-09-26

- [X] Fix: download video failed. Resolution parse error.
- [X] Windows: auto get accessToken from tidal-desktop cache
- [X] Download playlist to playlist folder
- [X] Fix: check exist
- [X] Support language vietnamese
- [X] Fix: download cover error (no album-cover)
- [X] Settings: usePlaylistFolder、 multiThreadDownload
- [X] Support language french

#### v2020-09-06

- usage by command: tidal-dl --help

#### v2020-08-30

- support language portuguese
- multithreading download a track

#### v2020-08-24

- add errmessage when downloading failed
- fix: macos - download failed

#### v2020-08-22

- support language spanish\croatian

#### v2020-08-21

- fix: get album path
- support download by file
- support language arabic\czech\itlian\russian\turkish\filipino

#### v2020-08-20

- fix: download playlist
- fix: settings
- fix: lack of multi-language module

#### v2020-08-19

- code rebuild
- multi-language

#### v2020-07-16

- Enter 10:Set AccessToken(authorization)

#### v2020-07-03

- Add label [E] before albumtitle #264
- Volume to CD
- Fix bug of ssl

#### v2020-06-28

- Fix bug of download-playlist
- ArtistName before title(settings)
- AlbumID before AlbumFolderName(settings)
- Add require-libs
- Add errmessage when download err

#### v2020-06-14

- Reduce the number of logins
- Use another login method(from Redsea)
- Download Dolby Atmos(AC4 Codec\Low Quality\Mp4 format)
- Download SONY_360RA(MHA1 Codec\Low Quality\Mp4 format)
- Skip convert to mp4 if File-Codec is AC4 or MHA1
- Fixed the bug of Download-HIRES

#### v2020-05-31

- Use CDN request
- Fix bug of redownload(download artist-albums)
- Add errmessage when login-err
- Fix bug of save-cover MacOs

#### v2020-05-19

- by Command(eg. tidal-dl https://tidal.com/browse/track/70973230)
- Add label [M] before albumtitle
- Update token

#### v2020-05-15

- Cloud token

#### v2020-05-14

- Update token

#### v2020-05-04

- Hide password

#### v2020-03-23

- Fix downloading redirects that can be obtained through the
  /playbackinfopostpaywall method.
- When downloading, download to a .part file, which is then
  either decrypted or renamed into place, to avoid leaving broken files.

#### v2020-3-17

- Fix bug of download ArtistAlbum

#### v2020-03-11

- Fix bug of 'Asset is not ready for playback'

#### v2020-03-10

- Update token

#### v2020-02-28

- Fix bug of savepath
- Add Year: before/After
- save covers(settings)
- Flac: add isrc
- Fix：no version in Tag

#### v2020-02-14

- Fix bug of download track
- ByUrl: add artist
- ByUrl: support 'https://tidal.com/browse/'

#### v2020-01-22

- Download artist album include singles(settings)
- Download by file include artist
- Fix english typos
- Fix bug of tracknumber(download playlist)

#### v2020-01-17

- Artists hyphen ';' to ', '
- Fix bug of download playlist
- Fix bug of download artwork
- Added Explicit to the file name(settings)
- Playlist organized with artist folder(settings)
- Playlist: add tracknum before tracktitle

#### v2019-10-26

- Download playlist by url
- Config 'AddYear' before album dir
- Download playlist track-picture

#### v2019-09-27

- Add skip switch when download atrist/file
- Fix bug of download playlist

#### v2019-09-10

- Fix bug of download videos
- Add version to title
- Add hyphen between number and title(settings)

#### v2019-09-02

- Fix bug of parse link
- Download by file

#### v2019-08-19

- Show Config
- Tag: add composer

#### v2019-08-17

- Download ArtistAlbum: Add EP&Singles

#### v2019-08-12

- Fix bug of tag
- Add setting-showprogress (Only enable when threadnum=1)

#### v2019-08-11

- Fix tag of title
- Download album videos

#### v2019-08-07

- Fix Bug: login;threadnum

#### v2019-08-05

- Support python 2.7

#### v2019-07-30

- Add Setting-OnlyM4a(auto covert mp4 To m4a)
- Fix some bug when first login
- Check ffmpeg status

#### v2019-07-23

- CLI: add a serial number before the file name

#### v2019-07-22

- Fix Some Bug

#### v2019-07-18

- Fix Bug: Set Metadata

#### v2019-07-12

- Fix Some Bug

#### v2019-07-11

- Add Func:Download By Url

#### v2019-07-01

- Add HI_RES Quality

#### v2019-06-24

- Fix Bug When Downloading Playlist

#### v2019-06-16

- Fix Bug Of Track Tag

#### v2019-06-01

- Fix Encoding BUG
- Add Cover To Track

#### v2019-05-08

- Update FFmpegTool

#### v2019-05-06

- Change 'Track' TargetDir
- Download 'Playlist'&'Track' Image
- Fuc: Download ArtistAlbums

#### v2019-04-23

- Add 'Resolution' To Config
- Change Playlist Items TrackNum

#### v2019-04-22

- Download Album: Track Title Append Version

#### v2019-04-16

- Change Album TargetDir
- Add 'ReleaseDate' to Track Metadata
- Remove BUG:Playlist Path

#### v2019-04-11

- Remove BUG:Download Playlist Video

#### v2019-04-08

- Change Tmp File Flag

#### v2019-04-02

- Highlight(Only Linux)

#### v2019-04-01

- Remove Encoding Err

#### v2019-03-29

- Dl Album:If Exist TrackFile. Support ReDownload Or Ignore

#### v2019-03-28

- Check After Set Metadata

#### v2019-03-13

- Deal Err: Get pip version failed

#### v2019-03-11

- Check Files After Download Playlist
- Show Last Version

#### v2019-03-06

- Add Config 'ThreadNum'
- Support Linux
- Add 'requirements.txt'
- Show Tool Version
- Set Metadata in Linux

#### v2019-03-04

- Simplified Code

#### v2019-02-27

- Download FavoriteVideos

#### v2019-02-26

- Download Playlist:Deal with err 'Too Big Page'

#### v2019-02-25

- Playlist LimitNum = 9999
- Download FavoriteTracks

#### v2019-02-19

- Print more err message

#### v2019-02-19

- Download AlbumCover
- Set Track Metadata

#### v2019-02-14

- Set music-filetype by StreamUrlInfo

#### v2019-01-28

- Add decryption.py -- Download LOSSLESS music

#### v2018-12-28

- Add Progressbar - Download Video

#### v2018-12-19

- Update ffmpegHelper
- Simplified Code

#### v2018-12-11

- Fuc: Download Playlist Video

#### v2018-12-01

- Optimized Code
- Multithreading Download Video
- Fuc: Download Playlist

#### v2018-11-22

- Multithreading Download
- Fuc: Download Track
- Fuc: Download Video

#### v2018-11-21

- Func: Download Album
- Func: Get SessionID By Account
- Upload Version To PIP Server : pip install tidal-dl
