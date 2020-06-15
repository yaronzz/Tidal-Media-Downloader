using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using AIGS.Common;
using AIGS.Helper;
using System.Collections.ObjectModel;
using System.IO;
using TagLib;
using TIDALDL_UI.Else;
using System.Windows.Data;
using System.Text.RegularExpressions;
using Newtonsoft.Json;
using System.Net.Http;
using System.Net;
using System.Collections.Specialized;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;

namespace Tidal
{
    public class TidalTool
    {
        #region CONSTANTS

        const int ALBUM_COVER_SIZE = 1280;
        const int ARTIST_COVER_SIZE = 480;
        const int PLAYLIST_COVER_SIZE = 480;
        const int VIDEO_COVER_SIZE = 1280;
        #endregion

        #region STATIC
        static string URL             = "https://api.tidalhifi.com/v1/";
        static string TOKEN           = "u5qPNNYIbD0S0o36MrAiFZ56K6qMCrCmYPzZuTnV";
        static string TOKEN_PHONE     = "hZ9wuySZCmpLLiui";
        //static string TOKEN_PHONE     = "kgsOOmYk3zShYrNP";
        static string VERSION         = "1.9.1";
        static byte[] MASTER_KEY      = System.Convert.FromBase64String("UIlTTEMmmLfGowo/UC60x2H45W6MdGgTRfo/umg4754=");
        static string USERNAME        = null;
        static string PASSWORD        = null;
        static string COUNTRY_CODE    = null;
        static string SESSIONID       = null;
        static string SESSIONID_PHONE = null;
        static bool   ISLOGIN         = false;
        static string[] LINKPRES      = { "https://tidal.com/browse/", "https://listen.tidal.com/"};
        public static HttpHelper.ProxyInfo PROXY = null;
        static int    SEARCH_NUM      = 30;
        public static string USER_INFO_KEY = "hOjn45fP";
        #endregion

        #region Login

        static bool tokenUpdateFlag = false;
        public static string loginErrlabel = "";

        /// <summary>
        /// Get token from github
        /// </summary>
        private static void updateToken()
        {
            if (tokenUpdateFlag)
                return;

            string sUrl = "https://raw.githubusercontent.com/yaronzz/Tidal-Media-Downloader/master/Else/tokens.json";
            RETRY_AGAIN:
            try
            {
                //string sReturn = NetHelper.DownloadString(sUrl, 10000);
                string sErrmsg;
                string sReturn = (string)HttpHelper.GetOrPost(sUrl, out sErrmsg, IsErrResponse: true, Timeout: 10* 1000, Proxy: PROXY);
                if (sReturn.IsNotBlank())
                {
                    TOKEN = JsonHelper.GetValue(sReturn, "token");
                    TOKEN_PHONE = JsonHelper.GetValue(sReturn, "token_phone");
                    tokenUpdateFlag = true;
                }
            }
            catch { }

            string sUrl2 = "https://cdn.jsdelivr.net/gh/yaronzz/Tidal-Media-Downloader@latest/Else/tokens.json";
            if (sUrl != sUrl2)
            {
                sUrl = sUrl2;
                goto RETRY_AGAIN;
            }
        }
        
        /// <summary>
        /// log out
        /// </summary>
        public static void logout()
        {
            ISLOGIN = false;
        }

        /// <summary>
        /// valid SessionID
        /// </summary>
        /// <param name="sUserID"></param>
        /// <param name="sSessionID"></param>
        /// <returns></returns>
        public static bool CheckSessionID(string sUserID, string sSessionID)
        {
            if (sUserID.IsBlank() || sSessionID.IsBlank())
                return false;

            string Errmsg;
            string sRet = (string)HttpHelper.GetOrPost(URL + "users/" + sUserID, out Errmsg, 
                        new Dictionary<string, string>() { {"sessionId", sSessionID }},
                        ContentType: "application/x-www-form-urlencoded",
                        IsErrResponse: true, Timeout: 30 * 1000, Proxy: PROXY);
            if (Errmsg.IsNotBlank())
                return false;
            string check = AIGS.Helper.JsonHelper.GetValue(Errmsg, "status");
            if (check.IsNotBlank())
                return false;
            return true;
        }

        static string getHttpSession(string UserName, string Password, string sToken, out string sErrmsg)
        {
            string sRet = (string)HttpHelper.GetOrPost(URL + "login/username", out sErrmsg, new Dictionary<string, string>() {
                {"username", UserName },
                {"password", Password },
                {"token", sToken},
                {"clientVersion", VERSION},
                {"clientUniqueKey", getUID()}},
                ContentType: "application/x-www-form-urlencoded",
                IsErrResponse: true, Timeout: 30 * 1000, Proxy: PROXY);

            if (sErrmsg.IsNotBlank())
            {
                sErrmsg = AIGS.Helper.JsonHelper.GetValue(sErrmsg, "userMessage");
                return null;
            }
            return sRet;
        }

