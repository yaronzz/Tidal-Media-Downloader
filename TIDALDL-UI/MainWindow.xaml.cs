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
using MahApps.Metro.Controls;
using AIGS.Helper;
using AIGS.Common;
using AIGS.Tools;
using MahApps.Metro.Controls.Dialogs;
using System.Threading;
using System.Threading.Tasks;
using System.ComponentModel;
using System.Collections.ObjectModel;

namespace TIDALDL
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        ObservableCollection<Model> data = new ObservableCollection<Model>();
        public MainWindow()
        {
            InitializeComponent();
            mCtrlGrid.ItemsSource = Para.pListData;

            //for (int i = 0; i < 10; i++)
            //{
            //    Model m = new Model();
            //    m.Title = "Name" + i;
            //    m.ID = i.ToString();
            //    m.AlbumTitle = "年级" + i;
            //    data.Add(m);
            //}
            //ICollectionView vw = CollectionViewSource.GetDefaultView(data);
            //vw.GroupDescriptions.Add(new PropertyGroupDescription("AlbumTitle")); 
        }

        private void mCtrl_ButAbout_Click(object sender, RoutedEventArgs e)
        {
            mForm_About.IsOpen = mForm_About.IsOpen ? false : true;
        }

        private async void mCtrlParseBut_Click(object sender, RoutedEventArgs e)
        {
            string sID = mCtrlInput.Text;
            if (String.IsNullOrWhiteSpace(sID)) 
            {
                await this.ShowMessageAsync("Warnnig!", "Please Input!");
                return;
            }

            GetAlbum(sID);
        }



        private async void GetAlbum(string sID)
        {
            AlbumDL aTool = new AlbumDL();
            while (true)
            {
                Thread aTheadHandle = aTool.StartGetAlbumInfoThread(sID);
                //等待
                var aSettings = new MetroDialogSettings()
                {
                    NegativeButtonText = "取消",
                    AnimateShow = false,
                    AnimateHide = false
                };
                var aController = await this.ShowProgressAsync("解析中...", "请稍等!", true, aSettings);
                aController.SetIndeterminate();
                while (!aController.IsCanceled && aTool.IsGetAlbumInfoOver == false)
                {
                    await Task.Delay(1000);
                }
                aTheadHandle.Abort();
                await aController.CloseAsync();

                if(aTool.aErrCode == AlbumDL.ErrCode.SUCCESS)
                    break;
                
                aSettings = new MetroDialogSettings()
                {
                    AffirmativeButtonText = "重试",
                    NegativeButtonText = "取消",
                    ColorScheme = MetroDialogOptions.ColorScheme
                };
                MessageDialogResult result = await this.ShowMessageAsync("提示!", "解析失败！", MessageDialogStyle.AffirmativeAndNegative, aSettings);
                if (result == MessageDialogResult.Negative)
                    break;
                
            }

            if(aTool.aTrackInfos != null)
            {
                for (int i = 0; i < aTool.aTrackInfos.Count; i++)
                {
                    Para.pListData.Add(aTool.aTrackInfos[i]);
                }
                ICollectionView vw = CollectionViewSource.GetDefaultView(Para.pListData);
                vw.GroupDescriptions.Add(new PropertyGroupDescription("AlbumTitle")); 
            }
        }

    }

    public class Model
    {
        public string Title
        {
            get;
            set;
        }

        public string ID
        {
            get;
            set;
        }

        public string AlbumTitle
        {
            get;
            set;
        }
    }
}
