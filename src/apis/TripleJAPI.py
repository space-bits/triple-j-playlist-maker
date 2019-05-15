# Class for querying the triple j api
import requests
import datetime as dt
from logger.logger import StructuredMessage


_ = StructuredMessage

class TripleJ():
    def __init__(self,url,limit,logging):
        # url to query
        self.url = url
        # limit to base how many queries each interval
        self.limit = limit
        self.url = self.url + '&limit=' + limit
        # pass in the self.logging.so we can track if things go wrong
        self.logging= logging

    def get_songs(self):
        '''Get the list of recently played songs from Triple J
        Strip any {feat. artist} from song titles as this
        query causes Spotify to return no tracks'''
        self.logging.info(_('Getting songs from Triple J...'))
        songs = []
        tracks = requests.get(self.url).json()

        # iterate over the json object and pull out the important data
        for track in tracks['items']:
            if track['service_id'] == 'triplej':
                # strip the {feat xyz.} from the title
                title = track['recording']['title'].split('{')[0].strip()
                artist = track['recording']['artists'][0]['name']
                self.logging.info(_('Found track \'%s\' by \'%s\'' % (title, artist)))

                # only append songs which shouldn't be ignored
                if song_is_ignored(track) is not None:
                    songs.append({'track':title,'artist':artist})

        # make sure the song played most recently is added first
        songs.reverse()
        return songs

def song_is_ignored(track):
    '''Determines if a song is from an ignored program,
    such as 'The Racket'

    Returns
        - None if from an ignored program,
        - Track if it is not from an ignored program
    '''
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
                ignored program'))
            return None
    return track
