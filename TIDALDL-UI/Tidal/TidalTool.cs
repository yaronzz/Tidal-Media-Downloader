using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using AIGS.Helper;
using System.Collections.ObjectModel;

namespace Tidal
{
    public enum Quality
    {
        LOW,
        HIGH,
        LOSSLESS,
        NONE,
    };


    public class TidalTool
    {
        public  static Account User;
        public  static string Errmsg;
        private static string Url = "https://api.tidalhifi.com/v1/";

        #region Common Tool
        /// <summary>
        /// http get 
        /// </summary>
        private static string Get(string Path, Dictionary<string, string> Paras = null, int RetryNum = 0)
        {
            if(User == null)
            {
                Errmsg = "Not login!";
                return null;
            }

            string sParams = "?countryCode=" + User.CountryCode;
            for (int i = 0; Paras != null && i < Paras.Count; i++)
            {
                sParams += "&" + Paras.ElementAt(i).Key + "=" + Paras.ElementAt(i).Value;
            }

            string sRet       = (string)HttpHelper.GetOrPost(Url + Path + sParams, Header: "X-Tidal-SessionId:" + User.SessionID, Retry:RetryNum);
            string sStatus    = JsonHelper.GetValue(sRet, "status");
            string sSubStatus = JsonHelper.GetValue(sRet, "subStatus");

            if (!string.IsNullOrEmpty(sStatus) && sStatus == "404" && sSubStatus == "2001")
                Errmsg = JsonHelper.GetValue(sRet, "userMessage") + ". This might be region-locked.";
            if (!string.IsNullOrEmpty(sStatus) && sStatus != "200")
                Errmsg = "Get operation err!";

            return sRet;
        }

        /// <summary>
        /// string -> Enum
        /// </summary>
        public static Quality ConverStringToQuality(string sStr, Quality eDefault)
        {
            if (string.IsNullOrEmpty(sStr))
                return eDefault;
            return (Quality)AIGS.Common.Convert.ConverStringToEnum(sStr, typeof(Quality), (int)eDefault);
        }

        public static long GetTotalDownloadSize(object oData, string sType)
        {
            long lRet = 0;
            if(sType == "ALBUM")
            {
                Album album = (Album)oData;
                foreach (Track item in album.Tracks)
                {
                    lRet += DownloadFileHepler.GetFileLength(item.StreamUrl.Url);
                }
            }
            return lRet;
        }
        #endregion

        #region Get Album
        public static Album GetAlbum(string sID, bool bGetTracksUrl = false, string sQuality = null)
        {
            string sRet = Get("albums/" + sID);
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            Album aRet     = JsonHelper.ConverStringToObject<Album>(sRet);
            aRet.CovrUrl   = "https://resources.tidal.com/images/" + aRet.Cover.Replace('-', '/') + "/1280x1280.jpg";
            aRet.CoverData = (byte[])HttpHelper.GetOrPost(aRet.CovrUrl, IsRetByte:true, Timeout:5000);
            aRet.Tracks    = GetAlbumTracks(sID, bGetTracksUrl, sQuality);
            return aRet;
        }

        public static ObservableCollection<Track> GetAlbumTracks(string sID, bool bGetUrl = false, string sQuality = null, Quality eQuality = Quality.LOSSLESS)
        {
            string sRet = Get("albums/" + sID + "/tracks");
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            ObservableCollection<Track> aRet = JsonHelper.ConverStringToObject<ObservableCollection<Track>>(sRet, "items");
            if (bGetUrl)
            {
                if (sQuality == null)
                    sQuality = AIGS.Common.Convert.ConverEnumToString((int)eQuality, typeof(Quality), 0);

                //ThreadHelper ThreadList = new ThreadHelper(1);
                ThreadHelper ThreadList = new ThreadHelper(aRet.Count);
                for (int i = 0; i < aRet.Count; i++)
                {
                    ThreadList.ThreadStartWait(GetStreamUrl, 0, aRet[i], sQuality);
                }
                ThreadList.WaitAll();
            }
            return aRet;
        }
        #endregion

        #region GetTrack
        public static Track GetTrack(string sID, string sQuality)
        {
            string sRet = Get("tracks/" + sID);
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            Track aRet     = JsonHelper.ConverStringToObject<Track>(sRet);
            aRet.StreamUrl = GetStreamUrl(sID, sQuality);
            return aRet;
        }
        #endregion

        #region Get Track StreamUrl
        public static StreamUrl GetStreamUrl(string sID, string sQuality)
        {
            string sRet = Get("tracks/" + sID + "/streamUrl", new Dictionary<string, string>() { { "soundQuality", sQuality } }, 3);
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            StreamUrl aRet = JsonHelper.ConverStringToObject<StreamUrl>(sRet);
            aRet.FileSize  = DownloadFileHepler.GetFileLength(aRet.Url);
            return aRet;
        }

        public static void GetStreamUrl(object[] paras)
        {
            Track track     = (Track)paras[0];
            string quality  = (string)paras[1];
            track.StreamUrl = GetStreamUrl(track.ID.ToString(), quality);
        }
        #endregion

        #region Get Video
        public static Video GetVideo(string sID)
        {
            string sRet = Get("videos/" + sID);
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            Video aRet = JsonHelper.ConverStringToObject<Video>(sRet);
            return aRet;
        }

        public static string GetVideoResolutionList(string sID)
        {
            string sRet = Get("videos/" + sID + "/streamurl");
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            string sUrl    = JsonHelper.GetValue(sRet, "url");
            string content = (string)HttpHelper.GetOrPost(sUrl);
            //todo
            return null;
        }
        #endregion

        #region Get Playlist
        #endregion

        #region Get Farviorte
        #endregion
    }
}
