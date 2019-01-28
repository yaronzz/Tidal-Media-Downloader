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

    }
}
