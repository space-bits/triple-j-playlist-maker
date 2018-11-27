import urllib.request

import spotipy
import spotipy.util as util


def main():
	username = input('Enter spotify username:')
	if username is None:
		return

	token = util.prompt_for_user_token(username)
	if not token or token is None:
		return
		
	sp = spotipy.Spotify(auth=token)	
	
	results = sp.search(q='weezer', limit=20)
	for i, t in enumerate(results['tracks']['items']):
		print(' ', i, t['name'])

if __name__ == '__main__':
    main()
