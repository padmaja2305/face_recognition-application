import base64
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
import numpy as np
import cv2
import os
import face_recognition
from .utility import *
from .models import Attendee, AttendanceLog
from django.views.decorators.csrf import csrf_exempt
import jwt
import datetime
from rest_framework.response import Response


# Test api for testing cors-issue
class CorsTest(APIView):
    def get(self, request):
        return Response({'success': True})

# API view for Home page for Attendee
class Home(APIView):
    def get(self, request):
        if request.user.is_authenticated & request.user.is_superuser:
            return redirect('/monitor')
        
        token = request.COOKIES.get('jwt')
        if not token:
            return redirect('/login')
        try:
            payload = jwt.decode(token, 'secret00', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return redirect('/login')

        user = Attendee.objects.get(id=payload['id'])

        return render(request, 'index.html', {'user': user})

# API view for Sign up for Attendee
class SignUp(APIView):
    def get(self, request):
        # redirecting to login page because login and signup are in same page
        return redirect('/login')

    def post(self, request):
        # creating user with name, email and password, sending json response
        name = request.data['name']
        email = request.data['username']
        password = request.data['password']
        password = hashpass(password)

        new_user = Attendee.objects.create(
            email = email,
            password = password,
            name = name
        )
        try:
            new_user.save()
            return JsonResponse({'message': 'User created'}, status=201)
        except:
            return JsonResponse({'message': 'User already exists'}, status=400)

# API view for Login for Attendee
class Login(APIView):
    def get(self, request):
        return render(request, 'auth.html')

    def post(self, request):
        email = request.data['username']
        password = request.data['password']
        password = hashpass(password)

        try:
            user = Attendee.objects.get(email=email, password=password)
            if user:
                # creating cookie with userid, expire-timestamp, creating timestamp
                payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow(),
                }
                token = jwt.encode(payload, 'secret00', algorithm='HS256')
                response = JsonResponse({'message': 'User logged in'}, status=200)
                response.set_cookie(key='jwt', value=token, max_age=31449600, samesite=None, secure=False)
                return response
            return JsonResponse({'message': 'User not found'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'User not found'}, status=404)

# API view for logout , deletes the stored cookie
class LogOut(APIView):
    def get(self, request):
        response = redirect('/login')
        response.delete_cookie('jwt')
        return response

