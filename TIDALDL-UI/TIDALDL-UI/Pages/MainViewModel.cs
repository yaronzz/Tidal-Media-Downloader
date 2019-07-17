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
using System.IO;
using ICSharpCode.SharpZipLib.Zip;

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
        /// Update Thread
        /// </summary>
        private Thread UpdateThread;

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
            SearchStr   = SearchList.Count > 0 ? SearchList[0] : null;

            UpdateThread = new Thread(ThreadUpdateFunc);
            UpdateThread.IsBackground = true;
            UpdateThread.Start();
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
                            sType   = VMSearch.ResultType;
                            oRecord = VMSearch.ResultObject;
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

        #region Version Update Thread
        public void ThreadUpdateFunc()
        {
            string PATH = Path.GetFullPath("./tidal_new/");
            string VERF = PATH + "version";
            string BATF = PATH + "update.bat";
            string sSelfVer = VersionHelper.GetSelfVersion();

            //Get Already Download Ver
            string sDlVer = FileHelper.Read(VERF);
            if(sDlVer.IsNotBlank() && VersionHelper.Compare(sSelfVer, sDlVer) < 0 && File.Exists(PATH + "tidal-gui.exe") && File.Exists(BATF))
            {
                MessageBoxResult ret = MessageBox.Show("Update New Version?", "Info", MessageBoxButton.YesNo);
                if (ret == MessageBoxResult.No)
                    return;

                if (Application.Current != null)
                {
                    Application.Current.Dispatcher.BeginInvoke((Action)delegate ()
                    {
                        CmdHelper.StartExe(BATF, null, IsShowWindow: false);
                        RequestClose();
                    });
                }
                return;
            }

            //Get Github Last Ver
            string sLastVer = githubHelper.getLastReleaseVersion("yaronzz", "Tidal-Media-Downloader");
            if (VersionHelper.Compare(sSelfVer, sLastVer) >= 0)
                return;

            if (Directory.Exists(PATH))
                Directory.Delete(PATH, true);
            PathHelper.Mkdirs(PATH);
            if (githubHelper.getLastReleaseFile("yaronzz", "Tidal-Media-Downloader", "tidal-gui.zip", PATH + "tidal-gui.zip"))
            {
                FastZip fz = new FastZip();
                try
                {
                    fz.ExtractZip(PATH + "tidal-gui.zip", PATH, null);
                    if (File.Exists(PATH + "tidal-gui.exe"))
                    {
                        string sBat = "ping -n 5 127.0.0.1\n";
                        sBat += string.Format("move {0}tidal-gui.exe {0}..\\tidal-gui.exe\n", PATH);
                        sBat += string.Format("start {0}..\\tidal-gui.exe\n", PATH);
                        FileHelper.Write(sBat, true, BATF);
                        FileHelper.Write(sLastVer, true, VERF);
                    }
                }
                catch (Exception e)
                {
                   return;
                }
            }
        }
        #endregion

    }
}