        /// <summary>
        /// login
        /// </summary>
        /// <param name="UserName"></param>
        /// <param name="Password"></param>
        /// <returns></returns>
        public static bool login(string UserName, string Password)
        {
            if (ISLOGIN)
                return true;

            //Use last session
            string sLastUserid = Config.Userid();
            string sLastCountryCode = Config.Countrycode();
            string sLastSession = null; 
            string sLastSessionPhone = null; 
            if (Config.Username() == UserName && Config.Password() == Password && sLastCountryCode.IsNotBlank())
            {
                sLastSession = Config.Sessionid();
                sLastSessionPhone = Config.SessionidPhone();
                if (!CheckSessionID(sLastUserid, sLastSession))
                    sLastSession = null;
                if (!CheckSessionID(sLastUserid, sLastSessionPhone))
                    sLastSessionPhone = null;
            }

            //Login
            string Errmsg1  = null;
            string Errmsg2 = null;
            string Str1 = null;
            string Str2 = null;
            string SessID1 = sLastSession;
            string SessID2 = sLastSessionPhone;
            string Ccode = null;
            string UserID = null;
            if (sLastSession.IsBlank())
            {
                updateToken();
                Str1 = getHttpSession(UserName, Password, TOKEN, out Errmsg1);
                if (Str1.IsNotBlank())
                {
                    SessID1 = JsonHelper.GetValue(Str1, "sessionId");
                    Ccode   = JsonHelper.GetValue(Str1, "countryCode");
                    UserID  = JsonHelper.GetValue(Str1, "userId");
                }
            }
            if (sLastSessionPhone.IsBlank())
            {
                updateToken();
                Str2 = getHttpSession(UserName, Password, TOKEN_PHONE, out Errmsg2);
                if (Str2.IsNotBlank())
                {
                    SessID2 = JsonHelper.GetValue(Str2, "sessionId");
                    Ccode = JsonHelper.GetValue(Str2, "countryCode");
                    UserID = JsonHelper.GetValue(Str2, "userId");
                }
            }

            //Check
            if(SessID1.IsBlank() && SessID2.IsBlank())
            {
                loginErrlabel = Errmsg1.IsBlank() ? Errmsg2 + "token2:" + TOKEN_PHONE : Errmsg1 + "token1:" + TOKEN;
                return false;
            }
            if (UserID.IsBlank())
                UserID = sLastUserid;
            if (Ccode.IsBlank())
                Ccode = sLastCountryCode;

            SESSIONID_PHONE = SessID1;
            SESSIONID       = SessID2;
            COUNTRY_CODE    = Ccode;
            USERNAME        = UserName;
            PASSWORD        = Password;
            ISLOGIN         = true;

            Config.Countrycode(COUNTRY_CODE);
            Config.Username(USERNAME);
            Config.Password(PASSWORD);
            Config.Sessionid(SESSIONID);
            Config.SessionidPhone(SESSIONID_PHONE);
            Config.Userid(UserID);
            return true;

        }


        static string getUID()
        {
            string sRet = "";
            string[] sArray = Guid.NewGuid().ToString().Split('-');
            for (int i = 0; i < sArray.Count(); i++)
                sRet += sArray[i];
            sRet = sRet.Substring(0, 16);
            return sRet;
        }

        #endregion

        #region get
        static string get(string Path, out string Errmsg, Dictionary<string, string> Paras = null, int RetryNum = 3)
        {
            Errmsg = null;
            string sParams = "?countryCode=" + COUNTRY_CODE;
            for (int i = 0; Paras != null && i < Paras.Count; i++)
                sParams += "&" + Paras.ElementAt(i).Key + "=" + Paras.ElementAt(i).Value;

            string sSessionID = SESSIONID;
            if (Paras != null && Paras.ContainsKey("soundQuality") && Paras["soundQuality"].ToLower() == "lossless")
                sSessionID = SESSIONID_PHONE;

            //Check Session
            if (sSessionID.IsBlank())
                sSessionID = SESSIONID.IsBlank() ? SESSIONID_PHONE : SESSIONID;

        POINT_RETURN:
            string sRet = (string)HttpHelper.GetOrPost(URL + Path + sParams, out Errmsg, Header: "X-Tidal-SessionId:" + sSessionID, Retry: RetryNum, IsErrResponse: true, Proxy: PROXY);
            if (!string.IsNullOrEmpty(Errmsg))
            {
                string sStatus = JsonHelper.GetValue(Errmsg, "status");
                string sSubStatus = JsonHelper.GetValue(Errmsg, "subStatus");
                string sMessage = JsonHelper.GetValue(Errmsg, "userMessage");
                if (sStatus.IsNotBlank() && sStatus == "404" && sSubStatus == "2001")
                    Errmsg = sMessage + ". This might be region-locked.";
                else if (sStatus.IsNotBlank() && sStatus == "401" && sSubStatus == "4005")//'Asset is not ready for playback'
                {
                    if (sSessionID != SESSIONID_PHONE)
                    {
                        sSessionID = SESSIONID_PHONE;
                        goto POINT_RETURN;
                    }
                    Errmsg = sMessage;
                }
                else if (sStatus.IsNotBlank() && sStatus != "200")
                    Errmsg = sMessage + ". Get operation err!";
                return null;
            }
            return sRet;
        }

        static T get<T>(string Path, out string Errmsg, Dictionary<string, string> Paras = null, int RetryNum = 3, params string[] sKeyName)
        {
            string sRet = get(Path, out Errmsg, Paras, RetryNum);
            if (sRet.IsBlank() || Errmsg.IsNotBlank())
                return default(T);
            T aRet = JsonHelper.ConverStringToObject<T>(sRet, sKeyName);
            return aRet;
        }

        static string getString(string sUrl, out string Errmsg)
        {
            string sRet = (string)HttpHelper.GetOrPost(sUrl, out Errmsg, Retry: 5, Proxy: PROXY);
            if (Errmsg.IsNotBlank())
                return null;
            return sRet;
        }

