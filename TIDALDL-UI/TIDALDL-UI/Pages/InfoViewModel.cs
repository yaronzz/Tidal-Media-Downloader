using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Imaging;
using Tidal;
using AIGS.Helper;
using AIGS.Common;
using System.Collections.ObjectModel;
using TIDALDL_UI.Else;
using Stylet;
namespace TIDALDL_UI.Pages
{
    public class InfoItem : Screen
    {
        public int    Number { get; set; }
        public string Title { get; set; }
        public string Type { get; set; }
        public string Duration { get; set; }
        public string AlbumTitle { get; set; }

        public InfoItem(int number, string title, string duration, string albumtitle, string type="TRACK")
        {
            Number     = number;
            Title      = title;
            Type       = type;
            Duration   = duration;
            AlbumTitle = albumtitle;
        }
    }

    public class InfoViewModel:Screen
    {
        public string Header { get; private set; }
        public string Title { get; private set; }
        public string Intro { get; private set; }
        public string ReleaseDate { get; private set; }
        public BitmapImage Cover { get; private set; }
        public bool   Result { get; set; }

        /// <summary>
        /// Item List
        /// </summary>
        public ObservableCollection<InfoItem> ItemList { get; private set; }

        #region Button
        public void Confirm()
        {
            Result = true;
            RequestClose();
        }

        public void Cancel()
        {
            Result = false;
            RequestClose();
        }
        #endregion

        public object Load(object data)
        {
            if(data.GetType() == typeof(Artist))
            {
                Artist artist = (Artist)data;
                Header        = "ARTISTINFO";
                Title         = artist.Name;
                Intro         = string.Format("by {0} Albums-{1}", artist.Name, artist.Albums.Count);
                Cover         = AIGS.Common.Convert.ConverByteArrayToBitmapImage(artist.CoverData);
                ReleaseDate   = "";
                ItemList      = new ObservableCollection<InfoItem>();
                if (artist.Albums != null)
                {
                    foreach (Album item in artist.Albums)
                        ItemList.Add(new InfoItem(artist.Albums.IndexOf(item) + 1, item.Title, TimeHelper.ConverIntToString(item.Duration), item.Title));
                }
            }
            if (data.GetType() == typeof(Album))
            { 
                Album album = (Album)data;
                Header      = "ALBUMINFO";
                Title       = album.Title;
                Intro       = string.Format("by {0}-{1} Tracks-{2} Videos-{3}", album.Artist.Name, TimeHelper.ConverIntToString(album.Duration), album.NumberOfTracks, album.NumberOfVideos);
                Cover       = AIGS.Common.Convert.ConverByteArrayToBitmapImage(album.CoverData);
                ReleaseDate = "Release date " + album.ReleaseDate;
                ItemList    = new ObservableCollection<InfoItem>();
                if (album.Tracks != null)
                {
                    foreach (Track item in album.Tracks)
                        ItemList.Add(new InfoItem(item.TrackNumber, item.Title, TimeHelper.ConverIntToString(item.Duration), item.Album.Title));
                }
                if (album.Videos != null)
                {
                    foreach (Video item in album.Videos)
                        ItemList.Add(new InfoItem(item.TrackNumber, item.Title, TimeHelper.ConverIntToString(item.Duration), item.Album.Title, "VIDEO"));
                }
            }
            else if (data.GetType() == typeof(Video))
            {
                Video video = (Video)data;
                Header      = "VIDEOINFO";
                Title       = video.Title;
                Cover       = AIGS.Common.Convert.ConverByteArrayToBitmapImage(video.CoverData);
                Intro       = string.Format("by {0}-{1}", video.Artist.Name, TimeHelper.ConverIntToString(video.Duration));
                ReleaseDate = "Release date " + video.ReleaseDate;
                ItemList    = new ObservableCollection<InfoItem>();
                ItemList.Add(new InfoItem(0, video.Title, TimeHelper.ConverIntToString(video.Duration), video.Album == null ? "" : video.Album.Title, "VIDEO"));
            }
            return data;
        }
    }
}
