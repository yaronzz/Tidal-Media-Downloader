using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Net;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using AIGS.Common;
using AIGS.Tools;
using AIGS.Helper;
using System.Threading;
namespace AlbumDownload
{
    class Program
    {
        /// 消息队列
        static Queue<string> m_Queue = new Queue<string>();
        static Thread m_ThreadQueue;

        //下载线程
        static ThreadHelper m_Thread;

        //下载等待
        static EventWaitHelper m_WaitDownloadEvent;
        
        //其他
        static TidalTool.SoundQuality m_SoundQuality;
        static TidalTool.CountryCode m_CountryCode;
        static string m_SessionID;
        static string m_TargetDir;
        static DateTime m_DateTimeHandle;
        static string m_OutputDir;
        static int m_Index;
        static object m_Lock = new object();
        static List<string> m_ErrDownloadTracks = new List<string>();

        static void Main(string[] args)
        {
            //读取配置文件
            string sOutputDir = AIGS.Helper.ConfigHelper.GetValue("OutputDir", ".\\", "BASE", ".\\AlbumDL.ini");
            string sSessionID = AIGS.Helper.ConfigHelper.GetValue("SessionID", "", "BASE", ".\\AlbumDL.ini");
            string SoundQuality = AIGS.Helper.ConfigHelper.GetValue("SoundQuality", "LOSSLESS", "BASE", ".\\AlbumDL.ini");
            string sCountryCode = AIGS.Helper.ConfigHelper.GetValue("CountryCode", "US", "BASE", ".\\AlbumDL.ini");
            string sXmlDir = AIGS.Helper.ConfigHelper.GetValue("Website", "http://144.202.15.40", "BASE", ".\\AlbumDL.ini");

            m_SoundQuality = (TidalTool.SoundQuality)AIGS.Common.Convert.ConverStringToEnum(SoundQuality, typeof(TidalTool.SoundQuality), (int)TidalTool.SoundQuality.LOSSLESS);
            m_CountryCode = (TidalTool.CountryCode)AIGS.Common.Convert.ConverStringToEnum(sCountryCode, typeof(TidalTool.CountryCode), (int)TidalTool.CountryCode.US);
            m_SessionID = sSessionID;
            m_OutputDir = sOutputDir;
//#if DEBUG
//            List<string> aFiles = new List<string>() { "TidalTool.exe", "AIGS.dll", "Newtonsoft.Json.dll" };
//            UpdateVersionHelper.CreatUpdateVersionFile(aFiles);
//#endif
            //更新
            Console.WriteLine("================================================");
            Console.WriteLine("Version:".PadRight(15) + VersionHelper.GetSelfVersion());
            //if (UpdateVersionHelper.UpdateOnlineVersion(args, sXmlDir + "/TidalTool"))
            //    return;

            Console.WriteLine("OutputDir:".PadRight(15) + sOutputDir);
            Console.WriteLine("SessionID:".PadRight(15) + sSessionID);
            Console.WriteLine("CountryCode:".PadRight(15) + AIGS.Common.Convert.ConverEnumToString((int)m_CountryCode, typeof(TidalTool.CountryCode)));
            Console.WriteLine("SoundQuality:".PadRight(15) + AIGS.Common.Convert.ConverEnumToString((int)m_SoundQuality, typeof(TidalTool.SoundQuality)));

            if (string.IsNullOrEmpty(sSessionID))
            {
                Console.Write("No SessionID In {" + Path.GetFullPath(".\\TidalTool.ini") + "}");
                Console.ReadLine();
                return;
            }

            //启动消息队列线程
            m_Thread = new ThreadHelper(40);
            m_ThreadQueue = ThreadHelper.Start(Thread_QueueEvent);

            while (true)
            {
                Console.WriteLine("=====================Choice=====================");
                Console.WriteLine(" Enter '1' : Download Album.");
                Console.WriteLine(" Enter '2' : Download Track.");
                Console.WriteLine(" Enter '3' : Download PlayList.");
                Console.WriteLine(" Enter '4' : Download Albums From 'AlbumDL.ini'");
                Console.WriteLine("================================================");
                Console.Write("Please enter Choice:");

                int iChoice = AIGS.Common.Convert.ConverStringToInt(Console.ReadLine(), 0);
                switch (iChoice)
                {
                    case 1: GetAlbum(); break;
                    case 2: GetTrack(); break;
                    case 3: GetPlayList(); break;
                    case 4: GetAlbumsFromIniFile(); break;
                }

            }
        }

