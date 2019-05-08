using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Tidal
{
    public class Artist
    {
        //艺人ID
        private string id;
        public string ID 
        {
            get { return id; }
            set { id = value; }
        }
        //艺人名称        
        private string name;
        public string Name
        {
            get { return name; }
            set { name = value; }
        }
        //连接
        private string url;
        public string Url
        {
            get { return url; }
            set { url = value; }
        }
        //图片
        private string pricture;
        public string Picture
        {
            get { return pricture; }
            set { pricture = value; }
        }
        //图片链接
        private string prictureurl;
        public string PictureUrl      
        {
            get { return prictureurl; }
            set { prictureurl = value; }
        }
        //热度
        private int popularity;
        public int Popularity          
        {
            get { return popularity; }
            set { popularity = value; }
        }

    }
}