        static ObservableCollection<T> getItems<T>(string Path, out string Errmsg, Dictionary<string, string> Paras = null, int RetryNum = 3, int CountLimt = -1)
        {
            if (Paras == null)
                Paras = new Dictionary<string, string>();
            Paras.Add("limit", "50");
            Paras.Add("offset", "0");

            int iOffset = 0;
            ObservableCollection<T> pRet = new ObservableCollection<T>();
            while (true)
            {
                string sRet = get(Path, out Errmsg, Paras, RetryNum);
                if (sRet.IsBlank() || Errmsg.IsNotBlank())
                    break;

                ObservableCollection<T> pList = JsonHelper.ConverStringToObject<ObservableCollection<T>>(sRet, "items");
                foreach (var item in pList)
                    pRet.Add(item);
                if (pList.Count() < 50)
                    break;
                if (CountLimt > 0 && pRet.Count() >= CountLimt)
                    break;
                iOffset += pList.Count();
                Paras["offset"] = iOffset.ToString();
            }
            return pRet;
        }
        #endregion

        #region Album
        public static Album getAlbum(string ID, out string Errmsg, bool GetItem = false)
        {
            Album oObj = get<Album>("albums/" + ID, out Errmsg);
            if (oObj == null)
                return null;

            getAlbumData(ref oObj, ID, out Errmsg, GetItem);
            return oObj;
        }

        private static void getAlbumData(ref Album oObj, string ID, out string Errmsg, bool GetItem = false)
        {
            oObj.CoverData = (byte[])HttpHelper.GetOrPost(getCoverUrl(ref oObj), out Errmsg, IsRetByte: true, Retry: 3, Timeout: 5000, Proxy: PROXY);
            oObj.Tracks = new ObservableCollection<Track>();
            oObj.Videos = new ObservableCollection<Video>();

            if(GetItem)
            {
                if(oObj.NumberOfVideos <= 0)
                    oObj.Tracks = get<ObservableCollection<Track>>("albums/" + ID + "/tracks", out Errmsg, null, 3, "items");
                else
                {
                    ObservableCollection<object> pArray = getItems<object>("albums/" + ID + "/items", out Errmsg, null, 3);
                    foreach (object item in pArray)
                    {
                        if (JsonHelper.GetValue(item.ToString(), "type") == "track")
                            oObj.Tracks.Add(JsonHelper.ConverStringToObject<Track>(item.ToString(), "item"));
                        else
                            oObj.Videos.Add(JsonHelper.ConverStringToObject<Video>(item.ToString(), "item"));
                    }
                }
            }

            for (int i = 0; i < oObj.Tracks.Count; i++)
            {
                if (oObj.Tracks[i].Version.IsNotBlank())
                    oObj.Tracks[i].Title = oObj.Tracks[i].Title + " - " + oObj.Tracks[i].Version;
            }
        }

        #endregion

        #region Track
        public static Track getTrack(string ID, out string Errmsg)
        {
            Track oObj = get<Track>("tracks/" + ID, out Errmsg);
            if (oObj == null)
                return null;
            if (oObj.Version.IsNotBlank())
                oObj.Title = oObj.Title + " - " + oObj.Version;
            return oObj;
        }

        public static StreamUrl getStreamUrl(string ID, eSoundQuality eQuality, out string Errmsg)
        {
            string sQua = AIGS.Common.Convert.ConverEnumToString((int)eQuality, typeof(eSoundQuality), 0);
            StreamUrl oObj = get<StreamUrl>("tracks/" + ID + "/streamUrl", out Errmsg, new Dictionary<string, string>() { { "soundQuality", sQua } }, 3);
            if(oObj == null)
            {
                string Errmsg2 = null;
                object resp = get<object>("tracks/" + ID + "/playbackinfopostpaywall", out Errmsg2,  new Dictionary<string, string>() { { "audioquality", sQua }, { "playbackmode", "STREAM" }, { "assetpresentation", "FULL" } }, 3);
                if (resp != null)
                {
                    string sNewID = JsonHelper.GetValue(resp.ToString(), "trackId");
                    if(sNewID.IsBlank())
                        return oObj;
                    oObj = get<StreamUrl>("tracks/" + sNewID + "/streamUrl", out Errmsg, new Dictionary<string, string>() { { "soundQuality", sQua } }, 3);
                }
            }
            return oObj;
        }

        public static ObservableCollection<Contributor> getTrackContributors(string ID, out string Errmsg)
        {
            ObservableCollection<Contributor> aObj = get<ObservableCollection<Contributor>>("tracks/" + ID + "/contributors", out Errmsg, null, 3, "items");
            return aObj;
        }
        #endregion

        #region Video
        public static Video getVideo(string ID, out string Errmsg)
        {
            Video oObj = get<Video>("videos/" + ID, out Errmsg);
            if (oObj == null)
                return null;
            oObj.CoverData = (byte[])HttpHelper.GetOrPost(getCoverUrl(ref oObj), out Errmsg, IsRetByte: true, Retry: 3, Timeout: 5000, Proxy: PROXY);
            return oObj;
        }

        static Dictionary<string, string> getVideoResolutionList(string sID, out string Errmsg)
        {
            string sRet = get("videos/" + sID + "/streamUrl", out Errmsg, RetryNum: 3);
            if (sRet.IsBlank() || Errmsg.IsNotBlank())
                return new Dictionary<string, string>();

            string sUrl = JsonHelper.GetValue(sRet, "url");
            string sTxt = getString(sUrl, out Errmsg);
            if (sTxt.IsBlank())
                return new Dictionary<string, string>();

            Dictionary<string, string> pHash = new Dictionary<string, string>();
            string[] sArray = sTxt.Split("#EXT-X-STREAM-INF");
            foreach (string item in sArray)
            {
                if (item.IndexOf("RESOLUTION=") < 0)
                    continue;
                string sKey = StringHelper.GetSubString(item, "RESOLUTION=", "\n");
                string sValue = "http" + StringHelper.GetSubString(item, "http", "\n");
                if (sKey.IndexOf(',') >= 0)
                    sKey = StringHelper.GetSubString(sKey, null, ",");

                if (pHash.ContainsKey(sKey))
                    continue;
                pHash.Add(sKey, sValue);
            }
            return pHash;
        }

