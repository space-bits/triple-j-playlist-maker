import os
import requests
import datetime as dt
import json

import spotipy
import spotipy.util as util
from logger.logger import StructuredMessage


_ = StructuredMessage

def add_to_playlist(sp,songs_to_add,playlist_name):
    """Obtains the current playlist, and only add songs if they aren't already in the playlist
    """
    logging.info(_('Attempting to add songs, %s, to \'%s\'' % (songs_to_add,playlist_name))
    # get the currently stored songs
    current_playlist = get_current_playlist(sp,playlist_name)

    # get the details to modify the playlist
    uid = sp.current_user()['id']
    playlist_id = find_playlist(sp, uid, playlist_name)['id']

    for track_id in songs_to_add:
        if track_id is not None:
            track_id = track_id.split(':')[2] # get the slice of the last segment
            # ignore the track_id if it's already in the playlist
            if track_id not in current_playlist:
                logging.info(_('Adding song with id \'%s\' to playlist \'%s\''
                % (track_id,playlist_name))
                track = [track_id]
                # ammend the playlist
                try:
                    sp.user_playlist_add_tracks(uid,playlist_id,
                    track,position=0)
                except(Exception) as e:
                    logging.warn(_('Exception occured ' + e)
            else:
                logging.info(_('Song with id \'%s\' already in playlist' % (track_id))

def get_current_playlist(sp, playlist_name):
    """Returns a list of songs from spotify that are in the current playlist
    """
    ret_playlist = []
    uid = sp.current_user()['id']
    playlist_id = find_playlist(sp, uid, playlist_name)['id']
    logging.info(_('Current playlist id \'%s\'' % (playlist_id))
    playlist = sp.user_playlist(uid,playlist_id)

    # store only the track IDs in the current playlist list
    for track in playlist['tracks']['items']:
        ret_playlist.append(track['track']['id'])

    logging.info(_('Song ids already in playlist: %s' % (ret_playlist))
    return ret_playlist


def get_triple_j_recently_played(triple_j_url):
    """Get the list of recently played songs from Triple J
    Strip any {feat. artist} from song titles as this
    query causes Spotify to return no tracks"""
    logging.info(_('Getting songs from Triple J...')
    songs = []
    tracks = requests.get(triple_j_url).json()

    # iterate over the json object and pull out the important data
    for track in tracks['items']:
        if track['service_id'] == 'triplej':
            # strip the {feat xyz.} from the title
            title = track['recording']['title'].split('{')[0].strip()
            artist = track['recording']['artists'][0]['name']
            logging.info(_('Found track \'%s\' by \'%s\'' % (title, artist))

            # only append songs which don't evaluate as being ignored
            if song_is_ignored(track) is not None:
                songs.append({'track':title,'artist':artist})
    return songs


def song_is_ignored(track):
    """Determines if a song is from an ignored program,
    such as 'The Racket'

    Returns
        - None if from an ignored program,
        - Track if it is not from an ignored program
    """
    # ignore songs played on 'The Racket'
    # create played time as datetime object
    played_at = dt.datetime.strptime(track['played_time'],
                                    '%Y-%m-%dT%H:%M:%S%z')

    # determine if the song was played between 2200 on a tuesday
    # and 0100 the following wednesday
    the_racket = {'start_day':'tuesday',
                  'start_time': '2200',
                  'end_day': 'wednesday',
                  'end_time': '0100'}
    day_played = dt.datetime.strftime(played_at, '%A')
    time_played = dt.datetime.strftime(played_at, '%T')
    if day_played == the_racket['start_day'] and \
        time_played > the_racket['start_time'] or \
        day_played == the_racket['end_day'] and \
        time_played < the_racket['end_time']:
            # don't append the song if it is played in an ignored
            # radio program
            logging.info(_('Skipping song played during an \
                ignored program')
            return None
    return track


def find_song_on_spotify(sp,songname,artist):
    """Method to find a song on Spotify to be added to the playlist"""
    logging.info(_('Finding song \'%s\', by \'%s\' on Spotify'
                % (songname,artist))
    # find the song in spotify's library, and return it
    results = sp.search(q='artist:%s track:%s' % (artist,songname),
                        limit=1)['tracks']['items']

    # returns the spotify:track:id of the particular song
    if results is None or len(results) == 0:
        return None
    song = results[0]['uri']
    if song is None:
        logging.warn(_('Unable to find song')
    logging.info(_('Spotify track id: \'%s\'' % (song))
    return song


def create_playlist(sp,username,playlist_name):
    """Determine if there is already a playlist, else create one"""
    playlist = None
    description = 'Playlist for Triple J\'s recently played songs.'

    playlist = find_playlist(sp,username,playlist_name)
    if playlist == None:
        logging.info(_('Creating new playlist \'%s\' for the first time'
                    % (playlist_name))
        # get the userid and create the playlist
        uid = sp.current_user()['id']
        sp.user_playlist_create(user=uid, name=playlist_name,public=True)
    else:
        logging.info(_('Playlist \'%s\' already exists.'
                    % (playlist['name']))
    return playlist


def find_playlist(sp,username,playlist_name):
    """Query the users playlist for if one already exists"""
    ret_playlist = None

    playlists = sp.user_playlists(username)
    # iterate over the collection and only get the playlists which
    # are owned by user
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            if playlist['name'] == playlist_name:
                ret_playlist = playlist

    return ret_playlist


def authenticate_account(username):
    """Authenticate the account and return the authenticated object."""
    if username is None:
        logging.error('Username is None when attempting to auth. Quitting.')
        return None

    scope = 'playlist-read-private playlist-modify-private playlist-modify-public'
    # try to get a new token or purge the old one if the scopes do not match
    try:
        token = util.prompt_for_user_token(username, scope)
        logging.info(_('Successfully got token')
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope)
        logging.warn(_('Successfully got token. Scopes may have changed.')

    if not token or token is None:
        logging.error('Unable to get token for \'%s\'' % (username))
        return None

    sp = spotipy.Spotify(auth=token)
    return sp
