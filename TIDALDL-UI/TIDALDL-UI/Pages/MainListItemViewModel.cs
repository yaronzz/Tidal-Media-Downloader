using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using AIGS.Helper;
using AIGS.Common;
using Stylet;
using System.Windows.Media.Imaging;
using Tidal;
using System.Diagnostics;
using TIDALDL_UI.Else;
using System.Collections.ObjectModel;
using System.Windows;
using System.IO;

namespace TIDALDL_UI.Pages
{
    public class MainListItemViewModel : Screen
    {
        /// <summary>
        /// Item Name | Type(Album\Track\Video\Playlist) | Cover | SvaePath | Quality
        /// </summary>
        public string Title { get; private set; }
        public string Type { get; private set; }
        public string Author { get; set; }
        public BitmapImage Cover { get; private set; }
        public string BasePath { get; private set; }
        public string Quality { get; private set; }

        /// <summary>
        /// Item Objec - Album|Playlist|Track|Video
        /// </summary>
        public Album TidalAlbum { get; private set; }
        public Playlist TidalPlaylist { get; private set; }
        public Track TidalTrack { get; private set; }
        public Video TidalVideo { get; private set; }

        /// <summary>
        /// Item DowmloadList
        /// </summary>
        public ObservableCollection<DownloadItem> DLItemList { get; set; }

        /// <summary>
        /// Progress
        /// </summary>
        public ProgressHelper Progress { get; set; }


        public MainListItemViewModel(Album album, string quality, string path)
        {
            TidalAlbum = album;
            Title      = album.Title;
            Type       = "Album";
            Quality    = quality;
            BasePath   = path + "\\Album\\" + Tool.GetAlbumFolderName(album);
            Cover      = AIGS.Common.Convert.ConverByteArrayToBitmapImage(album.CoverData);
            Author     = album.Artist.Name;
            Progress   = new ProgressHelper();

            //Save Cover
            string CoverPath = BasePath + '\\' + Tool.GetAlbumCoverName(album);
            FileHelper.Write(album.CoverData, true, CoverPath);

            //init DownloadList
            DLItemList = new ObservableCollection<DownloadItem>();
            foreach (Track item in album.Tracks)
                DLItemList.Add(new DownloadItem(DLItemList.Count, item, quality, BasePath, Update));
        }

        /// <summary>
        /// Update Progress
        /// </summary>
        /// <param name="item"></param>
        public void Update(DownloadItem item)
        {
            if (item.Progress.IsErr)
                this.Progress.IsErr = true;
            if (item.Progress.IsComplete)
                this.Progress.Update(this.Progress.CurSize + 1, DLItemList.Count);
        }

        /// <summary>
        /// Start All Download List Items
        /// </summary>
        public void StartWork()
        {
            foreach (DownloadItem item in DLItemList)
                item.Start();
        }

        #region Button
        /// <summary>
        /// Cancle Work
        /// </summary>
        public void Cancel()
        {
            foreach (DownloadItem item in DLItemList)
                item.Cancle();
            this.Progress.IsCancle = true;
        }

        /// <summary>
        /// Open BasePath
        /// </summary>
        public void OpenBasePath()
        {
            Process.Start(BasePath);
        }
        #endregion

    }
}
