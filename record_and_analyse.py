from video_analyzer import process_video, AnalysisMode
from record_video import record_video

if __name__ == "__main__":
    record_video()
    print(process_video(AnalysisMode['AV_DESCRIPTIONS']))