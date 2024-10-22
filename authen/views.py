from smtplib import SMTPResponseException
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from authen.forms import SignUpForm
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser
from rest_framework.views import APIView
from .utils import generate_otp, send_otp_email


def home(request):
    return  render(request, 'auth/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', { 'form' : form })


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)
 
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)    
    

@api_view(['POST'])
def user_logout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        


class LoginWithOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        user.otp = otp
        user.save()

        send_otp_email(email, otp)
    
        # Redirect to another URL after successful operation 
        return redirect('validate-otp') 

class ValidateOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        otp = request.data.get('otp', '')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.otp = None 
            user.save()

            token, _ = Token.objects.get_or_create(user=user)

            # Redirect to another URL after successful operation
            return redirect('home')  # Replace 'home' with your desired URL name
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


  

# views.py

from django.shortcuts import render
import subprocess
import shlex

from .forms import Emailform


def run_command(email):
    # Replace the email in the command
    command = f"$body = @{{ email = 'viswanathkausik22@gmail.com' }} | ConvertTo-Json; Invoke-RestMethod -Uri 'http://localhost:8000/login-with-otp/' -Method POST -Headers @{{ 'Content-Type' = 'application/json' }} -Body $body"

    # Split the command into arguments
    command_args = shlex.split(command)

    # Execute the command in the terminal
    try:
        result = subprocess.run(command_args, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
    



def index(request):
    if request.method == 'POST':
        form = Emailform(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            output = run_command(email)
            return render(request, 'auth/result.html', {'output': output})
    else:
        form = Emailform()
    return render(request, 'auth/index.html', {'form': form})

def execute_command(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Get the submitted email
        output = run_command(email)  # Execute the command with the provided email
        return HttpResponse(output)  # Return the output to the user or perform other actions
    return render(request, 'auth/result.html')
