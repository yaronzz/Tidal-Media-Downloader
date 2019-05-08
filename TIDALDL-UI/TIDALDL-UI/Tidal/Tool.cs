using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using AIGS.Helper;
using System.Collections.ObjectModel;
using System.IO;
using System.Windows;

namespace Tidal
{
    public class Tool
    {
        static string URL     = "https://api.tidalhifi.com/v1/";
        static string TOKEN   = "4zx46pyr9o8qZNRw";
        static string VERSION = "1.9.1";

        #region Account - Login

        static Account m_User = null;
        static bool m_isLogin = false;

        private static string GetUID()
        {
            string sRet = "";
            string[] sArray = Guid.NewGuid().ToString().Split('-');
            for (int i = 0; i < sArray.Count(); i++)
                sRet += sArray[i];
            return sRet;
        }

        public static bool IsLogin()
        {
            return m_isLogin;
        }

        public static bool LogIn(string user, string password, out string errmsg)
        {
            string sRet = (string)HttpHelper.GetOrPost(URL + "login/username", out errmsg, new Dictionary<string, string>() { 
                {"username", user},
                {"password", password},
                {"token", TOKEN},
                {"clientVersion", VERSION},
                {"clientUniqueKey", GetUID()}
            });

            if (!string.IsNullOrEmpty(errmsg))
                return false;

            m_User      = JsonHelper.ConverStringToObject<Account>(sRet);
            m_User.User = user;
            m_User.Pwd  = password;
            m_isLogin   = true;
            return true;
        }
        #endregion

        #region Http-Get
        private static string Get(string Path, out string Errmsg, Dictionary<string, string> Paras = null, int RetryNum = 0)
        {
            Errmsg = null;

            if(!IsLogin())
            {
                Errmsg = "Need Login!";
                return null;
            }

            string sParams = "?countryCode=" + m_User.CountryCode;
            for (int i = 0; Paras != null && i < Paras.Count; i++)
                sParams += "&" + Paras.ElementAt(i).Key + "=" + Paras.ElementAt(i).Value;

            string sRet = (string)HttpHelper.GetOrPost(URL + Path + sParams, out Errmsg, Header: "X-Tidal-SessionId:" + m_User.SessionID, Retry: RetryNum);
            if (!string.IsNullOrEmpty(Errmsg))
                return null;
            return sRet;
        }
       
        #endregion

        #region Album
        public static Album GetAlbum(string sID, out string Errmsg, bool GetTracks = true)
        {
            string sRet = Get("albums/" + sID, out Errmsg);
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;
            Album aRet = JsonHelper.ConverStringToObject<Album>(sRet);
            
            //get cover
            aRet.CoverUrl = "https://resources.tidal.com/images/" + aRet.Cover.Replace('-', '/') + "/1280x1280.jpg";
            aRet.CoverData = (byte[])HttpHelper.GetOrPost(aRet.CoverUrl, out Errmsg, IsRetByte: true, Timeout: 5000);

            //get tracklist
            if (GetTracks)
            {
                string sRet2 = Get("albums/" + sID + "/tracks", out Errmsg);
                if (string.IsNullOrEmpty(sRet2) || !string.IsNullOrEmpty(Errmsg))
                    return null;
                aRet.Tracks = JsonHelper.ConverStringToObject<ObservableCollection<Track>>(sRet2, "items");
            }
            else
                aRet.Tracks = new ObservableCollection<Track>();

            return aRet;
        }
        #endregion

        #region StreamUrl
        public static StreamUrl GetStreamUrl(string sID, string sQuality, out string Errmsg)
        {
            string sRet = Get("tracks/" + sID + "/streamUrl", out Errmsg, new Dictionary<string, string>() { { "soundQuality", sQuality } }, 3);
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            StreamUrl aRet = JsonHelper.ConverStringToObject<StreamUrl>(sRet);
            return aRet;
        }
        #endregion

        #region Track
        public static Track GetTrack(string sID, out string Errmsg)
        {
            string sRet = Get("tracks/" + sID, out Errmsg);
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            Track aRet = JsonHelper.ConverStringToObject<Track>(sRet);
            return aRet;
        }
        #endregion

