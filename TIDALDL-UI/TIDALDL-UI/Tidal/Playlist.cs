using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;

namespace Tidal
{
    public class Playlist
    {
        private string uuid;
        public string Uuid
        {
            get { return uuid; }
            set { uuid = value; }
        }
        private string title;
        public string Title
        {
            get { return title; }
            set { title = value; }
        }

        private int numberoftracks;
        public int NumberOfTracks
        {
            get { return numberoftracks; }
            set { numberoftracks = value; }
        }

        private int numberofvideos;
        public int NumberOfVideos
        {
            get { return numberofvideos; }
            set { numberofvideos = value; }
        }

        private string description;
        public string Description
        {
            get { return description; }
            set { description = value; }
        }


        private int duration;
        public int Duration
        {
            get { return duration; }
            set { duration = value; }
        }

        private string lastupdated;
        public string LastUpdated
        {
            get { return lastupdated; }
            set { lastupdated = value; }
        }

        private string created;
        public string Created
        {
            get { return created; }
            set { created = value; }
        }

        private string type;
        public string Type
        {
            get { return type; }
            set { type = value; }
        }

        private string url;
        public string Url
        {
            get { return url; }
            set { url = value; }
        }

        private string image;
        public string Image
        {
            get { return image; }
            set { image = value; }
        }

        private ObservableCollection<Track> tracks;
        public ObservableCollection<Track> Tracks
        {
            get { return tracks; }
            set { tracks = value; }
        }

        private ObservableCollection<Video> videos;
        public ObservableCollection<Video> Videos
        {
            get { return videos; }
            set { videos = value; }
        }
    }
}
