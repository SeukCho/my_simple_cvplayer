# My Video Player

import cv2 as cv

video_file = 'data\data_PETS09-S2L1-raw.webm'

video = cv.VideoCapture(video_file)

if video.isOpened():
    fps = video.get(cv.CAP_PROP_FPS)
    wait_msec = int(1 / fps * 1000)

    frame_total = int(video.get(cv.CAP_PROP_FRAME_COUNT))
    frame_shift = 10
    speed_table = [1/10, 1/8, 1/4, 1/2, 1, 2, 3, 4, 5, 8 ,10]
    speed_index = 4

    reverse_mode = False

    while True:

        if not reverse_mode:
            valid, img = video.read()
            if not valid:
                break
            frame = int(video.get(cv.CAP_PROP_POS_FRAMES))
        else:
            frame -= 1
            video.set(cv.CAP_PROP_POS_FRAMES, frame)
            valid, img = video.read()
            if not valid or frame < 0:
                reverse_mode = False
                frame = 0
                video.set(cv.CAP_PROP_POS_FRAMES, 0)
                valid, img = video.read()
        if reverse_mode:
            info = f'Frame: {frame}/{frame_total}, Speed: x-1'
        else:
            info = f'Frame: {frame}/{frame_total}, Speed: x{speed_table[speed_index]:.2g}'
        cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
        cv.imshow('Video Player', img)

        key = cv.waitKey(max(int(wait_msec / speed_table[speed_index]), 1))
        if key == ord(' '):
            key = cv.waitKey()
        if key == 27:
            break
        elif key == ord('\t'):
            speed_index = 4
        elif key == ord('>') or key == ord('.'):
            if reverse_mode == False:
                speed_index = min(speed_index + 1, len(speed_table) - 1)
        elif key == ord('<') or key == ord(","):
            if reverse_mode == False:
                speed_index = max(speed_index -1, 0)
        elif key == ord(']') or key == ord('}'):
            frame += frame_shift
            video.set(cv.CAP_PROP_POS_FRAMES, frame)
        elif key == ord('[') or key == ord('{'):
            frame -= frame_shift
            video.set(cv.CAP_PROP_POS_FRAMES, max(frame, 0))
        elif key == ord('r'):
            reverse_mode = not reverse_mode
            speed_index = 4

    cv.destroyAllWindows()
