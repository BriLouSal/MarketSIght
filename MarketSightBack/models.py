from django.db import models
from django.utils import timezone

import yfinance as yf  # (currently unused, but keeping since you may use it later)
import time            # (same here)

MAX_LENGTH_OF_TITLE = 255

MAX_CASH = 100000
# This should be the most important part of determining relevancy
# as it should carry more weigh
ACTIVITY_PARAMETERS = 1.25

DURATION_DECAY = 0.5

DEFAULT_VOTE = 0


class Profile(models.Model):
    username = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
    # We want to have money for the Users to simulate stock trading. We'll do it in Model
    # to remain dynamic and not remain static in views.
    money_owned = models.IntegerField(default=MAX_CASH)

    def __str__(self):
        return self.username


class Chat(models.Model):
    title = models.CharField(max_length=MAX_LENGTH_OF_TITLE)
    body = models.TextField()

    created_at = models.DateField(default=timezone.now)

    upvotes = models.IntegerField(default=DEFAULT_VOTE)
    downvotes = models.IntegerField(default=DEFAULT_VOTE)
    replies_count = models.IntegerField(default=DEFAULT_VOTE)
    # We need to convert self_created_at into integer in order to make my algorithim to work

    # This algorithim will ensure the relevancy is accurate
    def relevancy_algo(self):
        time_now = timezone.now()
        time_delta = time_now - self.created_at
        time_decay = time_delta.total_seconds() / 86400  # days
        return (
            (self.upvotes - self.downvotes)
            + (self.replies_count * ACTIVITY_PARAMETERS)
            + (time_decay * DURATION_DECAY)
        )


# User's owner of that Portfolio
# Requirements: Name and the Ticker of the Stock. The Book Cost, and the Total Return of that stock. 
#
# Important Database: Owner of the Portfolio and the name of it, and it was created
#
# Control System for StockOrder and StockPosition
class Portfolio(models.Model):
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="portfolios",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StockOrder(models.Model):

    # Let Buy = 0
    # Let sell = 1

    class OrderChoice(models.TextChoices):
        BUY = "BUY"
        SELL = "SELL"

    # This will show if the trade was executed or it has been rejected.
    class Status(models.TextChoices):
        PENDING = "PENDING"   # Pending Order (Able to cancel the Order)
        SUBMITTED = "SUBMITTED"  # The stock bought has been submitted
        FILLED = "FILLED"     # Order has been filled and the stock is in the Portfolio
        CANCELED = "CANCELED" # Canceled pending order
        REJECTED = "REJECTED" # Not enough capital to buy the stock

    # What relevant database do I want for Stockorder: Ticker Name, Book Cost, Percentage of the portfolio,
    # the quantity of the stock owned, etc. And their Order status
    user_portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="stock_orders",
    )

    ticker = models.CharField(max_length=10)

    # Consider Partial Ownership of the stock
    quantity = models.DecimalField(max_digits=10, decimal_places=4)

    order_choice = models.CharField(
        max_length=4,
        choices=OrderChoice.choices,
        default=OrderChoice.BUY,
    )

    price_bought = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def __str__(self):
        return f"{self.order_choice} {self.quantity} {self.ticker}"


class StockPosition(models.Model):
    user_portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="stock_positions",
    )

    ticker = models.CharField(max_length=10)

    quantity = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    book_cost = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    def __str__(self):
        return f"{self.ticker} - {self.quantity}"
