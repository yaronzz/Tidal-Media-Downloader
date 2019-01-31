using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using AIGS.Helper;
namespace Tidal
{
    public class Account
    {
        private static string Url     = "https://api.tidalhifi.com/v1/";
        private static string Token   = "4zx46pyr9o8qZNRw";
        private static string Version = "1.9.1";
        public  string Errmsg         = "";

        private string shortuser;
        public string ShortUser
        {
            get { return shortuser; }
            set { shortuser = value; }
        }

        private string user;
        public string User
        {
            get { return user; }
            set { user = value; }
        }
        private string userid;
        public string UserID
        {
            get { return userid; }
            set { userid = value; }
        }
        private string pwd;
        public string Pwd
        {
            get { return pwd; }
            set { pwd = value; }
        }
        private string sessionid;
        public string SessionID
        {
            get { return sessionid; }
            set { sessionid = value; }
        }
        private string countrycode;
        public string CountryCode
        {
            get { return countrycode; }
            set { countrycode = value; }
        }

        private string GetUID()
        {
            string sRet = "";
            string[] sArray = Guid.NewGuid().ToString().Split('-');
            for (int i = 0; i < sArray.Count(); i++)
            {
                sRet += sArray[i];
            }
            return sRet;
        }


        public bool LogIn(string sUser, string sPwd)
        {
            Errmsg = "";
            Dictionary<string,string>pPara = new Dictionary<string, string>()
            {
                {"username", sUser},
                {"password", sPwd},
                {"token", Token},
                {"clientVersion", Version},
                {"clientUniqueKey", GetUID()}
            };
            string sRet    = (string)HttpHelper.GetOrPost(Url+ "login/username", pPara);
            if (string.IsNullOrEmpty(sRet))
            {
                if (!string.IsNullOrEmpty(HttpHelper.Errmsg))
                {
                    if (HttpHelper.Errmsg.Contains("401"))
                        Errmsg = "Uername or password err!";
                    else
                        Errmsg = "Get sessionid err!";
                    return false;
                }
            }

            string sUserID      = JsonHelper.GetValue(sRet, "userId");
            string sSessionID   = JsonHelper.GetValue(sRet, "sessionId");
            string sCountryCode = JsonHelper.GetValue(sRet, "countryCode");

            if(string.IsNullOrEmpty(sUserID) || string.IsNullOrEmpty(sSessionID) || string.IsNullOrEmpty(sCountryCode))
            {
                Errmsg = "Get sessionid/userId/countryCode err!";
                return false;
            }

            string sRet2        = (string)HttpHelper.GetOrPost(Url + "users/" + sUserID, new Dictionary<string, string>() { { "sessionId", sSessionID } });
            string sStatus2     = JsonHelper.GetValue(sRet2, "status");
            if (!string.IsNullOrEmpty(sStatus2) && sStatus2 != "200")
            {
                Errmsg = "Sessionid is unvalid!";
                return false;
            }

            this.User        = sUser;
            this.ShortUser   = sUser;
            this.Pwd         = sPwd;
            this.SessionID   = sSessionID;
            this.UserID      = sUserID;
            this.CountryCode = sCountryCode;
            if (sUser.Contains("@"))
                this.ShortUser = sUser.Substring(0, sUser.IndexOf('@'));
            
            return true;
        }
    }
}
