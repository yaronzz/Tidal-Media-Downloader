using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TIDALDL_UI.Properties;
using Tidal;
using AIGS.Common;
using AIGS.Helper;
using System.Collections.ObjectModel;
using System.Threading;
using System.Windows;
using Stylet;

namespace TIDALDL_UI.Pages
{
    public class DllistItem : Screen
    {
        public bool Check { get; set; }
        public int Number { get; set; }
        public string Name { get; set; }
        public eObjectType Type { get; set; } 
        public string Status { get; set; } //wait-parse-err-success
        public object Data { get; set; }
        public DllistItem(int number, string name, eObjectType type)
        {
            Number = number;
            Check = true;
            Name = name;
            Type = type;
            Status = "Wait";
            Data = null;
        }
    }

    public class DllistViewModel : Screen
    {
        public string Errlabel { get; set; }
        public string Text { get; set; } = Resources.DllistExample;
        public ObservableCollection<DllistItem> Items { get; set; } = new ObservableCollection<DllistItem>();
        private Thread ThreadHandle;

        #region Button

        public void Convert()
        {
            if (Text.IsBlank())
                return;

            Dllist plist = Tidal.TidalTool.getDllist(Text);
            for (int i = 0; i < plist.AlbumIds.Count; i++)
            {
                AddToItems(Items.Count, plist.AlbumIds[i], eObjectType.ALBUM);
            }
            for (int i = 0; i < plist.TrackIds.Count; i++)
            {
                AddToItems(Items.Count, plist.TrackIds[i], eObjectType.TRACK);
            }
            for (int i = 0; i < plist.VideoIds.Count; i++)
            {
                AddToItems(Items.Count, plist.VideoIds[i], eObjectType.VIDEO);
            }
            for (int i = 0; i < plist.Urls.Count; i++)
            {
                AddToItems(Items.Count, plist.Urls[i], eObjectType.None);
            }
            for (int i = 0; i < plist.ArtistIds.Count; i++)
            {
                AddToItems(Items.Count, plist.ArtistIds[i], eObjectType.ARTIST);
            }

            if (ThreadHandle == null)
                ThreadHandle = ThreadHelper.Start(ThreadFunc);
        }

        public void Confirm()
        {
            Errlabel = null;
            for (int i = 0; i < Items.Count; i++)
            {
                if(Items[i].Status == "Wait" || Items[i].Status == "Parse")
                {
                    Errlabel = "Some items in parsing.";
                    return;
                }
            }
            ThreadHelper.Abort(ThreadHandle);
            ThreadHandle = null;
            RequestClose();
        }

        public void Cancel()
        {
            Errlabel = null;
            Items.Clear();
            ThreadHelper.Abort(ThreadHandle);
            ThreadHandle = null;
            RequestClose();
        }
        #endregion

        ~DllistViewModel()
        {
            ThreadHelper.Abort(ThreadHandle);
            ThreadHandle = null;
        }

        private void AddToItems(int iNumber, string sName, eObjectType sType)
        {
            for (int i = 0; i < Items.Count; i++)
            {
                if (sName == Items[i].Name)
                    return;
            }
            Items.Add(new DllistItem(iNumber, sName, sType));
        }

        public void ThreadFunc(object[] data)
        {
            while (true)
            {
                for (int i = 0; i < Items.Count; i++)
                {
                    if (Items[i].Status != "Wait")
                        continue;
                    Items[i].Status = "Parse";

                    //Get
                    eObjectType eType;
                    object Data = TidalTool.tryGet(Items[i].Name, out eType, Items[i].Type);

                    //Result
                    if (eType == eObjectType.None || Data == null)
                        Items[i].Status = "Err";
                    else
                    {
                        Items[i].Type = eType;
                        Items[i].Data = Data;
                        Items[i].Status = "Success";
                    }
                }
                Thread.Sleep(3000);
            }
        }
    }
}
