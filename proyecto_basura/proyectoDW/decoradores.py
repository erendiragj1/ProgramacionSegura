from django.shortcuts import redirect
 
def esta_logueado(vista):
    def interna(request):
        if not request.session.get('logueado', False):
            return redirect('/login/')
        return vista(request)
    return interna
