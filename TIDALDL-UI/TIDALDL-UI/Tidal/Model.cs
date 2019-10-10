using AIGS.Common;
using AIGS.Helper;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Imaging;
using TIDALDL_UI.Else;

namespace Tidal
{
    public class Album
    {
        public int ID { get; set; }
        public string Title { get; set; }
        public int Duration { get; set; }
        public bool StreamReady { get; set; }
        public string StreamStartDate { get; set; }
        public bool AllowStreaming { get; set; }
        public bool PremiumStreamingOnly { get; set; }
        public int NumberOfTracks { get; set; }
        public int NumberOfVideos { get; set; }
        public int NumberOfVolumes { get; set; }
        public string ReleaseDate { get; set; }
        public string Copyright { get; set; }
        public string Type { get; set; }
        public string Version { get; set; }
        public string Url { get; set; }
        public string Cover { get; set; }
        public string VideoCover { get; set; }
        public bool Exclicit { get; set; }
        public string Upc { get; set; }
        public int Popularity { get; set; }
        public string AudioQuality { get; set; }
        public Artist Artist { get; set; }
        public ObservableCollection<Artist> Artists { get; set; }

        public ObservableCollection<Track> Tracks { get; set; }
        public ObservableCollection<Video> Videos { get; set; }
        public byte[] CoverData { get; set; }

    }

    public class Artist
    {
        public int ID { get; set; }
        public string Name { get; set; }
        public string Type { get; set; }
        public string Url { get; set; }
        public string Picture { get; set; }
        public int Popularity { get; set; }
        public string[] ArtistTypes { get; set; }

        public ObservableCollection<Album> Albums { get; set; }
        public byte[] CoverData { get; set; }
    }

    public class Track
    {
        public int ID { get; set; }
        public string Title { get; set; }
        public int Duration { get; set; }
        public string ReplayGain { get; set; }
        public string Peak { get; set; }
        public bool AllowStreaming { get; set; }
        public bool StreamReady { get; set; }
        public string StreamStartDate { get; set; }
        public bool PremiumStreamingOnly { get; set; }
        public int TrackNumber { get; set; }
        public int VolumeNumber { get; set; }
        public string Version { get; set; }
        public int Popularity { get; set; }
        public string Copyright { get; set; }
        public string Url { get; set; }
        public string Isrc { get; set; }
        public bool Editable { get; set; }
        public bool Exclicit { get; set; }
        public string AudioQuality { get; set; }
        public Artist Artist { get; set; }
        public ObservableCollection<Artist> Artists { get; set; }
        public Album Album { get; set; }

    }

    public class StreamUrl
    {
        public int TrackID { get; set; }
        public string Url { get; set; }
        public string Codec { get; set; }
        public string EncryptionKey { get; set; }
        public int PlayTimeLeftInMinutes { get; set; }
        public string SoundQuality { get; set; }
    }

    public class Video
    {
        public int ID { get; set; }
        public string Title { get; set; }
        public int Duration { get; set; }
        public string ImageID { get; set; }
        public int TrackNumber { get; set; }
        public string ReleaseDate { get; set; }
        public string Version { get; set; }
        public string Copyright { get; set; }
        public Artist Artist { get; set; }
        public ObservableCollection<Artist> Artists { get; set; }
        public Album Album { get; set; }

        public byte[] CoverData { get; set; }
    }

    public class Contributor
    {
        public string Name { get; set; }
        public string Role { get; set; }
    }

    public class Playlist
    {
        public string UUID { get; set; }
        public string Title { get; set; }
        public int NumberOfTracks { get; set; }
        public int NumberOfVideos { get; set; }
        public string Description { get; set; }
        public int Duration { get; set; }
        public string LastUpdated { get; set; }
        public string Created { get; set; }
        public string Type { get; set; }
        public string Url { get; set; }
        public string Image { get; set; }
        public string SquareImage { get; set; }
        public bool PublicPlaylist { get; set; }
        public int Popularity { get; set; }

        public ObservableCollection<Track> Tracks { get; set; }
        public ObservableCollection<Video> Videos { get; set; }
        public byte[] CoverData { get; set; }
    }

    public class SearchResult
    {
        public ObservableCollection<Artist> Artists { get; set; }
        public ObservableCollection<Album> Albums { get; set; }
        public ObservableCollection<Track> Tracks { get; set; }
        public ObservableCollection<Video> Videos { get; set; }
        public ObservableCollection<Playlist> Playlists { get; set; }
    }

    public class Dllist
    {
        public ObservableCollection<string> AlbumIds{get;set;}
        public ObservableCollection<string> TrackIds{get;set;}
        public ObservableCollection<string> VideoIds{get;set;}
        public ObservableCollection<string> Urls{get;set;}

        public ObservableCollection<string> ArtistIds { get; set; } 
        public ObservableCollection<string> PlaylistIds { get; set; }
    }
}
