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
        static Queue<string> m_Queue = new Queue<string>();
        static Thread m_ThreadQueue;
        static ThreadHelper m_Thread;
        static string m_AlbumDir;
        static int m_DownladCount;
        static DateTime m_DateTimeHandle;
        static string m_SessionID;
        static AlbumDL.SoundQuality m_eQua;
        static AlbumDL.CountryCode m_eCode;
        static void Main(string[] args)
        {
            //读取配置文件
            string sOutputDir   = AIGS.Helper.ConfigHelper.GetValue("OutputDir", ".\\", "BASE", ".\\AlbumDL.ini");
            string sSessionID   = AIGS.Helper.ConfigHelper.GetValue("SessionID", "", "BASE", ".\\AlbumDL.ini");
            string SoundQuality = AIGS.Helper.ConfigHelper.GetValue("SoundQuality", "LOSSLESS", "BASE", ".\\AlbumDL.ini");
            string sCountryCode = AIGS.Helper.ConfigHelper.GetValue("CountryCode", "US", "BASE", ".\\AlbumDL.ini");
            string sXmlDir      = AIGS.Helper.ConfigHelper.GetValue("Website", "http://119.29.24.117:80", "BASE", ".\\AlbumDL.ini");

            AlbumDL.AlbumInfo m_AlbumInfo = new AlbumDL.AlbumInfo();
            m_eQua = (AlbumDL.SoundQuality)AIGS.Common.Convert.ConverStringToEnum(SoundQuality, typeof(AlbumDL.SoundQuality), (int)AlbumDL.SoundQuality.LOSSLESS);
            m_eCode = (AlbumDL.CountryCode)AIGS.Common.Convert.ConverStringToEnum(sCountryCode, typeof(AlbumDL.CountryCode), (int)AlbumDL.CountryCode.US);
            m_SessionID = sSessionID;
#if DEBUG
            //sSessionID = null;
            //sSessionID = "4c165e71-8748-47bf-94b9-7341616836a1";
            //eQua = AlbumDL.SoundQuality.LOW;

            //List<string> aFiles = new List<string>() { "AlbumDL.exe", "AIGS.dll", "Newtonsoft.Json.dll" };
            //UpdateVersionHelper.CreatAutoUpdateFile(aFiles);
            
            //sXmlDir = @"E:\working\通用库\AIGTool\Album-DL\code\AlbumDL\bin";
#endif
            //更新
            Console.WriteLine("================================================");
            //Console.WriteLine("Version:".PadRight(15) + VersionHelper.GetSelfVersion());
            //if (UpdateVersionHelper.UpdateOnlineVersion(args, sXmlDir + "/AlbumDL"))
            //    return;

            Console.WriteLine("OutputDir:".PadRight(15) + sOutputDir);
            Console.WriteLine("SessionID:".PadRight(15) + sSessionID);
            Console.WriteLine("CountryCode:".PadRight(15) + AIGS.Common.Convert.ConverEnumToString((int)m_eCode, typeof(AlbumDL.CountryCode)));
            Console.WriteLine("SoundQuality:".PadRight(15) + AIGS.Common.Convert.ConverEnumToString((int)m_eQua, typeof(AlbumDL.SoundQuality)));
            
            if (string.IsNullOrEmpty(sSessionID))
            {
                Console.Write("No SessionID In {" + Path.GetFullPath(".\\AlbumDL.ini") + "}");
                Console.ReadLine();
                return;
            }

            //启动消息队列线程
            m_Thread = new ThreadHelper(1);
            m_ThreadQueue = ThreadHelper.Start(Thread_QueueEvent);

            while (true)
            {
                Console.WriteLine("-----------------------------------------------");
                Console.Write("Please enter AlbumID:");
                int iID = Convert.ToInt32((Console.ReadLine()));
                Console.WriteLine("------------------------------------------------");

                //获取专辑信息
                if (AlbumDL.GetAlbumInfo(iID, ref m_AlbumInfo) != 0)
                {
                    Console.WriteLine("Get AlbumInfo Err!");
                    continue;
                }
                Console.WriteLine("[AlbumTitle]:".PadRight(15) + m_AlbumInfo.Title);
                Console.WriteLine("[SongNum   ]:".PadRight(15) + m_AlbumInfo.NumberOfTracks);
                Console.WriteLine();

                //获取专辑歌曲
                List<AlbumDL.TrackInfo> aTrackInfos = AlbumDL.GetAlbumTracks(iID);
                if (aTrackInfos == null)
                {
                    Console.WriteLine("Get TrackInfos Err!");
                    continue;
                }

                //创建输出目录
                m_AlbumDir = sOutputDir + '\\' + AIGS.Helper.PathHelper.ReplaceLimitChar(m_AlbumInfo.Title, "-");
                if (Directory.Exists(m_AlbumDir) == false)
                    Directory.CreateDirectory(m_AlbumDir);

                //写信息
                string sText = AlbumDL.ConvertAlbumInfoToString(m_AlbumInfo, aTrackInfos);
                File.WriteAllText(m_AlbumDir + "\\AlbumInfo.txt", sText);

                //下载
                m_DownladCount = 0;
                m_DateTimeHandle = DateTime.Now;
                for (int i = 0; i < m_AlbumInfo.NumberOfTracks; i++)
                {
                    m_Thread.ThreadStart(Thread_DownloadEvent, aTrackInfos[i]);
                }

                //等待
                while(!m_Thread.IsAllFree())
                {
                    Thread.Sleep(3000);
                }
            }
        }

        
        #region 下载

        static void Thread_DownloadEvent(object data)
        {
            AlbumDL.TrackInfo Info = (AlbumDL.TrackInfo)data;
            string SongFilePath = m_AlbumDir + "\\" + PathHelper.ReplaceLimitChar(Info.Title, "-") + ".m4a";
            string DlUrl = AlbumDL.GetStreamUrl(Info.ID, m_SessionID, m_eQua, m_eCode);

            string sRet = Info.Title;
            if (AIGS.Helper.NetHelper.DownloadFile(DlUrl, SongFilePath) != 0)
                sRet = Info.Title + "(Download Err!)";
            else
            {
                File.SetLastWriteTime(SongFilePath, m_DateTimeHandle.AddMinutes(Info.TrackNumber));
                File.SetCreationTime(SongFilePath, m_DateTimeHandle.AddMinutes(Info.TrackNumber));
            }

            m_Queue.Enqueue(sRet);
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
                    Thread.Sleep(3000);
                    continue;
                }

                //从队列中取出  
                string Info = m_Queue.Dequeue();
                Console.WriteLine(("[" + (m_DownladCount + 1) + "]").PadRight(8) + Info);
                m_DownladCount++;
            }
        }
        #endregion
    }
}
