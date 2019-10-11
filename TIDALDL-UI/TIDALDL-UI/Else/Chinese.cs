using AIGS.Helper;
using NPinyin;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TIDALDL_UI.Else
{
    public class CloudMusicArtist
    {
        public int id { get; set; }
        public string name { get; set; }
        public string picUrl { get; set; }
        public List<string> alias { get; set; }
        public List<string> alia { get; set; }
        public int albumSize { get; set; }
        public string picId { get; set; }
        public string img1v1Url { get; set; }
        public string img1v1 { get; set; }
        public int mvSize { get; set; }
        public bool followed { get; set; }
        public string trans { get; set; }
    }

    public class CloudMusicAlbum
    {
        public int id { get; set; }
        public string name { get; set; }
        public string type { get; set; }
        public int size { get; set; }
        public string picId { get; set; }
        public string blurPicUrl { get; set; }
        public string pic { get; set; }
        public string picUrl { get; set; }
        public string publishTime { get; set; }
        public string description { get; set; }
        public int companyId { get; set; }
        public List<string> tags { get; set; }
        public string company { get; set; }
        public string briefDesc { get; set; }
        public CloudMusicArtist artist { get; set; }
        public List<CloudMusicSong> songs { get; set; }
        public List<string> alias { get; set; }
        public int status { get; set; }
        public int copyrightId { get; set; }
        public string commentThreadId { get; set; }
        public List<CloudMusicArtist> artists { get; set; }
        public string picId_str { get; set; }
    }


    public class CloudMusicSong
    {
        public string name { get; set; }
        public int id { get; set; }
        public bool starred { get; set; }
        public int starredNum { get; set; }
        public int playedNum { get; set; }
        public int dayPlays { get; set; }
        public int hearTime { get; set; }
        public double popularity { get; set; }
        public string mp3Url { get; set; }
        public string rtUrls { get; set; }
        public int mark { get; set; }
        public List<CloudMusicArtist> artists { get; set; }
        public List<string> alias { get; set; }
        public int mvid { get; set; }
        public int duration { get; set; }
        public int position { get; set; }
    }

    public class DoubanMusicRecord
    {
        public string alt_title { get; set; }
        public string image { get; set; }
        public string mobile_link { get; set; }
        public string title { get; set; }
        public string alt { get; set; }
        public string id { get; set; }
        public DoubanMusicAttr attrs { get; set; }
        public DoubanMusicRating rating { get; set; }
        public List<DoubanMusicAuthor> author { get; set; }
        public List<DoubanMusicTag> tags { get; set; }
    }

    public class DoubanMusicRating
    {
        public int max { get; set; }
        public int min { get; set; }
        public int numRaters { get; set; }
        public string average { get; set; }
    }

    public class DoubanMusicAuthor
    {
        public string name { get; set; }
    }

    public class DoubanMusicTag
    {
        public string name { get; set; }
        public int count { get; set; }
    }

    public class DoubanMusicAttr
    {
        public List<string> publisher { get; set; }
        public List<string> singer { get; set; }
        public List<string> version { get; set; }
        public List<string> pubdate { get; set; }
        public List<string> title { get; set; }
        public List<string> media { get; set; }
        public List<string> tracks { get; set; }
        public List<string> discs { get; set; }
    }

    public class Chinese
    {
        /// <summary>
        /// 根据专辑和歌手获取匹配的网易云专辑
        /// </summary>
        /// <param name="sAlbumName">专辑名</param>
        /// <param name="sArtistName">歌手</param>
        /// <returns></returns>
        public static CloudMusicAlbum matchAlbum(string sAlbumName, string sArtistName)
        {
            //使用豆瓣接口搜索专辑，支持英文、中文、繁体搜索
            string serr;
            string stxt = (string)HttpHelper.GetOrPost("https://api.douban.com/v2/music/search?q=" + sAlbumName, out serr);
            List<DoubanMusicRecord> pDoubans = JsonHelper.ConverStringToObject<List<DoubanMusicRecord>>(stxt, "musics");

            //使用网易云接口搜索歌手
            string stxt2 = (string)HttpHelper.GetOrPost(string.Format("http://music.163.com/api/search/pc?s={0}&type=100&limit=10&offset=0", sArtistName), out serr);
            List<CloudMusicArtist> pClounds = JsonHelper.ConverStringToObject<List<CloudMusicArtist>>(stxt2, "result", "artists");

            //匹配
            int iIndex1 = -1;
            int iIndex2 = -1;
            for (int i = 0; pClounds != null && i < pClounds.Count && iIndex1 == -1; i++)
            {
                string skey = pClounds[i].name;
                for (int j = 0; pDoubans != null && j < pDoubans.Count && iIndex1 == -1; j++)
                {
                    for (int k = 0; pDoubans[j].author != null && k < pDoubans[j].author.Count; k++)
                    {
                        string stmp = converSimpleChinese(pDoubans[j].author[k].name);
                        if (skey == stmp || skey.Contains(stmp) || stmp.Contains(skey) || stmp == sArtistName)
                        {
                            iIndex1 = i;
                            iIndex2 = j;
                            break;
                        }
                    }
                }
            }

            if (iIndex1 < 0)
                return null;

            string sname = converSimpleChinese(pDoubans[iIndex2].title);
            string stxt3 = (string)HttpHelper.GetOrPost(string.Format("http://music.163.com/api/search/pc?s={0}&type=10&limit=30&offset=0", sname), out serr);
            List<CloudMusicAlbum> pCloundAlbums = JsonHelper.ConverStringToObject<List<CloudMusicAlbum>>(stxt3, "result", "albums");

            //匹配
            int iIndex3 = -1;
            for (int i = 0; pCloundAlbums != null && i < pCloundAlbums.Count; i++)
            {
                if (pCloundAlbums[i].artist.name == pClounds[iIndex1].name &&
                    pCloundAlbums[i].name == sname)
                {
                    iIndex3 = i;
                    break;
                }
            }
            if (iIndex3 < 0)
                return null;

            string stxt4 = (string)HttpHelper.GetOrPost(string.Format("http://music.163.com/api/album/{0}?ext=true&id={1}&offset=0&total=true&limit=10", pCloundAlbums[iIndex3].id.ToString(), pCloundAlbums[0].id.ToString()), out serr);
            CloudMusicAlbum pAlbum = JsonHelper.ConverStringToObject<CloudMusicAlbum>(stxt4, "album");
            return pAlbum;
        }

        /// <summary>
        /// 从专辑信息中获取歌曲的中文名
        /// </summary>
        /// <param name="sName"></param>
        /// <param name="pAlbum"></param>
        /// <returns></returns>
        public static string convertSongTitle(string sName, CloudMusicAlbum pAlbum)
        {
            if (pAlbum == null || pAlbum.songs.Count <= 0)
                return sName;

            int iIndex = -1;
            int iWeight = 0;
            for (int i = 0; i < pAlbum.songs.Count; i++)
            {
                int iTmp = calcWeight(sName, pAlbum.songs[i].name);
                if (iTmp > iWeight)
                {
                    iIndex = i;
                    iWeight = iTmp;
                }
            }
            if (iIndex < 0)
                return sName;
            return pAlbum.songs[iIndex].name;
        }

        /// <summary>
        /// 计算匹配度权重值
        /// </summary>
        /// <param name="sEngName"></param>
        /// <param name="sChnName"></param>
        /// <returns></returns>
        static int calcWeight(string sEngName, string sChnName)
        {
            //转拼音
            StringBuilder sPinyinName = new StringBuilder();
            for (int i = 0; i < sChnName.Length; i++)
            {
                if (StringHelper.IsChinese(sChnName[i]))
                    sPinyinName.Append(Pinyin.GetPinyin(sChnName[i]) + ' ');
                else
                    sPinyinName.Append(sChnName[i]);
            }

            int iRet = 0;
            //删除括号
            if (sEngName.IndexOf('(') >= 0)
                sEngName = sEngName.Substring(0, sEngName.IndexOf('('));
            if (sChnName.IndexOf('(') >= 0)
                sChnName = sChnName.Substring(0, sChnName.IndexOf('('));
            sEngName = sEngName.Trim().ToLower();
            sChnName = sPinyinName.ToString().Trim().ToLower();
            if (sEngName.Contains(sChnName) || sChnName.Contains(sEngName))
                iRet += 100;

            string[] sArr1 = sEngName.Split(' ');
            string[] sArr2 = sChnName.ToString().Trim().ToLower().Split(' ');
            for (int i = 0; i < sArr1.Count() && i < sArr2.Count(); i++)
            {
                string sitem = sArr1[i];
                string sitem2 = sArr2[i];
                for (int j = 0; j < sitem.Length && j < sitem2.Length; j++)
                {
                    if (sitem[j] == sitem2[j])
                        iRet++;
                }
            }

            if (iRet <= 0)
                return 0;
            if (sArr1.Count() == sArr2.Count())
                iRet += 100;
            return iRet;
        }

        /// <summary>
        /// 繁体转简体
        /// </summary>
        static string converSimpleChinese(string str)
        {
            StringBuilder ret = new StringBuilder();
            for (int i = 0; i < str.Length; i++)
            {
                if (StringHelper.IsChinese(str[i]))
                    ret.Append(Microsoft.VisualBasic.Strings.StrConv(str[i].ToString(), Microsoft.VisualBasic.VbStrConv.SimplifiedChinese, 0));
                else
                    ret.Append(str[i]);
            }
            return ret.ToString();
        }
    }
}
