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
using System.Windows.Controls;

namespace TIDALDL_UI.Pages
{
    public class MainViewModel : Screen
    {
        public string Errlabel { get; set; }
        public string SearchStr { get; set; }
        public bool   InSearch { get; set; }

        public string SearchHelperTip { get; set; } =
            "You can search album\\track\\video\\artist\\playlist! Example:\n\n" +
            "ID   : 71121869 (from https://listen.tidal.com/albums/71121869) \n" +
            "Title: Adele (or track\\video\\album title) \n" +
            "Url  : https://listen.tidal.com/albums/71121869";

        /// <summary>
        /// Download Items 
        /// </summary>
        public BindableCollection<MainListItemViewModel> ItemList { get; } = new BindableCollection<MainListItemViewModel>();
        public Thread UpdateThread;

        /// <summary>
        /// Combox
        /// </summary>
        public List<string> QualityList { get; set; }
        public int SelectQualityIndex { get; set; }
        public List<string> ResolutionList { get; set; }
        public int SelectResolutionIndex { get; set; }

        private IWindowManager Manager; 
        private LoginViewModel VMLogin;
        private SettingViewModel VMSetting;
        private AboutViewModel VMAbout;
        private InfoViewModel VMInfo;
        private SearchViewModel VMSearch;
        private DllistViewModel VMDllist;

        public MainViewModel(IWindowManager manager,
                            SettingViewModel setting,
                            AboutViewModel about,
                            InfoViewModel albuminfo,
                            SearchViewModel search,
                            DllistViewModel dllist)
        {
            Manager   = manager;
            VMSetting = setting;
            VMAbout   = about;
            VMInfo    = albuminfo;
            VMSearch  = search;
            VMDllist  = dllist;
            ThreadTool.SetThreadNum(int.Parse(Config.ThreadNum()));

            UpdateThread = new Thread(ThreadUpdateFunc);
            UpdateThread.IsBackground = true;
            UpdateThread.Start();

            QualityList = TidalTool.getQualityList();
            SelectQualityIndex = QualityList.IndexOf(Config.Quality().ToUpper());
            if (SelectQualityIndex < 0)
                SelectQualityIndex = 0;

            ResolutionList = TidalTool.getResolutionList();
            SelectResolutionIndex = ResolutionList.IndexOf(Config.Resolution().ToUpper());
            if (SelectResolutionIndex < 0)
                SelectResolutionIndex = 0;

            TidalTool.SetSearchMaxNum(int.Parse(Config.SearchNum()));

            //test
            //VMDllist.Convert();
            //return;
        }

        public void SetLogViewModel(LoginViewModel model)
        {
            VMLogin = model;
        }

        public void WindowClose()
        {
            ThreadTool.Close();
            ThreadHelper.Abort(UpdateThread);
            RequestClose();
        }

        //protected override void OnInitialActivate()
        //{
        //    //show about page
        //    if (Config.Version() != VersionHelper.GetSelfVersion())
        //    {
        //        Config.Version(VersionHelper.GetSelfVersion());
        //        Manager.ShowDialog(VMAbout);
        //    }
        //}

        public void QualityChanged(object sender, SelectionChangedEventArgs e)
        {
            Config.Quality(QualityList[SelectQualityIndex].ToLower());
        }

        public void ResolutionChanged(object sender, SelectionChangedEventArgs e)
        {
            Config.Resolution(ResolutionList[SelectResolutionIndex]);
        }

