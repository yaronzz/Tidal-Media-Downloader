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

        #region show about/update/setting window
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
        #endregion
    }
}
