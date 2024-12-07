import cv2
import numpy as np



def aruco_detection():

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
    arucoParams = cv2.aruco.DetectorParameters_create()

    aruco_center=[]
    
    vto_move=0
    hto_move=0
    # Loop through the frames
    while True:
        # Get the frame from the camera
        ret, frame = cap.read()
        fw= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fc=[int(fw/2),int(fh/2)]
        cutoff=100
        height= height_measure(2,3)
    
        # Detect the ArUco markers in the frame
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, aruco_dict,parameters=arucoParams)
    
        cv2.line(frame, (fc[0]-cutoff,fc[1]-cutoff), (fc[0]-cutoff,fc[1]+cutoff), ( 255, 0, 255), 1)
        cv2.line(frame, (fc[0]-cutoff,fc[1]-cutoff), (fc[0]+cutoff,fc[1]-cutoff), ( 255, 0, 255), 1)
        cv2.line(frame, (fc[0]+cutoff,fc[1]+cutoff), (fc[0]-cutoff,fc[1]+cutoff), ( 255, 0, 255), 1)
        cv2.line(frame, (fc[0]+cutoff,fc[1]+cutoff), (fc[0]+cutoff,fc[1]-cutoff), ( 255, 0, 255), 1)
    
        cv2.line(frame, (0,fc[1]), (fw,fc[1]), ( 255, 0, 0), 1)
        #cv2.line(frame, (320,240), (640,240), ( 255, 0, 0), 1)
    
        cv2.line(frame, (fc[0],0), (fc[0],fh), ( 0, 255, 0), 1)
    
        #cv2.putText(frame, '(1500,1500)',(280,250), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)
        #cv2.putText(frame, '(1180,1500)',(0,250), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)
        #cv2.putText(frame, '(1500,1260)',(285,10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)
        #cv2.putText(frame, '(1500,1740)',(285,480), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)
        #cv2.putText(frame, '(1820,1500)',(560,250), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)
        
        cv2.putText(frame, 'Height',(560,15), cv2.FONT_HERSHEY_SIMPLEX,0.35, (255, 255, 255), 1)
        cv2.putText(frame, str(height),(560,30), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 255, 255), 2)
        
        # If any markers are detected
        if ids is not None:
            # Draw the markers on the frame
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)      
            
        if len(corners) > 0:
            # flatten the ArUco IDs list
            ids = ids.flatten()
            # loop over the detected ArUCo corners
            for (markerCorner, markerID) in zip(corners, ids):
                # extract the marker corners (which are always returned in
                # top-left, top-right, bottom-right, and bottom-left order)
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                # convert each of the (x, y)-coordinate pairs to integers
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                
            cX = int((topLeft[0] + bottomRight[0]) // 2)
            cY = int((topLeft[1] + bottomRight[1]) // 2)
            aruco_center.append(cX)
            aruco_center.append(cY)
            disp=(cX+1180,cY+1260)
            cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
            cv2.putText(frame, str(disp),(cX,cY+20), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 255, 255), 2)
            cv2.putText(frame, 'Dropzone',(topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            if(1480<disp[1]<1520 and 1465<disp[1]<1535):
                cv2.putText(frame, 'Landing',(0,35), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
                print("landing")
            
            else:
                if(disp[1]<1500):
                    cv2.putText(frame, 'forward',(0,35), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)
                    vto_move=int(1500-disp[1])
                    print(f"Forward {disp[1]}")
                    cv2.putText(frame, str(disp[1]),(70,35), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)
                else:
                    cv2.putText(frame, 'backward',(0,35), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)
                    vto_move=int(disp[1]-1500)
                    print(f"Backward {disp[1]}")
                    cv2.putText(frame, str(disp[1]),(70,35), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)
                
                if(disp[0]<1500):
                    cv2.putText(frame, 'left',(0,50), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 255), 2)
                    hto_move=int(1500-disp[0])
                    print(f"Left {disp[0]}")
                    cv2.putText(frame, str(disp[0]),(50,50), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 255), 2)
                else:
                    cv2.putText(frame, 'right',(0,50), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 255), 2)
                    hto_move=int(disp[0]-1500)
                    print(f"Right {disp[0]}")
                    cv2.putText(frame, str(disp[0]),(50,50), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 255), 2)
        
    
        # Display the frame
        cv2.imshow('frame', frame)
    
    
        # Exit if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return aruco_center[-2:]

def get_limits(color):

    c = np.uint8([[color]])  # here insert the bgr values which you want to convert to hsv
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lowerLimit = hsvC[0][0][0] - 10, 100, 100
    upperLimit = hsvC[0][0][0] + 10, 255, 255

    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)

    return lowerLimit, upperLimit

def colour_detection():
    
    cap = cv2.VideoCapture(0)
    yellow=[255,255,0]
    center = None
    while True:
    
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        lower, upper=get_limits(color=yellow)

        mask = cv2.inRange(hsv, lower, upper)
    
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            #center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.rectangle(frame, (int(x - radius), int(y - radius)), (int(x + radius), int(y + radius)), (0, 255, 255), 2)
            if M['m00'] != 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return center

        

if __name__ == "__main__":
    from altitude_hold import height_measure
    center=aruco_detection()
    print("aruco center",center)
        

