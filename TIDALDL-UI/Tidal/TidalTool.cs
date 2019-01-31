using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using AIGS.Helper;
namespace Tidal
{
    public enum Quality
    {
        LOW,
        HIGH,
        LOSSLESS,
        HI_RES,
        NONE,
    };


    public class TidalTool
    {
        public  static Account User;
        public  static string Errmsg;
        private static string Url = "https://api.tidalhifi.com/v1/";

        #region tool
        /// <summary>
        /// http get 
        /// </summary>
        private static string Get(string Path, Dictionary<string, string> Paras = null)
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

            string sRet       = (string)HttpHelper.GetOrPost(Url + Path + sParams, Header: "X-Tidal-SessionId:" + User.SessionID);
            string sStatus    = JsonHelper.GetValue(sRet, "status");
            string sSubStatus = JsonHelper.GetValue(sRet, "subStatus");

            if (!string.IsNullOrEmpty(sStatus) && sStatus == "404" && sSubStatus == "2001")
                Errmsg = JsonHelper.GetValue(sRet, "userMessage") + ". This might be region-locked.";
            if (!string.IsNullOrEmpty(sStatus) && sStatus != "200")
                Errmsg = "Get operation err!";

            return sRet;
        }

        public static Quality ConverStringToQuality(string sStr, Quality eDefault)
        {
            if (string.IsNullOrEmpty(sStr))
                return eDefault;
            return (Quality)AIGS.Common.Convert.ConverStringToEnum(sStr, typeof(Quality), (int)eDefault);
        }

        #endregion




        public static Album GetAlbum(string sID, bool bGetTracks = false, string sQuality = null)
        {
            string sRet = Get("albums/" + sID);
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            Album aRet     = JsonHelper.ConverStringToObject<Album>(sRet);
            aRet.CovrUrl   = "https://resources.tidal.com/images/" + aRet.Cover.Replace('-', '/') + "/1280x1280.jpg";
            aRet.CoverData = (byte[])HttpHelper.GetOrPost(aRet.CovrUrl, IsRetByte:true);

            if (bGetTracks)
            {
                List<Track> aTracks = GetAlbumTracks(sID, true, sQuality);
                aRet.Tracks = aTracks;
            }
            return aRet;
        }

        public static List<Track> GetAlbumTracks(string sID, bool bGetUrl = false, string sQuality = null)
        {
            string sRet = Get("albums/" + sID + "/tracks");
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            List<Track> aRet = JsonHelper.ConverStringToObject<List<Track>>(sRet, "items");
            for (int i = 0; bGetUrl && i < aRet.Count; i++)
            {
                Track item     = aRet[i];
                item.StreamUrl = GetStreamUrl(item.ID.ToString(), sQuality);
                aRet[i]        = item;
            }
            return aRet;
        }

        public static Track GetTrack(string sID, string sQuality)
        {
            string sRet = Get("tracks/" + sID);
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            Track aRet     = JsonHelper.ConverStringToObject<Track>(sRet);
            aRet.StreamUrl = GetStreamUrl(sID, sQuality);
            return aRet;
        }

        public static StreamUrl GetStreamUrl(string sID, string sQuality)
        {
            string sRet = Get("tracks/" + sID + "/streamUrl", new Dictionary<string, string>() { { "soundQuality", sQuality } });
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            StreamUrl aRet = JsonHelper.ConverStringToObject<StreamUrl>(sRet);
            return aRet;
        }

    }
}
