using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using AIGS.Helper;
using System.Collections.ObjectModel;
using System.IO;
using System.Windows;
using AIGS.Common;
namespace Tidal
{
    public class Tool
    {
        static string URL = "https://api.tidalhifi.com/v1/";
        static string TOKEN = "4zx46pyr9o8qZNRw";
        static string PHONE_TOKEN = "kgsOOmYk3zShYrNP";
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
            errmsg = null;
            string sPhonesessionid = null;
            for (int i = 0; i < 2; i++)
            {
                string sRet = (string)HttpHelper.GetOrPost(URL + "login/username", out errmsg, new Dictionary<string, string>() {
                    {"username", user},
                    {"password", password},
                    {"token", i== 0 ? PHONE_TOKEN : TOKEN},
                    {"clientVersion", VERSION},
                    {"clientUniqueKey", GetUID()}
                });
                if (!string.IsNullOrEmpty(errmsg))
                    return false;
                if (i == 0)
                    sPhonesessionid = JsonHelper.GetValue(sRet, "sessionId");
                else
                {
                    m_User = JsonHelper.ConverStringToObject<Account>(sRet);
                    m_User.SessionID_Phone = sPhonesessionid;
                }
            }

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
            if (!IsLogin())
            {
                Errmsg = "Need Login!";
                return null;
            }

            string sParams = "?countryCode=" + m_User.CountryCode;
            for (int i = 0; Paras != null && i < Paras.Count; i++)
                sParams += "&" + Paras.ElementAt(i).Key + "=" + Paras.ElementAt(i).Value;

            string sSessionID = m_User.SessionID;
            if(Paras != null && Paras.ContainsKey("soundQuality"))
            {
                if (Paras["soundQuality"].ToLower() == "lossless")
                    sSessionID = m_User.SessionID_Phone;
            }

            string sRet = (string)HttpHelper.GetOrPost(URL + Path + sParams, out Errmsg, Header: "X-Tidal-SessionId:" + sSessionID, Retry: RetryNum);
            if (!string.IsNullOrEmpty(Errmsg))
                return null;
            return sRet;
        }

