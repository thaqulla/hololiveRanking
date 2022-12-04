from googleapiclient.discovery import build
with open('./SECRET/API_KEYs.txt', 'r', encoding='UTF-8') as f:
    API_KEY_Lists = f.read().splitlines()
    
def getPlaylistItems(pagetoken, playlistId, API_KEY):#チェックボックスの画像取得
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    response = youtube.playlistItems().list(
        part = "snippet",
        playlistId = playlistId,
        pageToken = pagetoken,
        maxResults = 50,
        ).execute()
    videoList = response['items']
    try:
        nextPagetoken =  response["nextPageToken"] 
        nextPageItems = getPlaylistItems(nextPagetoken, playlistId, API_KEY)
        videoList += nextPageItems
        return videoList
    except KeyError as e:
        return videoList


playListId =  "PLl62IkfhHtN5kDBdmZ96EisueppHSZmbi"
apiKey =  API_KEY_Lists[0]

ret_val = getPlaylistItems("", playListId, apiKey)

print(len(ret_val))

# for item in ret_val:
#     print(item)