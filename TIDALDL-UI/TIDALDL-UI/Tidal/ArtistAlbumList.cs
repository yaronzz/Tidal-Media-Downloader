
using Newtonsoft.Json;
using System.Collections.ObjectModel;

namespace Tidal
{
    public class ArtistAlbumList
    {
        [JsonProperty("totalNumberOfItems")]
        public int TotalAlbums { get; set; }

        private Artist artist;
        public Artist Artist
        {
            get { return artist; }
            set { artist = value; }
        }
        // items in json and Albums Really
        private ObservableCollection<Album> items;
        public ObservableCollection<Album> Items
        {
            get { return items; }
            set { items = value; }
        }
        public ObservableCollection<Album> Albums
        {
            get { return items; }
            set { items = value; }
        }

        private ObservableCollection<Video> videos;
        public ObservableCollection<Video> Videos
        {
            get { return videos; }
            set { videos = value; }
        }
    }
}
