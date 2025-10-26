
from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class GameResult(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    number_to_guess = models.IntegerField()
    attempts = models.IntegerField()
    success = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.name} - {'Win' if self.success else 'Lose'} - {self.date}"
