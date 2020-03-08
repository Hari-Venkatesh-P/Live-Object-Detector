import cv2,time,pandas
from datetime import datetime

first_frame = None
status_list = [None,None]
times=[]
times.append(datetime.now())
video = cv2.VideoCapture(0)
df = pandas.DataFrame(columns=["Start","End"])
while True:
		check,frame=video.read()
		status = 0
		#print(frame)
		#print("2nd++++++++++")
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray,(21,21),0)
		if first_frame is None:
			first_frame = gray
			#print("3rd++++++++++")
			continue
		
		delta_frame = cv2.absdiff(first_frame,gray)
		thresh_delta = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
		thresh_delta = cv2.dilate(thresh_delta,None,iterations=0)
		cnts,heirarchy = cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

		for contour in cnts:
			if cv2.contourArea(contour) < 1000:
				continue
			status = 1
			(x,y,w,h) = cv2.boundingRect(contour)
			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)		
		cv2.imshow("Delta",delta_frame)
		cv2.imshow("Thresh",thresh_delta)
		cv2.imshow("GrayScale",gray)
		cv2.imshow("Colored",frame)
		
		status_list.append(status)
		
		status_list = status_list[-2:]		
		
		if status_list[-1]==1 and status_list[-2]==0:
			print("Object Appeared at")
			print(datetime.now())
			times.append(datetime.now())
		
		if status_list[-1]==0 and status_list[-2]==1:
			print("Object Disappeared at")
			print(datetime.now())
			times.append(datetime.now())

		key = cv2.waitKey(1)
		if key == ord('q'):
			break

#print(status_list)
print(times)
for i in times:
	print(i)
#for i in range(0,len(times),2):
#	df = df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)
df2 = pandas.DataFrame(times)
df2.to_csv("Times.csv")
#df1.to_csv("Times1.csv")
video.release()
cv2.destroyAllWindows()