using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Stylet;
using AIGS.Helper;
using TIDALDL_UI.Properties;
using System.Windows.Media.Imaging;

namespace TIDALDL_UI.Pages
{
    public class AboutViewModel:Screen
    {
        public string Version { get; set; } = System.Reflection.Assembly.GetExecutingAssembly().GetName().Version.ToString();

        public void Confirm()
        {
            RequestClose();
        }

        public void GotoProject()
        {
            NetHelper.OpenWeb("https://github.com/yaronzz/Tidal-Media-Downloader");
        }
    }
}
