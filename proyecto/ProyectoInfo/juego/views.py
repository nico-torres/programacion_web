from django.shortcuts import render, redirect
from .models import Pregunta, Respuesta, Partida
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import PreguntaForm
from datetime import datetime
from .models import PostForm
from django.shortcuts import redirect


# Create your views here.
@login_required(login_url='/login')
def listar_preguntas(request):
    if request.method == "POST":
        resultado = 0
        for i in range(1,4):
            opcion = Respuesta.objects.get(pk=request.POST[str(i)])
            resultado += opcion.puntaje
        Partida.objects.create(usuario=request.user, fecha=datetime.now, resultado= resultado)
        return redirect("/")
    else:
        data = {}
        preguntas = Pregunta.objects.all().order_by('?')[:3]
        for item in preguntas:
            respuestas = Respuesta.objects.filter(id_pregunta=item.id)
            data[item.pregunta]= respuestas

        return render(request, 'juego/listar_preguntas.html', {"preguntas":data})

def crear_pregunta(request):
    if request.method == "juego":
        form = PreguntaForm(request.JUEGO)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.fecha_creacion = datetime.now()
            registro.save()
    form = PreguntaForm()
    return render(request, 'juego/crear_pregunta.html', {'form': form})

def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.fecha_creacion = datetime.now()
            post.save()
            return redirect('juego:detalle_post', identificador=post.id) #nombre de la vista a la que queremos ir
    else:
        form = PostForm()
    return render(request, 'crear_post.html', {'form': form})

def detalle_post(request, identificador):
    post = Post.objects.get(pk=identificador)
    context = {"posts": post}
    return render(request, 'detalle_post.html', context)

def editar_post(request, identificador):
    post = get_object_or_404(Post, pk=identificador)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.fecha_creacion = datetime.now()
            post.save()
            return redirect('juego:detalle_post', identificador=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'editar_post.html', {'form': form})

def eliminar_post(request, identificador):
    post = Post.objects.get(pk=identificador)
    context = {"posts": post}
    return render(request, 'detalle_post.html', context)
