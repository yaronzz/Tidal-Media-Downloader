using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Stylet;
using AIGS.Helper;
namespace TIDALDL_UI.Pages
{
    public class AboutViewModel:Screen
    {
        public string Version { get; set; }
        public AboutViewModel()
        {
            Version = System.Reflection.Assembly.GetExecutingAssembly().GetName().Version.ToString();
            return;
        }
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
