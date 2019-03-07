using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using AIGS.Helper;
using System.Threading;
using Tidal;
using System.Collections.ObjectModel;
using System.IO;

namespace TIDALDL_UI
{
    public class Downloader
    {
        private Thread MainThread;
        private ThreadHelper ThreadList;
        private object LockForMain;

        public Downloader()
        {
            MainThread  = ThreadHelper.Start(MainThreadFunc);
            LockForMain = new object();
        }

        #region Tool
        public bool ChangeThreadListNum(int iNum)
        {
            if (iNum <= 0)
                return false;
            if (ThreadList == null)
            {
                ThreadList = new ThreadHelper(iNum);
                return true;
            }

            if (!ThreadList.IsAllFree())
                return false;

            if (ThreadList.GetCount() == iNum)
                return true;

            ThreadList = new ThreadHelper(iNum);
            return true;
        }

        public string GetFilePath(MainItem main, SubItem sub)
        {
            string sRet = Para.Config.OutputDir + '\\' + main.Type + '\\' + main.Name + '\\' + AIGS.Helper.PathHelper.ReplaceLimitChar(sub.Name,"-") + ".m4a";
            return sRet;
        }

        public void ReadLoadSubList(MainItem main)
        {
            if(main.Type == "ALBUM")
            {
                ObservableCollection<Track> pList = TidalTool.GetAlbumTracks(((Album)main.data).ID.ToString(), true, eQuality:Para.Config.Quality);
                for (int i = 0; i < pList.Count; i++)
                {
                    if (pList[i].StreamUrl == null)
                        continue;
                    ((Track)main.SubList[i].data).StreamUrl = pList[i].StreamUrl;
                    main.SubList[i].DownloadUrl             = pList[i].StreamUrl;
                    main.SubList[i].TotalSize               = pList[i].StreamUrl.FileSize;
                    main.TotalSize                         += pList[i].StreamUrl.FileSize;
                }
            }
        }
        #endregion

        public void MainThreadFunc(object[] data)
        {
            
            while(true)
            {
                foreach (MainItem main in Para.MainItems)
                {
                    if (main.Status != AIGS.Common.Status.Wait)
                        continue;

                    ChangeThreadListNum(Para.Config.ThreadNum);
                    ReadLoadSubList(main);
                    foreach (SubItem sub in main.SubList)
                    {
                        ThreadList.ThreadStartWait(SubThreadFunc, 0, main, sub);
                    }
                    ThreadList.WaitAll();
                    main.Status = AIGS.Common.Status.Success;
                }
                Thread.Sleep(1000);
            }
        }

        public void SubThreadFunc(object[] paras)
        {
            MainItem main  = (MainItem)paras[0];
            SubItem sub    = (SubItem)paras[1];
            string sPath   = GetFilePath(main, sub);

            //CreatDir
            var di = new DirectoryInfo(Path.GetDirectoryName(sPath));
            if (!di.Exists)
                di.Create();

            if (sub.Type == "TRACK")
            {
                StreamUrl url = (StreamUrl)sub.DownloadUrl;
                if (url == null)
                {
                    sub.Status = AIGS.Common.Status.Err;
                    return;
                }
                DownloadFileHepler.Start(url.Url,
                                        sPath,
                                        Para.MainForm, 
                                        paras,
                                        UpdateDownloadNotify,
                                        CompleteDownloadNotify,
                                        ErrDownloadNotify,
                                        ContentType: null,
                                        RetryNum:3,
                                        UserAgent: null);
            }
            sub.Status = AIGS.Common.Status.Success;
        }

        void UpdateDownloadNotify(long lTotalSize, long lAlreadyDownloadSize, long lIncreSize,  object data)
        {
            object[] paras = (object[])data;
            MainItem main  = (MainItem)paras[0];
            SubItem sub    = (SubItem)paras[1];

            sub.DownloadSize = lAlreadyDownloadSize;
            sub.Percentage   = (int)(sub.DownloadSize * 100 / lTotalSize);

            lock (LockForMain)
            {
                //检查子项是否获取文件大小失败
                if (sub.TotalSize <= 0)
                {
                    sub.TotalSize   = lTotalSize;
                    main.TotalSize += lTotalSize;
                }

                main.DownloadSize += lIncreSize;
                main.Percentage    = (int)(main.DownloadSize * 100 / main.TotalSize);
            }
        }

        void CompleteDownloadNotify(long lTotalSize, object data)
        {
            object[] paras = (object[])data;
            MainItem main  = (MainItem)paras[0];
            SubItem sub    = (SubItem)paras[1];

            sub.Status = AIGS.Common.Status.Success;
        }

        void ErrDownloadNotify(long lTotalSize, long lAlreadyDownloadSize, string sErrMsg, object data)
        {
            object[] paras = (object[])data;
            MainItem main  = (MainItem)paras[0];
            SubItem sub    = (SubItem)paras[1];

            sub.Status = AIGS.Common.Status.Err;
        }
    }
}
