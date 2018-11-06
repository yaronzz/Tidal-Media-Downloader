using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Net;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
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
        static AlbumDL.SoundQuality m_SoundQuality;
        static AlbumDL.CountryCode m_CountryCode;
        static string m_SessionID;
        static string m_TargetDir;
        static DateTime m_DateTimeHandle;
        static string m_OutputDir;
        static int m_Index;
        static object m_Lock = new object();

        static void Main(string[] args)
        {
            //读取配置文件
            string sOutputDir = AIGS.Helper.ConfigHelper.GetValue("OutputDir", ".\\", "BASE", ".\\AlbumDL.ini");
            string sSessionID = AIGS.Helper.ConfigHelper.GetValue("SessionID", "", "BASE", ".\\AlbumDL.ini");
            string SoundQuality = AIGS.Helper.ConfigHelper.GetValue("SoundQuality", "LOSSLESS", "BASE", ".\\AlbumDL.ini");
            string sCountryCode = AIGS.Helper.ConfigHelper.GetValue("CountryCode", "US", "BASE", ".\\AlbumDL.ini");
            string sXmlDir = AIGS.Helper.ConfigHelper.GetValue("Website", "http://144.202.15.40", "BASE", ".\\AlbumDL.ini");

            m_SoundQuality = (AlbumDL.SoundQuality)AIGS.Common.Convert.ConverStringToEnum(SoundQuality, typeof(AlbumDL.SoundQuality), (int)AlbumDL.SoundQuality.LOSSLESS);
            m_CountryCode = (AlbumDL.CountryCode)AIGS.Common.Convert.ConverStringToEnum(sCountryCode, typeof(AlbumDL.CountryCode), (int)AlbumDL.CountryCode.US);
            m_SessionID = sSessionID;
            m_OutputDir = sOutputDir;
//#if DEBUG
//            List<string> aFiles = new List<string>() { "AlbumDL.exe", "AIGS.dll", "Newtonsoft.Json.dll" };
//            UpdateVersionHelper.CreatUpdateVersionFile(aFiles);
//#endif
            //更新
            Console.WriteLine("================================================");
            Console.WriteLine("Version:".PadRight(15) + VersionHelper.GetSelfVersion());
            if (UpdateVersionHelper.UpdateOnlineVersion(args, sXmlDir + "/AlbumDL"))
                return;

            Console.WriteLine("OutputDir:".PadRight(15) + sOutputDir);
            Console.WriteLine("SessionID:".PadRight(15) + sSessionID);
            Console.WriteLine("CountryCode:".PadRight(15) + AIGS.Common.Convert.ConverEnumToString((int)m_CountryCode, typeof(AlbumDL.CountryCode)));
            Console.WriteLine("SoundQuality:".PadRight(15) + AIGS.Common.Convert.ConverEnumToString((int)m_SoundQuality, typeof(AlbumDL.SoundQuality)));

            if (string.IsNullOrEmpty(sSessionID))
            {
                Console.Write("No SessionID In {" + Path.GetFullPath(".\\AlbumDL.ini") + "}");
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
                Console.WriteLine(" Enter '4' : Download ID-File.");
                Console.WriteLine("================================================");
                Console.Write("Please enter Choice:");

                int iChoice = AIGS.Common.Convert.ConverStringToInt(Console.ReadLine(), 0);
                switch (iChoice)
                {
                    case 1: GetAlbum(); break;
                    case 2: GetTrack(); break;
                    case 3: GetPlayList(); break;
                    case 4: GetIDFile(); break;
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
                AlbumDL.AlbumInfo aAlbumInfo = new AlbumDL.AlbumInfo();
                if (AlbumDL.GetAlbumInfo(iAlbumID, ref aAlbumInfo) != 0)
                {
                    sReturn = "Get AlbumInfo Err!";
                    Console.WriteLine(sReturn);
                    continue;
                }
                Console.WriteLine("[AlbumTitle]:".PadRight(15) + aAlbumInfo.Title);
                Console.WriteLine("[SongNum   ]:".PadRight(15) + aAlbumInfo.NumberOfTracks);
                Console.WriteLine();

                //获取专辑歌曲
                List<AlbumDL.TrackInfo> aTrackInfos = AlbumDL.GetAlbumTracks(iAlbumID);
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
                string sText = AlbumDL.ConvertAlbumInfoToString(aAlbumInfo, aTrackInfos);
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
                m_WaitDownloadEvent = new EventWaitHelper(true, aAlbumInfo.NumberOfTracks);
                for (int i = 0; i < aAlbumInfo.NumberOfTracks; i++)
                {
                    m_Thread.ThreadStartWait(Thread_DownloadEvent, aTrackInfos[i]);
                }

                //等待
                m_WaitDownloadEvent.WaitOne();
                Thread.Sleep(3000);
                Console.WriteLine("");
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
                AlbumDL.TrackInfo aTrackInfo = new AlbumDL.TrackInfo();
                if (AlbumDL.GetTrackInfo(iTrackID, ref aTrackInfo) != 0)
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
                AlbumDL.PlayListInfo aListInfo = new AlbumDL.PlayListInfo();
                if (AlbumDL.GetPlayList(sUuid, ref aListInfo) != 0)
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
                List<AlbumDL.TrackInfo> aTrackInfos = AlbumDL.GetPlayListTracks(sUuid, aListInfo.NumberOfTracks);
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
                string sText = AlbumDL.ConvertPlayListInfoToString(aListInfo, aTrackInfos);
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




        static void GetIDFile()
        {
            while (true)
            {
                Console.WriteLine("-------------------ID-FILE----------------------");
                Console.Write("Enter Path（Enter '0' go back）:");
                string sFilePath = Console.ReadLine();
                //string sFilePath = "e:\\fff.txt";
                string sInfo = "";

                if (String.IsNullOrWhiteSpace(sFilePath))
                {
                    Console.WriteLine("Get FilePath Err!");
                    continue;
                }
                if (!File.Exists(sFilePath))
                {
                    Console.WriteLine("File Not Exist!");
                    continue;
                }

                //先处理专辑
                sInfo += "[Album]\r\n";
                List<string> pAlbumList = AlbumDL.GetDownloadListFormFile(sFilePath, "Album");
                for (int i = 0; i < pAlbumList.Count; i++)
                {
                    //获取专辑信息
                    int iAlbumID = AIGS.Common.Convert.ConverStringToInt(pAlbumList[i], -999);
                    string sRet = GetAlbum(iAlbumID);
                    if (String.IsNullOrWhiteSpace(sRet))
                        sInfo += pAlbumList[i].PadRight(15) + "\r\n";
                    else
                        sInfo += pAlbumList[i].PadRight(15) + "(" + sRet + ")\r\n";

                }

                //保存信息
                m_TargetDir = m_OutputDir + "\\IDFile\\";
                if (Directory.Exists(m_TargetDir) == false)
                    Directory.CreateDirectory(m_TargetDir);

                string sPath = Path.GetDirectoryName(sFilePath);
                string sName = Path.GetFileNameWithoutExtension(sFilePath);
                File.Delete(sFilePath);
                File.Copy(sFilePath, m_TargetDir + sName + ".txt");
                File.WriteAllText(m_TargetDir + sName + "-Log.txt", sInfo);
            }
        }





        #region 下载

        static void Thread_DownloadEvent(object data)
        {
            AlbumDL.TrackInfo Info = (AlbumDL.TrackInfo)data;
            string StreamUrl = AlbumDL.GetStreamUrl(Info.ID, m_SessionID, m_SoundQuality, m_CountryCode);
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
            }
            else
            {
                string sRet = Info.Title;
                if (AIGS.Helper.NetHelper.DownloadFile(StreamUrl, SongFilePath) != 0)
                    sReturnMsg = "[ERR]".PadRight(12) + Info.Title + "(Download Err!)";
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

