from django.shortcuts import render
from rest_framework.generics import ListAPIView , DestroyAPIView ,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from task_management.permission import IsEmployee,IsManager,IsTeamLeader



