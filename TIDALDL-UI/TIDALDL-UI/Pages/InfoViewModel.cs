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
        public int Number { get; set; }
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

        /// <summary>
        /// Common Info
        /// </summary>
        public string Title { get; private set; }
        public string Intro { get; private set; }
        public string ReleaseDate { get; private set; }

        /// <summary>
        /// Conver
        /// </summary>
        public BitmapImage Cover { get; private set; }

        /// <summary>
        /// Item List
        /// </summary>
        public ObservableCollection<InfoItem> ItemList { get; private set; }

        /// <summary>
        /// Quality 
        /// </summary>
        public int SelectQualityIndex { get; set; }
        public Dictionary<int, string> QualityList { get; set; }
        public int QualityWidth { get; set; }

        /// <summary>
        /// Download Path
        /// </summary>
        public string OutputDir { get; set; }

        /// <summary>
        /// Is Download
        /// </summary>
        public bool Result { get; set; }

        #region Button
        public void Confirm()
        {
            Result = true;
            RequestClose();
        }

        public void Cancle()
        {
            Result = false;
            RequestClose();
        }
        #endregion



        public object Load(object data)
        {
            if(data.GetType() == typeof(Album))
            { 
                Album album = (Album)data;
                Header      = "ALBUMINFO";
                Title       = album.Title;
                Intro       = string.Format("by {0}-{1} Tracks-{2} Videos-{3}", album.Artist.Name, TimeHelper.ConverIntToString(album.Duration), album.NumberOfTracks, album.NumberOfVideos);
                Cover       = AIGS.Common.Convert.ConverByteArrayToBitmapImage(album.CoverData);
                ReleaseDate = "Release date " + album.ReleaseDate;
                ItemList    = new ObservableCollection<InfoItem>();
                if (album.Tracks.Count > 0)
                    QualityWidth = 90;

                if(album.Tracks != null)
                    foreach (Track item in album.Tracks)
                        ItemList.Add(new InfoItem(item.TrackNumber, item.Title, item.SDuration, item.Album.Title));
                if (album.Videos != null)
                    foreach (Video item in album.Videos)
                        ItemList.Add(new InfoItem(item.TrackNumber, item.Title, item.SDuration, item.Album.Title, "VIDEO"));
            }
            else if (data.GetType() == typeof(Video))
            {
                Video video = (Video)data;
                Header      = "VIDEOINFO";
                Title       = video.Title;
                Intro       = string.Format("by {0}-{1}", video.Artist.Name, video.SDuration);
                Cover       = AIGS.Common.Convert.ConverByteArrayToBitmapImage(video.CoverData);
                ReleaseDate = "Release date " + video.ReleaseDate;
                ItemList    = new ObservableCollection<InfoItem>();
                QualityWidth = 0;
                ItemList.Add(new InfoItem(0, video.Title, video.SDuration, video.Album == null? "" : video.Album.Title, "VIDEO"));
            }

            //Init QualityList
            QualityList = Config.QualityList();
            SelectQualityIndex = Config.QualityIndex();

            //Read OutputPath
            OutputDir = Config.OutputDir();

            return data;
        }
    }
}
