import os
import requests
import time
from pydub import AudioSegment
import concurrent.futures

LALALAI_UPLOAD_URL = 'https://www.lalal.ai/api/upload/'
LALALAI_CHECK_URL = "https://www.lalal.ai/api/check/"
LALALAI_DOWNLOAD_URL = 'https://www.lalal.ai/api/download/'
LALALAI_PREWVIEW_URL = "https://www.lalal.ai/api/preview/"


def split_and_merge_music(file_path):
    filename = os.path.basename(file_path)
    name_file = os.path.splitext(filename)[0]
    music_segments = split_music(file_path)
    if not music_segments:
        return {'status': 'error', 'message': 'Failed to split music.'}

    result_segments = []

    def process_segment(segment):
        segment_id = upload_music_segment(segment)
        if segment_id:
            post_preview(segment_id)
            result = wait_for_segment_processing(segment_id)
            if result:
                return result

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Sử dụng map để gửi các yêu cầu bất đồng bộ và thu thập kết quả theo đúng thứ tự
        results = executor.map(process_segment, music_segments)

        for result in results:
            if result:
                result_segments.append(result)

    merged_stem_track_path, merged_back_track_path = merge_music_segments(
        result_segments, name_file)
    if not merged_stem_track_path or not merged_back_track_path:
        return {'status': 'error', 'message': 'Failed to merge music segments.'}

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
            segment_status = json_data['result'].get(
                segment_id, {}).get('preview', {}).get('stem_track')
            if segment_status is not None:
                return json_data['result']
            elif segment_status == 'error':
                return None


def merge_music_segments(result_segments, name_file):
    stem_tracks = []
    back_tracks = []

    def download_track(segment_id, track_url):
        response = requests.get(track_url)
        if response.status_code == 200:
            track_path = f"./tmp/{segment_id}_{track_url.split('/')[-1]}.mp3"

            with open(track_path, 'xb') as file:
                file.write(response.content)

            return track_path

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Sử dụng map để tải xuống các tệp cùng một lúc và thu thập kết quả theo thứ tự
        track_urls = [(list(result_segment.keys())[0], result_segment[list(result_segment.keys())[
                       0]]['preview']['stem_track']) for result_segment in result_segments]
        stem_tracks = list(executor.map(
            lambda args: download_track(*args), track_urls))

        track_urls = [(list(result_segment.keys())[0], result_segment[list(result_segment.keys())[
                       0]]['preview']['back_track']) for result_segment in result_segments]
        back_tracks = list(executor.map(
            lambda args: download_track(*args), track_urls))

    # Loại bỏ các giá trị None (không tải được tệp) khỏi danh sách
    stem_tracks = [track for track in stem_tracks if track is not None]
    back_tracks = [track for track in back_tracks if track is not None]

    merged_stem_track_path = merge_tracks(stem_tracks, name_file + '_vocal')
    merged_back_track_path = merge_tracks(back_tracks, name_file + '_beat')

    print(merged_stem_track_path, merged_back_track_path)
    return merged_stem_track_path, merged_back_track_path


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
# wait_for_segment_processing('2473503a-7560-4ab6-8aba-929862acf47c')
print(split_and_merge_music('./ccc.wav'))
# print(split_and_merge_music('./test.mp3'))
