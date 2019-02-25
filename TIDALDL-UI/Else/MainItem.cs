using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using AIGS.Common;
namespace TIDALDL_UI
{
    public class MainItem : AIGS.Common.ViewMoudleBase
    {
        private object data;

        private string name;
        public string Name
        {
            get { return name; }
            set { name = value;
                OnPropertyChanged();
            }
        }
        private int totalsize;
        public int TotalSize
        {
            get { return totalsize; }
            set
            {
                totalsize = value;
                OnPropertyChanged();
            }
        }
        private int downloadsize;
        public int DownloadSize
        {
            get { return downloadsize; }
            set
            {
                downloadsize = value;
                OnPropertyChanged();
            }
        }
        private int percentage;
        public int Percentage
        {
            get { return percentage; }
            set
            {
                percentage = value;
                OnPropertyChanged();
            }
        }
    }
}
