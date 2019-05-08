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
        public string Errlabel { get; set; }

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
        private AlbumInfoViewModel VMAlbumInfo;

        public MainViewModel(IWindowManager manager,
                            SettingViewModel setting,
                            AboutViewModel about,
                            WaitViewModel wait,
                            AlbumInfoViewModel albuminfo)
        {
            Manager     = manager;
            VMSetting   = setting;
            VMAbout     = about;
            VMWait      = wait;
            VMAlbumInfo = albuminfo;
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
                Manager.ShowMessageBox(Errlabel);
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


        #region Thread
        /// <summary>
        /// Login Thread
        /// </summary>
        public void ThreadFuncSearch(object[] data)
        {
            string sID     = SearchStr;
            string sErrmsg = null;
            string sType   = null;
            Album aAlbum   = null;
            Track aTrack   = null;

            //Search Album
            aAlbum = Tool.GetAlbum(sID, out sErrmsg);
            if(aAlbum != null)
            {
                sType = "Album";
                goto SEARCH_POINT;
            }

            //Search Track
            aTrack = Tool.GetTrack(sID, out sErrmsg);
            if(aTrack != null)
            {
                aAlbum = Tool.GetAlbum(aTrack.Album.ID.ToString(), out sErrmsg, false);
                if(aAlbum != null)
                {
                    aAlbum.Tracks.Add(aTrack);
                    sType = "Album";
                    goto SEARCH_POINT;
                }
            }

        SEARCH_POINT:
            if (sType.IsNotBlank() && Application.Current != null)
            {
                Config.AddHistorySearch(SearchStr);
                SearchList = Config.HistorySearchs();

                Application.Current.Dispatcher.BeginInvoke((Action)delegate ()
                {
                    if (sType == "Album")
                    {
                        VMAlbumInfo.Init(aAlbum);
                        Manager.ShowDialog(VMAlbumInfo);
                        if(VMAlbumInfo.Result)
                        {
                            MainListItemViewModel newNode = new MainListItemViewModel(aAlbum, VMAlbumInfo.QualityList[VMAlbumInfo.SelectQualityIndex], VMAlbumInfo.OutputDir);
                            ItemList.Add(newNode);
                            newNode.StartWork();
                        }
                    }
                    CloseWaitView();
                });
                return;
            }

            Errlabel = "Search Err!";
            CloseWaitView();
            return;
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
