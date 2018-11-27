import urllib.request
import os
from json.decoder import JSONDecodeError

import spotipy
import spotipy.util as util


def main():
	username = '011011000110111101110110011001'
	sp = authenticate_account(username)
	if sp is None:
		return

	# save the user id for creating a playlist and modifying it
	user_id = None

	# create the playlist, if it doesn't exist	
	create_playlist()
	
def create_playlist():
	'''Determine if there is already a playlist, else create one'''
	playlist = None
	return playlist

def find_playlist(username, playlist_name):
	'''Query the users playlist for if one already exists'''
	playlist_id = None
	
	playlists = sp.user_playlists(username)
	for playlist in playlists['items']:
		if playlist['owner']['id'] == username:
			print(playlist['id'])

	return playlist_id

def authenticate_account(username):
	'''Authenticate the account and return the authenticated object.'''
	if username is None:
		username = input('Enter spotify username: ')
	
	scope = 'playlist-modify-public'
	# try to get a new token or purge the old one if the scopes do not match	
	try:
		token = util.prompt_for_user_token(username, scope)
	except (AttributeError, JSONDecodeError):
		os.remove(f".cache-{username}")
		token = util.prompt_for_user_token(username, scope)
	
	if not token or token is None:
		print('Unable to get token for %s' % (username))
		return None
	
	sp = spotipy.Spotify(auth=token)	
	return sp

if __name__ == '__main__':
    main()
