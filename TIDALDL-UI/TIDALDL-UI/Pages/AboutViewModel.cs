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
        /// <summary>
        /// Self Version
        /// </summary>
        public string Version { get; set; }

        public AboutViewModel()
        {
            Version = System.Reflection.Assembly.GetExecutingAssembly().GetName().Version.ToString();
            return;
        }

        /// <summary>
        /// Close Window
        /// </summary>
        public void Confirm()
        {
            RequestClose();
        }

        /// <summary>
        /// Go to Github Project
        /// </summary>
        public void GotoProject()
        {
            NetHelper.OpenWeb("https://github.com/yaronzz/Tidal-Media-Downloader");
        }
    }
}
