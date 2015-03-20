import cv2
import time

class CallBack:

    def __init__(self):
        cv2.namedWindow("Camera", cv2.CV_WINDOW_AUTOSIZE )
        self.capture = cv2.VideoCapture(0)

    def on_mouse(self,event, x, y, flag, param):
        if(event == cv2.cv.CV_EVENT_FLAG_LBUTTON):
            flag, src = self.capture.read()
            img = cv2.imshow("Foto normal", src)
                

    def callback(self):
        while True:
             flag, src = self.capture.read()
             cv2.setMouseCallback("Camera",self.on_mouse, param = 0)
             cv2.imshow("Camera", src)
             if cv2.waitKey(10) == 27:
                  break

if __name__ == '__main__':
    cb = CallBack()
    cb.callback()

    cv2.destroyAllWindows()
    
'''
1-Para que sirve el parametro param??? 
2-Tampoco entiendo porque hay parametros que en las llamadas se igualan a otros o a un valor...
3-Porque se pone un if delante del main
'''
