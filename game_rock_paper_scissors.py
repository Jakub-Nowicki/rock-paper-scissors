import cv2
import hand_tracking_module as htm

def winner(p1,p2): #function to determinate who wins
    if p1 == p2:
        return 'draw'
    
    if p1 == 'rock' and p2 == 'scissors':
        return 'player right wins'
    
    if p1 == 'rock' and p2 == 'paper':
        return 'player left wins'
    
    if p1 == 'scissors' and p2 == 'rock':
        return 'player left wins'
    
    if p1 == 'paper' and p2 == 'rock':
        return 'player right wins'
    
    if p1 == 'scissors' and p2 == 'paper':
        return 'player right wins'

    if p1 == 'paper' and p2 == 'scissors':
        return 'player left wins'

cap = cv2.VideoCapture(0)
overlayList = []
detector = htm.handDetector(detectionCon=0.75)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)  # position of first hand stored 0:20 and second from 21:22
        
    if len(lmList) == 42: 
        
        cv2.rectangle(img, (10,200), (370, 30), (249, 234, 222), cv2.FILLED)
        
        if lmList[12][1] < lmList[0][1]: #if the first hand is on the right 
            
            # print(lmList_1[0], lmList_1[21])
            if lmList[4][2] < lmList[3][2]:
                p1_thumb_up = True
            else:
                p1_thumb_up = False
            
            if lmList[8][1] < lmList[6][1]:
                p1_index_fg_up = True
            else:
                p1_index_fg_up = False
                
            if lmList[12][1] < lmList[10][1]:
                p1_middle_fg_up = True
            else:
                p1_middle_fg_up = False
                
            if lmList[16][1] < lmList[14][1]:
                p1_ring_fg_up = True
            else:
                p1_ring_fg_up = False
            
            if lmList[20][1] < lmList[18][1]:
                p1_pinky_fg_up = True
            else:
                p1_pinky_fg_up = False
                
        else: # this if first hand is on the left
            if lmList[4][2] < lmList[3][2]:
                p1_thumb_up = True
            else:
                p1_thumb_up = False
            
            if lmList[8][1] > lmList[6][1]:
                p1_index_fg_up = True
            else:
                p1_index_fg_up = False
                
            if lmList[12][1] > lmList[10][1]:
                p1_middle_fg_up = True
            else:
                p1_middle_fg_up = False
                
            if lmList[16][1] > lmList[14][1]:
                p1_ring_fg_up = True
            else:
                p1_ring_fg_up = False
            
            if lmList[20][1] > lmList[18][1]:
                p1_pinky_fg_up = True
            else:
                p1_pinky_fg_up = False
            
            
        if lmList[12+21][1] < lmList[0+21][1]: #if the second hand is on the right
            # print(lmList_1[0], lmList_1[21])
            if lmList[4+21][2] < lmList[3+21][2]:
                p2_thumb_up = True
            else:
                p2_thumb_up = False
            
            if lmList[8+21][1] < lmList[6+21][1]:
                p2_index_fg_up = True
            else:
                p2_index_fg_up = False
                
            if lmList[12+21][1] < lmList[10+21][1]:
                p2_middle_fg_up = True
            else:
                p2_middle_fg_up = False
                
            if lmList[16+21][1] < lmList[14+21][1]:
                p2_ring_fg_up = True
            else:
                p2_ring_fg_up = False
            
            if lmList[20+21][1] < lmList[18+21][1]:
                p2_pinky_fg_up = True
            else:
                p2_pinky_fg_up = False
                
                
            if lmList[0][1] < 600 and lmList[21][1] > 600:
                player = 'player left: '
            else:
                player = 'player right: '    
                
            #displaying the values   
            if p1_thumb_up and p1_index_fg_up and p1_middle_fg_up and p1_ring_fg_up and p1_pinky_fg_up:
                cv2.putText(img, f'{player}paper', (10,70), cv2.FONT_HERSHEY_PLAIN, 2, (102, 167, 197), 2)
                p1 = 'paper'
            elif (p1_thumb_up or p1_thumb_up == False) and p1_index_fg_up and p1_middle_fg_up and  p1_pinky_fg_up == False and p1_ring_fg_up == False:
                cv2.putText(img, f'{player}scissors', (10,70), cv2.FONT_HERSHEY_PLAIN, 2, (223, 50, 51), 2)
                p1 = 'scissors'
            elif (p1_thumb_up == False or p1_thumb_up) and p1_index_fg_up == False and p1_middle_fg_up == False and p1_pinky_fg_up == False and p1_pinky_fg_up == False:
                cv2.putText(img, f'{player}rock', (10,70), cv2.FONT_HERSHEY_PLAIN, 2, (223, 50, 51), 2)    
                p1 = 'rock'
                
            if lmList[0][1] > 600 and lmList[21][1] < 600:
                player = 'player left: '
            else:
                player = 'player right: '    
                
            if p2_thumb_up and p2_index_fg_up and p2_middle_fg_up and p2_ring_fg_up and p2_pinky_fg_up:
                cv2.putText(img, f'{player}paper', (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (223, 50, 51), 2)
                p2 = 'paper'
            elif (p2_thumb_up or p2_thumb_up == False) and p2_index_fg_up and p2_middle_fg_up and p2_pinky_fg_up == False and p2_ring_fg_up == False:
                cv2.putText(img, f'{player}scissors', (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (102, 167, 197), 2)
                p2 = 'scissors'
            elif (p2_thumb_up == False or p2_thumb_up) and p2_index_fg_up == False and p2_middle_fg_up == False and p2_pinky_fg_up == False and p2_pinky_fg_up == False:
                cv2.putText(img, f'{player}rock', (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (102, 167, 197), 2)
                p2 = 'rock'
            
            #deciding who won
            who_won = winner(p2,p1)
            cv2.putText(img, who_won, (10, 170), cv2.FONT_HERSHEY_PLAIN, 2, (250,198,14), 2)
                
        else: #if the second hand is on the left
            if lmList[4+21][2] < lmList[3+21][2]:
                p2_thumb_up = True
            else:
                p2_thumb_up = False
            
            if lmList[8+21][1] > lmList[6+21][1]:
                p2_index_fg_up = True
            else:
                p2_index_fg_up = False
                
            if lmList[12+21][1] > lmList[10+21][1]:
                p2_middle_fg_up = True
            else:
                p2_middle_fg_up = False
                
            if lmList[16+21][1] > lmList[14+21][1]:
                p2_ring_fg_up = True
            else:
                p2_ring_fg_up = False
            
            if lmList[20+21][1] > lmList[18+21][1]:
                p2_pinky_fg_up = True
            else:
                p2_pinky_fg_up = False
                
            if lmList[0][1] < 600 and lmList[21][1] > 600: #checking position of the hand and assignin it to the player
                player = 'player left : '
            else:
                player = 'player right: '    
                
            #displaying the values
            if p1_thumb_up and p1_index_fg_up and p1_middle_fg_up and p1_ring_fg_up and p1_pinky_fg_up:
                cv2.putText(img, f'{player}paper', (10,70), cv2.FONT_HERSHEY_PLAIN, 2, (223, 50, 51), 2)
                p1 = 'paper'
            elif (p1_thumb_up or p1_thumb_up == False) and p1_index_fg_up and p1_middle_fg_up and  p1_pinky_fg_up == False and p1_ring_fg_up == False:
                cv2.putText(img, f'{player}scissors', (10,70), cv2.FONT_HERSHEY_PLAIN, 2, (223, 50, 51), 2)
                p1 = 'scissors'
            elif (p1_thumb_up == False or p1_thumb_up) and p1_index_fg_up == False and p1_middle_fg_up == False and p1_pinky_fg_up == False and p1_pinky_fg_up == False:
                cv2.putText(img, f'{player}rock', (10,70), cv2.FONT_HERSHEY_PLAIN, 2, (223, 50, 51), 2)    
                p1 = 'rock'
                
            if lmList[0][1] > 600 and lmList[21][1] < 600:
                player = 'player left: '
            else:
                player = 'player right: '    
                
            if p2_thumb_up and p2_index_fg_up and p2_middle_fg_up and p2_ring_fg_up and p2_pinky_fg_up:
                cv2.putText(img, f'{player}paper', (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (102, 167, 197), 2)
                p2 = 'paper'
            elif (p2_thumb_up or p2_thumb_up == False) and p2_index_fg_up and p2_middle_fg_up and p2_pinky_fg_up == False and p2_ring_fg_up == False:
                cv2.putText(img, f'{player}scissors', (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (102, 167, 197), 2)
                p2 = 'scissors'
            elif (p2_thumb_up == False or p2_thumb_up) and p2_index_fg_up == False and p2_middle_fg_up == False and p2_pinky_fg_up == False and p2_pinky_fg_up == False:
                cv2.putText(img, f'{player}rock', (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (102, 167, 197), 2)
                p2 = 'rock'
                
            who_won = winner(p1,p2)
            cv2.putText(img, who_won, (10, 170), cv2.FONT_HERSHEY_PLAIN, 2, (250,198,14), 2)
                           
    cv2.imshow('Image', img)
    cv2.waitKey(1)
    