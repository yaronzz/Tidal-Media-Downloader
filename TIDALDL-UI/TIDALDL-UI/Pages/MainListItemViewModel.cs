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
        public string Title { get; private set; }
        public string Desc { get; set; }
        public BitmapImage Cover { get; private set; }
        public string BasePath { get; private set; }
        public ObservableCollection<DownloadItem> DLItemList { get; set; }
        private BindableCollection<MainListItemViewModel> Parents { get; set; }

        public string ButtonKind { get; set; } = "CloseCircle";
        public string ButtonTip { get; set; } = "Cancel";

        public MainListItemViewModel(object data, BindableCollection<MainListItemViewModel> parents)
        {
            Parents    = parents;
            DLItemList = new ObservableCollection<DownloadItem>();
            if (data.GetType() == typeof(Album))
            {
                Album album = (Album)data;
                Title       = album.Title;
                BasePath    = TidalTool.getAlbumFolder(Config.OutputDir(), album);
                Desc        = string.Format("by {0}-{1} Tracks-{2} Videos-{3}", album.Artist.Name, TimeHelper.ConverIntToString(album.Duration), album.NumberOfTracks, album.NumberOfVideos);
                Cover       = AIGS.Common.Convert.ConverByteArrayToBitmapImage(album.CoverData);

                AddAlbum(album);
            }
            else if (data.GetType() == typeof(Video))
            {
                Video video = (Video)data;
                Title       = video.Title;
                BasePath    = TidalTool.getVideoFolder(Config.OutputDir());
                Desc        = string.Format("by {0}-{1}", video.Artist.Name, TimeHelper.ConverIntToString(video.Duration));
                Cover       = AIGS.Common.Convert.ConverByteArrayToBitmapImage(video.CoverData);
                DLItemList.Add(new DownloadItem(DLItemList.Count + 1, null, video, null));
            }
            else if(data.GetType() == typeof(Artist))
            {
                Artist artist = (Artist)data;
                Title         = artist.Name;
                BasePath      = TidalTool.getArtistFolder(Config.OutputDir(), artist);
                Desc          = string.Format("by {0} Albums-{1}", artist.Name, artist.Albums.Count);
                Cover         = AIGS.Common.Convert.ConverByteArrayToBitmapImage(artist.CoverData);

                foreach (var item in artist.Albums)
                    AddAlbum(item);
            }
            else if(data.GetType() == typeof(Playlist))
            {
                Playlist plist = (Playlist)data;
                Title          = plist.Title;
                BasePath       = TidalTool.getPlaylistFolder(Config.OutputDir(), plist);
                //Desc         = string.Format("by {0}-{1} Tracks-{2} Videos-{3}", plist.Created, TimeHelper.ConverIntToString(plist.Duration), plist.NumberOfTracks, plist.NumberOfVideos);
                Desc           = string.Format("{0} Tracks-{1} Videos-{2}", TimeHelper.ConverIntToString(plist.Duration), plist.NumberOfTracks, plist.NumberOfVideos);
                Cover          = AIGS.Common.Convert.ConverByteArrayToBitmapImage(plist.CoverData);
                foreach (Track item in plist.Tracks)
                    DLItemList.Add(new DownloadItem(DLItemList.Count + 1, item, null, album: null, plist:plist));
                foreach (Video item in plist.Videos)
                    DLItemList.Add(new DownloadItem(DLItemList.Count + 1, null, item, album: null, plist: plist));
            }

            PathHelper.Mkdirs(BasePath);
        }

        private void AddAlbum(Album album)
        {
            string CoverPath = TidalTool.getAlbumCoverPath(Config.OutputDir(), album);
            FileHelper.Write(album.CoverData, true, CoverPath);

            foreach (Track item in album.Tracks)
                DLItemList.Add(new DownloadItem(DLItemList.Count +1, item, null, album: album));
            foreach (Video item in album.Videos)
                DLItemList.Add(new DownloadItem(DLItemList.Count + 1, null, item, album: album));
        }

        public void StartWork()
        {
            foreach (DownloadItem item in DLItemList)
                item.Start();
        }

        #region Button
        public void CancelAndRestart()
        {
            if (ButtonKind == "CloseCircle")
            {
                foreach (DownloadItem item in DLItemList)
                    item.Cancel();
                ButtonKind = "Restart";
                ButtonTip  = "Restart";
            }
            else
            {
                foreach (DownloadItem item in DLItemList)
                    item.Restart();
                ButtonKind = "CloseCircle";
                ButtonTip  = "Cancel";
            }
        }

        public void Delete()
        {
            foreach (DownloadItem item in DLItemList)
                item.Cancel();
            Parents.Remove(this);
        }

        public void OpenBasePath()
        {
            Process.Start(BasePath);
        }
        #endregion

    }
}