        static string GetAlbum(int in_ID = -999)
        {
            bool bHaveEntry = in_ID != -999 ? true : false;
            int iCount = bHaveEntry ? 1 : 100000;
            int iAlbumID;
            string sReturn = null;

            while (iCount-- > 0)
            {
                if (!bHaveEntry)
                {
                    Console.WriteLine("--------------------ALBUM-----------------------");
                    Console.Write("Enter AlbumID（Enter '0' go back）:");
                }
                iAlbumID = bHaveEntry ? in_ID : AIGS.Common.Convert.ConverStringToInt(Console.ReadLine(), 0);
                if (iAlbumID <= 0)
                    continue;

                //获取专辑信息
                Album aAlbumInfo = new Album();
                if (TidalTool.GetAlbumInfo(iAlbumID, ref aAlbumInfo) != 0)
                {
                    sReturn = "Get AlbumInfo Err!";
                    Console.WriteLine(sReturn);
                    continue;
                }
                Console.WriteLine("[AlbumTitle]:".PadRight(15) + aAlbumInfo.Title);
                Console.WriteLine("[SongNum   ]:".PadRight(15) + aAlbumInfo.NumberOfTracks);
                Console.WriteLine();

                //获取专辑歌曲
                List<Track> aTrackInfos = TidalTool.GetAlbumTracks(iAlbumID);
                if (aTrackInfos == null)
                {
                    sReturn = "Get TrackInfos Err!";
                    Console.WriteLine("Get TrackInfos Err!");
                    continue;
                }

                //创建输出目录
                m_TargetDir = m_OutputDir + "\\Album\\" + AIGS.Helper.PathHelper.ReplaceLimitChar(aAlbumInfo.Title, "-");
                if (Directory.Exists(m_TargetDir) == false)
                    Directory.CreateDirectory(m_TargetDir);
                for (int i = 0; aAlbumInfo.NumberOfVolumes > 1 && i < aAlbumInfo.NumberOfVolumes; i++)
                {
                    string VolumeDir = m_TargetDir + "\\Volume" + (i + 1);
                    if (Directory.Exists(VolumeDir) == false)
                        Directory.CreateDirectory(VolumeDir);
                }
                    

                //写信息
                string sText = TidalTool.ConvertAlbumInfoToString(aAlbumInfo, aTrackInfos);
                File.WriteAllText(m_TargetDir + "\\AlbumInfo.txt", sText);

                //下载封面
                if (!String.IsNullOrWhiteSpace(aAlbumInfo.ConvrUrl))
                {
                    string sConverPath = m_TargetDir + "\\" + AIGS.Helper.PathHelper.ReplaceLimitChar(aAlbumInfo.Title, "-") + ".jpg";
                    if (NetHelper.DownloadFile(aAlbumInfo.ConvrUrl, sConverPath) != 0)
                    {
                        sReturn = "Download Conver Failed!";
                        Console.WriteLine("[Err       ]:".PadRight(15) + sReturn);
                    }
                }

                //下载
                m_Index = 0;
                m_DateTimeHandle = DateTime.Now;
                m_ErrDownloadTracks = new List<string>();
                m_WaitDownloadEvent = new EventWaitHelper(true, aAlbumInfo.NumberOfTracks);
                for (int i = 0; i < aAlbumInfo.NumberOfTracks; i++)
                {
                    m_Thread.ThreadStartWait(Thread_DownloadEvent, aTrackInfos[i]);
                }
                //等待
                m_WaitDownloadEvent.WaitOne();
                Thread.Sleep(3000);
                Console.WriteLine("");

                while (true)
                {
                    if (m_ErrDownloadTracks.Count <= 0)
                        break;

                    Console.WriteLine("--------------------Retry-----------------------");
                    Console.Write("Some Tracks Download Err, Is Need Retry?（Enter '1' to retry）:");
                    if (Console.ReadLine() == "1")
                    {
                        m_WaitDownloadEvent = new EventWaitHelper(true, m_ErrDownloadTracks.Count);
                        for (int i = 0; i < aAlbumInfo.NumberOfTracks; i++)
                        {
                            if (!m_ErrDownloadTracks.Contains(aTrackInfos[i].Title))
                                continue;

                            m_Thread.ThreadStartWait(Thread_DownloadEvent, aTrackInfos[i]);
                        }
                        //等待
                        m_WaitDownloadEvent.WaitOne();
                        Thread.Sleep(3000);
                        Console.WriteLine("");
                    }
                    else
                        break;
                }

            }

            return sReturn;
        }


