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
        public Login()
        {
            InitializeComponent();
            this.WindowStartupLocation = WindowStartupLocation.CenterScreen;
            m_CUser.ItemsSource        = Para.Config.Accounts;
            m_CUser.SelectedIndex      = 0;
            m_CAuto.IsChecked          = Para.Config.AutoLogin;
            m_CRemember.IsChecked      = Para.Config.Remember;

            //auto login
            if ((bool)m_CAuto.IsChecked && Para.Config.Accounts.Count > 0)
            {
                AIGS.Common.Property aProperty = Para.Config.Accounts[0];
                if (aProperty.Key != null && aProperty.Value != null &&
                    !string.IsNullOrWhiteSpace(aProperty.Key.ToString()) &&
                    !string.IsNullOrWhiteSpace(aProperty.Value.ToString()))
                {
                    m_CAccountLabel.Content = aProperty.Key.ToString();

                    //show wait page
                    IsShowWaitPage(true);
                    ThreadHelper.Start(ThreadFunc_LogIn, aProperty);
                }
            }
        }

        #region button func
        /// <summary>
        /// Cloase window
        /// </summary>
        private void m_CClose_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }

        /// <summary>
        /// Cancle LogIn
        /// </summary>
        private void m_CCancle_Click(object sender, RoutedEventArgs e)
        {
            IsShowWaitPage(false);
        }

        /// <summary>
        /// LogIn
        /// </summary>
        private void m_CLogin_Click(object sender, RoutedEventArgs e)
        {
            string sUser = m_CUser.Text;
            string sPwd  = m_CPwd.Password;
            if (string.IsNullOrEmpty(sUser) || string.IsNullOrEmpty(sPwd))
            {
                m_CErrLabel.Badge = "UserName Or Password Err！";
                return;
            }

            m_CAccountLabel.Content = sUser;

            //show wait page
            IsShowWaitPage(true);
            ThreadHelper.Start(ThreadFunc_LogIn, new AIGS.Common.Property(sUser, sPwd));
            return;
        }
        #endregion

        #region operate callback
        /// <summary>
        /// Set passwordBox after combox select changed
        /// </summary>
        private void m_CUser_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (m_CUser.SelectedItem == null)
                return;
            m_CPwd.Password = ((AIGS.Common.Property)m_CUser.SelectedItem).Value.ToString();
        }

        /// <summary>
        /// Window move
        /// </summary>
        private void Grid_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            DragMove();
        }

        /// <summary>
        /// Check rememberBox after autoLogin checked
        /// </summary>
        private void m_CAuto_Checked(object sender, RoutedEventArgs e)
        {
            m_CRemember.IsChecked = true;
        }
        #endregion


        #region else
        /// <summary>
        /// Clear errmsg label after focus on edit control
        /// </summary>
        private void EditGotFocus(object sender, RoutedEventArgs e)
        {
            m_CErrLabel.Badge = "";
        }

        /// <summary>
        /// Show wait page after login 
        /// </summary>
        private void IsShowWaitPage(bool bFlag)
        {
            m_CLoginPage.Visibility = bFlag ? Visibility.Hidden : Visibility.Visible;
            m_CWaitPage.Visibility  = bFlag ? Visibility.Visible : Visibility.Hidden;
        }

        #endregion


        /// <summary>
        /// Login thread
        /// </summary>
        /// <param name="data">username and password</param>
        private void ThreadFunc_LogIn(object data)
        {
            Account aAccount               = new Account();
            AIGS.Common.Property aProperty = (AIGS.Common.Property)data;
            bool   bCheck                  = aAccount.LogIn(aProperty.Key.ToString(), aProperty.Value.ToString());

            ThreadResultNotify mothed = new ThreadResultNotify(LogInResult);
            this.Dispatcher.Invoke(mothed, aAccount);
            return;
        }

        /// <summary>
        /// Result callback func
        /// </summary>
        delegate void ThreadResultNotify(Account aUser);
        private void LogInResult(Account aUser)
        {
            if(!string.IsNullOrEmpty(aUser.Errmsg))
            {
                m_CErrLabel.Badge = aUser.Errmsg;
                IsShowWaitPage(false);
                return;
            }

            //add account to global para
            Para.User            = aUser;
            Tidal.TidalTool.User = aUser;

            //add account to config
            Para.Config.addAccount(aUser.User, aUser.Pwd);

            //open main window
            MainWindow Form = new MainWindow();
            Form.Show();

            //close login window
            this.Close();
        }


    }
}
