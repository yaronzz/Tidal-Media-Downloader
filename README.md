<br>
    <a href="https://github.com/yaronzz/Tidal-Media-Downloader-PRO">[GUI-REPOSITORY]</a>
<br>
<div align="center">
  <h1>Tidal-Media-Downloader</h1>
  <a href="https://github.com/yaronzz/Tidal-Media-Downloader/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/yaronzz/Tidal-Media-Downloader.svg?style=flat-square" alt="">
  </a>
  <a href="https://github.com/yaronzz/Tidal-Media-Downloader/releases">
    <img src="https://img.shields.io/github/v/release/yaronzz/Tidal-Media-Downloader.svg?style=flat-square" alt="">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/github/issues/yaronzz/Tidal-Media-Downloader.svg?style=flat-square" alt="">
  </a>
  <a href="https://github.com/yaronzz/Tidal-Media-Downloader">
    <img src="https://img.shields.io/github/downloads/yaronzz/Tidal-Media-Downloader/total?label=tidal-gui%20download" alt="">
  </a>
  <a href="https://pypi.org/project/tidal-dl/">
    <img src="https://img.shields.io/pypi/dm/tidal-dl?label=tidal-dl%20download" alt="">
  </a>
  <a href="https://github.com/yaronzz/Tidal-Media-Downloader/actions/workflows/build.yml">
    <img src="https://github.com/yaronzz/Tidal-Media-Downloader/actions/workflows/build.yml/badge.svg" alt="">
  </a>
