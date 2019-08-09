
using Newtonsoft.Json;
using System.Collections.ObjectModel;

namespace Tidal
{
    /*
     * {
            "items": [{
                    "allowStreaming": true,
                    "artist": {
                        "id": 3850668,
                        "name": "TOOL",
                        "type": "MAIN"
                    },
                    "artists": [{
                            "id": 3850668,
                            "name": "TOOL",
                            "type": "MAIN"
                        }
                    ],
                    "audioQuality": "LOSSLESS",
                    "copyright": "(P) 2006 Tool Dissectional, L.L.C./Volcano Entertainment II, L.L.C..",
                    "cover": "6055f90c-f266-4ca3-b863-2ae585784462",
                    "duration": 4551,
                    "explicit": true,
                    "id": 114331950,
                    "numberOfTracks": 11,
                    "numberOfVideos": 0,
                    "numberOfVolumes": 1,
                    "popularity": 25,
                    "premiumStreamingOnly": false,
                    "releaseDate": "2006-05-02",
                    "streamReady": true,
                    "streamStartDate": "2019-08-02T00:00:00.000+0000",
                    "surroundTypes": [],
                    "title": "10,000 Days",
                    "type": "ALBUM",
                    "upc": "886447824771",
                    "url": "http://www.tidal.com/album/114331950",
                    "version": null,
                    "videoCover": null
                }, {
                    "allowStreaming": true,
                    "artist": {
                        "id": 3850668,
                        "name": "TOOL",
                        "type": "MAIN"
                    },
                    "artists": [{
                            "id": 3850668,
                            "name": "TOOL",
                            "type": "MAIN"
                        }
                    ],
                    "audioQuality": "LOSSLESS",
                    "copyright": "(P) 2001 Tool Dissectional, L.L.C./Volcano Entertainment II, L.L.C..",
                    "cover": "8f02f358-64a0-4174-b3af-708a81231ac5",
                    "duration": 4601,
                    "explicit": false,
                    "id": 114330485,
                    "numberOfTracks": 13,
                    "numberOfVideos": 0,
                    "numberOfVolumes": 1,
                    "popularity": 25,
                    "premiumStreamingOnly": false,
                    "releaseDate": "2001-05-15",
                    "streamReady": true,
                    "streamStartDate": "2019-08-02T00:00:00.000+0000",
                    "surroundTypes": [],
                    "title": "Lateralus",
                    "type": "ALBUM",
                    "upc": "886447824764",
                    "url": "http://www.tidal.com/album/114330485",
                    "version": null,
                    "videoCover": null
                }, {
                    "allowStreaming": true,
                    "artist": {
                        "id": 3850668,
                        "name": "TOOL",
                        "type": "MAIN"
                    },
                    "artists": [{
                            "id": 3850668,
                            "name": "TOOL",
                            "type": "MAIN"
                        }
                    ],
                    "audioQuality": "LOSSLESS",
                    "copyright": "(P) 1996 Tool Dissectional, L.L.C./Volcano Entertainment II, L.L.C..",
                    "cover": "06973574-f86a-4d1b-9b65-845f03eed0dc",
                    "duration": 4643,
                    "explicit": true,
                    "id": 114331551,
                    "numberOfTracks": 15,
                    "numberOfVideos": 0,
                    "numberOfVolumes": 1,
                    "popularity": 27,
                    "premiumStreamingOnly": false,
                    "releaseDate": "1996-09-17",
                    "streamReady": true,
                    "streamStartDate": "2019-08-02T00:00:00.000+0000",
                    "surroundTypes": [],
                    "title": "Ænima",
                    "type": "ALBUM",
                    "upc": "886447824757",
                    "url": "http://www.tidal.com/album/114331551",
                    "version": null,
                    "videoCover": null
                }, {
                    "allowStreaming": true,
                    "artist": {
                        "id": 3850668,
                        "name": "TOOL",
                        "type": "MAIN"
                    },
                    "artists": [{
                            "id": 3850668,
                            "name": "TOOL",
                            "type": "MAIN"
                        }
                    ],
                    "audioQuality": "LOSSLESS",
                    "copyright": "(P) 1993 Tool Dissectional, L.L.C./Volcano Entertainment II, L.L.C..",
                    "cover": "5ff31a4a-f70a-451e-916a-15957d3cfc4a",
                    "duration": 4093,
                    "explicit": true,
                    "id": 114331080,
                    "numberOfTracks": 10,
                    "numberOfVideos": 0,
                    "numberOfVolumes": 1,
                    "popularity": 24,
                    "premiumStreamingOnly": false,
                    "releaseDate": "1993-04-06",
                    "streamReady": true,
                    "streamStartDate": "2019-08-02T00:00:00.000+0000",
                    "surroundTypes": [],
                    "title": "Undertow",
                    "type": "ALBUM",
                    "upc": "886447824740",
                    "url": "http://www.tidal.com/album/114331080",
                    "version": null,
                    "videoCover": null
                }
            ],
            "limit": 10,
            "offset": 0,
            "totalNumberOfItems": 4
        }
    */
    public class ArtistAlbumList
    {
        [JsonProperty("totalNumberOfItems")]
        public int TotalAlbums { get; set; }

        private Artist artist;
        public Artist Artist
        {
            get { return artist; }
            set { artist = value; }
        }
        // items in json and Albums Really
        private ObservableCollection<Album> items;
        public ObservableCollection<Album> Items
        {
            get { return items; }
            set { items = value; }
        }
        public ObservableCollection<Album> Albums
        {
            get { return items; }
            set { items = value; }
        }

        private ObservableCollection<Video> videos;
        public ObservableCollection<Video> Videos
        {
            get { return videos; }
            set { videos = value; }
        }
    }
}
