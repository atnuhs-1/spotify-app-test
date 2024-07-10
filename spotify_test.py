import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json

def get_track_info(client_id, client_secret, track_id):
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    track = sp.track(track_id)
    
    track_info = {
        'Track Name': track['name'],
        'Artists': [artist['name'] for artist in track['artists']],
        'Album': track['album']['name'],
        'Release Date': track['album']['release_date'],
        'Popularity': track['popularity']
    }
    
    return track_info


# def get_user_top_artists(client_id, client_secret, redirect_uri, scope='user-top-read', limit=10):
#     """
#     ユーザーのトップアーティストを取得する関数

#     Parameters:
#     - client_id (str): Spotify APIのクライアントID
#     - client_secret (str): Spotify APIのクライアントシークレット
#     - redirect_uri (str): Spotify認証のリダイレクトURI
#     - scope (str): Spotify APIのスコープ（デフォルトは'user-top-read'）
#     - limit (int): 取得するアーティストの数（デフォルトは10）

#     Returns:
#     - List[dict]: トップアーティストの情報を含む辞書のリスト
#     """
#     sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
#                                                    client_secret=client_secret,
#                                                    redirect_uri=redirect_uri,
#                                                    scope=scope))

#     # ユーザーのトップアーティストを取得
#     top_artists = sp.current_user_top_artists(limit=limit)
#     top_artists_json = json.dumps(top_artists, indent=4)
#     print(top_artists_json)

#     # トップアーティストのリストを作成
#     top_artists_list = []
#     # print(top_artists["items"])
#     for artist in top_artists['items']:
#         artist_info = {
#             'Name': artist['name'],
#             'Popularity': artist['popularity'],
#             'Genres': artist['genres'],
#             'Followers': artist['followers']['total']
#         }
#         top_artists_list.append(artist_info)

#     return top_artists_list

# クライアントIDとクライアントシークレット
client_id = '529e0412d0fa4602bf835e8dcd932723'
client_secret = '137e192d88b9478f895641e7a259c3b3'
redirect_uri = 'http://localhost:8888/callback'
track_id = '4I1L92UCPlYMdHYJ7r8Jhl'  # ここに取得したい曲のSpotify IDを入力
# https://open.spotify.com/intl-ja/track/4I1L92UCPlYMdHYJ7r8Jhl?si=ae7e67debb0d4fb7

# 曲の情報を取得
track_info = get_track_info(client_id, client_secret, track_id)
for key, value in track_info.items():
    print(f"{key}: {value}")


def get_user_top_artists(client_id, client_secret, redirect_uri, scope='user-top-read', limit=10):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope=scope))
    top_artists = sp.current_user_top_artists(limit=limit)
    return top_artists['items']

# トップアーティストを取得
# top_artists = get_user_top_artists(client_id, client_secret, redirect_uri)
# for artist in top_artists:
#     print(f"Name: {artist['Name']}, Popularity: {artist['Popularity']}, Genres: {artist['Genres']}, Followers: {artist['Followers']}")

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
