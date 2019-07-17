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
using System.Windows;

namespace TIDALDL_UI.Pages
{
    public class SearchItem
    {
        public string Title { get; set; }
        public string Artist { get; set; }
        public string Duration { get; set; }
        public SearchItem(string title, string artist, string duration)
        {
            Title = title;
            Artist = artist;
            Duration = duration;
        }
    }

    public class SearchViewModel:Screen
    {
        public string Header    { get; private set; } = "SEARCH";
        public int  SelectIndex { get; set; } = 0;
        public bool bCheckAlbum { get; set; } = true;
        public bool bCheckTrack { get; set; } = false;
        public bool bCheckVideo { get; set; } = false;
        public Visibility ShowWait { get; set; } = Visibility.Hidden;
        public List<SearchItem> AlbumList { get; set; } = new List<SearchItem>();
        public List<SearchItem> TrackList { get; set; } = new List<SearchItem>();
        public List<SearchItem> VideoList { get; set; } = new List<SearchItem>();
        public List<SearchItem> BindList {
            set { return; }
            get {
                if (bCheckAlbum) return AlbumList;
                if (bCheckTrack) return TrackList;
                return VideoList;
            }
        }
        public SearchResult SearchInfo = null;

        public string ResultID = null;
        public string ResultType = null;
        public object ResultObject = null;

        #region Button
        public async void Confirm()
        {
            ResultID = null;
            if (SelectIndex >= 0)
            {
                if (bCheckAlbum && SearchInfo.Albums.Count > 0)
                    ResultID = SearchInfo.Albums[SelectIndex].ID.ToString();
                if (bCheckTrack && SearchInfo.Tracks.Count > 0)
                    ResultID = SearchInfo.Tracks[SelectIndex].ID;
                if (bCheckVideo && SearchInfo.Videos.Count > 0)
                    ResultID = SearchInfo.Videos[SelectIndex].ID;

                ShowWait = Visibility.Visible;
                await Task.Run(() =>
                {
                    ResultObject = Tool.TryGet(ResultID, out ResultType);
                });
            }
            RequestClose();
        }

        public void Cancel()
        {
            ResultID = null;
            RequestClose();
        }
        #endregion

        public void Load(SearchResult SearchInfo)
        {
            ShowWait = Visibility.Hidden;
            AlbumList = new List<SearchItem>();
            TrackList = new List<SearchItem>();
            VideoList = new List<SearchItem>();
            this.SearchInfo = SearchInfo;
            foreach (Album item in SearchInfo.Albums)
                AlbumList.Add(new SearchItem(item.Title, item.Artists[0].Name, TimeHelper.ConverIntToString(item.Duration)));
            foreach (Track item in SearchInfo.Tracks)
                TrackList.Add(new SearchItem(item.Title, item.Artists[0].Name, TimeHelper.ConverIntToString(item.Duration)));
            foreach (Video item in SearchInfo.Videos)
                VideoList.Add(new SearchItem(item.Title, item.Artists[0].Name, TimeHelper.ConverIntToString(item.Duration)));
        }
    }
}