        static void GetTrack()
        {
            while (true)
            {
                Console.WriteLine("--------------------TRACK-----------------------");
                Console.Write("Enter TrackID（Enter '0' go back）:");
                int iTrackID = AIGS.Common.Convert.ConverStringToInt(Console.ReadLine(), 0);
                if (iTrackID == 0)
                    return;

                //获取曲目信息
                Track aTrackInfo = new Track();
                if (TidalTool.GetTrackInfo(iTrackID, ref aTrackInfo) != 0)
                {
                    Console.WriteLine("Get TrackInfo Err!");
                    continue;
                }
                Console.WriteLine("[TrackTitle ]:".PadRight(15) + aTrackInfo.Title);
                Console.WriteLine("[Duration   ]:".PadRight(15) + aTrackInfo.Duration);
                Console.WriteLine("[TrackNumber]:".PadRight(15) + aTrackInfo.TrackNumber);
                Console.WriteLine("[Version    ]:".PadRight(15) + aTrackInfo.Version);
                Console.WriteLine();

                //创建输出目录
                m_TargetDir = m_OutputDir + "\\Track\\";
                if (Directory.Exists(m_TargetDir) == false)
                    Directory.CreateDirectory(m_TargetDir);

                //下载
                m_Index = 0;
                m_DateTimeHandle = DateTime.Now;
                m_WaitDownloadEvent = new EventWaitHelper(true, 1);
                m_Thread.ThreadStart(Thread_DownloadEvent, aTrackInfo);

                //等待
                m_WaitDownloadEvent.WaitOne();
                Thread.Sleep(3000);
            }
        }



        static void GetPlayList()
        {
            while (true)
            {
                Console.WriteLine("------------------PLAY LIST---------------------");
                Console.Write("Enter uuid（Enter '0' go back）:");
                string sUuid = Console.ReadLine();
                if (sUuid == "0")
                    return;

                //获取曲目信息
                PlayList aListInfo = new PlayList();
                if (TidalTool.GetPlayList(sUuid, ref aListInfo) != 0)
                {
                    Console.WriteLine("Get PlayListInfo Err!");
                    continue;
                }
                Console.WriteLine("[Title         ]:".PadRight(15) + aListInfo.Title);
                Console.WriteLine("[Type          ]:".PadRight(15) + aListInfo.Type);
                Console.WriteLine("[Public        ]:".PadRight(15) + aListInfo.PublicPlaylist);
                Console.WriteLine("[NumberOfTracks]:".PadRight(15) + aListInfo.NumberOfTracks);
                Console.WriteLine("[NumberOfVideos]:".PadRight(15) + aListInfo.NumberOfVideos);
                Console.WriteLine("[Duration      ]:".PadRight(15) + aListInfo.Duration);
                Console.WriteLine();

                //获取歌曲
                List<Track> aTrackInfos = TidalTool.GetPlayListTracks(sUuid, aListInfo.NumberOfTracks);
                if (aTrackInfos == null)
                {
                    Console.WriteLine("Get TrackInfos Err!");
                    continue;
                }

                //创建输出目录
                m_TargetDir = m_OutputDir + "\\PlayList\\" + AIGS.Helper.PathHelper.ReplaceLimitChar(aListInfo.Title, "-");
                if (Directory.Exists(m_TargetDir) == false)
                    Directory.CreateDirectory(m_TargetDir);

                //写信息
                string sText = TidalTool.ConvertPlayListInfoToString(aListInfo, aTrackInfos);
                File.WriteAllText(m_TargetDir + "\\PlayListInfo.txt", sText);

                //下载封面
                if (!String.IsNullOrWhiteSpace(aListInfo.ImageUrl))
                {
                    string sConverPath = m_TargetDir + "\\" + AIGS.Helper.PathHelper.ReplaceLimitChar(aListInfo.Title, "-") + ".jpg";
                    if (NetHelper.DownloadFile(aListInfo.ImageUrl, sConverPath) != 0)
                        Console.WriteLine("[Err           ]:".PadRight(15) + "Download Conver Failed!");
                }

                //下载
                m_Index = 0;
                m_DateTimeHandle = DateTime.Now;
                m_WaitDownloadEvent = new EventWaitHelper(true, aTrackInfos.Count);
                for (int i = 0; i < aTrackInfos.Count; i++)
                {
                    m_Thread.ThreadStartWait(Thread_DownloadEvent, aTrackInfos[i]);
                }

                //等待
                m_WaitDownloadEvent.WaitOne();
                Thread.Sleep(3000);
            }
        }

