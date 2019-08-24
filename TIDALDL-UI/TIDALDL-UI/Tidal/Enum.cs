using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tidal
{
    public enum eSoundQuality
    {
        LOW,
        HIGH,
        LOSSLESS,
        HI_RES,
    }

    public enum eObjectType
    {
        ALBUM,
        ARTIST,
        PLAYLIST,
        TRACK,
        VIDEO,
        SEARCH,
        None,
    }

    public enum eResolution
    {
        e240P = 240,
        e360P = 360,
        e480P = 480,
        e720P = 720,
        e1080P = 1080
    }
}
