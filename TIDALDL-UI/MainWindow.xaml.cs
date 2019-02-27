using MaterialDesignThemes.Wpf;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Tidal;
namespace TIDALDL_UI
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            this.WindowStartupLocation = WindowStartupLocation.CenterScreen;
            m_CAllList.ItemsSource     = Para.MainItems;
        }

        #region close/min/max/move window
        private void m_CClose_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }
        private void m_CMinWindow_Click(object sender, RoutedEventArgs e)
        {
            this.WindowState = WindowState.Minimized;
        }
        private void m_CMaxWindow_Click(object sender, RoutedEventArgs e)
        {
            int iMargin        = this.WindowState == WindowState.Maximized ? 20 : 0;
            m_CMainCard.Margin = new Thickness(iMargin, iMargin, iMargin, iMargin);

            if (this.WindowState == WindowState.Maximized)          
                this.WindowState = WindowState.Normal;
            else
                this.WindowState = WindowState.Maximized;
        }
        private void ColorZone_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            DragMove();
        }
        #endregion

        #region show about/update/setting/login window
        private void m_CAbout_Click(object sender, RoutedEventArgs e)
        {

        }

        private void m_CUpdate_Click(object sender, RoutedEventArgs e)
        {

        }

        private async void m_CSetting_Click(object sender, RoutedEventArgs e)
        {
            Setting Form = new Setting();
            await DialogHost.Show(Form, Form.ExtendedOpenedEventHandler);
        }

        private void Chip_DeleteClick(object sender, RoutedEventArgs e)
        {
            Login Form = new Login(true);
            Form.Show();
            this.Close();
        }
        #endregion

        #region search
        private System.Threading.Thread SearchThread;

        /// <summary>
        /// Search button click
        /// </summary>
        private async void m_CSearch_Click(object sender, RoutedEventArgs e)
        {
            string sID = m_CIDText.Text;
            if (string.IsNullOrEmpty(sID))
                return;

            //start thread
            SearchThread = AIGS.Helper.ThreadHelper.Start(ThreadFunc_Search, sID);

            //show wait window
            Para.WaitForm = new Wait(SearchCancle);
            await DialogHost.Show(Para.WaitForm, Para.WaitForm.ExtendedOpenedEventHandler);
        }

        /// <summary>
        /// Search thread
        /// </summary>
        /// <param name="data">ID</param>
        private void ThreadFunc_Search(object data)
        {
            ThreadResultNotify mothed = new ThreadResultNotify(SearchResult);

            //search album
            Album aAlbum = TidalTool.GetAlbum(data.ToString(), true, Enum.GetName(typeof(Quality), Para.Config.Quality));
            if(aAlbum != null)
            {
                this.Dispatcher.Invoke(mothed, "Album", aAlbum);
                return;
            }


        }

        /// <summary>
        /// Result callback func
        /// </summary>
        delegate void ThreadResultNotify(string typeName, object data);
        private async void SearchResult(string typeName, object data)
        {
            if(typeName == "Album")
            {
                Para.WaitForm.Close();
                AlbumInfo Form = new AlbumInfo((Album)data);
                await DialogHost.Show(Form, Form.ExtendedOpenedEventHandler);
            }
            
            return;
        }

        /// <summary>
        /// Cancle search
        /// </summary>
        private void SearchCancle()
        {
            if (SearchThread != null &&
                (SearchThread.ThreadState == System.Threading.ThreadState.Running ||
                SearchThread.ThreadState == System.Threading.ThreadState.Suspended))
                SearchThread.Abort();
            SearchThread = null;
        }
        #endregion

        #region datagrid callback
        /// <summary>
        /// Show sequence number
        /// </summary>
        private void m_CAllList_LoadingRow(object sender, DataGridRowEventArgs e)
        {
            e.Row.Header = e.Row.GetIndex() + 1;
        }
        #endregion
    }
}