        public static string[] getVideoDLUrls(string sID, eResolution eType, out string Errmsg)
        {
            Dictionary<string, string> pHash = getVideoResolutionList(sID, out Errmsg);
            if (pHash.Count <= 0)
                return null;

            List<int> aRes = new List<int>();
            for (int i = 0; i < pHash.Count; i++)
            {
                string item = StringHelper.GetSubString(pHash.ElementAt(i).Key, "x", null);
                aRes.Add(int.Parse(item));
            }

            int iCmp = (int)eType;
            int iIndex = aRes.Count - 1;
            for (int i = 0; i < aRes.Count; i++)
            {
                if (iCmp >= aRes[i])
                {
                    iIndex = i;
                    break;
                }
            }

            string sUrl = pHash.ElementAt(iIndex).Value;
            string sTxt = getString(sUrl, out Errmsg);
            List<string> pList = new List<string>();
            string[] sArray = sTxt.Split("#EXTINF");
            foreach (string item in sArray)
            {
                if (item.IndexOf("http") < 0)
                    continue;
                string sValue = "http" + StringHelper.GetSubString(item, "http", "\n");
                pList.Add(sValue);
            }
            return pList.ToArray();
        }
        #endregion

        #region Artist

        public static Artist getArtist(string ID, out string Errmsg, bool GetItem = false, bool IncludeEp = true)
        {
            Artist oObj = get<Artist>("artists/" + ID, out Errmsg);
            if (oObj == null)
                return null;

            oObj.CoverData = (byte[])HttpHelper.GetOrPost(getCoverUrl(ref oObj), out Errmsg, IsRetByte: true, Retry: 3, Timeout: 5000, Proxy: PROXY);
            oObj.Albums = new ObservableCollection<Album>();

            if (GetItem)
            {
                ObservableCollection<Album> albums = getItems<Album>("artists/" + ID + "/albums", out Errmsg, null, CountLimt:100);
                if (IncludeEp)
                {
                    ObservableCollection<Album> eps = getItems<Album>("artists/" + ID + "/albums", out Errmsg, new Dictionary<string, string>() { { "filter", "EPSANDSINGLES" } }, CountLimt: 100);
                    for (int i = 0; i < eps.Count; i++)
                    {
                        albums.Add(eps[i]);
                    }
                }
                oObj.Albums = albums;

                //debug
                //{
                //    string sTxt = "";
                //    for (int i = 0; i < oObj.Albums.Count(); i++)
                //    {
                //        sTxt += string.Format("id:{0} name:{1}\n", oObj.Albums[i].ID.ToString(), oObj.Albums[i].Title);
                //    }
                //    FileHelper.Write(sTxt, true, "e:\\plist.txt");
                //}

                for (int i = 0; i < oObj.Albums.Count(); i++)
                {
                    Album item = oObj.Albums[i];
                    getAlbumData(ref item, item.ID.ToString(), out Errmsg, true);
                    oObj.Albums[i] = item;
                }
            }
            return oObj;
        }

        #endregion

        #region CoverURLs

        public static string getCoverUrl(ref Album album)
        {
            string sRet = string.Empty;
            if (!string.IsNullOrWhiteSpace(album.Cover))
                sRet = formatCoverUrl(album.Cover, ALBUM_COVER_SIZE);
            else if (album.Artist != null)
                sRet = getFallbackArtistCoverUrl(album.Artist.ID);
            return sRet;
        }

        public static string getCoverUrl(ref Playlist plist)
        {
            return string.Format("http://images.tidalhifi.com/im/im?w={1}&h={1}&uuid={0}&rows=2&cols=3&noph", plist.UUID, PLAYLIST_COVER_SIZE);
        }

        public static string getCoverUrl(ref Artist artist)
        {
            string sRet = string.Empty;
            if (!string.IsNullOrWhiteSpace(artist.Picture))
                sRet = formatCoverUrl(artist.Picture, ARTIST_COVER_SIZE);
            return sRet;
        }

        public static string getCoverUrl(ref Video video)
        {
            string sRet = string.Empty;
            if (!string.IsNullOrWhiteSpace(video.ImageID))
                sRet = formatCoverUrl(video.ImageID, VIDEO_COVER_SIZE);
            else if (video.Artist != null)
                sRet = getFallbackArtistCoverUrl(video.Artist.ID);
            return sRet;
        }

        private static string formatCoverUrl(string fileName, int Size)
        {
            return string.Format("https://resources.tidal.com/images/{0}/{1}x{1}.jpg", fileName.Replace('-', '/'), Size);
        }

        private static string getFallbackArtistCoverUrl(int artistID)
        {
            string fallbackCoverUrl = string.Empty;
            try
            {
                string Errmsg;
                Artist artistObj = get<Artist>("artists/" + artistID, out Errmsg);
                fallbackCoverUrl = getCoverUrl(ref artistObj);
            }
            catch (Exception)
            {
                // No exception handling needed.
            }
            return fallbackCoverUrl;
        }

        #endregion

        #region Playlist

