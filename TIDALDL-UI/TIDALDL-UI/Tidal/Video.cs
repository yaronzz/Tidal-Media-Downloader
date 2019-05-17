using AIGS.Helper;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;

namespace Tidal
{
    public class Video
    {
        private string id;
        public string ID
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
            set { duration = value;
                SDuration = TimeHelper.ConverIntToString(value);
            }
        }

        private string sduration;
        public string SDuration
        {
            get { return sduration; }
            set { sduration = value; }
        }
        //专辑封面编码
        private string imageID;
        public string ImageID
        {
            get { return imageID; }
            set { imageID = value; }
        }
        //专辑封面链接
        private string coverurl;
        public string CoverUrl
        {
            get { return coverurl; }
            set { coverurl = value; }
        }
        //封面数据
        private Byte[] coverdata;
        public Byte[] CoverData
        {
            get { return coverdata; }
            set { coverdata = value; }
        }


        private int tracknumber;
        public int TrackNumber
        {
            get { return tracknumber; }
            set { tracknumber = value; }
        }
        private string releasedate;
        public string ReleaseDate
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
        private ObservableCollection<Artist> artists;
        public ObservableCollection<Artist> Artists
        {
            get { return artists; }
            set { artists = value; }
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
