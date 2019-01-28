using MaterialDesignThemes.Wpf;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using Tidal;
using AIGS.Helper;

namespace TIDALDL_UI
{
    public partial class Login : Window
    {
        private string UserName;
        private string Password;

        public Login()
        {
            InitializeComponent();
            this.WindowStartupLocation = WindowStartupLocation.CenterScreen;
            m_CUser.ItemsSource        = Para.Config.Accounts;
            m_CUser.SelectedIndex      = 0;
            m_CAuto.IsChecked          = Para.Config.AutoLogin;
            m_CRemember.IsChecked      = Para.Config.Remember;
        }

        private void m_CUser_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (m_CUser.SelectedItem == null)
                return;
            m_CPwd.Password = ((AIGS.Common.Property)m_CUser.SelectedItem).Value.ToString();
        }

        private void Grid_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            DragMove();
        }

        private void m_CAuto_Checked(object sender, RoutedEventArgs e)
        {
            m_CRemember.IsChecked = true;
        }

        private void m_CClose_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }

        private void GotFocus(object sender, RoutedEventArgs e)
        {
            m_CErrLabel.Badge = "";
        }

        private void m_CCancle_Click(object sender, RoutedEventArgs e)
        {
            IsShowWaitPage(false);
        }

        private void IsShowWaitPage(bool bFlag)
        {
            m_CLoginPage.Visibility = bFlag ? Visibility.Hidden : Visibility.Visible;
            m_CWaitPage.Visibility = bFlag ? Visibility.Visible : Visibility.Hidden;
        }

        private void m_CLogin_Click(object sender, RoutedEventArgs e)
        {
            string sUser = m_CUser.Text;
            string sPwd  = m_CPwd.Password;
            if (string.IsNullOrEmpty(sUser) || string.IsNullOrEmpty(sPwd))
            {
                m_CErrLabel.Badge = "UserName Or Password Err！";
                return;
            }

            //show wait page
            IsShowWaitPage(true);

            //start login thread
            this.UserName = sUser;
            this.Password = sPwd;
            ThreadHelper.Start(ThreadFunc_LogIn);
            return;
        }

        private void ThreadFunc_LogIn(object data)
        {
            ThreadResultNotify mothed = new ThreadResultNotify(LogInResult);

            Account aUser = new Account();
            bool bCheck = aUser.LogIn(this.UserName, this.Password);
            this.Dispatcher.Invoke(mothed, aUser);
            return;
        }

        delegate void ThreadResultNotify(Account aUser);
        private void LogInResult(Account aUser)
        {
            if(!string.IsNullOrEmpty(aUser.Errmsg))
            {
                m_CErrLabel.Badge = aUser.Errmsg;
                IsShowWaitPage(false);
                return;
            }

            Para.User            = aUser;
            Tidal.TidalTool.User = aUser;

            //add account to config
            Para.Config.addAccount(this.UserName, this.Password);

            //open main window
            MainWindow Form = new MainWindow();
            Form.Show();
            this.Close();
        }


    }
}
