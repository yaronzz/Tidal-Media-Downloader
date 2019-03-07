using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using AIGS.Common;
namespace TIDALDL_UI
{
    public class SubItem : AIGS.Common.ViewMoudleBase
    {
        public object data;

        private string name;
        public string Name
        {
            get { return name; }
            set
            {
                name = value;
                OnPropertyChanged();
            }
        }
        private string type;
        public string Type
        {
            get { return type; }
            set
            {
                type = value;
                OnPropertyChanged();
            }
        }
        private AIGS.Common.Status status;
        public AIGS.Common.Status Status
        {
            get { return status; }
            set
            {
                status = value;
                OnPropertyChanged();
            }
        }
        private long totalsize;
        public long TotalSize
        {
            get { return totalsize; }
            set
            {
                totalsize = value;
                OnPropertyChanged();
            }
        }
        private long downloadsize;
        public long DownloadSize
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
        private Object downloadurl;
        public Object DownloadUrl
        {
            get { return downloadurl; }
            set
            {
                downloadurl = value;
                OnPropertyChanged();
            }
        }
    }
}
