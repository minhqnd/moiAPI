import os
import requests
import time
from pydub import AudioSegment

LALALAI_UPLOAD_URL = 'https://www.lalal.ai/api/upload/'
LALALAI_CHECK_URL = "https://www.lalal.ai/api/check/"
LALALAI_DOWNLOAD_URL = 'https://www.lalal.ai/api/download/'
LALALAI_PREWVIEW_URL = "https://www.lalal.ai/api/preview/"


def split_and_merge_music(file_path):
    # name_file = file_path.split('/')[-1]
    filename = os.path.basename(file_path)
    name_file = os.path.splitext(filename)[0]
    # Tách file nhạc thành các đoạn 1 phút
    music_segments = split_music(file_path)
    if not music_segments:
        return {'status': 'error', 'message': 'Failed to split music.'}

    # Gửi từng đoạn lên API để tách beat và vocal
    print(f'Có tổng {len(music_segments)} files')
    result_segments = []
    for segment in music_segments:
        segment_id = upload_music_segment(segment)
        if segment_id:
            print('Upload xong')
            post_preview(segment_id)
            result = wait_for_segment_processing(segment_id)
            if result:
                result_segments.append(result)
                # print(result_segments)

    # Tổng hợp kết quả và ghép lại các file stem_track và back_track
    merged_stem_track_path, merged_back_track_path = merge_music_segments(
        result_segments, name_file)
    if not merged_stem_track_path or not merged_back_track_path:
        return {'status': 'error', 'message': 'Failed to merge music segments.'}

    # Trả về đường dẫn của các file stem_track và back_track đã ghép
    return {'status': 'success', 'stem_track': merged_stem_track_path, 'back_track': merged_back_track_path}


def post_preview(segment_id):
    # Gửi yêu cầu xem trước của một đoạn nhạc
    payload = {'id': segment_id,
               'filter': '1',
               'stem': 'vocals',
               'splitter': 'phoenix'}
    response = requests.request("POST", LALALAI_PREWVIEW_URL, data=payload)
    if response.status_code == 200:
        print(f'Đã gửi yêu cầu xử lý {segment_id}')
        return response.json()
    return None


def split_music(file_path):
    # Đọc file nhạc và tách thành các đoạn 1 phút
    # Hàm này cần được triển khai dựa trên cách bạn muốn tách file nhạc thành các đoạn 1 phút
    # Trong ví dụ này, chúng ta sử dụng pydub để tách file nhạc

    music = AudioSegment.from_file(file_path)
    duration = len(music)

    segment_duration = 60 * 1000  # 1 phút
    music_segments = []
    for start_time in range(0, duration, segment_duration):
        end_time = start_time + segment_duration
        segment = music[start_time:end_time]
        music_segments.append(segment)

    return music_segments


def upload_music_segment(segment):
    # Gửi đoạn nhạc lên API của lalal.ai để tách beat và vocal
    payload = {}
    headers = headers = {
        'Content-Disposition': 'attachment; filename*=UTF-8\'\'segment.mp3'
    }
    files = {'file': segment.export(format='mp3')}
    # files = [
    #     ('file', ('tnoaa demo1.mp3', open(
    #         './test.mp3', 'rb'), 'audio/mpeg'))
    # ]
    response = requests.request(
        "POST", LALALAI_UPLOAD_URL, headers=headers, data=payload, files=files)
    if response.status_code == 200:
        json_data = response.json()
        segment_id = json_data['id']
        return segment_id
    else:
        print(response.text)


import time
import requests

def wait_for_segment_processing(segment_id):
    # Chờ xử lý và kiểm tra trạng thái của đoạn nhạc
    while True:
        time.sleep(2)  # Chờ 2 giây trước khi kiểm tra lại
        payload = {'id': segment_id}
        headers = {
            'Content-Disposition': 'form-data; name="params"'
        }
        response = requests.request(
            "POST", LALALAI_CHECK_URL, headers=headers, data=payload)
        # print(response.json())
        if response.status_code == 200:
            json_data = response.json()
            segment_status = json_data['result'].get(segment_id, {}).get('preview', {}).get('stem_track')
            if segment_status is not None:
                return json_data['result']
            elif segment_status == 'error':
                return None




def merge_music_segments(result_segments, name_file):
    # Tải về và ghép lại các file stem_track và back_track
    stem_tracks = []
    back_tracks = []
    index = 0
    for result_segment in result_segments:
        segment_id = list(result_segment.keys())[0]
        print(segment_id)
        stem_track_url = result_segment[segment_id]['preview']['stem_track']
        back_track_url = result_segment[segment_id]['preview']['back_track']
        
        stem_track_path = download_music_track(segment_id, stem_track_url)
        back_track_path = download_music_track(segment_id, back_track_url)

        index+=1
        if stem_track_path and back_track_path:
            stem_tracks.append(stem_track_path)
            back_tracks.append(back_track_path)


    # Ghép lại các file stem_track và back_track
    merged_stem_track_path = merge_tracks(stem_tracks, name_file + '_vocal')
    merged_back_track_path = merge_tracks(back_tracks, name_file + '_beat')

    # Trả về đường dẫn của các file stem_track và back_track đã ghép
    print(merged_stem_track_path, merged_back_track_path)
    return merged_stem_track_path, merged_back_track_path


def download_music_track(segment_id, track_url):
    # Tải về file nhạc từ URL
    
    response = requests.get(track_url)
    if response.status_code == 200:
        track_path = f"./tmp/{segment_id}_{track_url.split('/')[-1]}.mp3"

        with open(track_path, 'xb') as file:
            file.write(response.content)
        print(track_path)
        return track_path


def merge_tracks(tracks, name_file):
    # Ghép lại các file nhạc thành một file duy nhất
    # Hàm này cần được triển khai dựa trên cách bạn muốn ghép lại các file nhạc
    # Trong ví dụ này, chúng ta sử dụng pydub để ghép lại các file nhạc
    from pydub import AudioSegment

    merged_track = AudioSegment.empty()
    for track_path in tracks:
        track = AudioSegment.from_file(track_path)
        merged_track += track

    merged_track_path = f'./tmp/{name_file}.mp3'
    merged_track.export(merged_track_path, format='mp3')

    return merged_track_path


# upload_music_segment(AudioSegment.from_file('./test.mp3'))
# print(upload_music_segment('./test.mp3'))
print(split_and_merge_music('./test.mp3'))
# wait_for_segment_processing('2473503a-7560-4ab6-8aba-929862acf47c')