        #region Vide
        public static Video GetVideo(string sID, out string Errmsg)
        {
            string sRet = Get("videos/" + sID, out Errmsg);
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            Video aRet = JsonHelper.ConverStringToObject<Video>(sRet);
            return aRet;
        }
        #endregion

        #region Playlist
        private static string GetPlaylistItems(string sID, int iSum, out ObservableCollection<Track> Tracks, out ObservableCollection<Video> Videos)
        {
            int iLimit    = 100;
            int iOffset   = 0;
            string Errmsg = null;

            Tracks = new ObservableCollection<Track>();
            Videos = new ObservableCollection<Video>();

            while(iOffset < iSum)
            {
                string sRet = Get("playlists/" + sID + "/items", out Errmsg, new Dictionary<string, string>() { { "offset", iOffset.ToString() }, { "limit", iLimit.ToString() } });
                if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                    return Errmsg;

                List<object> sItems = JsonHelper.ConverStringToObject<List<object>>(sRet, "items");
                foreach (object item in sItems)
                {
                    string sType = JsonHelper.GetValue(item.ToString(), "type");
                    if(sType.ToLower() == "video")
                        Videos.Add(JsonHelper.ConverStringToObject<Video>(item.ToString(), "item"));
                    else
                        Tracks.Add(JsonHelper.ConverStringToObject<Track>(item.ToString(), "item"));
                }
                iOffset += sItems.Count;
            }

            return Errmsg;
        }

        public static Playlist GetPlaylist(string sID, out string Errmsg)
        {
            string sRet = Get("playlists/" + sID, out Errmsg);
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;
            Playlist aRet = JsonHelper.ConverStringToObject<Playlist>(sRet);

            //get itemlist
            ObservableCollection<Track> Tracks;
            ObservableCollection<Video> Videos;
            Errmsg = GetPlaylistItems(sID, aRet.NumberOfTracks + aRet.NumberOfVideos, out Tracks, out Videos);
            aRet.Tracks = Tracks;
            aRet.Videos = Videos;

            return aRet;
        }
        #endregion

        #region Save Path
        public static string GetAlbumFolderName(Album album)
        {
            string sRet = PathHelper.ReplaceLimitChar(album.Title, "-");
            return sRet.Trim();
        }
        
        public static string GetAlbumCoverName(Album album)
        {
            string sRet = GetAlbumFolderName(album);
            return sRet.Trim() + ".jpg";
        }

        public static string GetTrackFileName(Track track, StreamUrl stream)
        {
            string sName = track.Title;
            if (!string.IsNullOrWhiteSpace(track.Version))
                sName += '(' + track.Version + ')';

            string sRet = PathHelper.ReplaceLimitChar(sName, "-");
            string sExt = ".m4a";
            if (stream.Url.IndexOf(".flac?") > 0)
                sExt = ".flac";
            if (stream.Url.IndexOf(".mp4?") > 0)
                sExt = ".mp4";
            return sRet.Trim() + sExt;
        }

        public static string GetVideoFileName(Video video)
        {
            string sRet = PathHelper.ReplaceLimitChar(video.Title, "-");
            return sRet.Trim() + ".mp4";
        }

        public static string GetPlaylistFolderName(Playlist playlist)
        {
            string sRet = PathHelper.ReplaceLimitChar(playlist.Title, "-");
            return sRet.Trim();
        }
        #endregion

        #region Parse Url
        //https://listen.tidal.com/album/18447849
        public static string ParseUrl(string sUrl)
        {
            if (string.IsNullOrEmpty(sUrl))
                return sUrl;

            int index = sUrl.IndexOf("https://listen.tidal.com/");
            if (index != 0)
                return sUrl;

            string sType = "";
            if (sUrl.IndexOf("album") > 0)
                sType = "album";
            if (sUrl.IndexOf("track") > 0)
                sType = "track";
            if (sUrl.IndexOf("video") > 0)
                sType = "video";
            if (sUrl.IndexOf("playlist") > 0)
                sType = "playlist";
            if (string.IsNullOrEmpty(sType))
                return sUrl;

            sUrl = sUrl.Substring(("https://listen.tidal.com/" + sType).Length);
            if (sUrl.IndexOf("/") >= 0)
                sUrl = sUrl.Substring(0, sUrl.IndexOf("/"));
            return sUrl;
        }

        #endregion


    }
}
