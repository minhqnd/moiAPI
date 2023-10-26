import os
import requests
import time
from pydub import AudioSegment
import concurrent.futures

LALALAI_UPLOAD_URL = "https://www.lalal.ai/api/upload/"
LALALAI_CHECK_URL = "https://www.lalal.ai/api/check/"
LALALAI_DOWNLOAD_URL = "https://www.lalal.ai/api/download/"
LALALAI_PREWVIEW_URL = "https://www.lalal.ai/api/preview/"


def split_and_merge_music(file_path):
    """

    Split and merge music file into segments and merge them back into a single file.

    Args:
        file_path (str): The path of the music file to be split and merged.

    Returns:
        dict: A dictionary containing the status of the operation and the paths of the merged stem and back tracks.
              If the operation is successful, the status will be 'success' and the paths of the merged stem and back tracks
              will be returned. If the operation fails, the status will be 'error' and an error message will be returned.

    Raises:
        None

    """
    filename = os.path.basename(file_path)
    name_file = os.path.splitext(filename)[0]
    music_segments = split_music(file_path)
    global music_lens
    music_lens = {seg: int(len(seg) / 1000) for seg in music_segments}
    if not music_segments:
        return {"status": "error", "message": "Failed to split music."}

    result_segments = []

    def process_segment(segment):
        """
        Process a music segment by uploading it, posting a preview, and waiting for it to be processed.

        Args:
            segment (bytes): The music segment to be processed.

        Returns:
            dict: A dictionary containing the result of the segment processing.

        Raises:
            None
        """
        segment_id = upload_music_segment(segment)
        if segment_id:
            post_preview(segment_id)
            result = wait_for_segment_processing(segment_id)
            print(segment_id)
            return result

        # print(music_lens[segment], 'ok ')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Sử dụng map để gửi các yêu cầu bất đồng bộ và thu thập kết quả theo đúng thứ tự
        results = executor.map(process_segment, music_segments)
        # print(results)
        filtered_results = [item for item in results if item is not None]
        # print(filtered_results)
        for result in filtered_results:
            # if not result:
            #     return {'status': 'error', 'message': 'Failed to merge music segments.'}
            # else:
            result_segments.append(result)
    # print("done")
    # print(result_segments)
    merged_stem_track_path, merged_back_track_path = merge_music_segments(
        result_segments, name_file
    )
    if not merged_stem_track_path or not merged_back_track_path:
        return {"status": "error", "message": "Failed to merge music segments."}

    return {
        "status": "success",
        "stem_track": merged_stem_track_path,
        "back_track": merged_back_track_path,
    }


def post_preview(segment_id):
    """
    Send a preview request for a music segment.

    Args:
        segment_id (str): The ID of the music segment to be previewed.

    Returns:
        dict: A dictionary containing the preview result.

    Raises:
        None
    """
    # Gửi yêu cầu xem trước của một đoạn nhạc
    payload = {"id": segment_id, "filter": "1", "stem": "vocals", "splitter": "phoenix"}
    response = requests.request("POST", LALALAI_PREWVIEW_URL, data=payload)
    if response.status_code == 200:
        print(f"Đã gửi yêu cầu xử lý {segment_id}")
        return response.json()
    return None


def split_music(file_path):
    """
    Split a music file into segments.

    Args:
        file_path (str): The path of the music file to be split.

    Returns:
        list: A list of music segments.

    Raises:
        None
    """
    music = AudioSegment.from_file(file_path)
    segment_duration = 60 * 1000
    # 1 phút
    music_segments = []

    start_time = 0
    while start_time < len(music):
        end_time = start_time + segment_duration
        segment = music[start_time:end_time]
        music_segments.append(segment)
        start_time = end_time

    return music_segments


def upload_music_segment(segment):
    """
    Upload a music segment to the lalal.ai API for beat and vocal separation.

    Args:
        segment (AudioSegment): The music segment to be uploaded.

    Returns:
        str: The ID of the uploaded music segment.

    Raises:
        None
    """
    # Gửi đoạn nhạc lên API của lalal.ai để tách beat và vocal
    while True:
        segment_len = None
        print(music_lens[segment])
        payload = {}
        headers = headers = {
            "Content-Disposition": "attachment; filename*=UTF-8''segment.mp3"
        }
        files = {"file": segment.export(format="mp3")}
        response = requests.request(
            "POST", LALALAI_UPLOAD_URL, headers=headers, data=payload, files=files
        )
        if response.status_code == 200:
            json_data = response.json()
            segment_id = json_data["id"]
            segment_len = json_data["duration"]
            if segment_len == music_lens[segment]:
                return segment_id
            else:
                print(f"{music_lens[segment]} Segment length does not match. Requesting segment again.")
        else:
            print(response.text)


