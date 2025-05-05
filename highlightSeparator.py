from scenedetect import SceneManager, open_video, split_video_ffmpeg
from scenedetect.detectors import HashDetector, ThresholdDetector, AdaptiveDetector, ContentDetector, HistogramDetector
import shutil
import os

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)  # remove file or symbolic link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # remove directory
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

clear_folder("./Output")
highlightClip = "Highlights/test2.mp4"

video = open_video(highlightClip)
scene_manager = SceneManager()

scene_manager.add_detector(HashDetector(threshold=0.3, size=32))
# scene_manager.add_detector(ThresholdDetector(threshold=12))
# scene_manager.add_detector(HistogramDetector(0.05, bins=1))

customWeights = ContentDetector.Components(
    delta_hue=0.8,
    delta_sat=0.7,
    delta_lum=1.5,
    delta_edges=0.8
)

scene_manager.add_detector(ContentDetector(threshold=8, weights=customWeights))

scene_manager.add_detector(AdaptiveDetector(
    adaptive_threshold=6,
    luma_only=False,
    min_content_val=5.1,
    window_width=2,
    kernel_size=5,
    weights=customWeights
))

scene_manager.detect_scenes(video, show_progress=True)
scene_list = scene_manager.get_scene_list()

print(f"Detected {len(scene_list)} scenes.")

split_video_ffmpeg(highlightClip, scene_list, output_dir="./Output/", show_progress=True)

# scene_list = detect(highlightClip, HashDetector(), show_progress=True)
# split_video_ffmpeg(highlightClip, scene_list, output_dir='./Output/', show_progress=True)