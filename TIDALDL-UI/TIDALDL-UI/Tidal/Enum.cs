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
        ALBUMS,
        ARTISTS,
        PLAYLISTS,
        TRACKS,
        VIDEOS,
    }

    public enum eResolution
    {
        e240P = 0,
        e360P = 1,
        e480P = 2,
        e720P = 3,
        e1080P = 4
    }
}
