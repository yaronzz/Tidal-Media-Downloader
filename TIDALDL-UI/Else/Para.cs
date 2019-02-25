using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Tidal;
namespace TIDALDL_UI
{
    public class Para
    {
        public static Account User { set; get; }

        public static Config Config = new Config();

        public static Wait WaitForm = null;

        public static List<MainItem> MainItems = new List<MainItem>();
    }
}