# collecting attandance data for that user and sending in csv format
class MyAttendance(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return redirect('/login')
        try:
            payload = jwt.decode(token, 'secret00', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return redirect('/login')

        return render(request, 'calendar.html')

    def post(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            return redirect('/login')
        try:
            payload = jwt.decode(token, 'secret00', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return redirect('/login')

        user = Attendee.objects.get(id=payload['id'])
        today = datetime.datetime.today()
        
        try:
            month = int(request.data['month'])
        except :
            month = today.month

        try:
            year = int(request.data['year'])
        except :
            year = today.year

        if month < 1 or month > 12:
            return JsonResponse({'message': 'Invalid month'}, status=400)
        
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if month == 2:
            if year % 4 == 0:
                days_in_month[2] = 29
        
        attandance_Array = [0]*days_in_month[month]
        logs = AttendanceLog.objects.filter(attendee = user, month = month, year=year)
        for log in logs:
            attandance_Array[log.day-1] = 1

        return JsonResponse({'attandance_Array': attandance_Array}, status=200)
        
# Exporting attandance data for given year in csv format
class ExportData(APIView):
    def get(self,request):
        if request.user.is_authenticated & request.user.is_superuser:
            return render(request, 'export.html')
        return redirect('/login')
        # return render(request, 'export.html')
    def post(self, request):
        if request.user.is_authenticated & request.user.is_superuser:

            today = datetime.date.today()
            try:
                month = int(request.data['month'])
            except:
                month = today.month

            try:
                year = int(request.data['year'])
            except:
                year = today.year

            try:
                logs = AttendanceLog.objects.filter( month = month)
                days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                if month == 2:
                    if year % 4 == 0:
                        days_in_month[2] = 29

                # attandance_Array = [0]*(days_in_month[month]+1)
                users = Attendee.objects.all()
                logs = AttendanceLog.objects.filter(month = month)

                total_user = len(users)

                top_row = ['name']
                for i in range(days_in_month[month]):
                    top_row.append(i+1)

                matrix = [top_row ]
                for i in range(len(users)):
                    matrix.append([0]*(days_in_month[month]+1))

                for log in logs:
                    matrix[log.attendee.id][log.day] = 1

                for usr in users:
                    matrix[usr.id][0] = usr.name
                
                csv = ""
                for i in range(len(matrix)):
                    for j in range(len(matrix[i])):
                        csv += str(matrix[i][j]) + ','
                    csv = csv[:-1] + '\n'
                csv = csv[:-1]

                data2 = []
                for i in range(1,len(matrix)):
                    k = [0,0]
                    k[0] = matrix[i][0]
                    for j in range(1,len(matrix[0])):
                        k[1] += matrix[i][j]
                    data2.append(k)

                data2_key = []
                data2_value = []
                for i in range(len(data2)):
                    data2_key.append(data2[i][0])
                    data2_value.append(data2[i][1])


                csv2 = "name,total\n"
                for i in range(len(data2)):
                    csv2 += str(data2[i][0]) + ',' + str(data2[i][1]) + '\n'
                csv2 = csv2[:-1]

                return JsonResponse({'csv1': csv, 'csv2':csv2 , 'key1':data2_key, 'value1':data2_value}, status=200)
            except:
                return JsonResponse({'message': 'server Error'}, status=500)
        else:
            token = request.COOKIES.get('jwt')

            if not token:
                return redirect('/login')
            try:
                payload = jwt.decode(token, 'secret00', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return redirect('/login')

            today = datetime.date.today()
            year = today.year

            user = Attendee.objects.get(id=payload['id'])
            logs = AttendanceLog.objects.filter( month = today.month, attendee = user)

            # filltering all logs by month and year, than adding data in 2d list for respective user
            _1st_row = ['date', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
            matrix = [_1st_row]
            for i in range(31):
                matrix.append([0]*13)
                matrix[i+1][0] = i+1
            for log in logs:
                matrix[log.day][log.month] = 1
            csv = ""
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    csv += str(matrix[i][j]) + ','
                csv = csv[:-1] + '\n'
            csv = csv[:-1]
            return JsonResponse({'csv1': csv}, status=200)

# Fetching User profile
class UserProfile(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return redirect('/login')
        try:
            payload = jwt.decode(token, 'secret00', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return redirect('/login')
        
        user = Attendee.objects.get(id=payload['id'])
        return render(request, 'profile.html', {'user': user})
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return redirect('/login')
        try:
            payload = jwt.decode(token, 'secret00', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return redirect('/login')
        
        user = Attendee.objects.get(id=payload['id'])
        return render(request, 'profile.html', {'user': user})


# Edit profile API view 
class EditProfile(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return redirect('/login')
        try:
            payload = jwt.decode(token, 'secret00', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return redirect('/login')
        
        user = Attendee.objects.get(id=payload['id'])
        return render(request, 'editprofile.html', {'user': user})
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return redirect('/login')
        try:
            payload = jwt.decode(token, 'secret00', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return redirect('/login')
        
        user = Attendee.objects.get(id=payload['id'])
        try:
            user.profile_img = request.data['profile_img']
        except:
            pass

        user.name = request.data['name']
        user.phone = request.data['phone']
        user.last_name = request.data['last_name']
        user.pin = request.data['pin']
        user.address = request.data['address']
        user.class_sec = request.data['class_sec']
        user.save()
        return JsonResponse({'message': 'success'}, status=200)


# Render Attendance data with some value
class AttendaceData(APIView):
    def get(self, request):
        if request.user.is_superuser:
            today = datetime.date.today()
            if (today.month < 10):
                date = f"{today.year}-0{today.month}"
            else:
                date = f"{today.year}-{today.month}"
            print(request.user.username)
            return render(request, 'data.html',{'date' : date,'user': request.user}) 
    def post(self,request):
        if request.user.is_superuser:
            try:
                date = request.data['date']
            except:
                today = datetime.date.today()
                if (today.month < 10):
                    date = f"{today.year}-0{today.month}"
                else:
                    date = f"{today.year}-{today.month}"
            print(date)
            return render(request, 'data.html',{'date' : date, 'user': request.user})
        else:
            return redirect('/admin/login')