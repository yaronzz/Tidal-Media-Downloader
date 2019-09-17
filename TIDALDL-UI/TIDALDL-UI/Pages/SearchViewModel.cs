using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Imaging;
using AIGS.Helper;
using AIGS.Common;
using System.Collections.ObjectModel;
using TIDALDL_UI.Else;
using Stylet;
using System.Windows;
using Tidal;

namespace TIDALDL_UI.Pages
{
    public class SearchItem
    {
        public string Title { get; set; }
        public string Artist { get; set; }
        public string Duration { get; set; }
        public int Index { get; set; }
        public SearchItem(int index, string title, string artist, string duration)
        {
            Index = index;
            Title = title;
            Artist = artist;
            Duration = duration;
        }
    }

    public class SearchViewModel : Screen
    {
        public string Header { get; private set; } = "SEARCH";
        public int SelectIndex { get; set; } = 0;
        public bool bCheckPlaylist { get; set; } = false;
        public bool bCheckArtist { get; set; } = false;
        public bool bCheckAlbum { get; set; } = true;
        public bool bCheckTrack { get; set; } = false;
        public bool bCheckVideo { get; set; } = false;
        public Visibility ShowWait { get; set; } = Visibility.Hidden;
        public List<SearchItem> PlayList { get; set; } = new List<SearchItem>();
        public List<SearchItem> ArtistList { get; set; } = new List<SearchItem>();
        public List<SearchItem> AlbumList { get; set; } = new List<SearchItem>();
        public List<SearchItem> TrackList { get; set; } = new List<SearchItem>();
        public List<SearchItem> VideoList { get; set; } = new List<SearchItem>();
        public List<SearchItem> BindList
        {
            set { return; }
            get
            {
                if (bCheckPlaylist) return PlayList;
                if (bCheckArtist) return ArtistList;
                if (bCheckAlbum) return AlbumList;
                if (bCheckTrack) return TrackList;
                return VideoList;
            }
        }
        public SearchResult SearchInfo = null;
        public eObjectType ResultType = eObjectType.None;
        public object ResultObject = null;

        #region Button
        public async void Confirm()
        {
            string ResultID = null;
            if (SelectIndex >= 0)
            {
                if (bCheckPlaylist && SearchInfo.Playlists.Count > 0)
                {
                    ResultID = SearchInfo.Playlists[SelectIndex].UUID.ToString();
                    ResultType = eObjectType.PLAYLIST;
                }
                if (bCheckArtist && SearchInfo.Artists.Count > 0)
                {
                    ResultID = SearchInfo.Artists[SelectIndex].ID.ToString();
                    ResultType = eObjectType.ARTIST;
                }
                if (bCheckAlbum && SearchInfo.Albums.Count > 0)
                {
                    ResultID = SearchInfo.Albums[SelectIndex].ID.ToString();
                    ResultType = eObjectType.ALBUM;
                }
                if (bCheckTrack && SearchInfo.Tracks.Count > 0)
                {
                    ResultID = SearchInfo.Tracks[SelectIndex].ID.ToString();
                    ResultType = eObjectType.TRACK;
                }
                if (bCheckVideo && SearchInfo.Videos.Count > 0)
                {
                    ResultID = SearchInfo.Videos[SelectIndex].ID.ToString();
                    ResultType = eObjectType.VIDEO;
                }

                ShowWait = Visibility.Visible;
                await Task.Run(() =>
                {
                    ResultObject = TidalTool.tryGet(ResultID, out ResultType, ResultType);
                });
            }
            RequestClose();
        }

        public void Cancel()
        {
            ResultType = eObjectType.None;
            RequestClose();
        }
        #endregion

        public void Load(SearchResult SearchInfo)
        {
            ShowWait = Visibility.Hidden;
            PlayList = new List<SearchItem>();
            ArtistList = new List<SearchItem>();
            AlbumList = new List<SearchItem>();
            TrackList = new List<SearchItem>();
            VideoList = new List<SearchItem>();
            this.SearchInfo = SearchInfo;
            foreach (Playlist item in SearchInfo.Playlists)
                PlayList.Add(new SearchItem(SearchInfo.Playlists.IndexOf(item) + 1, item.Title, item.Title, TimeHelper.ConverIntToString(item.Duration)));
            foreach (Artist item in SearchInfo.Artists)
                ArtistList.Add(new SearchItem(SearchInfo.Artists.IndexOf(item) + 1, item.Name, item.Name, ""));
            foreach (Album item in SearchInfo.Albums)
                AlbumList.Add(new SearchItem(SearchInfo.Albums.IndexOf(item) + 1, item.Title, item.Artists[0].Name, TimeHelper.ConverIntToString(item.Duration)));
            foreach (Track item in SearchInfo.Tracks)
                TrackList.Add(new SearchItem(SearchInfo.Tracks.IndexOf(item) + 1, item.Title, item.Artists[0].Name, TimeHelper.ConverIntToString(item.Duration)));
            foreach (Video item in SearchInfo.Videos)
                VideoList.Add(new SearchItem(SearchInfo.Videos.IndexOf(item) + 1, item.Title, item.Artists[0].Name, TimeHelper.ConverIntToString(item.Duration)));
        }
    }
}
