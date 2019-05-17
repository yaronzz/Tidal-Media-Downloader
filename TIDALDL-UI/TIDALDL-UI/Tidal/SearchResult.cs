using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tidal
{
    public class SearchResult
    {
        public ObservableCollection<Album> Albums { get; set; }
        public ObservableCollection<Track> Tracks { get; set; }
        public ObservableCollection<Video> Videos { get; set; }
        public ObservableCollection<Playlist> Playlists { get; set; }
    }
}
