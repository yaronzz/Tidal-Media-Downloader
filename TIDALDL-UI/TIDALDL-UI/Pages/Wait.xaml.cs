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
    public partial class Wait : UserControl
    {
        public Wait(CancleEventFunc func = null)
        {
            InitializeComponent();
            this._callback = func;
        }

        /// <summary>
        /// 用于关闭窗口
        /// </summary>
        private DialogSession _session;
        public void ExtendedOpenedEventHandler(object sender, DialogOpenedEventArgs eventargs)
        {
            _session = eventargs.Session;
        }
        public void Close()
        {
            _session.Close();
        }

        /// <summary>
        /// when click cancle button callback
        /// </summary>
        public delegate void CancleEventFunc();
        private CancleEventFunc _callback;

        /// <summary>
        /// cancle click
        /// </summary>
        private void Button_Click(object sender, RoutedEventArgs e)
        {
            _session.Close();
            if (_callback != null)
                _callback();
        }


    }
}