        public static Playlist getPlaylist(string ID, out string Errmsg)
        {
            Playlist oObj = get<Playlist>("playlists/" + ID, out Errmsg);
            if (oObj == null)
                return null;

            oObj.Tracks = new ObservableCollection<Track>();
            oObj.Videos = new ObservableCollection<Video>();
            ObservableCollection<object> pArray = getItems<object>("playlists/" + ID + "/items", out Errmsg, null, 3);
            foreach (object item in pArray)
            {
                if (JsonHelper.GetValue(item.ToString(), "type") == "track")
                    oObj.Tracks.Add(JsonHelper.ConverStringToObject<Track>(item.ToString(), "item"));
                else
                    oObj.Videos.Add(JsonHelper.ConverStringToObject<Video>(item.ToString(), "item"));
            }

            oObj.CoverData = (byte[])HttpHelper.GetOrPost(getCoverUrl(ref oObj), out Errmsg, IsRetByte: true, Retry: 3, Timeout: 5000, Proxy: PROXY);
            return oObj;
        }

        #endregion

        #region Search
        public static void SetSearchMaxNum(int iNum)
        {
            if (iNum <= 0)
                return;
            if (iNum > 50)
                iNum = 50;
            SEARCH_NUM = iNum;
        }

        public static SearchResult Search(string sQuery, int iLimit, out string Errmsg)
        {
            string sRet = get("search", out Errmsg, new Dictionary<string, string>() {
                { "query", sQuery },
                { "offset", "0" },
                { "limit", iLimit.ToString()},
            });
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            SearchResult pRet = new SearchResult();
            pRet.Artists = JsonHelper.ConverStringToObject<ObservableCollection<Artist>>(sRet, "artists", "items");
            pRet.Albums = JsonHelper.ConverStringToObject<ObservableCollection<Album>>(sRet, "albums", "items");
            pRet.Tracks = JsonHelper.ConverStringToObject<ObservableCollection<Track>>(sRet, "tracks", "items");
            pRet.Videos = JsonHelper.ConverStringToObject<ObservableCollection<Video>>(sRet, "videos", "items");
            pRet.Playlists = JsonHelper.ConverStringToObject<ObservableCollection<Playlist>>(sRet, "playlists", "items");
            if (pRet.Artists.Count == 0 && pRet.Albums.Count == 0 && pRet.Tracks.Count == 0 && pRet.Videos.Count == 0 && pRet.Playlists.Count == 0)
                return null;

            pRet.Artists = pRet.Artists == null ? new ObservableCollection<Artist>() : pRet.Artists;
            pRet.Albums = pRet.Albums == null ? new ObservableCollection<Album>() : pRet.Albums;
            pRet.Tracks = pRet.Tracks == null ? new ObservableCollection<Track>() : pRet.Tracks;
            pRet.Videos = pRet.Videos == null ? new ObservableCollection<Video>() : pRet.Videos;
            pRet.Playlists = pRet.Playlists == null ? new ObservableCollection<Playlist>() : pRet.Playlists;
            return pRet;
        }
        #endregion

        #region Dllist

        private static ObservableCollection<string> listToObser(List<string> pRecords, bool bIsInt=true)
        {
            ObservableCollection<string> pRet = new ObservableCollection<string>();
            foreach (string item in pRecords)
            {
                if (item.IsBlank())
                    continue;
                if (bIsInt && item.ParseInt(-1) == -1)
                    continue;
                pRet.Add(item.Trim());
            }
            return pRet;
        }

        public static Dllist getDllist(string sText)
        {
            if(sText.IsBlank())
                return null;
            Dictionary<string, List<string>> pHash = ConfigHelper.ParseNoEqual(null, sText);
            Dllist pRet = new Dllist();
            pRet.AlbumIds   = new ObservableCollection<string>();
            pRet.TrackIds   = new ObservableCollection<string>();
            pRet.VideoIds   = new ObservableCollection<string>();
            pRet.Urls       = new ObservableCollection<string>();
            pRet.ArtistIds  = new ObservableCollection<string>();
            pRet.PlaylistIds= new ObservableCollection<string>();
            if (pHash.ContainsKey("album"))
                pRet.AlbumIds = listToObser(pHash["album"]);
            if(pHash.ContainsKey("track"))
                pRet.TrackIds = listToObser(pHash["track"]);
            if (pHash.ContainsKey("video"))
                pRet.VideoIds = listToObser(pHash["video"]);
            if (pHash.ContainsKey("url"))
                pRet.Urls = listToObser(pHash["url"], true);
            if (pHash.ContainsKey("artist"))
                pRet.ArtistIds = listToObser(pHash["artist"], true);
            if (pHash.ContainsKey("playlist"))
                pRet.ArtistIds = listToObser(pHash["playlist"], true);
            return pRet;
        } 

        #endregion   

        #region Convert Mp4 to M4a
        public static bool ConvertMp4ToM4a(string sFilePath, out string sNewFilePath)
        {
            sNewFilePath = sFilePath;
            if (Path.GetExtension(sFilePath).ToLower().IndexOf("mp4") < 0)
                return true;

            sNewFilePath = sFilePath.Replace(".mp4", ".m4a");            
            if (FFmpegHelper.Convert(sFilePath, sNewFilePath))
            {
                System.IO.File.Delete(sFilePath);
                return true;
            }
            return false;
        }
        #endregion

        #region Decrypt File

        private static byte[] ReadFile(string filepath)
        {
            FileStream fs = new FileStream(filepath, FileMode.Open);
            byte[] array = new byte[fs.Length];
            fs.Read(array, 0, array.Length);
            fs.Close();
            return array;
        }

