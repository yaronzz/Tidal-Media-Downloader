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

        /// <summary>
        /// Item Para - BasePath | FilePath | Track Quality | Title | Duration | Type
        /// </summary>
        public string BasePath { get; set; }
        public string FilePath { get; set; }
        public string Quality { get; set; }
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

        public DownloadItem(int index, Track track, string quality, string basePath, UpdateNotify Func)
        {
            TidalTrack       = track;
            Quality          = quality;
            Title            = track.Title;
            Duration         = track.SDuration;
            BasePath         = basePath;
            sType            = "Track";
            Index            = index;
            Errlabel         = "";
            Progress         = new ProgressHelper();
            UpdataFunc       = Func;
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

            //Download
            bool bFlag = (bool)DownloadFileHepler.Start(TidalStream.Url,
                                FilePath,
                                RetryNum:3,
                                UpdateFunc: UpdateDownloadNotify,
                                CompleteFunc: CompleteDownloadNotify,
                                ErrFunc: ErrDownloadNotify);
            //Err
            if(!bFlag)
            {
                Errlabel = "Download Failed!";
                Progress.IsErr = true;
                Progress.Errlabel = Errlabel;
                return;
            }

            try
            {
                //Set MetaData
                var tfile = TagLib.File.Create(FilePath);
                tfile.Tag.Album = TidalTrack.Album.Title;
                tfile.Tag.Track = (uint)Index;
                tfile.Tag.Title = TidalTrack.Title;
                tfile.Tag.AlbumArtists = new string[1] { TidalTrack.Artist.Name };
                tfile.Tag.Copyright = TidalTrack.CopyRight;
                tfile.Save();
            }
            catch { }
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
