            if not timerlocked:
                ref_time = time.ctime()[17] + time.ctime()[18]
                timerlocked = True
                print(ref_time)

            cur_time = int(time.ctime()[17] + time.ctime()[18])
            print("curtime =",cur_time)
            if name in names:
                if (cur_time - int(ref_time))== 3 : 
                    counts.append(len(counts)+1)
                    print("counts =", counts)
                    cv2.destroyAllWindows()
                    cam.release()
                    sys.exit()
                elif (cur_time - int(ref_time)) > 4:
                    print("Face not matched ....Reseting timer ")
                    timerlocked = False    
            else:
                print("not matched")
                