        private static bool WriteFile(string filepath, byte[] txt)
        {
            try
            {
                FileStream fs = new FileStream(filepath, FileMode.Create);
                fs.Write(txt, 0, txt.Length);
                fs.Close();
                return true;
            }
            catch { return false; }
        }

        public static bool DecryptTrackFile(StreamUrl stream, string filepath)
        {
            try
            {
                if (!System.IO.File.Exists(filepath))
                    return false;
                if (stream.EncryptionKey.IsBlank())
                    return true;

                byte[] security_token = System.Convert.FromBase64String(stream.EncryptionKey);

                byte[] iv = security_token.Skip(0).Take(16).ToArray();
                byte[] str = security_token.Skip(16).ToArray();
                byte[] dec = AESHelper.Decrypt(str, MASTER_KEY, iv);

                byte[] key = dec.Skip(0).Take(16).ToArray();
                byte[] nonce = dec.Skip(16).Take(8).ToArray();
                byte[] nonce2 = new byte[16];
                nonce.CopyTo(nonce2, 0);

                byte[] txt = ReadFile(filepath);
                AES_CTR tool = new AES_CTR(key, nonce2);
                byte[] newt = tool.DecryptBytes(txt);
                bool bfalg = WriteFile(filepath, newt);
                return bfalg;
            }
            catch
            {
                return false;
            }
        }

        #endregion

        #region SetMetaData

        private static string[] GetArtistNames(ObservableCollection<Artist> Artists)
        {
            List<string> pArrayStr = new List<string>();
            for(int i = 0; i < Artists.Count; i++)
                pArrayStr.Add(Artists[i].Name);
            return pArrayStr.ToArray();
        }

        private static string[] GetRoles(ObservableCollection<Contributor> pContributors, eContributorRole eRole)
        {
            string sName = AIGS.Common.Convert.ConverEnumToString((int)eRole, typeof(eContributorRole));

            List<string> pArrayStr = new List<string>();
            for (int i = 0; i < pContributors.Count; i++)
            {
                if (pContributors[i].Role.ToUpper().Replace(' ', '_') == sName)
                    pArrayStr.Add(pContributors[i].Name);
            }
            return pArrayStr.ToArray();
        }

        public static string SetMetaData(string filepath, Album TidalAlbum, Track TidalTrack, string CoverPath, ObservableCollection<Contributor> pContributors)
        {
            try
            {
                var tfile              = TagLib.File.Create(filepath);
                tfile.Tag.Album        = TidalAlbum.Title;
                tfile.Tag.Track        = (uint)TidalTrack.TrackNumber;
                tfile.Tag.TrackCount   = (uint)TidalAlbum.NumberOfTracks;
                tfile.Tag.Title        = TidalTrack.Title;
                tfile.Tag.Disc         = (uint)TidalTrack.VolumeNumber;
                tfile.Tag.DiscCount    = (uint)TidalAlbum.NumberOfVolumes;
                tfile.Tag.Copyright    = TidalTrack.Copyright;
                tfile.Tag.AlbumArtists = GetArtistNames(TidalAlbum.Artists);
                tfile.Tag.Performers   = GetArtistNames(TidalTrack.Artists);
                tfile.Tag.Composers    = GetRoles(pContributors, eContributorRole.COMPOSER);

                //ReleaseDate
                if (TidalAlbum.ReleaseDate.IsNotBlank())
                    tfile.Tag.Year = (uint)AIGS.Common.Convert.ConverStringToInt(TidalAlbum.ReleaseDate.Split("-")[0]);

                //Cover
                var pictures = new Picture[1];
                if (CoverPath.IsNotBlank() && System.IO.File.Exists(CoverPath))
                    pictures[0] = new Picture(CoverPath);
                else if(TidalAlbum.CoverData != null)
                    pictures[0] = new Picture(TidalAlbum.CoverData);
                        
                tfile.Tag.Pictures = pictures;

                tfile.Save();
                return null;
            }
            catch(Exception e)
            {
                return e.Message;
            }

        }

        #endregion

        #region Path
        static string formatPath(string Name)
        {
            return PathHelper.ReplaceLimitChar(Name, "-");
        }

        static string getExtension(string DlUrl)
        {
            if (DlUrl.IndexOf(".flac") >= 0)
                return ".flac";
            if (DlUrl.IndexOf(".mp4") >= 0)
                return ".mp4";
            return ".m4a";
        }

        public static string getPlaylistFolder(string basePath, Playlist plist)
        {
            string sRet = string.Format("{0}/Playlist/{1}/", basePath, formatPath(plist.Title));
            return Path.GetFullPath(sRet);
        }

        public static string getArtistFolder(string basePath, Artist artist)
        {
            string sRet = string.Format("{0}/Album/{1}/", basePath, formatPath(artist.Name));
            return Path.GetFullPath(sRet);
        }

        public static string getAlbumFolder(string basePath, Album album, int addYear = 0)
        {
            string sQualityFlag = "";
            string sss = Config.Quality();
            if (Config.Quality().ToUpper().IndexOf("RES") >= 0 && album.AudioQuality == "HI_RES")
                sQualityFlag = "[M] ";

            string sRet;
            if(addYear < 1 || addYear > 2 || album.ReleaseDate.IsBlank())
                sRet = string.Format("{0}/Album/{1}/{3}{2}/", basePath, formatPath(album.Artist.Name), formatPath(album.Title), sQualityFlag);
            else
            {
                string sYearStr = '[' + album.ReleaseDate.Substring(0,4) + ']';
                if(addYear == 1)
                    sRet = string.Format("{0}/Album/{1}/{4}{3} {2}/", basePath, formatPath(album.Artist.Name), formatPath(album.Title), sYearStr, sQualityFlag);
                else
                    sRet = string.Format("{0}/Album/{1}/{4}{2} {3}/", basePath, formatPath(album.Artist.Name), formatPath(album.Title), sYearStr, sQualityFlag);
            }
            sRet = cutFilePath(sRet);
            return Path.GetFullPath(sRet);
        }

