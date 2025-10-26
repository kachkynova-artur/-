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
    
    # Пытаемся найти последнюю незавершённую игру
    result = GameResult.objects.filter(player=player, success=False).order_by('-date').first()
    
    # Если такой игры нет, создаём новую
    if not result:
        result = GameResult.objects.create(
            player=player,
            number_to_guess=random.randint(1, 100),
            attempts=0,
            success=False
        )
    
    feedback = ""
    
    if request.method == "POST":
        guess = int(request.POST['guess'])
        result.attempts += 1
        
        if guess == result.number_to_guess:
            feedback = "Угадал(а)!"
            result.success = True
        elif guess < result.number_to_guess:
            feedback = "Больше!"
        else:
            feedback = "Меньше!"
        
        result.save()
    
    context = {
        'player': player,
        'feedback': feedback,
        'attempts': result.attempts
    }
    return render(request, 'game_app/play_game.html', context)
