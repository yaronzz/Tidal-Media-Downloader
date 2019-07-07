using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Stylet;
using System.Windows.Media;
using AIGS.Common;

namespace TIDALDL_UI.Else
{
    public class ProgressHelper:Screen
    {
        /// <summary>
        /// Progress Para
        /// </summary>
        public string ProgressPercent { get; private set; }
        public int    ProgressMaxValue { get; private set; }
        public int    ProgressCurValue { get; private set; }

        public long AllSize { get; set; }
        public long CurSize { get; set; }
        public long ErrSize { get; set; }

        /// <summary>
        /// Flag
        /// </summary>
        public bool IsComplete { get;  set; }
        public bool IsCancle { get;  set; }
        public bool IsErr { get;  set; }
        public bool IsSomeErr { get; set; }
        public string Errlabel { get; set; }
        public int HeightOfErrlable
        {
            get { if (Errlabel.IsBlank()) return 0;return 18; }
            set { }
        }

        /// <summary>
        /// Status
        /// </summary>
        public System.Windows.Media.SolidColorBrush StatusColor { get; set; } = System.Windows.Media.Brushes.White;
        public string Status
        {
            get {
                if (IsComplete)
                {
                    StatusColor = System.Windows.Media.Brushes.Green;
                    return "[COMPLETE]";
                }
                if (IsErr)
                {
                    StatusColor = System.Windows.Media.Brushes.DarkRed;
                    return "[ERR]";
                }
                if(IsSomeErr)
                {
                    StatusColor = System.Windows.Media.Brushes.DarkRed;
                    return "[SOME-ERR]";
                }
                if (IsCancle)
                {
                    StatusColor = System.Windows.Media.Brushes.DarkRed;
                    return "[CANCEL]";
                }
                StatusColor = System.Windows.Media.Brushes.Black;
                return ProgressPercent;
            }
        }

        public ProgressHelper()
        {
            ProgressMaxValue = 100;
            ProgressCurValue = 0;
            ProgressPercent  = "0%";

            IsComplete       = false;
            IsCancle         = false;
            IsErr            = false;
        }

        public void Update(long lCurSize, long lAllSize)
        {
            this.AllSize = lAllSize;
            this.CurSize = lCurSize;

            this.ProgressCurValue = (int)(lCurSize * this.ProgressMaxValue / lAllSize);
            this.ProgressPercent  = this.ProgressCurValue.ToString() + "%";
        }

        public void UpdateErr(long lErrSize, long lAllSize)
        {
            this.AllSize = lAllSize;
            this.ErrSize = lErrSize;
        }
    }
}
