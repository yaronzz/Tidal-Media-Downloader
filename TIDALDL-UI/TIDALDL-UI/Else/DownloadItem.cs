using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Tidal;
using AIGS.Common;
using AIGS.Helper;
using Stylet;
using TagLib;
using System.IO;
using System.Collections.ObjectModel;

namespace TIDALDL_UI.Else
{
    public class DownloadItem : Screen
    {
        public Playlist TidalPlaylist { get; set; }
        public Album TidalAlbum { get; set; }
        public Track TidalTrack { get; set; }
        public Video TidalVideo { get; set; }

        /// <summary>
        /// Item Para - OutputDir | FilePath | Track Quality | Title | Type
        /// </summary>
        public string OutputDir { get; set; }
        public string FilePath { get; set; }
        public eSoundQuality Quality { get; set; }
        public eResolution Resolution { get; set; }
        public int Index { get; set; }
        public string Title { get; set; }
        public string sType { get; set; }
        public int ErrlabelHeight { get; set; }
        public bool OnlyM4a { get; set; }
        public bool AddHyphen { get; set; } 
        public string Own { get; set; }
        public bool ToChinese { get; set; }
        public bool CheckExist { get; set; }
        public bool ArtistBeforeTitle { get; set; }
        
        ///// <summary>
        ///// Progress 
        ///// </summary>
        public ProgressHelper Progress { get; set; }

        public DownloadItem(int index, Track track = null, Video video = null, Album album = null, Playlist plist = null)
        {
            TidalPlaylist = plist;
            TidalAlbum = album;
            TidalVideo = video;
            TidalTrack = track;
            Quality    = TidalTool.getQuality(Config.Quality());
            Resolution = TidalTool.getResolution(Config.Resolution());
            OutputDir  = Config.OutputDir();
            Index      = index;
            Progress   = new ProgressHelper();
            OnlyM4a    = Config.OnlyM4a();
            AddHyphen  = Config.AddHyphen();
            Own        = album == null?null : album.Title;
            ToChinese  = Config.ToChinese();
            CheckExist = Config.CheckExist();
            ArtistBeforeTitle = Config.ArtistBeforeTitle();

            if (TidalTrack != null)
            {
                Title = track.Title;
                sType = "MusicCircle";
            }
            else
            {
                Title = video.Title;
                sType = "PlayCircle";
            }
        }


        #region Method
        public void Start()
        {
            //Add to threadpool
            ThreadTool.AddWork((object[] data) =>
            {
                if (Progress.GetStatus() != ProgressHelper.STATUS.WAIT)
                    return;

                ErrlabelHeight = 0;
                Progress.SetStatus(ProgressHelper.STATUS.RUNNING);
                if (TidalTrack != null)
                    DownloadTrack();
                else
                    DownloadVideo();
            });
        }

        public void Cancel()
        {
            if (Progress.GetStatus() != ProgressHelper.STATUS.COMPLETE)
                Progress.SetStatus(ProgressHelper.STATUS.CANCLE);
        }

        public void Restart()
        {
            ProgressHelper.STATUS status = Progress.GetStatus();
            if (status == ProgressHelper.STATUS.CANCLE || status == ProgressHelper.STATUS.ERROR)
            {
                Progress.Clear();
                Start();
            }
        }
        #endregion


        #region DownloadVideo
        public bool ProgressNotify(long lCurSize, long lAllSize)
        {
            Progress.Update(lCurSize, lAllSize);
            if (Progress.GetStatus() != ProgressHelper.STATUS.RUNNING)
                return false;
            return true;
        }

        public void DownloadVideo()
        {
            //GetStream
            Progress.StatusMsg = "GetStream...";
            string Errlabel = "";
            string[] TidalVideoUrls = TidalTool.getVideoDLUrls(TidalVideo.ID.ToString(), Resolution, out Errlabel);
            if (Errlabel.IsNotBlank())
                goto ERR_RETURN;
            string TsFilePath = TidalTool.getVideoPath(OutputDir, TidalVideo, TidalAlbum, ".ts", hyphen: AddHyphen, plist: TidalPlaylist, artistBeforeTitle:ArtistBeforeTitle);

            //Download
            Progress.StatusMsg = "Start...";
            if(!(bool)M3u8Helper.Download(TidalVideoUrls, TsFilePath, ProgressNotify, Proxy:TidalTool.PROXY))
            {
                Errlabel = "Download failed!";
                goto ERR_RETURN;
            }
            
            //Convert
            FilePath = TidalTool.getVideoPath(OutputDir, TidalVideo, TidalAlbum, hyphen:AddHyphen, plist:TidalPlaylist, artistBeforeTitle: ArtistBeforeTitle);
            if(!FFmpegHelper.IsExist())
            {
                Errlabel = "FFmpeg is not exist!";
                goto ERR_RETURN;
            }
            if (!FFmpegHelper.Convert(TsFilePath, FilePath))
            {
                Errlabel = "Convert failed!";
                goto ERR_RETURN;
            }
            System.IO.File.Delete(TsFilePath);
            Progress.SetStatus(ProgressHelper.STATUS.COMPLETE);
            return;

        ERR_RETURN:
            if (Progress.GetStatus() == ProgressHelper.STATUS.CANCLE)
                return;

            ErrlabelHeight = 15;
            Progress.SetStatus(ProgressHelper.STATUS.ERROR);
            Progress.Errmsg = Errlabel;
        }
        #endregion