def wait_for_segment_processing(segment_id):
    """
    Wait for a music segment to be processed by checking its status periodically.

    Args:
        segment_id (str): The ID of the music segment to be checked.

    Returns:
        dict: A dictionary containing the result of the segment processing.

    Raises:
        None
    """
    while True:
        time.sleep(2)
        payload = {"id": segment_id}
        headers = {"Content-Disposition": 'form-data; name="params"'}
        response = requests.request(
            "POST", LALALAI_CHECK_URL, headers=headers, data=payload
        )

        if response.status_code == 200:
            json_data = response.json()
            segment_status = (
                json_data["result"]
                .get(segment_id, {})
                .get("preview", {})
                # .get("stem_track")
            )

            if segment_status is not None:
                return json_data["result"]
            elif not segment_status:
                task_error = (
                    json_data["result"].get(segment_id, {}).get("task", {}).get("error")
                )
                if task_error:
                    print(f"task_error {segment_id}")
                    return None

        if response.status_code != 200 or "result" not in json_data:
            return None


def merge_music_segments(result_segments, name_file):
    """
    Merge the stem and back tracks of music segments into two separate tracks.

    Args:
        result_segments (list): A list of dictionaries containing the result of the segment processing.
        name_file (str): The name of the merged file.

    Returns:
        tuple: A tuple containing the paths of the merged stem and back tracks.

    Raises:
        None
    """
    # print("run")
    stem_tracks = []
    back_tracks = []

    def download_track(segment_id, track_url):
        """
        Download a music track from a URL.

        Args:
            segment_id (str): The ID of the music segment.
            track_url (str): The URL of the music track to be downloaded.

        Returns:
            str: The path of the downloaded music track.

        Raises:
            None
        """
        response = requests.get(track_url)
        if response.status_code == 200:
            track_path = f"./tmp/{segment_id}_{track_url.split('/')[-1]}.mp3"

            with open(track_path, "xb") as file:
                file.write(response.content)

            return track_path

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Sử dụng map để tải xuống các tệp cùng một lúc và thu thập kết quả theo thứ tự
        track_urls = [
            (
                list(result_segment.keys())[0],
                result_segment[list(result_segment.keys())[0]]["preview"]["stem_track"],
            )
            for result_segment in result_segments
        ]
        stem_tracks = list(executor.map(lambda args: download_track(*args), track_urls))

        track_urls = [
            (
                list(result_segment.keys())[0],
                result_segment[list(result_segment.keys())[0]]["preview"]["back_track"],
            )
            for result_segment in result_segments
        ]
        back_tracks = list(executor.map(lambda args: download_track(*args), track_urls))

    # Loại bỏ các giá trị None (không tải được tệp) khỏi danh sách
    stem_tracks = [track for track in stem_tracks if track is not None]
    back_tracks = [track for track in back_tracks if track is not None]

    merged_stem_track_path = merge_tracks(stem_tracks, name_file + "_vocal")
    merged_back_track_path = merge_tracks(back_tracks, name_file + "_beat")

    print(merged_stem_track_path, merged_back_track_path)
    return merged_stem_track_path, merged_back_track_path


def merge_tracks(tracks, name_file):
    """
    Merge multiple music tracks into a single track.

    Args:
        tracks (list): A list of paths of music tracks to be merged.
        name_file (str): The name of the merged file.

    Returns:
        str: The path of the merged music track.

    Raises:
        None
    """
    # Ghép lại các file nhạc thành một file duy nhất
    # Hàm này cần được triển khai dựa trên cách bạn muốn ghép lại các file nhạc
    # Trong ví dụ này, chúng ta sử dụng pydub để ghép lại các file nhạc
    from pydub import AudioSegment

    merged_track = AudioSegment.empty()
    for track_path in tracks:
        track = AudioSegment.from_file(track_path)
        merged_track += track

    merged_track_path = f"./tmp/{name_file}.mp3"
    merged_track.export(merged_track_path, format="mp3")

    return merged_track_path


print(split_and_merge_music("./ngonngang.wav"))
# print(split_and_merge_music("./demo.mp3"))
# print(split_and_merge_music('./test.mp3'))
# print(split_music('./testtung.mp3'))
