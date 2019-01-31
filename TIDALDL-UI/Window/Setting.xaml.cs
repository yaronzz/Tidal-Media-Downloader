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
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace TIDALDL_UI
{
    /// <summary>
    /// Password.xaml 的交互逻辑
    /// </summary>
    public partial class Setting : UserControl
    {
        public Setting()
        {
            InitializeComponent();
        }

        /// <summary>
        /// 用于关闭窗口
        /// </summary>
        private DialogSession _session;
        public void ExtendedOpenedEventHandler(object sender, DialogOpenedEventArgs eventargs)
        {
            _session = eventargs.Session;
        }

        private void m_CPath_Click(object sender, RoutedEventArgs e)
        {
            System.Windows.Forms.FolderBrowserDialog aDialog = new System.Windows.Forms.FolderBrowserDialog();
            aDialog.RootFolder = Environment.SpecialFolder.MyComputer;

            if (aDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                Para.Config.OutputDir = aDialog.SelectedPath;
            }
        }
    }
}