        #region Button
        public async void Search()
        {
            if (InSearch)
                return;
            if (SearchStr.IsBlank())
            {
                Errlabel = "Search string is empty!";
                return;
            }
            
            //Search
            InSearch               = true;
            eObjectType SearchType = eObjectType.None;
            object SearchObj       = await Task.Run(() => { return TidalTool.tryGet(SearchStr, out SearchType); });
            InSearch               = false;

            if (SearchType == eObjectType.None)
            {
                Errlabel = "Search Err!";
                return;
            }
            if (SearchType == Tidal.eObjectType.SEARCH)
            {
                VMSearch.Load((Tidal.SearchResult)SearchObj);
                Manager.ShowDialog(VMSearch);
                SearchType = VMSearch.ResultType;
                SearchObj  = VMSearch.ResultObject;
                if (SearchType == eObjectType.None)
                    return;
            }

            SearchObj = VMInfo.Load(SearchObj);
            Manager.ShowDialog(VMInfo);
            if (VMInfo.Result)
            {
                MainListItemViewModel newNode = new MainListItemViewModel(SearchObj, ItemList);
                ItemList.Add(newNode);
                newNode.StartWork();
            }
        }

        public void OpenDllist()
        {
            VMDllist.Items.Clear();
            Manager.ShowDialog(VMDllist);
            for (int i = 0; i < VMDllist.Items.Count; i++)
            {
                if (VMDllist.Items[i].Type == eObjectType.None)
                    continue;
                MainListItemViewModel newNode = new MainListItemViewModel(VMDllist.Items[i].Data, ItemList);
                ItemList.Add(newNode);
                newNode.StartWork();
            }
        }
        public void Logout()
        {
            TidalTool.logout();
            Manager.ShowWindow(VMLogin);
            WindowClose();
        }
        public void Setting()
        {
            VMSetting.RefreshSetting();
            Manager.ShowDialog(VMSetting);
            string sValue = Config.ThreadNum();
            ThreadTool.SetThreadNum(int.Parse(sValue));

            SelectQualityIndex = QualityList.IndexOf(Config.Quality().ToUpper());
            SelectResolutionIndex = ResolutionList.IndexOf(Config.Resolution().ToUpper());
        }
        public void About()
        {
            Manager.ShowDialog(VMAbout);
        }
        public void FeedBack()
        {
            NetHelper.OpenWeb("https://github.com/yaronzz/Tidal-Media-Downloader/issues");
        }
        public void CloseErrlabel()
        {
            Errlabel = null;
        }
        public void WindowMin()
        {
            ((MainView)this.View).WindowState = WindowState.Minimized;
        }
        public void WindowMax()
        {
            ScreenShotHelper.MaxWindow((Window)this.View);
        }
        #endregion

        #region Version Update Thread
        public void ThreadUpdateFunc()
        {
            string PATH = Path.GetFullPath("./tidal_new/");
            string VERF = PATH + "version";
            string BATF = PATH + "update.bat";
            string sSelfVer = VersionHelper.GetSelfVersion();

            //Replace new version 
            string sDlVer = FileHelper.Read(VERF);
            if (sDlVer.IsNotBlank() && VersionHelper.Compare(sSelfVer, sDlVer) < 0 && File.Exists(PATH + "tidal-gui.exe") && File.Exists(BATF))
            {
                MessageBoxResult ret = MessageBox.Show("Update new version?", "Info", MessageBoxButton.YesNo, MessageBoxImage.Information);
                if (ret == MessageBoxResult.No)
                    return;

                if (Application.Current != null)
                {
                    Application.Current.Dispatcher.BeginInvoke((Action)delegate ()
                    {
                        CmdHelper.StartExe(BATF, null, IsShowWindow: false);
                        WindowClose();
                    });
                }
                return;
            }

           
            //Get github new version
            string sLastVer = GithubHelper.getLastReleaseVersion("yaronzz", "Tidal-Media-Downloader");
            if (VersionHelper.Compare(sSelfVer, sLastVer) >= 0)
                return;

            if (Directory.Exists(PATH))
                Directory.Delete(PATH, true);
            PathHelper.Mkdirs(PATH);
            if (GithubHelper.getLastReleaseFile("yaronzz", "Tidal-Media-Downloader", "tidal-gui.zip", PATH + "tidal-gui.zip"))
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
                catch
                {
                    return;
                }
            }
        }
        #endregion
    }
}
