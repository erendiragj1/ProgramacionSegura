from re import compile
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import Template, Context
from django.shortcuts import render, redirect
from app_proyectoDW import models
from proyectoDW import decoradores
from datetime import datetime, date, time, timedelta
import locale
import calendar

def login(request):
   errores = {}
   t = 'login.html'
   if request.method=='GET':
      return render(request,t)
   elif request.method=="POST":
      usuario = request.POST.get('usr','')
      password = request.POST.get('pwd','')
      if (usuario != '') and (password !=''):
         if (models.Usuarios.objects.filter(usr=usuario,pwd=password)):
            request.session['logueado'] = True
            return redirect('/servidores/')
         else:
            errores={'errores': 'Usuario y contraseña inválidos.'}
      else:
         errores={'errores': 'Deben de indicarse un usuario y contraseña.'}
      
      if (errores):
         return render(request, t, errores)
      else:
         return redirect('/login/')

@decoradores.esta_logueado
def servidores(request):
   t = 'servidores.html'
   errores = ''
   lista_servidores = models.Servidores.objects.all()
   c = {'lista_servidores': lista_servidores}
   if request.method=='GET':
      return render(request, t, c)
   elif request.method=="POST":
      desc_srv=request.POST.get('servidor','').strip()
      ip_srv=request.POST.get('ip_srv','').strip()
      patron=compile('^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}.[0-9]{1,3}$')
      if (ip_srv=='') or (desc_srv==''):
         errores='Debe de colocarse la descripción del servidor y dirección ip.'
      try:
         if not(patron.match(ip_srv)) and not errores:
            errores='Dirección ip inválida, sintaxis inválida'
         for nodo in ip_srv.split('.'):
            if (int(nodo)>255):
               errores='Dirección ip inválida, nodo mayor a 255.'
         if (models.Servidores.objects.filter(ip_srv=ip_srv)):
            errores='Ya existe un servidor registrado con esa dirección IP.'
      except:
         errores='Dirección ip inválida, error al leer nodos.'
      
      if not (errores):
         objServidores=models.Servidores()
         objServidores.desc_srv=desc_srv
         objServidores.ip_srv=ip_srv
         objServidores.fh_srv=datetime.now()
         objServidores.status='E'
         objServidores.save()
      else:
         c = {'lista_servidores': lista_servidores,'errores':errores}
      return render(request, t, c)
         

@decoradores.esta_logueado
def usuarios(request):
   t = 'usuarios.html'
   return render(request,t)

def logout(request):
   t = 'login.html'
   request.session['logueado'] = False
   return render(request,t)

def actualizaSrv(request):
   html='Error'
   ip = request.META.get('REMOTE_ADDR')
   if request.method=='GET':
      id=request.GET.get('id','')
      # if not(models.Usuarios.objects.filter(ip_srv=ip,id=id)): #Valida que la ip coincida con la del servidor
      #    print('Hola')
      #    return HttpResponse(html) #Si no coinciden regresara html con error
      s=request.GET.get('s',None)
      html = id
      if (id!=''):
         objServidores=models.Servidores.objects.get(id=id)
         if (str(ip)!=str(objServidores.ip_srv)): #Se valida que la dirección IP sea válida con la registrada y la de la petición
            return HttpResponse(html)
         #locale.setlocale(locale.LC_TIME,'')
         objServidores.fh_srv=datetime.now()
         if (s=='A'):
            objServidores.status='A'#Apagado
         else:
            objServidores.status='E'#Encendido
         objServidores.save()
   return HttpResponse(html)

def actualizaStatus(request):
   if request.method=='GET':
      T_Diferencia=10#Tiempo de difencia, se asigna como variable por si hay que cambiarlo jeje
      for servidor in models.Servidores.objects.all():
         objServidores=models.Servidores.objects.get(id=servidor.id)
         #locale.setlocale(locale.LC_TIME,'')
         fecha_act=datetime.now() #Fecha actual
         #fecha_act=fecha_act-timedelta(hours=5) #Se le quita 5 horas por problema horario
         fecha_srv=objServidores.fh_srv #Fecha del servidor registrada en la bd 
         l_datetime_srw=str(fecha_srv).split() #Se consigue separar fecha y tiempo
         l_datetime_srw=datetime.strptime(l_datetime_srw[0]+' '+l_datetime_srw[1],"%Y-%m-%d %H:%M:%S")
         #Si la fecha actual + tiempo rango es mayor a la fecha del srv Y Si la fecha del srv + fecha actual es mayor...
         if (objServidores.status != 'A'):
            if (fecha_act+timedelta(minutes=T_Diferencia)>l_datetime_srw) and (l_datetime_srw+timedelta(minutes=T_Diferencia)>fecha_act): 
               objServidores.status='E' #...Se actualiza estatus a activo
            else:
               objServidores.status='I' #...Se actualiza estatus a indeterminado por que no se ha recibido mensaje de vida del srv
            objServidores.save()
   return redirect('../servidores/')