        static void GetAlbumsFromIniFile()
        {
            Console.WriteLine("--------------DL ALBUMS FROM INI----------------");
            string sString = AIGS.Helper.ConfigHelper.GetValue("Albums", ".\\", "DOWNLOADLIST", ".\\AlbumDL.ini");
            if(String.IsNullOrWhiteSpace(sString))
            {
                Console.WriteLine("No 'DOWNLOADLIST-Albums' Para in ConfigFile!");
                return;
            }

            HashSet<int> pIDList = new HashSet<int>();
            string[] sParts = sString.Split(',');
            foreach (string item in sParts)
            {
                if (pIDList.Contains(AIGS.Common.Convert.ConverStringToInt(item)))
                    continue;

                pIDList.Add(AIGS.Common.Convert.ConverStringToInt(item));
            }

            Console.WriteLine("[AlbumNum ]:".PadRight(15) + pIDList.Count);
            for (int i = 0; i < pIDList.Count; i++)
            {
                int iID = pIDList.ElementAt(i);
                Console.WriteLine("------" + i + "、" + iID + "------");
                GetAlbum(iID);
            }
        }






        #region 下载

        static void Thread_DownloadEvent(object data)
        {
            Track Info = (Track)data;
            string StreamUrl = TidalTool.GetStreamUrl(Info.ID, m_SessionID, m_SoundQuality, m_CountryCode);
            string sReturnMsg = "";
            string SongFilePath = "";
            string VolumeDir = m_TargetDir + "\\Volume" + Info.VolumeNumber;
            if (Directory.Exists(VolumeDir) == false)
                SongFilePath = m_TargetDir + "\\" + PathHelper.ReplaceLimitChar(Info.Title, "-") + ".m4a";
            else
                SongFilePath = VolumeDir + "\\" + PathHelper.ReplaceLimitChar(Info.Title, "-") + ".m4a";

            if (String.IsNullOrWhiteSpace(StreamUrl))
            {
                sReturnMsg = "[ERR]".PadRight(12) + Info.Title + "(Get StreamUrl Err!)";
                m_ErrDownloadTracks.Add(Info.Title);
            }
            else
            {
                string sRet = Info.Title;
                if (AIGS.Helper.NetHelper.DownloadFile(StreamUrl, SongFilePath) != 0)
                {
                    sReturnMsg = "[ERR]".PadRight(12) + Info.Title + "(Download Err!)";
                    m_ErrDownloadTracks.Add(Info.Title);
                }
                else
                {
                    File.SetLastWriteTime(SongFilePath, m_DateTimeHandle.AddMinutes(Info.TrackNumber));
                    File.SetCreationTime(SongFilePath, m_DateTimeHandle.AddMinutes(Info.TrackNumber));
                    sReturnMsg = "[SUCCESS]".PadRight(12) + Info.Title;
                }
            }

            lock (m_Lock)
            {
                m_Queue.Enqueue(sReturnMsg);
            }

            Thread.Sleep(1000);
            m_WaitDownloadEvent.Set();
        }

        #endregion

        #region 队列

        static void Thread_QueueEvent(object data)
        {
            while (true)
            {
                //没有任务，休息3秒钟  
                if (m_Queue.Count <= 0)
                {
                    Thread.Sleep(1000);
                    continue;
                }

                //从队列中取出  
                string Info = m_Queue.Dequeue();
                Console.WriteLine(m_Index.ToString().PadRight(3) + Info);
                m_Index++;
            }
        }
        #endregion
    }
}