        private static T Get<T>(string Path, out string Errmsg, Dictionary<string, string> Paras = null, int RetryNum = 0)
        {
            string sRet = Get(Path, out Errmsg, Paras, RetryNum);
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return default(T);

            T aRet = JsonHelper.ConverStringToObject<T>(sRet);
            return aRet;
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
            if (GetTracks == false)
            {
                aRet.Tracks = new ObservableCollection<Track>();
                return aRet;
            }

            string sRet2 = Get("albums/" + sID + "/tracks", out Errmsg);
            if (string.IsNullOrEmpty(sRet2) || !string.IsNullOrEmpty(Errmsg))
                return null;
            aRet.Tracks = JsonHelper.ConverStringToObject<ObservableCollection<Track>>(sRet2, "items");

            //change track title
            for (int i = 0; i < aRet.Tracks.Count; i++)
            {
                if (string.IsNullOrWhiteSpace(aRet.Tracks[i].Version))
                    continue;
                if (aRet.Tracks[i].Title.IndexOf(aRet.Tracks[i].Version) >= 0)
                    continue;
                aRet.Tracks[i].Title += '(' + aRet.Tracks[i].Version + ')';
            }

            //remove same title
            List<int> pSameIndex = new List<int>();
            for (int i = 0; i < aRet.Tracks.Count; i++)
            {
                pSameIndex.Clear();
                for (int j  = 0; j < aRet.Tracks.Count; j++)
                    if (aRet.Tracks[i].Title == aRet.Tracks[j].Title)
                        pSameIndex.Add(j);

                if (pSameIndex.Count <= 1)
                    continue;

                for (int j = 0; j < pSameIndex.Count; j++)
                    aRet.Tracks[pSameIndex[j]].Title += (j + 1).ToString();
            }
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

        #region Video Urls

        public static Dictionary<string, string> GetVideoResolutionList(string sID, out string Errmsg)
        {
            Dictionary<string, string> pHash = new Dictionary<string, string>();
            string sRet = Get("videos/" + sID + "/streamUrl", out Errmsg, RetryNum:3);
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return pHash;

            string sUrl = JsonHelper.GetValue(sRet, "url");
            string sTxt = NetHelper.DownloadString(sUrl);

            string[] sArray = sTxt.Split("#EXT-X-STREAM-INF");
            foreach (string item in sArray)
            {
                if (item.IndexOf("RESOLUTION=") < 0)
                    continue;
                string sKey   = StringHelper.GetSubString(item, "RESOLUTION=", "\n");
                string sValue = "http" + StringHelper.GetSubString(item, "http", "\n");
                if (sKey.IndexOf(',') >= 0)
                    sKey = StringHelper.GetSubString(sKey, null, ",");

                if (pHash.ContainsKey(sKey))
                    continue;
                pHash.Add(sKey, sValue);
            }
            return pHash;
        }

        public static string[] ParseM3u8Url(string sUrl)
        {
            string sTxt = NetHelper.DownloadString(sUrl);
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

        public static string[] GetVideoDLUrls(string sID, string sResolution, out string Errmsg)
        {
            int iCmp = AIGS.Common.Convert.ConverStringToInt(sResolution, 0);
            Dictionary<string, string> pHash = GetVideoResolutionList(sID, out Errmsg);
            if (pHash.Count <= 0)
                return null;

            List<int> aRes = new List<int>();
            for (int i = 0; i < pHash.Count; i++)
            {
                string item = StringHelper.GetSubString(pHash.ElementAt(i).Key, "x", null);
                aRes.Add(int.Parse(item));
            }

            int iIndex = aRes.Count - 1;
            for (int i = 0; i < aRes.Count; i++)
            {
                if(iCmp >= aRes[i])
                {
                    iIndex = i;
                    break;
                }
            }

            return ParseM3u8Url(pHash.ElementAt(iIndex).Value);
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
            //get cover
            aRet.CoverUrl = "https://resources.tidal.com/images/" + aRet.ImageID.Replace('-', '/') + "/1280x1280.jpg";
            aRet.CoverData = (byte[])HttpHelper.GetOrPost(aRet.CoverUrl, out Errmsg, IsRetByte: true, Timeout: 5000);

            //aRet.CoverUrl = "http://images.tidalhifi.com/im/im?w=1280&h=1280&uuid=" + sID + "&rows=2&cols=3&noph";
            //aRet.CoverData = (byte[])HttpHelper.GetOrPost(aRet.CoverUrl, out Errmsg, IsRetByte: true, Timeout: 5000);
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
            string sRet  = PathHelper.ReplaceLimitChar(sName, "-");
            string sExt  = ".m4a";
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
        public static string GetVideoCoverName(Video video)
        {
            string sRet = PathHelper.ReplaceLimitChar(video.Title, "-");
            return sRet.Trim() + ".jpg";
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

        #region Decrypt File

        private static byte[] ReadFile(string filepath)
        {
            FileStream fs = new FileStream(filepath, FileMode.Open);
            byte[] array  = new byte[fs.Length];
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
            if (!File.Exists(filepath))
                return false;
            if (stream.EncryptionKey.IsBlank())
                return true;

            byte[] master_key     = System.Convert.FromBase64String("UIlTTEMmmLfGowo/UC60x2H45W6MdGgTRfo/umg4754=");
            byte[] security_token = System.Convert.FromBase64String(stream.EncryptionKey);

            byte[] iv  = security_token.Skip(0).Take(16).ToArray();
            byte[] str = security_token.Skip(16).ToArray();
            byte[] dec = AESHelper.Decrypt(str, master_key, iv);

            byte[] key    = dec.Skip(0).Take(16).ToArray();
            byte[] nonce  = dec.Skip(16).Take(8).ToArray();
            byte[] nonce2 = new byte[16];
            nonce.CopyTo(nonce2, 0);

            byte[] txt   = ReadFile(filepath);
            AES_CTR tool = new AES_CTR(key, nonce2);
            byte[] newt  = tool.DecryptBytes(txt);
            bool bfalg   = WriteFile(filepath, newt);
            return bfalg;
        }

        #endregion

        #region Search
        public static SearchResult Search(string sQuery, int iLimit, out string Errmsg)
        {
            string sRet = Get("search", out Errmsg, new Dictionary<string, string>() {
                { "query", sQuery },
                { "offset", "0" },
                { "limit", iLimit.ToString()},
            });
            if (string.IsNullOrEmpty(sRet) || !string.IsNullOrEmpty(Errmsg))
                return null;

            SearchResult pRet = new SearchResult();
            pRet.Albums     = JsonHelper.ConverStringToObject<ObservableCollection<Album>>(sRet, "albums", "items");
            pRet.Tracks     = JsonHelper.ConverStringToObject<ObservableCollection<Track>>(sRet, "tracks", "items");
            pRet.Videos     = JsonHelper.ConverStringToObject<ObservableCollection<Video>>(sRet, "videos", "items");
            pRet.Playlists  = JsonHelper.ConverStringToObject<ObservableCollection<Playlist>>(sRet, "playlists", "items");
            if (pRet.Albums.Count == 0 && pRet.Tracks.Count == 0 && pRet.Videos.Count == 0)
                return null;

            pRet.Albums     = pRet.Albums == null ? new ObservableCollection<Album>() : pRet.Albums;
            pRet.Tracks     = pRet.Tracks == null ? new ObservableCollection<Track>() : pRet.Tracks;
            pRet.Videos     = pRet.Videos == null ? new ObservableCollection<Video>() : pRet.Videos;
            pRet.Playlists  = pRet.Playlists == null ? new ObservableCollection<Playlist>() : pRet.Playlists;
            return pRet;
        }
        #endregion

        #region TryGet
        public static object TryGet(string sID, out string sType)
        {
            string sErrmsg;

            //Search Album
            Album aAlbum = Tool.GetAlbum(sID, out sErrmsg);
            if (aAlbum != null)
            {
                sType = "Album";
                return aAlbum;
            }

            //Search Track
            Track aTrack = Tool.GetTrack(sID, out sErrmsg);
            if (aTrack != null)
            {
                aAlbum = Tool.GetAlbum(aTrack.Album.ID.ToString(), out sErrmsg, false);
                if (aAlbum != null)
                {
                    aAlbum.Tracks.Add(aTrack);
                    sType = "Album";
                    return aAlbum;
                }
            }

            //Search Video
            Video aVideo = Tool.GetVideo(sID, out sErrmsg);
            if (aVideo != null)
            {
                if (aVideo.Album != null)
                {
                    aAlbum = Tool.GetAlbum(aVideo.Album.ID.ToString(), out sErrmsg, false);
                    if (aAlbum != null)
                    {
                        aAlbum.Videos.Add(aVideo);
                        sType = "Album";
                        return aAlbum;
                    }
                }
                else
                {
                    sType = "Video";
                    return aVideo;
                }
            }

            //Search All
            SearchResult aResult = Tool.Search(sID, 10, out sErrmsg);
            if (aResult != null)
            {
                sType = "Search";
                return aResult;
            }

            sType = null;
            return null;
        }

        #endregion
    }
}
