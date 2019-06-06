using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Stylet;
using AIGS.Common;
using AIGS.Helper;
using Tidal;
using TIDALDL_UI.Else;
using MaterialDesignThemes.Wpf;
using System.Threading;
using System.Windows;
using System.Collections.ObjectModel;

namespace TIDALDL_UI.Pages
{
    public class MainViewModel : Screen
    {
        /// <summary>
        /// Errmsg
        /// </summary>
        public string Errlabel { get; set; } = "";
        public bool ShowErrlabel { get; set; } = false;
        /// <summary>
        /// Search Text/List/Thread 
        /// </summary>
        public string SearchStr { get; set; }
        public int SelectIndex { get; set; }
        public ObservableCollection<string> SearchList { get; set; }
        private Thread SearchTread;

        /// <summary>
        /// Download Items
        /// </summary>
        public BindableCollection<MainListItemViewModel> ItemList { get; } = new BindableCollection<MainListItemViewModel>();

        /// <summary>
        /// Open Window Tool
        /// </summary>
        private IWindowManager Manager;

        /// <summary>
        /// All Windows
        /// </summary>
        private LoginViewModel VMLogin;
        private SettingViewModel VMSetting;
        private AboutViewModel VMAbout;
        private WaitViewModel VMWait;
        private InfoViewModel VMInfo;
        private SearchViewModel VMSearch;

        public MainViewModel(IWindowManager manager,
                            SettingViewModel setting,
                            AboutViewModel about,
                            WaitViewModel wait,
                            InfoViewModel albuminfo,
                            SearchViewModel search)
        {
            Manager     = manager;
            VMSetting   = setting;
            VMAbout     = about;
            VMWait      = wait;
            VMInfo      = albuminfo;
            VMSearch    = search;
            SearchList  = Config.HistorySearchs();
            SearchStr   = "79412401";
            return;
        }

        public void SetLogViewModel(LoginViewModel model)
        {
            VMLogin = model;
        }

        public void WindowClose()
        {
            ThreadTool.Close();
            RequestClose();
        }

        public void SelectChange()
        {
            if (SelectIndex < 0 || SelectIndex >= SearchList.Count)
                return;
            SearchStr = SearchList[SelectIndex];
        }

        #region Button
        /// <summary>
        /// Search Func
        /// </summary>
        public void Search()
        {
            Errlabel = "";
            if (SearchStr.IsBlank())
                Errlabel = "Search String is Err!";
            if(SearchTread != null)
                Errlabel = "Somethig is in Searching!";
            if (Errlabel.IsNotBlank())
            {
                ShowErrlabel = true;
                return;
            }
            
            SearchTread = ThreadHelper.Start(ThreadFuncSearch);
            ShowWaitView(ThreadSearchClose);
        }

        public void Logout()
        {
            Manager.ShowWindow(VMLogin);
            WindowClose();
        }

        /// <summary>
        /// Show Setting Window
        /// </summary>
        public void Setting()
        {
            Manager.ShowDialog(VMSetting);

            string sValue = Config.ThreadNum();
            ThreadTool.SetThreadNum(int.Parse(sValue));
        }

        /// <summary>
        /// Show About Window
        /// </summary>
        public void About()
        {
            Manager.ShowDialog(VMAbout);
        }

        /// <summary>
        /// FeedBack In Project Page
        /// </summary>
        public void FeedBack()
        {
            NetHelper.OpenWeb("https://github.com/yaronzz/Tidal-Media-Downloader/issues");
        }

        /// <summary>
        /// Close Errlabel Box
        /// </summary>
        public void CloseErrlabel()
        {
            ShowErrlabel = false;
        }
        #endregion

        #region WaitForm
        /// <summary>
        /// Show Wait Window
        /// </summary>
        public void ShowWaitView(WaitViewModel.CloseFunc Func)
        {
            VMWait.Init(Func);
            Manager.ShowDialog(VMWait);
        }

        /// <summary>
        /// Close Wait Window
        /// </summary>
        public void CloseWaitView()
        {
            VMWait.Close();
        }

        #endregion 



        #region Search Thread
        /// <summary>
        /// Login Thread
        /// </summary>
        public void ThreadFuncSearch(object[] data)
        {
            string sID           = SearchStr;
            string sType         = null;
            object oRecord       = null;

            oRecord = Tool.TryGet(sID, out sType);
            if (Application.Current != null)
            {
                Application.Current.Dispatcher.BeginInvoke((Action)delegate ()
                {
                    if (sType.IsNotBlank())
                    {
                        Config.AddHistorySearch(SearchStr);
                        SearchList = Config.HistorySearchs();
                        if (sType == "Search")
                        {
                            VMSearch.Load((SearchResult)oRecord);
                            Manager.ShowDialog(VMSearch);
                            if (VMSearch.ResultID.IsNotBlank())
                            {
                                sID = VMSearch.ResultID;
                                oRecord = Tool.TryGet(sID, out sType);
                            }
                        }

                        if (sType.IsNotBlank() && sType != "Search")
                        {
                            oRecord = VMInfo.Load(oRecord);
                            Manager.ShowDialog(VMInfo);
                            if (VMInfo.Result)
                            {
                                MainListItemViewModel newNode = new MainListItemViewModel(oRecord, VMInfo.OutputDir, VMInfo.QualityList[VMInfo.SelectQualityIndex], Config.Resolution());
                                ItemList.Add(newNode);
                                newNode.StartWork();
                            }
                        }
                    }
                    else
                    {
                        Errlabel = "Search Err!";
                        ShowErrlabel = true;
                    }
                    CloseWaitView();
                });
            }
        }

        /// <summary>
        /// Close Login Thread
        /// </summary>
        public void ThreadSearchClose()
        {
            SearchTread.Abort();
            SearchTread = null;
        }
        #endregion
    }
}
