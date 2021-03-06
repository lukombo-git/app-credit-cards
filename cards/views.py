from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.shortcuts import render,redirect
from django.contrib import messages
from .processamento_dados import *
from .models import Clientes
from .forms import *

#User register view
def UserRegister(request):
    form=CreateUserForm(request.POST)
    image_form = UploadImageForm(request.POST,request.FILES)
    if request.method == 'POST':
        if form.is_valid() and image_form.is_valid():
            username = form.save()
            instance = image_form.save(commit=False)
            instance.user=username
            instance.save()
            update_session_auth_hash(request, username)
            messages.success(request, 'Usuário Criado com sucesso!')

            return redirect('login')

    else:
        form = CreateUserForm()
        image_form=UploadImageForm()
    return render(request, 'user_register.html',{'form':form,'image_form':image_form})


def UserLogin(request):
    if request.method == "POST":
       form = LoginForm(request.POST)
       if form.is_valid():
          username = form.cleaned_data['username']
          password = form.cleaned_data['password']
          user = authenticate(request,username=username,password=password)
          if user is not None:
            login(request, user)
            return redirect('list_clientes')
       else:
           messages.info(request,'Usuário ou senha errado!')
    return render(request, 'user_login.html')


def UserProfile(request):
    return render(request, 'user_profile.html')


def UserEditProfile(request):
    if request.method =='POST':
        form =UserProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,'A tua conta foi actualizada com sucesso!')
            return redirect('user_profile')
    else:
         form = UserProfileForm(instance=request.user)   
    contexto ={'form':form}
    return render(request, 'user_profile_edit.html',contexto) 


def UserChangePassword(request):
    if request.method =='POST':
        form =UserPasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,'Tu adicionaste uma nova password!')
            return redirect('user_profile')
    else:
         form =UserPasswordChangeForm(user=request.user)   
    contexto ={'form':form}
    return render(request, 'user_change_password.html',contexto)


def UserLogout(request):
    logout(request)
    return redirect('login')


def paginaInicial(request):
    return render(request,'base_site.html')


def RegisterClientes(request):
    if request.method == 'POST':
        #criando um novo cliente
        cliente = Clientes(
        nome_completo = request.POST.get('nome_completo'),
        provincia = request.POST.get('provincia'),
        idade = request.POST.get('idade'),
        tipo_credito = request.POST.get('tipo_credito'),
        salario_mensal  = request.POST.get('salario_mensal'),
        empreendedor = request.POST.get('empreendedor'),
        montate_credito = request.POST.get('montante_credito'),
        como_quer_pagar = request.POST.get('como_quer_pagar'),
        valor_mes_prestacao = request.POST.get('valor_mes_prestacao')
        )
        #salvando o cliente
        cliente.save()
        #mensagem de sucesso
        messages.success(request, 'Candidatura submetida com Sucesso!')
    return render(request, 'form_wizard_c.html')

def ListClientes(request):
    clientes=Clientes.objects.all()
    proba = getDataset()
    mylista = zip(clientes, proba)
    return render(request,'list_clientes.html',{'my_lista':mylista})

def ClientesView(request,pk):
    cliente = Clientes.objects.get(id_cliente=pk)
    form=ClientesViewForm(instance=cliente)
    if request.method == 'POST':
        form = ClientesViewForm(request.POST, instance = cliente)
        if form.is_valid():
            form.save()
            messages.success(request,'Cliente alterado com sucesso!')
        return redirect('list_clientes')
    contexto ={
            'form':form
    }
    return render(request,'clientes_view.html',contexto)

def ClientesDelete(request,pk):
    cliente = Clientes.objects.get(id_cliente=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request,'Cliente eliminado com sucesso!')
        return redirect('list_clientes')
    contexto ={
            'cliente':cliente
    }
    return render(request,'cliente_delete.html',contexto)
