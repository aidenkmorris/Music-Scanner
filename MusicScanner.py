#built in and supported in Python 3.8
import praw #Reddit API
import spotipy #Spotify API
from spotipy.oauth2 import SpotifyOAuth
import os

class MusicScanner:
    #setup Reddit credentials
    reddit = praw.Reddit(
    client_id = "",
    client_secret = "",
    user_agent = "",
    )
    #setup Spotify credentials and redirect URI
    spotify = spotipy.Spotify(auth_manager = SpotifyOAuth(
    scope = "playlist-modify-private",
    client_id = "",
    client_secret = "",
    redirect_uri = ""
    ))

    #declare variables
    validPosts = []
    validResults = []
    validTracks = []
    validSubreddits = ["baroque", "classicalmusic", "futurefunk", "composer", "contemporary", "concertband", "choralmusic", "chambermusic", "earlymusic", "earlymusicalnotation", "elitistclassical", "icm", "opera", "orchestra", "acidhouse", "ambientmusic", "astateoftrance", "atmosphericdnb", "bigbeat", "boogiemusic", "breakbeat", "breakcore", "chicagohouse", "chillout", "chipbreak", "chiptunes", "complextro", "cxd", "darkstep", "deephouse", "dnb", "dubstep", "edm", "ebm", "electronicdancemusic", "electronicjazz", "electronicblues", "electrohiphop", "electrohouse", "electronicmagic", "electronicmusic", "electropop", "electroswing", "experimentalmusic", "fidget", "filth", "frenchelectro", "frenchhouse", "funkhouse", "fusiondancemusic", "futurebeats", "futurefunkairlines", "futuregarage", "futuresynth", "gabber", "glitch", "glitchop", "grime", "happyhardcore", "hardhouse", "hardstyle", "house", "idm", "industrialmusic", "italodisco", "latinhouse", "liquiddubstep", "mashups", "melodichouse", "minimal", "mixes", "moombahcore", "nightstep", "oldskoolrave", "outrun", "theoverload", "partymusic", "plunderphonics", "psybient", "psybreaks", "psytrance", "purplemusic", "raggajungle", "realdubstep", "skweee", "swinghouse", "tech_house", "techno", "trance", "tranceandbass", "trap", "tribalbeats", "tropicalhouse", "ukfunky", "witch_house", "wuub", "80shardcorepunk", "90salternative", "90spunk", "90srock", "alternativerock", "altcountry", "aormelodic", "ausmetal", "blackmetal", "bluegrass", "blues", "bluesrock", "boneyard", "canadianclassicrock", "canadianmusic", "classicrock", "country", "christcore", "crunkcore", "deathcore", "deathmetal", "djent", "doommetal", "drone", "emo", "emoscreamo", "epicmetal", "flocked", "folk", "folkmetal", "folkpunk", "folkrock", "folkunknown", "garagepunk", "gothicmetal", "grunge", "hardcore", "hardrock", "horrorpunk", "indie_rock", "jrock", "krautrock", "ladiesofmetal", "mathrock", "melodicdeathmetal", "melodicmetal", "metalnews", "metalmusic", "metal", "metalcore", "modernrockmusic", "monsterfuzz", "neopsychedelia", "newwave", "noiserock", "numetal", "pianorock", "poppunkers", "posthardcore", "postrock", "powermetal", "powerpop", "progmetal", "progrockmusic", "psychedelicrock", "punk", "punkskahardcore", "punk_rock", "raprock", "rock", "shoegaze", "stonerrock", "symphonicblackmetal", "symphonicmetal", "synthrock", "throwbackcore", "truethrash", "truemetal", "outlawcountry", "womenrock", "80shiphop", "90shiphop", "altrap", "asianrap", "backpacker", "backspin", "bayrap", "chaphop", "chiefkeef", "drillandbop", "emo_trap", "gfunk", "hiphopheads", "hiphopheadsnorthwest", "hiphop101", "memphisrap", "nyrap", "rap", "raprock", "rapverses", "rhymesandbeats", "trapmuzik", "ukhiphopheads", "undergroundchicago", "lofihiphop", "2010smusic", "2000smusic", "90smusic", "80sremixes", "80smusic", "70smusic", "60smusic", "50smusic", "africanmusic", "afrobeat", "balkanbrass", "balkanmusic", "brazilianmusic", "britpop", "croatianmusic", "flamenco", "international_music", "irishmusic", "italianmusic", "jpop", "koreanrock", "kpop", "moscowbeat", "romusic", "spop", "somluso", "ukbands", "worldmusic", "70s", "acappella", "acousticcovers", "ambientfolk", "animemusic", "bestofdisney", "boomswing", "bossanova", "carmusic", "concerts", "chillmusic", "chillwave", "cpop", "complextro", "dancepunk", "dembow", "disco", "dreampop", "dub", "elephant6", "etimusic", "exotica", "filmmusic", "funksoumusic", "gamemusic", "gamesmusicmixmash", "gunslingermusic", "gypsyjazz", "indiefolk", "jambands", "jazz", "jazzfusion", "jazzinfluence", "listentoconcerts", "klezmer", "lt10k", "medievalmusic", "melancholymusic", "minimalism_music", "motown", "musicforconcentration", "muzyka", "nudisco", "oldiemusic", "oldiesmusic", "pianocovers", "popheads", "poptorock", "quietstorm", "rainymood", "recordstorefinds", "reggae", "remixxd", "retromusic", "rnb", "rnbheads", "rootsmusic", "salsamusic", "ska", "soca", "songbooks", "soulies", "souldivas", "soundsvintage", "spacemusic", "surfpunk", "swing", "tango", "therealbookvideos", "touhoumusic", "traditionalmusic", "treemusic", "triphop", "vaporwave", "vintageobscura", "vocaloid", "indie"]
    targetSubreddit = ""

    def select(this): #user selects a subreddit to search
        while this.targetSubreddit not in this.validSubreddits:
            this.targetSubreddit = input("Select a music subreddit to search: r/").lower()

    def searchReddit(this): #searches the target subreddit for the 100 newest and 100 hottest posts
        for submission in this.reddit.subreddit(this.targetSubreddit).new(limit=100):
            title = submission.title

            if ("-" in title or "by" in title.lower()) and "bpm" not in title.lower():
                this.validPosts.append(title)
        
        for submission in this.reddit.subreddit(this.targetSubreddit).hot(limit=100):
            title = submission.title

            if (("-" in title or "by" in title.lower()) and "bpm" not in title.lower()) and title not in this.validPosts:
                this.validPosts.append(title)

    def searchSpotify(this): #searches Spotify for results that match Reddit posts
        counter = 1

        for post in this.validPosts:
            os.system("cls")
            print("Searching for Songs - " + str(round(100 * (counter / len(this.validPosts)), 2)) + "%")
            print("X" * int(counter / len(this.validPosts) * 20) + "-" * int((1 - (counter / len(this.validPosts))) * 20))

            query = post.replace("-", " ").lower().replace("by", " ")[:100]

            results = this.spotify.search(q = query, type = "track")

            if not results["tracks"]["items"]:
                counter = counter + 1
                continue
            
            top_result = results["tracks"]["items"][0]

            artists = [artist["name"] for artist in top_result["artists"]]

            for artist in artists:
                if (str(artist)) in post:
                    this.validResults.append(", ".join(artists) + " - " + top_result["name"] + " (" + top_result["id"] + ")")
                    this.validTracks.append("spotify:track:" + top_result["id"])
                    break

            counter = counter + 1
        
        print("\nSearch Complete! Enjoy your playlist!")
    
    def createPlaylist(this): #creates a Spotify playlists using tracks confirmed to give a reasonable result
        playlist_name = "r/" + this.targetSubreddit + "'s Top Recommendations"
        playlist_description = "A playlist automatically generated from posts on r/" + this.targetSubreddit + ". Developed by Aiden K Morris."
        user_id = this.spotify.me()['id']

        playlist_id = this.spotify.user_playlist_create(user = user_id, name = playlist_name,
                    public = False, description = playlist_description)["id"]
        
        this.spotify.user_playlist_add_tracks(user = user_id, playlist_id = playlist_id, tracks = this.validTracks)
        
def main():
    ms = MusicScanner()
    ms.select()
    ms.searchReddit()
    ms.searchSpotify()
    ms.createPlaylist()

if __name__ == "__main__":
    main()
