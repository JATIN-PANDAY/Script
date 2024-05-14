import re
import pyautogui
import keyboard
from pynput import keyboard

import time
import threading
from django.shortcuts import render, redirect 
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from .models import User
from datetime import datetime, timedelta


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate

from django.contrib.messages import error
import os  # For environment variables

# Create your views here.



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





# def check_activity_wrapper(mouse_interval=5, keyboard_interval=5):
#     def check_mouse_activity(interval):
#         last_position = pyautogui.position()
#         last_move_time = time.time()

#         while True:
#             current_position = pyautogui.position()

#             if current_position != last_position:
#                 last_move_time = time.time()
#                 last_position = current_position
#                 print("Cursor moved")
                
#             else:
#                 if time.time() - last_move_time >= interval:
#                     print('Cursor not moved')
#                     return HttpResponse("Cursor not moved")
#                     return False  
#             time.sleep(1)

#     def check_keyboard_activity(interval):
#         last_key_press_time = time.time()

#         while True:
#             if keyboard.is_pressed('q'):  
#                 last_key_press_time = time.time()  
#                 print('Key pressed')
#             elif time.time() - last_key_press_time >= interval:
#                 print('No key pressed')
#                 return False  
#             time.sleep(1)
        

#     mouse_result = check_mouse_activity(mouse_interval)
#     keyboard_result = check_keyboard_activity(keyboard_interval)

#     return mouse_result and keyboard_result




def check_activity(mouse_interval=5, keyboard_interval=5):
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

            def on_press(key):
                nonlocal last_key_press_time
                last_key_press_time = time.time()
                print('Key pressed')

            listener = keyboard.Listener(on_press=on_press)
            listener.start()

            while True:
                if time.time() - last_key_press_time >= interval:
                    listener.stop()
                    print('No key pressed')
                    return False
                time.sleep(1)

    mouse_active = check_mouse_activity(mouse_interval)
    keyboard_active = check_keyboard_activity(keyboard_interval)

    return mouse_active and keyboard_active






########### Check activity function ###################








''' Update Index '''




def index(request):
    interval=5
    uid = request.COOKIES.get('uid')
    last_position = pyautogui.position()
    last_move_time = time.time()
    last_key_press_time = time.time()

    # if uid:
    #     return render(request,'index.html',{'uid':uid})

    while True:
        if uid:
            current_position = pyautogui.position()

            
            if current_position != last_position:
                    last_move_time = time.time()
                    last_position = current_position
                    print('cursor moved')
                    return render(request,'index.html',{'uid':uid})
            elif time.time() - last_move_time >= interval: 
                # if time.time() - last_move_time >= interval:
                messages.warning(request, 'No  activity detected. Please log in again.')
#             return redirect('signin')

                print('Cursor  not  moved')
                return redirect('signin')
                        # return HttpResponse("Cursor not moved")
                return False
            time.sleep(1)
    
    while True:
            if keyboard.is_pressed('q'):  
                last_key_press_time = time.time()  
                print('Key pressed')
            elif time.time() - last_key_press_time >= interval:
                print('No key pressed')
                return False  
            time.sleep(1)
            
    else:
        return redirect('/signin')
       











# Signup

@csrf_exempt
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
                #  Create a dictionary containing email and password
                user_data = {
                    'email': email,
                    'password': password
                }

                # Convert the dictionary to JSON format
                user_json = json.dumps(user_data)
                print(user_json)

                # Return the JSON response
                return JsonResponse(user_data)
                return redirect('/index')
            else:
                messages.warning(request,"Password and confirm password not match")
                return HttpResponseRedirect(request.path_info)
                

    return render(request,'signup.html')
        





# def signin(request):
#     if request.method=="POST":
#         email=request.POST.get('email')
#         password=request.POST.get("password")

            
        
#         url = 'https://projektly.com/api/login'

#         payload = {
#             'email': email,
#             'password': password
#         }

#         # payload = {
#         #     'email': ' testabhi@gmail.com ',
#         #     'password': '123456'
#         # }

#         headers = {
#             'Accept': 'application/json',
#             'Content-Type': 'application/json',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

#         }
        
#         try:
#             response = requests.post(url, json=payload, headers=headers)
#             response.raise_for_status()  # Raise an exception for 4XX/5XX status codes
#             data = response.json()
#             if response.status_code == 200:
#                 print("Login successful!")
#                 return redirect('/')



#             elif response.status_code == 401:
#                 print("Login failed. Unauthorized access. Please check your credentials.")
#             else:
#                 print("Login failed. Status code:", response.status_code)
#             print("Response data:", data)
#         except requests.exceptions.HTTPError as err:
#             print("HTTP Error:", err)
#         except requests.exceptions.JSONDecodeError as err:
#             print("JSON Decode Error:", err)
#         except Exception as err:
#             print("Error:", err)
#     return render(request,'signin.html')





# def signin(request):
#     if request.method=="POST":
#         email=request.POST.get('email')
#         password=request.POST.get("password")

            
        
#         url = 'https://projektly.com/api/login'

#         payload = {
#             'email': email,
#             'password': password
#         }

#         # payload = {
#         #     'email': ' testabhi@gmail.com ',
#         #     'password': '123456'
#         # }

#         headers = {
#             'Accept': 'application/json',
#             'Content-Type': 'application/json',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

#         }
        
#         try:
#             response = requests.post(url, json=payload, headers=headers)
#             response.raise_for_status()  # Raise an exception for 4XX/5XX status codes
#             data = response.json()
#             if response.status_code == 200:
#                 print("Login successful!")
#                 mouse_result, keyboard_result = check_activity_wrapper()
#                 messages.warning("No activity detched")
#                 return HttpResponseRedirect(request.path_info)


#                 # return redirect('/')



#             elif response.status_code == 401:
#                 print("Login failed. Unauthorized access. Please check your credentials.")
#             else:
#                 print("Login failed. Status code:", response.status_code)
#             print("Response data:", data)
#         except requests.exceptions.HTTPError as err:
#             print("HTTP Error:", err)
#         except requests.exceptions.JSONDecodeError as err:
#             print("JSON Decode Error:", err)
#         except Exception as err:
#             print("Error:", err)
#     return render(request,'signin.html')



def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, 'signin.html')

        url = 'https://projektly.com/api/login'
        payload = {
            'email': email,
            'password': password
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            if response.status_code == 200:
                print("Login successful!")
                # messages.success(request, "Login successful!")

                # Call the mouse and keyboard activity checker
                if not check_activity():
                    return HttpResponse("User inactive")

                # Redirect to the home page or dashboard
                return redirect('/')  

            elif response.status_code == 401:
                print("Login failed. Unauthorized access. Please check your credentials.")
                # messages.error(request, "Invalid email or password.")
            else:
                print("Login failed. Status code:", response.status_code)
                # messages.error(request, "Login failed. Please try again.")

            print("Response data:", data)
        except requests.exceptions.HTTPError as err:
            print("HTTP Error:", err)
            # messages.error(request, "HTTP error occurred. Please try again.")
        except requests.exceptions.JSONDecodeError as err:
            print("JSON Decode Error:", err)
            # messages.error(request, "Failed to decode response. Please try again.")
        except requests.exceptions.RequestException as err:
            print("Request Exception:", err)
            # messages.error(request, "A request error occurred. Please try again.")
        except Exception as err:
            print("Error:", err)
            # messages.error(request, "An error occurred. Please try again.")
            
    return render(request, 'signin.html')