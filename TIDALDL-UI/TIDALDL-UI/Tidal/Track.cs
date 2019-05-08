using AIGS.Helper;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Tidal
{
    public class Track
    {
        //曲目ID
        private string id;
        public string ID
        {
            get { return id; }
            set { id = value; }
        }
        //曲目名称
        private string title;
        public string Title
        {
            get { return title; }
            set { title = value; }
        }
        //曲目时长(单位秒)
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

        //曲目序号
        private int tracknumber;
        public int TrackNumber
        {
            get { return tracknumber; }
            set { tracknumber = value; }
        }
        //曲目所属碟
        private int volumenumber;
        public int VolumeNumber
        {
            get { return volumenumber; }
            set { volumenumber = value; }
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

        //private StreamUrl streamurl;
        //public StreamUrl StreamUrl
        //{
        //    get { return streamurl; }
        //    set { streamurl = value; }
        //}
    }
}
