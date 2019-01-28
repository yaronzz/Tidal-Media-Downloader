using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Tidal
{
    public class Album
    {
        //专辑ID
        private int id;
        public int ID
        {
            get { return id; }
            set { id = value; }
        }
        //专辑名称
        private string title;
        public string Title
        {
            get { return title; }
            set { title = value; }
        }
        //专辑发行日期
        private string releasedate;
        public string ReleaseDate
        {
            get { return releasedate; }
            set { releasedate = value; }
        }
        //专辑版权所属
        private string copyright;
        public string CopyRight
        {
            get { return copyright; }
            set { copyright = value; }
        }
        //专辑时长
        private int duration;
        public int Duration
        {
            get { return duration; }
            set { duration = value; }
        }
        //专辑封面编码
        private string cover;
        public string Cover
        {
            get { return cover; }
            set { cover = value; }
        }
        //专辑封面链接
        private string convrurl;
        public string ConvrUrl
        {
            get { return convrurl; }
            set { convrurl = value; }
        }
        //专辑曲目数量
        private int numberoftracks;
        public int NumberOfTracks
        {
            get { return numberoftracks; }
            set { numberoftracks = value; }
        }
        //专辑视频数量
        private int numberofvideos;
        public int NumberOfVideos
        {
            get { return numberofvideos; }
            set { numberofvideos = value; }
        }
        //专辑碟数量
        private int numberofvolumes;
        public int NumberOfVolumes
        {
            get { return numberofvolumes; }
            set { numberofvolumes = value; }
        }
        //歌手
        private Artist artist;
        public Artist Artist
        {
            get { return artist; }
            set { artist = value; }
        }
    }
}
