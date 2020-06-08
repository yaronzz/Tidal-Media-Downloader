using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using AIGS.Common;
using AIGS.Helper;
using System.Collections.ObjectModel;

namespace TIDALDL_UI.Else
{
    public class Config
    {
        private static string CONFIGPATH   = "./tidal-dl.ini";
        private static string BASEGROUP    = "base";
        private static string HISTORYGROUP = "history";

        private static string SetOrGet(string Key, string SetValue = null, string GetDefault = "", string Group = null)
        {
            if (Group.IsBlank())
                Group = BASEGROUP;
            if (SetValue.IsBlank())
                return ConfigHelper.GetValue(Key, GetDefault, Group, CONFIGPATH);
            else
                ConfigHelper.SetValue(Key, SetValue, Group, CONFIGPATH);
            return null;
        }
        private static string SetOrGetPrivate(string Key, string SetValue = null, string GetDefault = "", string Group = null)
        {
            if (Group.IsBlank())
                Group = BASEGROUP;
            if (SetValue.IsBlank())
            {
                string sTmp = ConfigHelper.GetValue(Key, GetDefault, Group, CONFIGPATH);
                return Decode(sTmp);
            }
            else
                ConfigHelper.SetValue(Key, Encode(SetValue), Group, CONFIGPATH);
            return null;
        }


        #region Base Config
        public static string Version(string Setvalue = null)
        {
            return SetOrGet("version", Setvalue, "null");
        }

        public static string OutputDir(string Setvalue = null)
        {
            return SetOrGet("outputdir", Setvalue, "./");
        }

        public static bool OnlyM4a(string Setvalue = null)
        {
            string sValue = SetOrGet("onlym4a", Setvalue, "true");
            if (sValue == null || sValue.ToLower() != "true")
                return false;
            return true;
        }

        public static bool AddExplicitTag(string Setvalue = null)
        {
            string sValue = SetOrGet("addexplicit", Setvalue, "false");
            if (sValue == null || sValue.ToLower() != "true")
                return false;
            return true;
        }

        public static bool IncludeEP(string Setvalue = null)
        {
            string sValue = SetOrGet("includesingle", Setvalue, "false");
            if (sValue == null || sValue.ToLower() != "true")
                return false;
            return true;
        }

        public static bool SaveCovers(string Setvalue = null)
        {
            string sValue = SetOrGet("savephoto", Setvalue, "true");
            if (sValue == null || sValue.ToLower() != "true")
                return false;
            return true;
        }
        
        public static bool AddHyphen(string Setvalue = null)
        {
            string sValue = SetOrGet("addhyphen", Setvalue, "true");
            if (sValue == null || sValue.ToLower() != "true")
                return false;
            return true;
        }

        public static bool UseTrackNumber(string Setvalue = null)
        {
            string sValue = SetOrGet("useTrackNumber", Setvalue, "true");
            if (sValue == null || sValue.ToLower() != "true")
                return false;
            return true;
        }

        public static string Quality(string Setvalue = null)
        {
            return SetOrGet("quality", Setvalue, "HIGH");
        }

        public static int AddYear(int Setvalue = -1)
        {
            if (Setvalue == -1)
            {
                string sValue = SetOrGet("addyear", null, "No").ToLower();
                if (sValue == "before")
                    return 1;
                else if (sValue == "after")
                    return 2;
                return 0;
            }
            else
            {
                string sValue = "No";
                if (Setvalue == 1) 
                    sValue = "Before";
                if (Setvalue == 2) 
                    sValue = "After";
                SetOrGet("addyear", sValue, "No");
                return 0;
            }
        }

        public static Dictionary<int, string> QualityList()
        {
            return AIGS.Common.Convert.ConverEnumToDictionary(typeof(Tidal.eSoundQuality));
        }

        public static int QualityIndex()
        {
            string sValue = Config.Quality();
            Dictionary<int, string> pList = QualityList();
            for (int i = 0; i < pList.Count; i++)
            {
                if (sValue.ToUpper() == pList.ElementAt(i).Value)
                    return i;
            }
            return 0;
        }

        public static string ThreadNum(string Setvalue = null)
        {
            return SetOrGet("threadnum", Setvalue, "1");
            //SetOrGet("threadnum", Setvalue, "1");
            //return "1";
        }

        public static string SearchNum(string Setvalue = null)
        {
            return SetOrGet("searchnum", Setvalue, "30");
        }

        public static string Username(string Setvalue = null)
        {
            return SetOrGet("username", Setvalue, "");
        }

        public static string Password(string Setvalue = null)
        {
            return SetOrGetPrivate("password", Setvalue, "");
        }

        public static string Sessionid(string Setvalue = null)
        {
            return SetOrGet("sessionid", Setvalue, "");
        }
        public static string SessionidPhone(string Setvalue = null)
        {
            return SetOrGet("sessionidphone", Setvalue, "");
        }

        public static string Countrycode(string Setvalue = null)
        {
            return SetOrGet("countrycode", Setvalue, "");
        }

        public static string Userid(string Setvalue = null)
        {
            return SetOrGet("userid", Setvalue, "");
        }

        public static bool Remember(string Setvalue = null)
        {
            string sRet = SetOrGet("remember", Setvalue, "true");
            if (sRet.IsNotBlank() && sRet.ToLower() == "true")
                return true;
            return false;
        }

        public static bool ToChinese(string Setvalue = null)
        {
            string sRet = SetOrGet("tochinese", Setvalue, "false");
            if (sRet.IsNotBlank() && sRet.ToLower() == "true")
                return true;
            return false;
        }