        #region DownloadTrack
        public void DownloadTrack()
        {
            string Errlabel = "";

            //GetStream
            Progress.StatusMsg = "GetStream...";
            StreamUrl TidalStream = TidalTool.getStreamUrl(TidalTrack.ID.ToString(), Quality, out Errlabel);
            if (Errlabel.IsNotBlank())
                goto ERR_RETURN;

            //Get path
            FilePath = TidalTool.getTrackPath(OutputDir, TidalAlbum, TidalTrack, TidalStream.Url, AddHyphen, TidalPlaylist, artistBeforeTitle: ArtistBeforeTitle);

            //Check if song is downloaded already
            string CheckName = OnlyM4a ? FilePath.Replace(".mp4", ".m4a") : FilePath;
            if (CheckExist && System.IO.File.Exists(CheckName))
            {
                Progress.Update(100, 100);
                Progress.SetStatus(ProgressHelper.STATUS.COMPLETE);
                return;
            }

            //Get contributors
            ObservableCollection<Contributor> pContributors = TidalTool.getTrackContributors(TidalTrack.ID.ToString(), out Errlabel);

            //To chinese 
            if (ToChinese)
            {
                CloudMusicAlbum cloalbum = Chinese.matchAlbum(TidalAlbum.Title, TidalAlbum.Artist.Name);
                string chnname = Chinese.convertSongTitle(TidalTrack.Title, cloalbum);
                if (chnname != TidalTrack.Title)
                {
                    FilePath = TidalTool.getTrackPath(OutputDir, TidalPlaylist != null ? null : TidalAlbum, TidalTrack, TidalStream.Url, AddHyphen, TidalPlaylist, chnname, artistBeforeTitle: ArtistBeforeTitle);
                    TidalTrack.Title = chnname;
                }
            }

            //Download
            Progress.StatusMsg = "Start...";
            for (int i = 0; i < 100 && Progress.GetStatus() != ProgressHelper.STATUS.CANCLE; i++)
            {
                if ((bool)DownloadFileHepler.Start(TidalStream.Url, FilePath, Timeout: 5 * 1000, UpdateFunc: UpdateDownloadNotify, ErrFunc: ErrDownloadNotify, Proxy:TidalTool.PROXY))
                {
                    //Decrypt
                    if (!TidalTool.DecryptTrackFile(TidalStream, FilePath))
                    {
                        Errlabel = "Decrypt failed!";
                        goto ERR_RETURN;
                    }

                    if(OnlyM4a)
                    {
                        string sNewName;
                        if (!TidalTool.ConvertMp4ToM4a(FilePath, out sNewName))
                        {
                            Errlabel = "Convert mp4 to m4a failed!";
                            ErrlabelHeight = 15;
                        }
                        else
                            FilePath = sNewName;
                    }

                    //SetMetaData 
                    if (TidalAlbum == null && TidalTrack.Album != null)
                    {
                        string sErrcode = null;
                        TidalAlbum = TidalTool.getAlbum(TidalTrack.Album.ID.ToString(), out sErrcode);
                    }
                    string sLabel = TidalTool.SetMetaData(FilePath, TidalAlbum, TidalTrack, TidalTool.getAlbumCoverPath(OutputDir, TidalAlbum), pContributors);
                    if (sLabel.IsNotBlank())
                    {
                        Errlabel = "Set metadata failed!";
                        goto ERR_RETURN;
                    }

                    Progress.SetStatus(ProgressHelper.STATUS.COMPLETE);
                    return;
                }
            }
            Errlabel = "Download failed!";

        ERR_RETURN:
            if (Progress.GetStatus() == ProgressHelper.STATUS.CANCLE)
                return;

            ErrlabelHeight = 15;
            Progress.SetStatus(ProgressHelper.STATUS.ERROR);
            Progress.Errmsg = Errlabel;
        }

        public void ErrDownloadNotify(long lTotalSize, long lAlreadyDownloadSize, string sErrMsg, object data)
        {
            return;
        }

        public bool UpdateDownloadNotify(long lTotalSize, long lAlreadyDownloadSize, long lIncreSize, object data)
        {
            Progress.Update(lAlreadyDownloadSize, lTotalSize);
            if (Progress.GetStatus() != ProgressHelper.STATUS.RUNNING)
                return false;
            return true;
        }
        #endregion
    }
}
