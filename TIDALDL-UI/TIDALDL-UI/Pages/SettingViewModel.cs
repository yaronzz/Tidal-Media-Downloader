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
using System.Windows.Forms;

namespace TIDALDL_UI.Pages
{
    public class SettingViewModel: Stylet.Screen
    {
        /// <summary>
        /// Download Path
        /// </summary>
        public string OutputDir { get; set; }

        /// <summary>
        /// Err msg
        /// </summary>
        public string Errlabel { get; set; }

        /// <summary>
        /// Thread Num
        /// </summary>
        public int ThreadNum { get; set; }

        /// <summary>
        /// Quality 
        /// </summary>
        public int SelectQualityIndex { get; set; }
        public ObservableCollection<string> QualityList { get; set; }


        public SettingViewModel()
        {
            OutputDir     = Config.OutputDir();
            QualityList   = new ObservableCollection<string>();

            //Set ThreadNum
            string sValue = Config.ThreadNum();
            ThreadNum = AIGS.Common.Convert.ConverStringToInt(sValue);

            //Init QualityList
            Dictionary<int, string> pArray = AIGS.Common.Convert.ConverEnumToDictionary(typeof(Tidal.eSoundQuality));
            for (int i = 0; i < pArray.Count; i++)
                QualityList.Add(pArray.ElementAt(i).Value);

            //Set Quality
            sValue = Config.Quality();
            if(sValue.IsNotBlank())
            {
                int iIndex = QualityList.IndexOf(sValue.ToUpper());
                if(iIndex >= 0 && iIndex < QualityList.Count)
                    SelectQualityIndex = iIndex;
            }
        }

        /// <summary>
        /// Choose OutputDir
        /// </summary>
        public void SetOutputDir()
        {
            FolderBrowserDialog openFileDialog = new FolderBrowserDialog();
            if (openFileDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                OutputDir = openFileDialog.SelectedPath;
        }

        /// <summary>
        /// Set Config And Close
        /// </summary>
        public void Confirm()
        {
            if(!AIGS.Helper.PathHelper.Mkdirs(OutputDir))
            {
                Errlabel = "Creat Output Path Err!";
                return;
            }
        
            Config.ThreadNum(ThreadNum.ToString());
            Config.Quality(QualityList[SelectQualityIndex].ToLower());
            Config.OutputDir(OutputDir);
            ThreadTool.SetThreadNum(ThreadNum);
            RequestClose();                                                                 
        }
    }
}