        public static string getAlbumCoverPath(string basePath, Album album, int addYear = 0)
        {
            string sAlbumDir = getAlbumFolder(basePath, album, addYear);
            string title = Regex.Replace(album.Title.Replace("（", "(").Replace("）", ")"), @"\([^\(]*\)", "");
            string sRet = string.Format("{0}/{1}.jpg", sAlbumDir, formatPath(title));

            sRet = cutFilePath(sRet);
            return Path.GetFullPath(sRet);
        }
            
        public static string getTrackPath(string basePath, Album album, Track track, string sdlurl, 
                                            bool hyphen=false, Playlist plist=null, string trackTitle = null, 
                                            bool artistBeforeTitle = false, bool addexplicit=false, int addYear = 0,
                                            bool useTrackNumber = true)
        {
            //Get sArtistStr
            string sArtistStr = "";
            if (artistBeforeTitle && track.Artist != null)
            {
                sArtistStr = formatPath(track.Artist.Name) + " - ";
            }

            //Get Explicit
            string sExplicitStr = "";
            if(addexplicit && track.Explicit)
            {
                sExplicitStr = "(Explicit)";
            }

            string sRet = "";
            if (album != null)
            {
                string sAlbumDir = getAlbumFolder(basePath, album, addYear);
                string sTrackDir = sAlbumDir;
                if (album.NumberOfVolumes > 1)
                    sTrackDir += "Volume" + track.VolumeNumber.ToString() + "/";


                string sChar = hyphen ? "- " : "";
                string trackNumber = track.TrackNumber.ToString().PadLeft(2, '0');

                string sPrefix = useTrackNumber ? $"{trackNumber} {sChar}" : "";
                string sTitle = trackTitle == null ? formatPath(track.Title) : formatPath(trackTitle);

                string sName = string.Format("{0}{1}{2}{3}{4}",
                    sPrefix,
                    sArtistStr,
                    sTitle,
                    sExplicitStr,
                    getExtension(sdlurl));
                sRet = sTrackDir + sName;
            }
            else
            {
                string sPlistDir = getPlaylistFolder(basePath, plist);
                string sTrackDir = sPlistDir;

                string sChar = hyphen ? "- " : "";
                string trackNumber = (plist.Tracks.IndexOf(track) + 1).ToString().PadLeft(2, '0');

                string sPrefix = useTrackNumber ? $"{trackNumber} {sChar}" : "";

                string sName = string.Format("{0}{1}{2}{3}",
                    sPrefix,
                    sArtistStr,
                    trackTitle == null ? formatPath(track.Title) : formatPath(trackTitle),
                    getExtension(sdlurl));
                sRet = sTrackDir + sName;
            }

            sRet = cutFilePath(sRet);
            return Path.GetFullPath(sRet);
        }

        public static string getVideoPath(string basePath, Video video, Album album, string sExt = ".mp4", bool hyphen = false, Playlist plist = null, bool artistBeforeTitle = false, int addYear = 0)
        {
            string sArtistStr = "";
            if(artistBeforeTitle && video.Artist != null)
            {
                sArtistStr = formatPath(video.Artist.Name) + " - ";
            }

            if (album != null)
            {
                string sRet = getAlbumFolder(basePath, album, addYear) + sArtistStr + formatPath(video.Title) + sExt;
                sRet = cutFilePath(sRet);
                return Path.GetFullPath(sRet);

            }
            else if(plist != null)
            {
                string sRet = getPlaylistFolder(basePath, plist);
                string sChar = hyphen ? "- " : "";
                string sName = string.Format("{0} {1}{2}{3}{4}",
                    (plist.Tracks.Count + plist.Videos.IndexOf(video) + 1).ToString().PadLeft(2, '0'),
                    sChar,
                    sArtistStr,
                    formatPath(video.Title),
                    sExt);
                sRet = cutFilePath(sRet + sName);
                return Path.GetFullPath(sRet);
            }
            else
            { 
                string sRet = string.Format("{0}/Video/{1}{2}{3}", basePath, sArtistStr, formatPath(video.Title), sExt);
                sRet = cutFilePath(sRet);
                return Path.GetFullPath(sRet);
            }
        }

        public static string getVideoFolder(string basePath)
        {
            string sRet = string.Format("{0}/Video/", basePath);
            return Path.GetFullPath(sRet);
        }
        #endregion

        #region tryGet
        private static bool parseLink(ref string insStr, ref eObjectType inType)
        {
            string sPre = null;
            string sStr = insStr.Trim();
            foreach (string item in LINKPRES)
            {
                if (sStr.IndexOf(item) >= 0)
                    sPre = item;
            }
            if (sPre.IsBlank())
                return false;

            string sTail  = sStr.Substring(sPre.Length);
            string[] sArr = sTail.Split('/');
            if (sArr.Count() < 2)
                return false;

            string sID = sArr[1];
            eObjectType sType = eObjectType.None;
            if (AIGS.Common.Convert.ConverStringToInt(sID, -1) == -1)
            {
                if (sArr[0] == "playlist") sType = eObjectType.PLAYLIST;
            }
            else
            {
                if (sArr[0] == "album") sType = eObjectType.ALBUM;
                if (sArr[0] == "track") sType = eObjectType.TRACK;
                if (sArr[0] == "video") sType = eObjectType.VIDEO;
                if (sArr[0] == "artist") sType = eObjectType.ARTIST;
            }
            if (sType == eObjectType.None)
                return false;

            insStr = sID;
            inType = sType;
            return true;

        }

