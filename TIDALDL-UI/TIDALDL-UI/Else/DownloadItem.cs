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
        public Album TidalAlbum { get; set; }
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
        public byte[] Cover { get; set; }
        public string CoverPath { get; set; }

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

        public DownloadItem(int index, string basePath, UpdateNotify Func, Track track = null, string quality = "LOW", Video video = null, string resolution = "720", byte[] cover = null, string coverPath = null, Album album = null)
        {
            TidalAlbum       = album;
            TidalVideo       = video;
            TidalTrack       = track;
            Quality          = quality;
            Resolution       = resolution;
            BasePath         = basePath;
            Index            = index;
            Errlabel         = "";
            Progress         = new ProgressHelper();
            UpdataFunc       = Func;
            Cover            = cover;
            CoverPath        = coverPath;

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
                else if (TidalVideoUrls == null)
                    return "Get DownloadUrl Err!";
                FilePath = BasePath + '\\' + Tool.GetVideoFileName(TidalVideo);
            }
            return null;
        }

        #region Method
        public void Cancel()
        {
            Progress.IsCanceled = true;
        }
            
        public void Start()
        {
            if (ThreadTool.GetThreadNum() <= 0)
                ThreadTool.SetThreadNum(int.Parse(Config.ThreadNum()));
            ThreadTool.AddWork(ThreadFuncDownload);
        }

        public bool MergerTsFiles(string sPath, string sToFile)
        {
            try
            {
                string[] sFileNames = PathHelper.GetFileNames(sPath);
                List<string> sList = new List<string>();
                foreach (string item in sFileNames)
                {
                    if (item.IndexOf(".ts") < 0)
                        continue;
                    sList.Add(item);
                }

                return FFmpegHelper.MergerByFiles(sList.ToArray(), sToFile);
            }
            catch
            {
                return false;
            }
        }
        #endregion


        #region Thread
        public void ThreadFuncDownload(object data)
        {
            if (Progress.IsCanceled)
                return;

            //Prepare
            Errlabel = Prepare();
            if (Errlabel.IsNotBlank())
            {
                Progress.Errlabel = Errlabel;
                Progress.IsErr    = true;
                UpdataFunc(this);
                return;
            }

            if (sType == "Track")
                DownloadTrack();
            if (sType == "Video")
                DownloadVideo();


        }

        public void DownloadVideo()
        {
            string sTmpDir = BasePath + '\\' + PathHelper.ReplaceLimitChar(TidalVideo.Title, "-") + "TMP" + RandHelper.GetIntRandom(5, 9, 0);
            try
            {
                if (Directory.Exists(sTmpDir))
                    Directory.Delete(sTmpDir, true);
                PathHelper.Mkdirs(sTmpDir);

                long lCount = TidalVideoUrls.Count();
                for (int i = 0; i < lCount; i++)
                {
                    string sUrl = TidalVideoUrls[i];
                    string sName = sTmpDir + '\\' + (100000 + i + 1).ToString() + ".ts";
                    bool bFlag = (bool)DownloadFileHepler.Start(sUrl, sName, Timeout:9999*1000);
                    if (bFlag == false)
                    {
                        Progress.Errlabel = "Download failed!";
                        goto ERR_POINT;
                    }

                    Progress.Update(i + 1, lCount);
                    if (Progress.IsCanceled)
                        goto CANCEL_POINT;
                }
                if (!MergerTsFiles(sTmpDir + '\\', FilePath))
                {
                    Progress.Errlabel = "FFmpeg merger err!";
                    goto ERR_POINT;
                }

                Progress.Update(lCount, lCount);
                Progress.IsComplete = true;
                UpdataFunc(this);

            CANCEL_POINT:
                if (Directory.Exists(sTmpDir))
                    Directory.Delete(sTmpDir, true);
                return;
            }
            catch(Exception e)
            {
                Progress.Errlabel = "Err!" + e.Message;
            }

        ERR_POINT:
            Progress.IsErr = true;
            UpdataFunc(this);
            if (Directory.Exists(sTmpDir))
                Directory.Delete(sTmpDir, true);
        }
        
        public void DownloadTrack()
        {
            // Check if the track was existing
            if (System.IO.File.Exists(FilePath))
            {
                Errlabel = "Existing";
                goto UPDATE_RETURN;
            }
                

            //Download
            bool bFlag = (bool)DownloadFileHepler.Start(TidalStream.Url,
                                FilePath,
                                RetryNum: 3,
                                Timeout: 99999 * 1000,
                                UpdateFunc: UpdateDownloadNotify,
                                CompleteFunc: CompleteDownloadNotify,
                                ErrFunc: ErrDownloadNotify);
            //Err
            if (!bFlag)
            {
                Errlabel = "Download failed!";
                Progress.IsErr = true;
                goto UPDATE_RETURN;
            }

            if(!Tool.DecryptTrackFile(TidalStream, FilePath))
            {
                Errlabel = "Decrypt Failed!";
                Progress.IsErr = true;
                goto UPDATE_RETURN;
            }

            string sLabel = Tool.SetMetaData(FilePath, TidalAlbum, TidalTrack, CoverPath);
            if(sLabel.IsNotBlank())
            {
                Errlabel = "SetMetaData Failed! " + sLabel;
                Progress.IsErr = true;
                goto UPDATE_RETURN;
            }

        UPDATE_RETURN:
            if(!Progress.IsErr)
                Progress.IsComplete = true;

            Progress.Errlabel = Errlabel;
            UpdataFunc(this);
        }

        public bool UpdateDownloadNotify(long lTotalSize, long lAlreadyDownloadSize, long lIncreSize, object data)
        {
            Progress.Update(lAlreadyDownloadSize, lTotalSize);
            if (Progress.IsCanceled)
                return false;
            return true;
        }

        public void CompleteDownloadNotify(long lTotalSize, object data)
        {
            Progress.Update(lTotalSize, lTotalSize);
        }

        public void ErrDownloadNotify(long lTotalSize, long lAlreadyDownloadSize, string sErrMsg, object data)
        {
            Progress.IsErr = true;
        }
        #endregion
    }
}
