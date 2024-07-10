from flask import Flask, render_template, request, redirect, url_for, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import config 

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Spotify APIの設定をconfig.pyから読み込む
client_id = config.client_id
client_secret = config.client_secret
redirect_uri = config.redirect_uri
scope = config.scope

# キャッシュファイルのパス
cache_path = '.spotifycache'

def get_spotify_oauth():
    return SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        scope=scope,
                        cache_path=cache_path)

@app.route('/')
def index():
    if not session.get('token_info'):
        return redirect(url_for('login'))

    token_info = session.get('token_info')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_artists = sp.current_user_top_artists(limit=10, time_range="short_term")['items']

    return render_template('index.html', top_artists=top_artists)

@app.route('/login')
def login():
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = get_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info if isinstance(token_info, dict) else {'access_token': token_info}
    return redirect(url_for('index'))

@app.route('/artist/<artist_id>')
def artist_detail(artist_id):
    token_info = get_token_info()
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_tracks = sp.artist_top_tracks(artist_id, country='US')['tracks']
    return render_template('artist_detail.html', top_tracks=top_tracks)

def get_artist_top_tracks(artist_id):
    token_info = get_token_info()
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_tracks = sp.artist_top_tracks(artist_id, country='US')['tracks']
    return top_tracks

def get_token_info():
    sp_oauth = get_spotify_oauth()
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        return redirect(url_for('login'))
    return token_info

@app.route('/logout')
def logout():
    session.clear()
    try:
        os.remove(cache_path)
    except OSError as e:
        print(f"Error: {cache_path} : {e.strerror}")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)