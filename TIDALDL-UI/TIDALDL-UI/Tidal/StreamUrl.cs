using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tidal
{
    public class StreamUrl
    {
        private string codec;
        public string Codec
        {
            get { return codec; }
            set { codec = value; }
        }

        private string encryptionKey;
        public string EncryptionKey
        {
            get { return encryptionKey; }
            set { encryptionKey = value; }
        }


        private int playTimeLeftInMinutes;
        public int PlayTimeLeftInMinutes
        {
            get { return playTimeLeftInMinutes; }
            set { playTimeLeftInMinutes = value; }
        }

        private string soundQuality;
        public string SoundQuality
        {
            get { return soundQuality; }
            set { soundQuality = value; }
        }

        private int trackId;
        public int TrackId
        {
            get { return trackId; }
            set { trackId = value; }
        }

        private string url;
        public string Url
        {
            get { return url; }
            set { url = value; }
        }

        //private long filesize;
        //public long FileSize
        //{
        //    get { return filesize; }
        //    set { filesize = value; }
        //}
    }
}
