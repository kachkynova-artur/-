from django.shortcuts import render, redirect, get_object_or_404
from .models import Player, GameResult
from .forms import PlayerForm, GameResultForm
import random

# --- CRUD Игроков ---
def player_list(request):
    players = Player.objects.all()
    return render(request, 'game_app/player_list.html', {'players': players})

def player_create(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_list')
    else:
        form = PlayerForm()
    return render(request, 'game_app/player_form.html', {'form': form})

def player_update(request, pk):
    player = get_object_or_404(Player, pk=pk)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('player_list')
    else:
        form = PlayerForm(instance=player)
    return render(request, 'game_app/player_form.html', {'form': form})

def player_delete(request, pk):
    player = get_object_or_404(Player, pk=pk)
    player.delete()
    return redirect('player_list')

# --- CRUD Результатов ---
def result_list(request):
    results = GameResult.objects.all()
    return render(request, 'game_app/result_list.html', {'results': results})

def result_update(request, pk):
    result = get_object_or_404(GameResult, pk=pk)
    if request.method == 'POST':
        form = GameResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            return redirect('result_list')
    else:
        form = GameResultForm(instance=result)
    return render(request, 'game_app/result_form.html', {'form': form})

def result_delete(request, pk):
    result = get_object_or_404(GameResult, pk=pk)
    result.delete()
    return redirect('result_list')

# --- Игра "Угадай число" ---
def play_game(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    message = ''
    if 'number_to_guess' not in request.session:
        request.session['number_to_guess'] = random.randint(1, 100)
        request.session['attempts'] = 0

    if request.method == 'POST':
        guess = int(request.POST['guess'])
        request.session['attempts'] += 1
        if guess == request.session['number_to_guess']:
            GameResult.objects.create(
                player=player,
                number_to_guess=request.session['number_to_guess'],
                attempts=request.session['attempts'],
                success=True
            )
            message = f"Поздравляю! Вы угадали число за {request.session['attempts']} попыток."
            del request.session['number_to_guess']
            del request.session['attempts']
        elif guess < request.session['number_to_guess']:
            message = "Слишком маленькое!"
        else:
            message = "Слишком большое!"

    return render(request, 'game_app/play_game.html', {'player': player, 'message': message})
