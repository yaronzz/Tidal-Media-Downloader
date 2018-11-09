using AIGS.Helper;
using AIGS.Common;
using MahApps.Metro.Controls;
using System;
using System.Data;
using System.Threading;
using System.Windows.Media.Imaging;
using System.Windows.Documents;
using System.Diagnostics;

namespace TIDALDL
{
    public sealed partial class AboutForm : Flyout
    {
        public AboutForm()
        {
            this.InitializeComponent();
        }

        /// <summary>
        /// 返回
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void CBackButton_Click(object sender, System.Windows.RoutedEventArgs e)
        {
            this.IsOpen = false;
        }

        /// <summary>
        /// 超链接
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Hyperlink_Click(object sender, System.Windows.RoutedEventArgs e)
        {
            Hyperlink aLink = sender as Hyperlink;
            NetHelper.OpenWeb(aLink.NavigateUri.AbsoluteUri);
        }
    }
}