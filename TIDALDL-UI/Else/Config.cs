using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Data;

namespace TIDALDL_UI
{
    public class Config : AIGS.Common.ViewMoudleBase
    {
        private string Path = AIGS.Helper.SystemHelper.GetExeDirectoryName() + "/Tidal-dl.ini";

        #region account

        private List<AIGS.Common.Property> accounts;
        public List<AIGS.Common.Property> Accounts
        {
            get
            {
                if (accounts == null)
                {
                    accounts = new List<AIGS.Common.Property>();
                    int count = AIGS.Helper.ConfigHelper.GetValue("num", 0, "account", Path);
                    for (int i = 0; i < count; i++)
                    {
                        string sUser = AIGS.Helper.ConfigHelper.GetValue("user" + i, null, "account", Path);
                        string sPwd = AIGS.Helper.ConfigHelper.GetValue("pwd" + i, null, "account", Path);
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
                AIGS.Helper.ConfigHelper.SetValue("user" + i, Accounts[i].Key.ToString(), "account", Path);
                AIGS.Helper.ConfigHelper.SetValue("pwd" + i, Accounts[i].Value.ToString(), "account", Path);
            }
            return;
        }
        #endregion

        #region login window para
        public bool Remember
        {
            get { return AIGS.Helper.ConfigHelper.GetValue("remember", true, "common", Path); }
            set { AIGS.Helper.ConfigHelper.SetValue("remember", value, "common", Path);
                OnPropertyChanged();
            }
        }
        public bool AutoLogin
        {
            get { return AIGS.Helper.ConfigHelper.GetValue("autologin", true, "common", Path); }
            set { AIGS.Helper.ConfigHelper.SetValue("autologin", value, "common", Path);
                OnPropertyChanged();
            }
        }
        #endregion

        private string outputDir;
        public string OutputDir
        {
            get
            {
                if (string.IsNullOrEmpty(outputDir))
                    outputDir = AIGS.Helper.ConfigHelper.GetValue("outputdir", "./tidal", "common", Path);
                return outputDir;
            }
            set
            {
                outputDir = value;
                OnPropertyChanged();

                AIGS.Helper.ConfigHelper.SetValue("outputdir", value, "common", Path);
            }
        }

        private Tidal.Quality quality = Tidal.Quality.NONE;
        public Tidal.Quality Quality
        {
            get
            {
                if (quality == Tidal.Quality.NONE)
                {
                    string sStr = AIGS.Helper.ConfigHelper.GetValue("quality", "HIGH", "common", Path).ToUpper();
                    quality = Tidal.TidalTool.ConverStringToQuality(sStr, Tidal.Quality.HIGH);
                }
                return quality;
            }
            set
            {
                quality = value;
                OnPropertyChanged();

                string sStr = AIGS.Common.Convert.ConverEnumToString((int)value, typeof(Tidal.Quality), (int)Tidal.Quality.HIGH);
                AIGS.Helper.ConfigHelper.SetValue("quality", sStr, "common", Path);
            }
        }


        private int threadnum = -1;
        public int ThreadNum
        {
            get
            {
                if (threadnum == -1)
                    threadnum = AIGS.Helper.ConfigHelper.GetValue("threadnum", 10, "common", Path);
                return threadnum;
            }
            set
            {
                threadnum = value;
                OnPropertyChanged();

                AIGS.Helper.ConfigHelper.SetValue("threadnum", value, "common", Path);
            }
        }

    }


}
