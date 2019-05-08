using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Imaging;
using Tidal;
using AIGS.Helper;
using AIGS.Common;
using System.Collections.ObjectModel;
using TIDALDL_UI.Else;
using Stylet;
namespace TIDALDL_UI.Pages
{
    public class AlbumInfoViewModel:Screen
    {
        /// <summary>
        /// Common Info
        /// </summary>
        public string Title { get; private set; }
        public string Intro { get; private set; }
        public string ReleaseDate { get; private set; }

        /// <summary>
        /// Conver
        /// </summary>
        public BitmapImage Cover { get; private set; }

        /// <summary>
        /// Main Para
        /// </summary>
        public Album Record { get; private set; }

        /// <summary>
        /// Quality 
        /// </summary>
        public int SelectQualityIndex { get; set; }
        public ObservableCollection<string> QualityList { get; set; }

        /// <summary>
        /// Download Path
        /// </summary>
        public string OutputDir { get; set; }

        /// <summary>
        /// Is Download
        /// </summary>
        public bool Result { get; set; }

        public AlbumInfoViewModel()
        {
        }

        public void Init(Album data)
        {
            Record      = data;
            Title       = Record.Title;
            Intro       = string.Format("by {0}-{1} Tracks-{2}", Record.Artist.Name, Record.NumberOfTracks, TimeHelper.ConverIntToString(Record.Duration));
            Cover       = AIGS.Common.Convert.ConverByteArrayToBitmapImage(Record.CoverData);
            ReleaseDate = "Release date " + Record.ReleaseDate;
            QualityList = new ObservableCollection<string>();

            //Init QualityList
            Dictionary<int, string> pArray = AIGS.Common.Convert.ConverEnumToDictionary(typeof(Tidal.eSoundQuality));
            for (int i = 0; i < pArray.Count; i++)
                QualityList.Add(pArray.ElementAt(i).Value);

            //Set Quality
            string sValue = Config.Quality();
            if (sValue.IsNotBlank())
            {
                int iIndex = QualityList.IndexOf(sValue.ToUpper());
                if (iIndex >= 0 && iIndex < QualityList.Count)
                    SelectQualityIndex = iIndex;
            }

            //Read OutputPath
            OutputDir = Config.OutputDir();
        }

        public void Confirm()
        {
            Result = true;
            RequestClose();
        }

        public void Cancle()
        {
            Result = false;
            RequestClose();
        }
    }
}
