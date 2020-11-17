import cv2
import numpy as np

# Defining a class to handle object tracking related functionality
class ObjectTracking(object):
    def __init__(self, s_factor=0.5):
        # Initialize the video capture object
        self.cap = cv2.VideoCapture(0)

        # Capture the frame from the webcam
        _, self.frame = self.cap.read()

        # Scaling factor for the captured frame
        self.s_factor = s_factor

        # Resize the frame
        self.frame = cv2.resize(self.frame, None, 
                fx=self.s_factor, fy=self.s_factor, 
                interpolation=cv2.INTER_AREA)

        # Creating a window to display the frame
        cv2.namedWindow('Live Object Tracking')

        # Setting the mouse callback function to track the mouse
        cv2.setMouseCallback('Live Object Tracking', self.mouse_event)

        self.selection = None

        self.drag_start = None

        self.tracking_state = 0

    # Defining a method to track the mouse events
    def mouse_event(self, event, x, y, flags, parameter):
        x, y = np.int16([x, y]) 

        # Checking if a mouse button down event has occurred
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)
            self.tracking_state = 0

        # Checking if the user has started selecting the region
        if self.drag_start:
            if flags & cv2.EVENT_FLAG_LBUTTON:
                # Extracting the dimensions of the frame
                h, w = self.frame.shape[:2]

                xi, yi = self.drag_start

                x0, y0 = np.maximum(0, np.minimum([xi, yi], [x, y]))
                x1, y1 = np.minimum([w, h], np.maximum([xi, yi], [x, y]))

                self.selection = None

                if x1-x0 > 0 and y1-y0 > 0:
                    self.selection = (x0, y0, x1, y1)

            else:
                # If the selection is done, starting live tracking of object  
                self.drag_start = None
                if self.selection is not None:
                    self.tracking_state = 1

    # Method to start tracking the object
    def start_track(self):
        while True:
            _, self.frame = self.cap.read()
            
            self.frame = cv2.resize(self.frame, None, 
                    fx=self.s_factor, fy=self.s_factor, 
                    interpolation=cv2.INTER_AREA)

            vis = self.frame.copy()

            hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(hsv, np.array((0., 60., 32.)), 
                        np.array((180., 255., 255.)))

            if self.selection:
                x0, y0, x1, y1 = self.selection

                self.track_window = (x0, y0, x1-x0, y1-y0)

                hsv_region = hsv[y0:y1, x0:x1]
                mask_region = mask[y0:y1, x0:x1]

                histogram = cv2.calcHist( [hsv_region], [0], mask_region, 
                        [16], [0, 180] )

                # Normalize and reshape the histogram
                cv2.normalize(histogram, histogram, 0, 255, cv2.NORM_MINMAX);
                self.histogram = histogram.reshape(-1)

                vis_region = vis[y0:y1, x0:x1]

                cv2.bitwise_not(vis_region, vis_region)
                vis[mask == 0] = 0

            if self.tracking_state == 1:
                self.selection = None
                
                # Compute the histogram back projection
                hsv_back_projection = cv2.calcBackProject([hsv], [0], 
                        self.histogram, [0, 180], 1)

               
                hsv_back_projection &= mask

                termination_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 
                        10, 1)

                # Applying CAMShift on 'hsv_backproj'
                track_box, self.track_window = cv2.CamShift(hsv_back_projection, 
                        self.track_window, termination_criteria)

                cv2.ellipse(vis, track_box, (0, 255, 0), 2)

            cv2.imshow('Live Object Tracking', vis)

            c = cv2.waitKey(5)
            if c == 27:
                break

        cv2.destroyAllWindows()

if __name__ == '__main__':
    ObjectTracker().start_tracking()

