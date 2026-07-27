from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.sessions.backends.db import SessionStore
from django.db import connection
from decimal import Decimal
from .models import Account
import logging

logger = logging.getLogger(__name__)

# Fix for A07
# @login_required
def homePageView(request):
	# VULNERABLE: Broken Access Control (A01)
	# VULNERABLE: Injection (A05)
	# VULNERABLE: Authentication Failures (A07)
	# VULNERABLE: Security Logging and Monitoring Failures (A09)
	to_username = request.GET.get('to')
	amount = request.GET.get('amount')
	from_username = request.GET.get('from', request.user.username)

	session_key = request.GET.get('session')
	if session_key and not request.user.is_authenticated:
		session_store = SessionStore(session_key=session_key)
		try:
			data = session_store.load()
		except Exception:
			data = {}

		user_id = data.get('_auth_user_id')
		if user_id:
			try:
				user = User.objects.get(pk=user_id)
			except User.DoesNotExist:
				user = None
			if user:
				auth_login(request, user)

	if not request.user.is_authenticated:
		return redirect('login')

	search = request.GET.get('search')
	if search:
		# Fix for A05.
		""" query = "SELECT id, username FROM auth_user WHERE username LIKE %s;"
		with connection.cursor() as cursor:
			cursor.execute(query, [f"%{search}%"]) """
		query = f"SELECT id, username FROM auth_user WHERE username LIKE '%{search}%';"
		with connection.cursor() as cursor:
			cursor.execute(query)
			users = [{'id': row[0], 'username': row[1]} for row in cursor.fetchall()]
	else:
		users = []

	if to_username and amount:
		amount = Decimal(amount)
		if amount < 0:
			# Fix for A09
			# logger.warning(f"Negative transfer: user={request.user.username} requested negative amount={amount} from={from_username} to={to_username}")
			return redirect('home')
		from_user = get_object_or_404(User, username=from_username)
		to_user = get_object_or_404(User, username=to_username)

		from_account = get_object_or_404(Account, user=from_user)
		to_account = get_object_or_404(Account, user=to_user)


		# Fix for A01.
		""" if request.user != from_user:
			return redirect('home')"""
		from_account.balance -= amount
		to_account.balance += amount
		from_account.save()
		to_account.save()

		# Fix for A09
		# logger.info(f"Transfer executed: user={request.user.username} moved amount={amount} from={from_username} to={to_username}")

		return redirect('home')

	accounts = Account.objects.exclude(user=request.user)
	return render(request, 'index.html', {'accounts': accounts, 'users': users})


