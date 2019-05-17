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
        /// <summary>
        /// Show ErrMsg In LoginButton
        /// </summary>
        public string Errlabel { get; set; }

        /// <summary>
        /// Account
        /// </summary>
        public string Username { get; set; }
        public string Password { get; set; }

        /// <summary>
        /// History AccountList
        /// </summary>
        public ObservableCollection<Property> PersonList { get; private set; }

        /// <summary>
        /// Select History-Account Index
        /// </summary>
        public int SelectIndex { get; set; }

        /// <summary>
        /// Thread Handle
        /// </summary>
        public Thread LoginThread;

        /// <summary>
        /// Show Main or Wait Page
        /// </summary>
        public Visibility MainVisibility { get; set; }
        public Visibility WaitVisibility { get; set; }

        /// <summary>
        /// Check Control - Remember & AutoLogin 
        /// </summary>
        public bool Remember { get; set; }
        public bool AutoLogin { get; set; }

        private IWindowManager Manager;
        private MainViewModel VMMain;

        /// <summary>
        /// Init
        /// </summary>
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
        /// <summary>
        /// Select History-User
        /// </summary>
        public void SelectChange()
        {
            if (SelectIndex >= 0 && SelectIndex <= PersonList.Count)
                Password = PersonList[SelectIndex].Value.ToString();
        }

        /// <summary>
        /// Show Main or Wait Page
        /// </summary>
        public void ShowMainPage(bool bFlag)
        {
            MainVisibility = bFlag ? Visibility.Visible : Visibility.Hidden;
            WaitVisibility = bFlag ? Visibility.Hidden : Visibility.Visible;
        }
        #endregion 

        #region Button
        /// <summary>
        /// Login
        /// </summary>
        public void Confirm()
        {
            Errlabel = "";
            if (Username.IsBlank() || Password.IsBlank())
            {
                Errlabel = "Username or password is err!";
                return;
            }
            ShowMainPage(false);
            LoginThread = ThreadHelper.Start(ThreadFuncLogin);
            return;
        }

        /// <summary>
        /// Cancle Login
        /// </summary>
        public void Cancle()
        {
            LoginThread.Abort();
            ShowMainPage(true);
        }
        #endregion

        #region Thread
        /// <summary>
        /// Login Thread
        /// </summary>
        public void ThreadFuncLogin(object[] data)
        {
            string Errmsg = ""; 
            if (!Tool.LogIn(Username, Password, out Errmsg))
            {
                Errlabel = "Login Err!";
                ShowMainPage(true);
                return;
            }

            //Set Config
            Config.AddHistoryAccount(Username, Password);
            
            //Test
            //Tool.GetVideoDLUrls("25747558", "720", out Errmsg);
            //Tool.Search("Rolling", 10, out Errmsg);

            //Open MainWindow
            if (Application.Current != null)
            {
                Application.Current.Dispatcher.BeginInvoke((Action)delegate ()
                {
                    VMMain.SetLogViewModel(this);
                    Manager.ShowWindow(VMMain);
                    RequestClose();
                    ShowMainPage(true);
                });
            }
        }
        #endregion
    }



}
