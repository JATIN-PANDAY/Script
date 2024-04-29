import re
import pyautogui
import keyboard

import time
import threading
from django.shortcuts import render, redirect 
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from .models import User
from datetime import datetime, timedelta

# Create your views here.



# Mouse movement Function


# def check_mouse_activity(interval=10, warning_interval=5):
#     last_position = pyautogui.position()
#     last_move_time = time.time()
#     last_key_press_time = time.time()

#     while True:
#         current_position = pyautogui.position()

#         if current_position != last_position:
#             last_move_time = time.time()
#             last_position = current_position
#             last_key_press_time = time.time()
            
#         else:
#             if time.time() - last_move_time >= interval:
#                 print("Mouse pointer not moved for {} seconds.".format(interval))
#                 # messages.warning(request, 'No  activity detected. Please log in again.')
#                 if time.time() - last_key_press_time >= warning_interval:
#                     print("Warning: No keyboard activity for {} seconds.".format(warning_interval))
#                     # messages.warning(request, 'No  activity detected. Please log in again.')

#         time.sleep(1)

''' This function work properly '''

# def check_mouse_activity(interval=10):
#     last_position = pyautogui.position()
#     last_move_time = time.time()

#     while True:
#         current_position = pyautogui.position()

#         if current_position != last_position:
#             last_move_time = time.time()
#             last_position = current_position
            
#         else:
#             if time.time() - last_move_time >= interval:
#                 return False  # Mouse pointer not moved
#         time.sleep(1)


# def check_keyboard_activity(interval=5):
#     last_key_press_time = time.time()

#     while True:
#         if keyboard.is_pressed('q'):  # Check if specific key is pressed
#             last_key_press_time = time.time()  # Update last key press time
#             print('key pressed')
#         elif time.time() - last_key_press_time >= interval:
#             print('No key pressed')
#             return False  # No keyboard activity detected for the specified interval
#         time.sleep(1)

''' Function end '''



def check_activity_wrapper(mouse_interval=300, keyboard_interval=300):
    def check_mouse_activity(interval):
        last_position = pyautogui.position()
        last_move_time = time.time()

        while True:
            current_position = pyautogui.position()

            if current_position != last_position:
                last_move_time = time.time()
                last_position = current_position
                print("Cursor moved")
                
            else:
                if time.time() - last_move_time >= interval:
                    print('Cursor not moved')
                    return False  
            time.sleep(1)

    def check_keyboard_activity(interval):
        last_key_press_time = time.time()

        while True:
            if keyboard.is_pressed('q'):  
                last_key_press_time = time.time()  
                print('Key pressed')
            elif time.time() - last_key_press_time >= interval:
                print('No key pressed')
                return False  
            time.sleep(1)

    mouse_result = check_mouse_activity(mouse_interval)
    keyboard_result = check_keyboard_activity(keyboard_interval)

    return mouse_result and keyboard_result










# def check_activity(interval=10):
#     last_position = pyautogui.position()
#     last_move_time =time.time()
#     last_key_press = time.time()

#     while True:
#         current_position = pyautogui.position()
#         if current_position != last_position:
#             last_move_time = time.time()
#             last_position = current_position
#             print("cursor moved")
#         elif keyword.is_pressed('q'):
#                 last_key_press = time.time()
#                 print("key pressed")

#                 time.time()-last_key_press >= interval
#                 print("no key pressed")
#                 return False
#         time.sleep(1)
#         else:
#             if time.time() - last_move_time >= interval:
#                 print("Cursor not moved")
#                 return False
#             time.sleep(1)








########### Check activity function ###################



def index(request):
    uid = request.COOKIES.get('uid')
    if uid:
        # Check mouse activity
        if check_activity_wrapper():
        # Call function to check activity
        # if check_activity():

            response = render(request, 'index.html', {'uid': uid})
            response.set_cookie('uid', uid, max_age=86400)  
            return response
        else:
            messages.warning(request, 'No  activity detected. Please log in again.')
            return redirect('signin')
    else:
        return redirect('signin')



# Signup

def signup(request):
    if request.method == 'POST':
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword=request.POST.get("cpassword")

        user_obj= User.objects.filter(email=email)
        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)
            
        else:
            if password==cpassword:
                user = User.objects.create(email=email,password=password)
                return redirect('signin')
            else:
                messages.warning(request,"Password and confirm password not match")
                return HttpResponseRedirect(request.path_info)

    return render(request,'signup.html')
        



################ Set activity on login page #######################################


def signin(request):
    try:
        if request.method == 'POST':
            
            email = request.POST.get('email')
            password = request.POST.get('password')

            user_obj = User.objects.get(email=email)
                
            if user_obj:
                if user_obj.password == password:
                    response = redirect('/')
                    response.set_cookie('email', email, max_age=60)  
                    # response.set_cookie('password', password, max_age=60)  
                    response.set_cookie('uid', user_obj.uid, max_age=60) 
                    
                    return response
                else:
                    messages.warning(request, 'Incorrect Password')
                    return HttpResponseRedirect(request.path_info)
            else:
                messages.warning(request, 'Invalid credentials')
                return HttpResponseRedirect(request.path_info)

    except User.DoesNotExist:
        messages.warning(request, 'Incorrect Email')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'signin.html')
