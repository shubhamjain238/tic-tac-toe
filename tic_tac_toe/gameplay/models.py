from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class GameQuerySet(models.QuerySet):
    def games_for_user(self, user):
        return self.filter(Q(first_user = user) | Q(second_user = user))

    def active(self):
        return self.filter(Q(status='F') | Q(status='S'))


status_choices = [
    ('F', 'First Player to move'),
    ('S', 'Second Player to move'),
    ('W', 'First Player Won'),
    ('L', 'Second Player Won'),
    ('D', 'Draw')
]


class Game(models.Model):
    first_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='first_user')
    second_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='second_user')
    start_time = models.DateTimeField(auto_now_add=True)
    active_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default='F', choices=status_choices)
    objects = GameQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('game_detail', args=[self.id])

    def is_user_move(self, user):
        return (user==self.first_user and self.status=='F') or (user==self.second_user and self.status=='S')


    def board(self):
        board = [[None for i in range(3)] for j in range(3)]
        for move in self.move_set.all():
            board[move.x][move.y] = move
        return board

    def new_move(self):
        if self.status not in 'FS':
            raise ValueError('Cannot make move in Completed move')
        new_move = Move(game = self, by_first_user = self.status=='F')
        return new_move


    def update_after_move(self, move):
        self.status = self._get_status_after_move(move)

    def _get_status_after_move(self, move):
        x, y = move.x, move.y
        board = self.board()
        if (board[x][0] == board[x][1] == board[x][2]) or (board[0][y] == board[1][y] == board[2][y]) \
                (board[0][0] == board[0][1] == board[0][2]) or (board[0][2] == board[1][1] == board[2][0]):
            return 'W' if move.by_first_user else 'L'
        if self.move_set.count()>=9:
            return 'D'
        return 'S' if self.status == 'F' else 'F'


    def __str__(self):
        return f'{self.first_user} vs {self.second_user}'


class Move(models.Model):
    x = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)])
    y = models.IntegerField()
    comments = models.CharField(max_length = 100, blank = True)
    by_first_user = models.BooleanField(editable=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __eq__(self, other):
        if other is None:
            return False
        return other.by_first_user == self.by_first_user

    def save(self, *args, **kwargs):
        super(Move, self).save(*args, **kwargs)
        self.game.update_after_move(self)
        self.game.save()