using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Stylet;

namespace TIDALDL_UI.Pages
{
    public class WaitViewModel : Screen
    {
        /// <summary>
        /// Work Before Close Window
        /// </summary>
        private CloseFunc Func;
        public delegate void CloseFunc();

        public WaitViewModel()
        {
            
        }

        /// <summary>
        /// Set CloseFunc
        /// </summary>
        public void Init(CloseFunc Func)
        {
            this.Func = Func;
        }

        /// <summary>
        /// Close This Window 
        /// </summary>
        public void Close()
        {
            if (Func != null)
                Func();
            RequestClose();
        }


    }
}
