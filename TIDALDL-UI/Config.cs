using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TIDALDL_UI
{
    public class Config
    {
        private string Path = AIGS.Helper.SystemHelper.GetExeDirectoryName() + "/Tidal-dl.ini";

        #region account

        private List<AIGS.Common.Property> accounts;
        public List<AIGS.Common.Property> Accounts
        {
            get {
                if(accounts == null)
                {
                    accounts = new List<AIGS.Common.Property>();
                    int count = AIGS.Helper.ConfigHelper.GetValue("num", 0, "account", Path);
                    for (int i = 0; i < count; i++)
                    {
                        string sUser = AIGS.Helper.ConfigHelper.GetValue("user"+i, null, "account", Path);
                        string sPwd = AIGS.Helper.ConfigHelper.GetValue("pwd"+i, null, "account", Path);
                        if (string.IsNullOrEmpty(sUser))
                            continue;

                        accounts.Add(new AIGS.Common.Property(sUser, sPwd));
                    }
                }
                return accounts;
            }
            set { accounts = value; }
        }
        public void addAccount(string sUser, string sPwd)
        {
            for (int i = 0; i < Accounts.Count; i++)
            {
                if (Accounts[i].Key.ToString() == sUser)
                {
                    Accounts.RemoveAt(i);
                    break;
                }
            }
            Accounts.Insert(0, new AIGS.Common.Property(sUser, sPwd));
            AIGS.Helper.ConfigHelper.SetValue("num", Accounts.Count, "account", Path);
            for (int i = 0; i < Accounts.Count; i++)
            {
                AIGS.Helper.ConfigHelper.SetValue("user"+i, Accounts[i].Key.ToString(), "account", Path);
                AIGS.Helper.ConfigHelper.SetValue("pwd" + i, Accounts[i].Value.ToString(), "account", Path);
            }
            return;
        }
        #endregion

        #region login window para
        public bool Remember
        {
            get {return AIGS.Helper.ConfigHelper.GetValue("remember", true, "common", Path); }
            set { AIGS.Helper.ConfigHelper.SetValue("remember", value, "common", Path); }
        }
        public bool AutoLogin
        {
            get { return AIGS.Helper.ConfigHelper.GetValue("autologin", true, "common", Path); }
            set { AIGS.Helper.ConfigHelper.SetValue("autologin", value, "common", Path); }
        }
        #endregion

        private string outputDir;
        public  string OutputDir
        {
            get
            {
                if(string.IsNullOrEmpty(outputDir))
                    outputDir = AIGS.Helper.ConfigHelper.GetValue("outputdir", "./tidal", "common", Path);
                return outputDir;
            }
            set
            {
                outputDir = value;
                AIGS.Helper.ConfigHelper.SetValue("outputdir", value, "common", Path);
            }
        }

        private string quality;
        public string  Quality
        {
            get
            {
                if (string.IsNullOrEmpty(quality))
                {
                    quality = AIGS.Helper.ConfigHelper.GetValue("quality", "HIGH", "common", Path).ToUpper();
                    if (quality != "LOW" && quality != "HIGH" && quality != "LOSSLESS" && quality != "HI_RES")
                        quality = "HIGH";
                }
                return outputDir;
            }
            set
            {
                quality = value;
                AIGS.Helper.ConfigHelper.SetValue("quality", value, "common", Path);
            }
        }
        public int QualityIndex
        {
            get
            {
                if (Quality == "LOW")      return 0;
                if (Quality == "HIGH")     return 1;
                if (Quality == "LOSSLESS") return 2;
                if (Quality == "HI_RES")   return 3;
                return 0;
            }
            set
            {
                if (value == 0) Quality = "LOW";      return;
                if (value == 1) Quality = "HIGH";     return;
                if (value == 2) Quality = "LOSSLESS"; return;
                if (value == 3) Quality = "HI_RES";   return;
            }
        }

        private int threadnum;
        public int ThreadNum
        {
            get
            {
                if (string.IsNullOrEmpty(quality))
                    threadnum = AIGS.Helper.ConfigHelper.GetValue("threadnum", 10, "common", Path);
                return threadnum;
            }
            set
            {
                threadnum = value;
                AIGS.Helper.ConfigHelper.SetValue("threadnum", value, "common", Path);
            }
        }

    }
}