</div>
<p align="center">
  «Tidal-Media-Downloader» is an application that lets you download videos and tracks from Tidal. It supports two version: tidal-dl and tidal-gui. (This repository only contains tidal-dl, and the release isn't the newest gui version.)
    <br>
        <a href="https://github.com/yaronzz/Tidal-Media-Downloader-PRO/releases">Download</a> |
        <a href="https://yaronzz.com/post/tidal_dl_installation/">Documentation</a> |
        <a href="https://yaronzz.com/post/tidal_dl_installation_chn/">中文文档</a> |
    <br>
</p>

## 📺 Installation

| Name                                | platform                          | Install                                                                                                               |
| ----------------------------------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| tidal-dl (cli)                      | Windows \ Linux \ Macos \ Android | ``pip3 install tidal-dl --upgrade``<br />[Detailed Description](https://yaronzz.com/post/tidal_dl_installation/#Install) |
| tidal-gui                           | Windows                           | [GUI Repository](https://github.com/yaronzz/Tidal-Media-Downloader-PRO)                                                  |
| tidal-gui(**Cross-platform**) | Windows \ Linux \ Macos           | ``pip3 install tidal-gui --upgrade``                                                                                  |

### Nightly Builds

| Download nightly builds from continuous integration: | [Build Status][Actions] |
| ---------------------------------------------------- | ----------------------- |

## 🤖 Features

- Download album \ track \ video \ playlist \ artist-albums
- Add metadata to songs
- Selectable video resolution and track quality

## 💽 User Interface

<img src="https://i.loli.net/2020/08/19/gqW6zHI1SrKlomC.png" alt="image" style="zoom: 50%;" />

![image-20200806013705425](https://i.loli.net/2020/08/06/sPLowIlCGyOdpVN.png)

## Settings - Possible Tags

### Album

| Tag               | Example value                        |
| ----------------- | ------------------------------------ |
| {ArtistName}      | The Beatles                          |
| {AlbumArtistName} | The Beatles                          |
| {Flag}            | M/A/E  (Master/Dolby Atmos/Explicit) |
| {AlbumID}         | 55163243                             |
| {AlbumYear}       | 1963                                 |
| {AlbumTitle}      | Please Please Me (Remastered)        |
| {AudioQuality}    | LOSSLESS                             |
| {DurationSeconds} | 1919                                 |
| {Duration}        | 31:59                                |
| {NumberOfTracks}  | 14                                   |
| {NumberOfVideos}  | 0                                    |
| {NumberOfVolumes} | 1                                    |
| {ReleaseDate}     | 1963-03-22                           |
| {RecordType}      | ALBUM                                |
| {None}            |                                      |

### Track

| Tag               | Example Value                              |
| ----------------- | ------------------------------------------ |
| {TrackNumber}     | 01                                         |
| {ArtistName}      | The Beatles                                |
| {ArtistsName}     | The Beatles                                |
| {TrackTitle}      | I Saw Her Standing There (Remastered 2009) |
| {ExplicitFlag}    | (*Explicit*)                             |
| {AlbumYear}       | 1963                                       |
| {AlbumTitle}      | Please Please Me (Remastered)              |
| {AudioQuality}    | LOSSLESS                                   |
| {DurationSeconds} | 173                                        |
| {Duration}        | 02:53                                      |
| {TrackID}         | 55163244                                   |

### Video

| Tag            | Example Value      |
| -------------- | ------------------ |
| {VideoNumber}  | 00                 |
| {ArtistName}   | DMX                |
| {ArtistsName}  | DMX, Westside Gunn |
| {VideoTitle}   | Hood Blues         |
| {ExplicitFlag} | (*Explicit*)     |
| {VideoYear}    | 2021               |
| {TrackID}      | 188932980          |

## ☕ Support

If you really like my projects and want to support me, you can buy me a coffee and star this project.

<a href="https://www.buymeacoffee.com/yaronzz" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/arial-orange.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" ></a>

## 🎂 Contributors

This project exists thanks to all the people who contribute.
`<a href="https://github.com/yaronzz/Tidal-Media-Downloader/graphs/contributors"><img src="https://contributors-img.web.app/image?repo=yaronzz/Tidal-Media-Downloader" />``</a>`

## 🎨 Libraries and reference

- [aigpy](https://github.com/yaronzz/AIGPY)
- [python-tidal](https://github.com/tamland/python-tidal)
- [redsea](https://github.com/redsudo/RedSea)
- [tidal-wiki](https://github.com/Fokka-Engineering/TIDAL/wiki)

## 📜 Disclaimer

- Private use only.
- Need a Tidal-HIFI subscription.
- You should not use this method to distribute or pirate music.
- It may be illegal to use this in your country, so be informed.

## Developing

```shell
pip3 uninstall tidal-dl
pip3 install -r requirements.txt --user
python3 setup.py install
```

## Fork changes - Scenario and comments:

I would be content with TIDAL download feature, to give me off-line music on my device.  I find playlists good for that.

But playlist changes are not done well.  If I add 1 song to a 100 song playlist, the only way I can get it on my phone is: -
delete all 100 songs - download 101 songs.  It's the time, the wear and tear on my device sd card... nope... don't like it at all.

But I see tidal-dl can create a "mirror image" of that playlist.  And has some smarts: if I add a song to the playlist, download again, it will ONLY download that song.  Cool.  But - what if I delete a song?

Background: I use PC MediaMonkey for my non-TIDAL mp3s... it will download a music folder to my device... with MediaMonkey for Android and my home Wifi.  Of course, MM can also see tidal-dl that "mirror image" playlist.  And crucially: if there are adds/deletes, MM makes just the changes on my phone.  Other files are untouched.  Deletes are done too, smart!

But... now tidal-dl is the weak link.  If I add 1 file to a playlist, and delete 1 file... it gives me the add... but it doesn't handle the delete.  And the "mirror image" is not a mirror image any more.

So this is to fill that gap in my scenario.  But the effect seems useful for other use-cases.  SUMMARY: Suppose you download a playlist, on top of a previous download.  If files are deleted on the playlist, they will also be deleted in the mirror image.

Also: some improved handling of the "onlyM4A" flag.  If files have been renamed from mp4 to m4a, the SKIP download logic wasn't working.  Now it's handled for the simple case at least.

[Actions]: https://github.com/yaronzz/Tidal-Media-Downloader/actions
[Build]: https://github.com/yaronzz/Tidal-Media-Downloader/workflows/Tidal%20Media%20Downloader/badge.svg
