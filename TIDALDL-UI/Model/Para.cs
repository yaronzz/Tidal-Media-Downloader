using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using AIGS.Tools;

namespace TIDALDL
{
    public class Para
    {
        static public ObservableCollection<TrackInfo> pListData = new ObservableCollection<TrackInfo>();

        static public string SessionID { get; set; } 
        static public AlbumDL.CountryCode CountryCode { get; set; }
        static public AlbumDL.SoundQuality SoundQuality { get; set; } 

    }
}