        public static bool CheckExist(string Setvalue = null)
        {
            string sRet = SetOrGet("checkexist", Setvalue, "false");
            if (sRet.IsNotBlank() && sRet.ToLower() == "true")
                return true;
            return false;
        }

        public static bool ArtistBeforeTitle(string Setvalue = null)
        {
            string sRet = SetOrGet("artistbeforetitle", Setvalue, "false");
            if (sRet.IsNotBlank() && sRet.ToLower() == "true")
                return true;
            return false;
        }

        public static bool AutoLogin(string Setvalue = null)
        {
            string sRet = SetOrGet("autologin", Setvalue, "true");
            if (sRet.IsNotBlank() && sRet.ToLower() == "true")
                return true;
            return false;
        }

        public static string Resolution(string Setvalue = null)
        {
            return SetOrGet("resolution", Setvalue, "e720P");
        }

        public static bool ProxyEnable(string Setvalue = null)
        {
            string sRet = SetOrGet("proxyenable", Setvalue, "false");
            if (sRet.IsNotBlank() && sRet.ToLower() == "true")
                return true;
            return false;
        }

        public static string ProxyHost(string Setvalue = null)
        {
            return SetOrGet("proxyhost", Setvalue, "");
        }

        public static int ProxyPort(string Setvalue = null)
        {
            string sValue = SetOrGet("proxyport", Setvalue, "");
            return AIGS.Common.Convert.ConverStringToInt(sValue, 0);
        }

        public static string ProxyUser(string Setvalue = null)
        {
            return SetOrGet("proxyuser", Setvalue, "");
        }

        public static string ProxyPwd(string Setvalue = null)
        {
            return SetOrGet("proxypwd", Setvalue, "");
        }
        #endregion

        #region History Account
        /// <summary>
        /// Get History Account List
        /// </summary>
        public static List<Property> HistoryAccounts()
        {
            List<Property> pRet = new List<Property>();
            string sValue = SetOrGet("historyusernum", null, "", HISTORYGROUP);
            int iNum      = AIGS.Common.Convert.ConverStringToInt(sValue, 0);
            for (int i = 0; i < iNum; i++)
            {
                string sUser = SetOrGet("historyuser" + i, null, "", HISTORYGROUP);
                string sPwd  = SetOrGetPrivate("historypwd" + i, null, "", HISTORYGROUP);
                if (sUser.IsNotBlank() && pRet.FindIndex((Property user) => user.Key.ToString() == sUser) < 0)
                    pRet.Add(new Property(sUser, sPwd));
            }
            return pRet;
        }
        
        /// <summary>
        /// Add Account To Config File
        /// </summary>
        public static void AddHistoryAccount(string sUsername, string sPassword)
        {
            List<Property> pArray = HistoryAccounts();
            int iIndex = pArray.FindIndex((Property user) => user.Key.ToString() == sUsername);
            if (iIndex >= 0)
                pArray.RemoveAt(iIndex);

            pArray.Insert(0, new Property(sUsername, sPassword));
            for (int i = 0; i < pArray.Count; i++)
            {
                SetOrGet("historyuser" + i, pArray[i].Key.ToString(), "", HISTORYGROUP);
                SetOrGetPrivate("historypwd" + i, pArray[i].Value.ToString(), "", HISTORYGROUP);
            }
            SetOrGet("historyusernum", pArray.Count.ToString(), "", HISTORYGROUP);
            Username(sUsername);
            Password(sPassword);
        }
        #endregion

        #region History Search
        /// <summary>
        /// Get History Search List
        /// </summary>
        public static ObservableCollection<string> HistorySearchs()
        {
            ObservableCollection<string> pRet = new ObservableCollection<string>();
            string sValue = SetOrGet("historysearchnum", null, "", HISTORYGROUP);
            int iNum = AIGS.Common.Convert.ConverStringToInt(sValue, 0);
            for (int i = 0; i < iNum; i++)
            {
                string sStr = SetOrGet("historysearch" + i, null, "", HISTORYGROUP);
                if (sStr.IsNotBlank() && pRet.IndexOf(sStr) < 0)
                    pRet.Add(sStr);
            }
            return pRet;
        }
        /// <summary>
        /// Add Search To Config File
        /// </summary>
        public static void AddHistorySearch(string sNewStr)
        {
            ObservableCollection<string> pArray = HistorySearchs();
            int iIndex = pArray.IndexOf(sNewStr);
            if (iIndex >= 0)
                pArray.RemoveAt(iIndex);

            pArray.Insert(0, sNewStr);
            for (int i = 0; i < pArray.Count; i++)
                SetOrGet("historysearch" + i, pArray[i], "", HISTORYGROUP);
            SetOrGet("historysearchnum", pArray.Count.ToString(), "", HISTORYGROUP);
        }
        #endregion


        #region Encryption
        private static string EncryptionFlag = "Ax*~!9";
        private static string Encode(string sStr)
        {
            if (sStr.IsBlank())
                return sStr;
            string sTmp = EncryptHelper.Encode(sStr, Tidal.TidalTool.USER_INFO_KEY);
            return EncryptionFlag + sTmp;
        }
        private static string Decode(string data)
        {
            if (data.IsBlank())
                return data;
            if (data.IndexOf(EncryptionFlag) != 0)
                return data;
            string sTmp = data.Substring(EncryptionFlag.Length);
            return EncryptHelper.Decode(sTmp, Tidal.TidalTool.USER_INFO_KEY);
        }
        #endregion
    }
}
