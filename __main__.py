import os
from json.decoder import JSONDecodeError
import urllib.request
import logging

import spotipy
import spotipy.util as util


# create the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# define the file to log to
fh = logging.FileHandler('main.log')
fh.setLevel(logging.INFO)
# create formatter for both console and file
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')

# add formatter to fh
fh.setFormatter(formatter)
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
logger.addHandler(fh)

# main method
def main():
    '''Main method for the app
    Sets up the Spotipy user auth, queries for the existence of a playlist, 
    and creates it if it doesn't exist. 
    '''

    # my spotify username
    username = '011011000110111101110110011001'
    logger.info('Application starting for user \'%s\'' % (username))

    triple_j_url = 'https://www.abc.net.au/triplej/featured-music/recently-played/'
    # set the name for the playlist
    playlist_name = 'Triple J Recently Played'
    
    # authenticate the account with the spotify endpoint to get an auth token
    sp = authenticate_account(username)
    if sp is None:
        logger.error('Could not authenticate for spotify user %s' % (username)) 
        return
    # create the playlist, if it doesn't exist
    create_playlist(sp, username, playlist_name)
    '''
    recently_played_songs = get_triple_j_recently_played()
    # create an empty list for storing the songs to be added to the playlist
    playlist_new_songs = []
    # get a list of recently played songs from triple j's recently played url
    for songname,artist in recently_played_songs:
        # find each song and append it to a new songs list
        playlist_new_songs.append(find_song_on_spotify(sp,songname,artist))
    '''

    # add the songs to the playlist
    add_to_playlist(sp, playlist_new_songs)
     
    # find the songs in the list
    find_song_on_spotify(sp,'Everybody','Logic')
    
    logger.info('Program finished')

def add_to_playlist():
    '''Obtains the current playlist, and only add songs if they aren't already in the playlist
    '''
    # do some stuff
    pass


def get_triple_j_recently_played():
    '''Get the list of recently played songs from triple j'''
    songs = []
    logger.inf('Getting songs from Triple J')
    return songs


def find_song_on_spotify(sp,songname,artist):
    '''Method to find a song on Spotify to be added to the playlist'''
    logger.info('Finding song \'%s\', by \'%s\' on Spotify' % (songname,artist))
    # find the song in spotify's library, and return it
    results = sp.search(q='artist:%s track:%s' % (artist,songname), limit=1)
    # returns the spotify:track:id of the particular song
    song = results['tracks']['items'][0]['uri']
    if song is None:
        logger.warn('Unable to find song')
        return None
    logger.info('Spotify track id: \'%s\'' % (song))
    return song


def create_playlist(sp,username,playlist_name):
    '''Determine if there is already a playlist, else create one'''
    logger.info('Creating new playlist \'%s\' for the first time' % (playlist_name))
    playlist = None
    description = 'Playlist for Triple J\'s recently played songs.'
    
    playlist = find_playlist(sp,username,playlist_name)
    if playlist == None:
        uid = sp.current_user()['id']
        sp.user_playlist_create(user=uid, name=playlist_name,public=True)   
    return playlist


def find_playlist(sp, username, playlist_name):
    '''Query the users playlist for if one already exists'''
    ret_playlist = None
    
    playlists = sp.user_playlists(username)
    # iterate over the collection and only get the playlists which are owned by user with 
    # the specified username
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            if playlist['name'] == playlist_name:
                ret_playlist = playlist
                logger.info('Playlist \'%s\' already exists.' % (playlist['name']))
    
    logger.info('Playlist \'%s\' doesn\'t exist yet.' % (playlist['name']))
    return ret_playlist


def authenticate_account(username):
    '''Authenticate the account and return the authenticated object.'''
    if username is None:
        logger.error('Username is None when attempting to auth. Quitting.')
        return
    
    scope = 'playlist-read-private playlist-modify-private playlist-modify-public'
    # try to get a new token or purge the old one if the scopes do not match    
    try:
        token = util.prompt_for_user_token(username, scope)
        logger.info('Successfully got token')
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope)
        logger.warn('Successfully got token. Scopes may have changed.')
    
    if not token or token is None:
        logger.error('Unable to get token for %s' % (username))
        return None
    
    sp = spotipy.Spotify(auth=token)    
    return sp


if __name__ == '__main__':
    main()
