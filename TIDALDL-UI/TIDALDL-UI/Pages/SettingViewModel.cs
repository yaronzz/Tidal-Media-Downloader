using Stylet;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TIDALDL_UI.Else;
using AIGS.Common;
using System.IO;
using Tidal;
using System.Windows.Forms;
using AIGS.Helper;

namespace TIDALDL_UI.Pages
{
    public class SettingViewModel: Stylet.Screen
    {
        public string OutputDir { get; set; }
        public int    ThreadNum { get; set; }
        public int    SearchNum { get; set; }
        public int    SelectQualityIndex { get; set; }
        public int    SelectResolutionIndex { get; set; }
        public bool   OnlyM4a { get; set; }
        public bool   AddHyphen { get; set; }
        public bool   ToChinese { get; set; }
        public bool   CheckExist { get; set; }
        public bool   ArtistBeforeTitle { get; set; }

        public bool CheckCommon { get; set; } = true;
        public bool CheckTrack { get; set; } = false;
        public bool CheckVideo { get; set; } = false;

        public List<string> QualityList { get; set; }
        public List<string> ResolutionList { get; set; }
        
        public SettingViewModel()
        {
            RefreshSetting();
        }

        public void RefreshSetting()
        {
            OutputDir             = Config.OutputDir();
            OnlyM4a               = Config.OnlyM4a();
            AddHyphen             = Config.AddHyphen();
            ToChinese             = Config.ToChinese();
            CheckExist            = Config.CheckExist();
            ArtistBeforeTitle     = Config.ArtistBeforeTitle();
            ThreadNum             = AIGS.Common.Convert.ConverStringToInt(Config.ThreadNum()) - 1;
            SearchNum             = AIGS.Common.Convert.ConverStringToInt(Config.SearchNum()) / 10 - 1;
            QualityList           = TidalTool.getQualityList();
            ResolutionList        = TidalTool.getResolutionList();
            SelectQualityIndex    = QualityList.IndexOf(Config.Quality().ToUpper());
            SelectResolutionIndex = ResolutionList.IndexOf(Config.Resolution().ToUpper());

            if (SelectQualityIndex < 0)
                SelectQualityIndex = 0;
            if (SelectResolutionIndex < 0)
                SelectResolutionIndex = 0;
            if (ThreadNum < 0)
                ThreadNum = 0;
            if (SearchNum < 0 || SearchNum > 5)
                SearchNum = 0;
        }

        public void SetOutputDir()
        {
            FolderBrowserDialog openFileDialog = new FolderBrowserDialog();
            if (openFileDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                OutputDir = openFileDialog.SelectedPath;
        }

        public void Confirm()
        {
            Config.ThreadNum((ThreadNum + 1).ToString());
            Config.SearchNum(((SearchNum + 1)*10).ToString());
            Config.OnlyM4a(OnlyM4a.ToString());
            Config.ToChinese(ToChinese.ToString());
            Config.CheckExist(CheckExist.ToString());
            Config.ArtistBeforeTitle(ArtistBeforeTitle.ToString());
            Config.AddHyphen(AddHyphen.ToString());
            Config.Quality(QualityList[SelectQualityIndex].ToLower());
            Config.Resolution(ResolutionList[SelectResolutionIndex]);
            Config.OutputDir(OutputDir);

            TidalTool.SetSearchMaxNum(int.Parse(Config.SearchNum()));
            ThreadTool.SetThreadNum(ThreadNum + 1);
            RequestClose();                                                                 
        }
    }
}