        public static object tryGet(string sStr, out eObjectType eType, eObjectType inType = eObjectType.None)
        {
            object oRet    = null;
            string sErrmsg = null;
            Track  oTrack  = null;
            sStr = sStr.Trim();

            //check url
            parseLink(ref sStr, ref inType);
            if (AIGS.Common.Convert.ConverStringToInt(sStr, -1) == -1)
                goto POINT_SEARCH;

            //jump
            if (inType != eObjectType.None)
            {
                switch(inType)
                {
                    case eObjectType.ARTIST:goto POINT_ARTIST;
                    case eObjectType.ALBUM:goto POINT_ALBUM;
                    case eObjectType.TRACK:goto POINT_TRACK;
                    case eObjectType.VIDEO:goto POINT_VIDEO;
                }
            }

            //if not id, jump search
            if (sStr.ParseInt(-1) == -1)
                goto POINT_SEARCH;

            //get
        POINT_ALBUM:
            oRet = getAlbum(sStr, out sErrmsg, true);
            if (oRet != null)
            {
                eType = eObjectType.ALBUM;
                return oRet;
            }
            if (inType == eObjectType.ALBUM)
                goto POINT_ERR;
        POINT_TRACK:
            oTrack = getTrack(sStr, out sErrmsg);
            if (oTrack != null)
            {
                oRet = getAlbum(oTrack.Album.ID.ToString(), out sErrmsg);
                ((Album)oRet).Tracks = new ObservableCollection<Track>() { oTrack };
                eType = eObjectType.ALBUM;
                return oRet;
            }
            if (inType == eObjectType.TRACK)
                goto POINT_ERR;
        POINT_VIDEO:
            oRet = getVideo(sStr, out sErrmsg);
            if (oRet != null)
            {
                eType = eObjectType.VIDEO;
                return oRet;
            }
            if (inType == eObjectType.VIDEO)
                goto POINT_ERR;
        POINT_ARTIST:
            oRet = getArtist(sStr, out sErrmsg, true, Config.IncludeEP());
            if (oRet != null)
            {
                eType = eObjectType.ARTIST;
                return oRet;
            }
            if (inType == eObjectType.ARTIST)
                goto POINT_ERR;
        POINT_SEARCH:
            if(sStr.IndexOf('-') >= 0)
            {
                oRet = getPlaylist(sStr, out sErrmsg);
                if (oRet != null)
                {
                    eType = eObjectType.PLAYLIST;
                    return oRet;
                }
            }
            oRet = Search(sStr, SEARCH_NUM, out sErrmsg);
            if (oRet != null)
            {
                eType = eObjectType.SEARCH;
                return oRet;
            }

        POINT_ERR:
            eType = eObjectType.None;
            return null;
        }
        #endregion

        #region Common
        public static List<string> getQualityList()
        {
            Dictionary<int, string> pHash = AIGS.Common.Convert.ConverEnumToDictionary(typeof(eSoundQuality));
            List<string> pRet = new List<string>();
            foreach (var item in pHash)
            {
                pRet.Add(item.Value);
            }
            return pRet;
        }
        
        public static List<string> getResolutionList()
        {
            Dictionary<int, string> pHash = AIGS.Common.Convert.ConverEnumToDictionary(typeof(eResolution));
            List<string> pRet = new List<string>();
            foreach (var item in pHash)
            {
                pRet.Add(item.Key.ToString());
            }
            return pRet;
        }

        public static eSoundQuality getQuality(string sStr)
        {
            Dictionary<int, string> pHash = AIGS.Common.Convert.ConverEnumToDictionary(typeof(eSoundQuality));
            foreach (var item in pHash)
            {
                if (item.Value.ToLower().Contains(sStr.ToLower()))
                    return (eSoundQuality)item.Key;
            }
            return eSoundQuality.HIGH;
        }

        public static eResolution getResolution(string sStr)
        {
            Dictionary<int, string> pHash = AIGS.Common.Convert.ConverEnumToDictionary(typeof(eResolution));
            foreach (var item in pHash)
            {
                if (item.Value.Contains(sStr))
                    return (eResolution)item.Key;
            }
            return eResolution.e1080P;
        }

        public static string getFlag(object item)
        {
            Type t = item.GetType();
            if (typeof(Album) == t)
            {
                Album obj = (Album)item;
                if (obj.AudioQuality == "HI_RES")
                    return "M";
            }
            else if (typeof(Track) == t)
            {
                Track obj = (Track)item;
                if (obj.AudioQuality == "HI_RES")
                    return "M";
            }
            return null;
        }

        public static string cutFilePath(string sFilePath)
        {
            if (sFilePath.Length >= 260)
            {
                int iLen = sFilePath.Length - 260 + 10; //10 set aside 
                string sName = Path.GetFileNameWithoutExtension(sFilePath);
                string sExt = Path.GetExtension(sFilePath);
                string sPath = sFilePath.Substring(0, sFilePath.Length - sName.Length - sExt.Length);
                if (sName.Length > iLen)
                {
                    string sRet = sPath + sName.Substring(0, sName.Length - iLen) + sExt;
                    return sRet;
                }
            }
            return sFilePath;
        }
        #endregion
    }
}
