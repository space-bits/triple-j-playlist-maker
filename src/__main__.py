import os
import requests
import logging
import datetime as dt
import json

import spotipy
import spotipy.util as util

from api.api import *
from logger.logger import *


# main method
def main():
    """Main method for the app
    Sets up the Spotipy user auth, queries for the existence of a playlist,
    and creates it if it doesn't exist.
    """
    # my spotify username
    username = '011011000110111101110110011001'
    logger.info('Application starting for user \'%s\'' % (username))

    # api endpoint for the triple j radio service
    limit = '50'
    triple_j_url = 'https://music.abcradio.net.au/api/v1/plays.json?order=desc&limit=' + limit

    # set the name for the playlist
    playlist_name = 'Triple J Recently Played'

    # authenticate the account with the spotify endpoint to get an auth token
    sp = authenticate_account(username)
    if sp is None:
        logger.error('Could not authenticate for spotify user %s' % (username))
        return None

    # create the playlist, if it doesn't exist
    create_playlist(sp, username, playlist_name)

    recently_played_songs = get_triple_j_recently_played(triple_j_url)

    # create an empty list for storing the songs to be added to the playlist
    songs_to_add = []

    # get a list of recently played songs from triple j's recently played url
    for song in recently_played_songs:
        # find each song and append it to a new songs list
        new_song = find_song_on_spotify(sp,
                                songname=song['track'],
                                artist=song['artist'])
        if new_song is not None:
            logger.info('Adding %s' % (new_song))
            songs_to_add.append(new_song)
        else:
            logger.info('%s, by %s is too underground. Lookout.' % (song['track'], song['artist']))

    # add the songs to the playlist
    add_to_playlist(sp,songs_to_add,playlist_name)
    logger.info('Program finished')


if __name__ == '__main__':
    main()
