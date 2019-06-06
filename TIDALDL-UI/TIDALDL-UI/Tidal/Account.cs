using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using AIGS.Helper;
namespace Tidal
{
    public class Account
    {
        private string shortuser;
        public string ShortUser
        {
            get { return shortuser; }
        }

        private string user;
        public string User
        {
            get { return user; }
            set { 
                user = value;
                if (value.Contains("@"))
                    this.shortuser = value.Substring(0, value.IndexOf('@'));
                else
                    this.shortuser = value;
            }
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
        private string sessionid_phone;
        public string SessionID_Phone
        {
            get { return sessionid_phone; }
            set { sessionid_phone = value; }
        }
        private string countrycode;
        public string CountryCode
        {
            get { return countrycode; }
            set { countrycode = value; }
        }
    }
}
