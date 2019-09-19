using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using AIGS.Helper;
using AIGS.Common;
using System.Threading;

namespace TIDALDL_UI.Else
{
    public class ThreadTool
    {
        private static ThreadPoolManager Pool = new ThreadPoolManager(1);

        public static void SetThreadNum(int iNum)
        {
            if (iNum < 1)
                iNum = 1;
            Pool.SetPoolSize(iNum);
        }

        public static int GetThreadNum()
        {
            if (Pool == null)
                return 0;
            return Pool.GetPoolSize();
        }

        /// <summary>
        /// Add Download
        /// </summary>
        public static bool AddWork(ThreadPoolManager.EventFunc Func, object[] data=null)
        {
            if (Pool == null)
                return false;
            Pool.AddWork(Func, data);
            return true;
        }

        /// <summary>
        /// End
        /// </summary>
        public static void Close()
        {
            if (Pool == null)
                return;
            Pool.CloseAll(true);
        }
    }
}
