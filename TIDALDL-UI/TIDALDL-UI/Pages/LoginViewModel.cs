using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using Stylet;
using System.ComponentModel;
using System.Collections.ObjectModel;
using AIGS.Common;
using AIGS.Helper;
using Tidal;
using System.Windows;
using TIDALDL_UI.Else;
using System.Windows.Threading;

namespace TIDALDL_UI.Pages
{
    public class LoginViewModel: Screen
    {
        public string Errlabel { get; set; }
        public string Username { get; set; }
        public string Password { get; set; }
        public bool   Remember { get; set; }
        public bool   AutoLogin { get; set; }

        /// <summary>
        /// History AccountList
        /// </summary>
        public ObservableCollection<Property> PersonList { get; private set; }
        public int SelectIndex { get; set; }

        /// <summary>
        /// Show Wait Page
        /// </summary>
        public Visibility WaitVisibility { get; set; }

        /// <summary>
        /// Proxy
        /// </summary>
        public bool   ProxyViewShow { get;set; } = false;
        public bool   ProxyEnable { get;set; } = Config.ProxyEnable();
        public string ProxyHost { get; set; } = Config.ProxyHost();
        public int    ProxyPort { get; set; } = Config.ProxyPort();
        public string ProxyUser { get; set; } = Config.ProxyUser();
        public string ProxyPwd { get; set; } = Config.ProxyPwd();

        /// <summary>
        /// View
        /// </summary>
        private IWindowManager Manager;
        private MainViewModel VMMain;

        public LoginViewModel(IWindowManager manager, MainViewModel vmmain)
        {
            Manager    = manager;
            VMMain     = vmmain;

            PersonList = new ObservableCollection<Property>();
            Remember   = Config.Remember();
            AutoLogin  = Config.AutoLogin();
            ShowMainPage(true);

            //Read History Account
            List<Property> pList = Config.HistoryAccounts();
            for (int i = 0; i < pList.Count; i++)
                PersonList.Add(pList[i]);

            //If AutoLogin
            if(AutoLogin && pList.Count > 0)
            {
                Username = pList[0].Key.ToString();
                Password = pList[0].Value.ToString();
                Confirm();
            }
            return;
        }

        #region Common
        public void SelectChange()
        {
            if (SelectIndex >= 0 && SelectIndex <= PersonList.Count)
                Password = PersonList[SelectIndex].Value.ToString();
        }

        public void ShowMainPage(bool bFlag)
        {
            WaitVisibility = bFlag ? Visibility.Hidden : Visibility.Visible;
        }
        #endregion 

        #region Button
        public async void Confirm()
        {
            Errlabel = "";
            if (Username.IsBlank() || Password.IsBlank())
            {
                Errlabel = "Username or password is err!";
                return;
            }
            Config.AddHistoryAccount(Username, Password);

            ShowMainPage(false);
            //Proxy
            TidalTool.PROXY = ProxyEnable ? new HttpHelper.ProxyInfo(ProxyHost, ProxyPort, ProxyUser, ProxyPwd) : null;
            bool bRet = await Task.Run(() => { return TidalTool.login(Username, Password);});
            if (!bRet)
                Errlabel = "Login Err!";
            else
            {
                //DEBUG
                //eObjectType eType = eObjectType.None;
                //object obj = Tidal.TidalTool.tryGet("19297475", out eType, eObjectType.ALBUM);
                //Artist obj = (Artist)Tidal.TidalTool.tryGet("eason chan", out eType, eObjectType.ARTIST);

                VMMain.SetLogViewModel(this);
                Manager.ShowWindow(VMMain);
                RequestClose();
            }
            
            ShowMainPage(true);
            return;
        }

        public void Cancle()
        {
            ShowMainPage(true);
        }

        public void Setting()
        {
            if(!ProxyViewShow)
            {
                ProxyViewShow = true;
                return;
            }
            else
            {
                ProxyViewShow = false;
                Config.ProxyEnable(ProxyEnable.ToString());
                Config.ProxyHost(ProxyHost);
                Config.ProxyPort(ProxyPort.ToString());
                Config.ProxyUser(ProxyUser);
                Config.ProxyPwd(ProxyPwd);
            }
        }
        #endregion
    }
}
