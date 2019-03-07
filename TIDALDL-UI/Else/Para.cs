using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Tidal;
namespace TIDALDL_UI
{
    public class Para
    {
        public static MainWindow MainForm;
        public static Account User { set; get; }

        public static Config Config = new Config();

        public static Wait WaitForm = null;

        public static ObservableCollection<MainItem> MainItems = new ObservableCollection<MainItem>();

        public static Downloader Downloader = new Downloader();
    }
}
