#!/usr/bin/env python3

one_frame = 1/60

breakpoint = [
    (0, 0),
    (2, 4.48),
    (4, 8.6),
    (4+one_frame, 15.0)
]

pts = []
#audio_sum = 0
for (vid_ts, audio_ts) , (prev_vid_ts, prev_audio_ts) in zip(breakpoint[1:], breakpoint):
    video_delta = vid_ts - prev_vid_ts
    new_video_ts = prev_audio_ts + video_delta
    pts.append(f"gte(T,{vid_ts})*({audio_ts - new_video_ts}/TB)")
    #audio_sum += audio_len
    # print(f"{prev_vid_ts}, {prev_audio_ts}, {vid_ts}, {vid_ts}")
    # print(f"{prev_vid_ts}, {prev_audio_ts}, {vid_ts}, {vid_ts}")

print("+\n".join(pts))

