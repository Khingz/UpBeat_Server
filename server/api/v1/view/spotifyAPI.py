from flask import Blueprint, jsonify, request
from ..spotify import SpotifyAPI
import os


spotify = Blueprint('spotifyAPI', __name__)

client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
spotify_api = SpotifyAPI(client_id=client_id, client_secret=client_secret)


@spotify.route('/featured_playlist/', methods=['GET'], endpoint='featured_playlist')
def featured_playlist():
    """ Gets featured playlist
    """
    playlist = spotify_api.fetch_featured_playlist()
    return jsonify(playlist)

@spotify.route('/new_release/', methods=['GET'], endpoint='new_release')
def new_release():
    """ Gets new release
    """
    release = spotify_api.fetch_new_releases()
    if release is None:
        return jsonify({'msg': 'could not fetch new release'}), 404
    return jsonify(release)


@spotify.route('/playlist/<playlist_id>/tracks', methods=['GET'])
def playlist_tracks(playlist_id):
    """ Gets new release
    """
    tracks = spotify_api.get_playlist_tracks(playlist_id)
    if tracks is None:
        return jsonify({'msg': 'could not fetch tracks'}), 404
    return jsonify(tracks)

@spotify.route('/album/<album_id>/tracks', methods=['GET'])
def album_tracks(album_id):
    """ Gets album tracks
    """
    tracks = spotify_api.get_album_tracks(album_id)
    if tracks is None:
        return jsonify({'msg': 'could not fetch tracks'}), 404
    return jsonify(tracks)

@spotify.route('/track/<track_id>', methods=['GET'])
def tracks(track_id):
    """ Gets new release
    """
    track = spotify_api.get_track(track_id)
    if track is None:
        return jsonify({'msg': 'could not fetch track'}), 404
    return jsonify(track)