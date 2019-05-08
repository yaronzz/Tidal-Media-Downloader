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


        #region Base Config
        public static string OutputDir(string Setvalue = null)
        {
            return SetOrGet("outputdir", Setvalue, "./");
        }

        public static string Quality(string Setvalue = null)
        {
            return SetOrGet("quality", Setvalue, "HIGH");
        }

        public static string ThreadNum(string Setvalue = null)
        {
            return SetOrGet("threadnum", Setvalue, "3");
        }

        public static string Username(string Setvalue = null)
        {
            return SetOrGet("username", Setvalue, "");
        }

        public static string Password(string Setvalue = null)
        {
            return SetOrGet("password", Setvalue, "");
        }

        public static string Sessionid(string Setvalue = null)
        {
            return SetOrGet("sessionid", Setvalue, "");
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

        public static bool AutoLogin(string Setvalue = null)
        {
            string sRet = SetOrGet("autologin", Setvalue, "true");
            if (sRet.IsNotBlank() && sRet.ToLower() == "true")
                return true;
            return false;
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
                string sPwd  = SetOrGet("historypwd" + i, null, "", HISTORYGROUP);
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
                SetOrGet("historypwd" + i, pArray[i].Value.ToString(), "", HISTORYGROUP);
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
    }
}
