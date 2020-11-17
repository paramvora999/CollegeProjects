import cv2
import numpy as np

def start_track():
    cap = cv2.VideoCapture(0)

    # Define the scaling factor for the frames
    s_factor = 0.5

    num_frame_track = 7

    num_frame_jump = 2

    tracking_path = []
    frame_index = 0

    # Define tracking parameters
    tracking_parameters = dict(winSize  = (11, 11), maxLevel = 2,
            criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 
                10, 0.03))

    while True:
        _, frame = cap.read()

        frame = cv2.resize(frame, None, fx=s_factor, 
                fy=s_factor, interpolation=cv2.INTER_AREA)

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        output_image = frame.copy()

        if len(tracking_path) > 0:
            prev_img, current_img = prev_gray, frame_gray

            feature_point_0 = np.float32([tp[-1] for tp in \
                    tracking_path]).reshape(-1, 1, 2)

            feature_point_1, _, _ = cv2.calcOpticalFlowPyrLK(
                    prev_img, current_img, feature_point_0, 
                    None, **tracking_parameters)

            feature_point_0_rev, _, _ = cv2.calcOpticalFlowPyrLK(
                    current_img, prev_img, feature_point_1, 
                    None, **tracking_parameters)

            
            diff_feature_point = abs(feature_point_0 - \
                    feature_point_0_rev).reshape(-1, 2).max(-1)

            good_point = diff_feature_point < 1

            new_tracking_path = []

            for tp, (x, y), good_point_flag in zip(tracking_path, 
                        feature_point_1.reshape(-1, 2), good_point):
                if not good_point_flag:
                    continue

                tp.append((x, y))
                if len(tp) > num_frame_track:
                    del tp[0]

                new_tracking_path.append(tp)

                # Drawing a circle around the feature points
                cv2.circle(output_img, (x, y), 3, (0, 255, 0), -1)

            # Updating the tracking paths
            tracking_path = new_tracking_path

            cv2.polylines(output_image, [np.int32(tp) for tp in \
                    tracking_path], False, (0, 150, 0))

        if not frame_index % num_frame_jump:
            mask = np.zeros_like(frame_gray)
            mask[:] = 255
            for x, y in [np.int32(tp[-1]) for tp in tracking_path]:
                cv2.circle(mask, (x, y), 6, 0, -1)

            # Compute good features to track
            feature_point = cv2.goodFeaturesToTrack(frame_gray, 
                    mask = mask, maxCorners = 500, qualityLevel = 0.3, 
                    minDistance = 7, blockSize = 7) 

            # Checking if feature points exist. If so, appending them
            # to the tracking paths
            if feature_point is not None:
                for x, y in np.float32(feature_point).reshape(-1, 2):
                    tracking_path.append([(x, y)])

        frame_index += 1
        prev_gray = frame_gray

        # Displaying output
        cv2.imshow('Live Optical Flow', output_image)

        c = cv2.waitKey(1)
        if c == 27:
            break

if __name__ == '__main__':
    start_tracking()

    cv2.destroyAllWindows()

