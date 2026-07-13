from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Account


@login_required
def homePageView(request):
	# VULNERABLE: Broken Access Control (A01)
	# VULNERABLE: Mishandling of Exceptional Conditions (A10)
	to_username = request.GET.get('to')
	amount = request.GET.get('amount')
	from_username = request.GET.get('from', request.user.username)

	if to_username and amount:
		amount = Decimal(amount)
		from_user = get_object_or_404(User, username=from_username)
		to_user = get_object_or_404(User, username=to_username)

		from_account = get_object_or_404(Account, user=from_user)
		to_account = get_object_or_404(Account, user=to_user)

		""" if request.user != from_user:
			return """ # This could maybe include an error 	screen. A10 vulnerability like this.
		from_account.balance -= amount
		to_account.balance += amount
		from_account.save()
		to_account.save()

		return redirect('home')

	accounts = Account.objects.exclude(user=request.user)
	return render(request, 'index.html', {'accounts': accounts})

