using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Tidal
{
    public class Video
    {
        private int id;
        public int ID
        {
            get { return id; }
            set { id = value; }
        }
        private string title;
        public string Title
        {
            get { return title; }
            set { title = value; }
        }
        private int duration;
        public int Duration
        {
            get { return duration; }
            set { duration = value; }
        }
        private int tracknumber;
        public int TrackNumber
        {
            get { return tracknumber; }
            set { tracknumber = value; }
        }
        private int releasedate;
        public int ReleaseDate
        {
            get { return releasedate; }
            set { releasedate = value; }
        }
        //曲目版本
        private string version;
        public string Version
        {
            get { return version; }
            set { version = value; }
        }
        //专辑版权所属
        private string copyright;
        public string CopyRight
        {
            get { return copyright; }
            set { copyright = value; }
        }
        //歌手
        private Artist artist;
        public Artist Artist
        {
            get { return artist; }
            set { artist = value; }
        }
        //专辑
        private Album album;
        public Album Album
        {
            get { return album; }
            set { album = value; }
        }
    }
}
