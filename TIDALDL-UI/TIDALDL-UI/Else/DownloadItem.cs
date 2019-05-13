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

namespace TIDALDL_UI.Else
{
    public class DownloadItem:Screen
    {
        /// <summary>
        /// Item Object - Track | Videp
        /// </summary>
        public Track TidalTrack { get; set; }
        public Video TidalVideo { get; set; }
        public StreamUrl TidalStream { get; set; }
        public string[] TidalVideoUrls { get; set; }

        /// <summary>
        /// Item Para - BasePath | FilePath | Track Quality | Title | Duration | Type
        /// </summary>
        public string BasePath { get; set; }
        public string FilePath { get; set; }
        public string Quality { get; set; }
        public string Resolution { get; set; }
        public int    Index { get; set; }
        public string Title { get; set; }
        public string Duration { get; set; }
        public string sType { get; set; }

        /// <summary>
        /// Errmsg
        /// </summary>
        public string Errlabel { get; set; }

        ///// <summary>
        ///// Progress 
        ///// </summary>
        public ProgressHelper Progress { get; set; }

        /// <summary>
        /// SendMessage To Parent
        /// </summary>
        public delegate void UpdateNotify(DownloadItem item);
        public UpdateNotify UpdataFunc { get; set; }

        public DownloadItem(int index, string basePath, UpdateNotify Func, Track track = null, string quality = "LOW", Video video = null, string resolution = "720")
        {
            TidalVideo       = video;
            TidalTrack       = track;
            Quality          = quality;
            Resolution       = resolution;
            BasePath         = basePath;
            Index            = index;
            Errlabel         = "";
            Progress         = new ProgressHelper();
            UpdataFunc       = Func;

            if (TidalTrack != null)
            {
                Title = track.Title;
                Duration = track.SDuration;
                sType = "Track";
            }
            else
            {
                Title = video.Title;
                Duration = video.SDuration;
                sType = "Video";
            }
        }

        /// <summary>
        /// Prepare Before Download
        /// </summary>
        private string Prepare()
        {
            string Errmsg;
            if (sType == "Track")
            {
                TidalStream = Tool.GetStreamUrl(TidalTrack.ID, Quality, out Errmsg);
                if (Errmsg.IsNotBlank())
                    return Errmsg;
                FilePath = BasePath + '\\' + Tool.GetTrackFileName(TidalTrack, TidalStream);
            }
            if(sType == "Video")
            {
                TidalVideoUrls = Tool.GetVideoDLUrls(TidalVideo.ID, Resolution, out Errmsg);
                if (Errmsg.IsNotBlank())
                    return Errmsg;
                FilePath = BasePath + '\\' + Tool.GetVideoFileName(TidalVideo);
            }
            return null;
        }

        #region Method
        public void Cancle()
        {
            Progress.IsCancle = true;
        }
            
        public void Start()
        {
            if (ThreadTool.GetThreadNum() <= 0)
                ThreadTool.SetThreadNum(int.Parse(Config.ThreadNum()));
            ThreadTool.AddWork(ThreadFuncDownlaod);
        }
        #endregion


        #region Thread
        public void ThreadFuncDownlaod(object data)
        {
            if (Progress.IsCancle)
                return;

            //Prepare
            Errlabel = Prepare();
            if (Errlabel.IsNotBlank())
            {
                Progress.Errlabel = Errlabel;
                Progress.IsErr    = true;
                return;
            }

            if (sType == "Track")
                DownloadTrack();
            if (sType == "Video")
                DownloadVideo();


        }

        public void DownloadVideo()
        {
            string sTmpDir = BasePath + '\\' + PathHelper.ReplaceLimitChar(TidalVideo.Title, "-") + "TMP";
            if(Directory.Exists(sTmpDir))
                Directory.Delete(sTmpDir, true);
            PathHelper.Mkdirs(sTmpDir);

            long lCount = TidalVideoUrls.Count();
            for (int i = 0; i < lCount; i++)
            {
                string sUrl  = TidalVideoUrls[i];
                string sName = sTmpDir + '\\' + (100000 + i + 1).ToString() + ".ts";
                bool bFlag = (bool)DownloadFileHepler.Start(sUrl, sName, RetryNum: 3);
                if (bFlag == false)
                    goto ERR_POINT;

                Progress.Update(i + 1, lCount);
                UpdataFunc(this);

                if (Progress.IsCancle)
                    goto CANCLE_POINT;
            }

            Progress.Update(lCount, lCount);
            Progress.IsComplete = true;
            UpdataFunc(this);
        CANCLE_POINT:
            Directory.Delete(sTmpDir, true);
            return;

        ERR_POINT:
            Progress.IsErr = true;
            UpdataFunc(this);
            Directory.Delete(sTmpDir, true);
        }

        public void DownloadTrack()
        {
            //Download
            bool bFlag = (bool)DownloadFileHepler.Start(TidalStream.Url,
                                FilePath,
                                RetryNum: 3,
                                UpdateFunc: UpdateDownloadNotify,
                                CompleteFunc: CompleteDownloadNotify,
                                ErrFunc: ErrDownloadNotify);
            //Err
            if (!bFlag)
            {
                Errlabel = "Download Failed!";
                Progress.IsErr = true;
                Progress.Errlabel = Errlabel;
                return;
            }

            try
            {
                //Decrypt / Set MetaData
                Tool.DecryptTrackFile(TidalStream, FilePath);
                var tfile = TagLib.File.Create(FilePath);
                tfile.Tag.Album = TidalTrack.Album.Title;
                tfile.Tag.Track = (uint)Index;
                tfile.Tag.Title = TidalTrack.Title;
                tfile.Tag.AlbumArtists = new string[1] { TidalTrack.Artist.Name };
                tfile.Tag.Copyright = TidalTrack.CopyRight;
                tfile.Save();
            }
            catch
            {
                Errlabel = "Decrypt-SetMetaData Failed!";
                Progress.IsErr = true;
                Progress.Errlabel = Errlabel;
                return;
            }
        }

        public bool UpdateDownloadNotify(long lTotalSize, long lAlreadyDownloadSize, long lIncreSize, object data)
        {
            Progress.Update(lAlreadyDownloadSize, lTotalSize);
            UpdataFunc(this);
            if (Progress.IsCancle)
                return false;
            return true;
        }

        public void CompleteDownloadNotify(long lTotalSize, object data)
        {
            Progress.Update(lTotalSize, lTotalSize);
            Progress.IsComplete = true;
            UpdataFunc(this);
        }

        public void ErrDownloadNotify(long lTotalSize, long lAlreadyDownloadSize, string sErrMsg, object data)
        {
            Progress.IsErr = true;
            UpdataFunc(this);
        }
        #endregion
    }
}
