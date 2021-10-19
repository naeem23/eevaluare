import math, random
import hashlib
from django.contrib.auth import authenticate, login, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils import http
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import UpdateView

User = get_user_model()
from . import forms
from . import models



# ============================================================================
# =============================== Sing in view ===============================
# ============================================================================
class SigninView(View):
	template_name = 'authentication/login.html'
	form_class = forms.SigninForm
	msg = None

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {'form': self.form_class, 'msg': self.msg})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None and (user.verified or user.is_superuser):
				login(request, user)
				return redirect('/')
			else:
				self.msg = 'Invalid credentials'
		else:
			self.msg = 'Error validating the form'

		return render(request, self.template_name, {'form': form, 'msg': self.msg})



# ============================================================================
# =============================== Sing Up view ===============================
# ============================================================================
class SignupView(View):
	msg = None 
	template_name = 'authentication/register.html'
	form_class = forms.SignupForm

	def get(self, request, *args, **kwargs):
		data = {
			'form': self.form_class,
			'msg': self.msg,
		}
		return render(request, self.template_name, data)

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save()
			otp = generateOTP()
			hashed_otp = hash_OTP(otp, user.id)
			subject = 'Verify you new Evaluari account'
			text_content = f'Your security code {otp}. To authenticate, please use this One Time Password (OTP).'
			email_type = 'Verify Evaluari account'
			to_email = user.email
			send_email(subject, text_content, otp, email_type, to_email)
			return redirect('authentication:signup_verify', hashed_otp=hashed_otp)
		else:
			self.msg = 'Whoops! Something went wrong.'

		data = {
			'form': form,
			'msg': self.msg,
		}

		return render(request, self.template_name, data)



# ============================================================================
# ============================== otp generation ==============================
# ============================================================================
def generateOTP():
	otp = []
	for i in range(2):
		otp.append(str(random.randint(0,9)))
		otp.append(chr(random.randint(65,90)))
		otp.append(chr(random.randint(97,122)))

	verification_code = "".join(otp)
	return verification_code



# ============================================================================
# ========================== account verification ============================
# ============================================================================
def signup_verify(request, hashed_otp):
	if request.session.get('resend_msg'):
		resend_msg = 'A new code has been sent to your email.'
		try:
			del request.session['resend_msg']
		except KeyError:
			pass
	else:
		resend_msg = None
	msg = None
	page = 'signup'
	form = forms.OTPForm()	
	if request.method == 'POST':
		form = forms.OTPForm(request.POST)
		if form.is_valid():
			otp = form.cleaned_data.get('otp')
			check, uid = check_otp(hashed_otp, otp)
			user_id = force_text(http.urlsafe_base64_decode(uid))
			user = get_object_or_404(User, id=user_id)
			if check:
				user.verified = True 
				user.save()
				login(request, user)
				return redirect('/')
			else:
				msg = 'We failed to verify your email. Please try again.'

	context = {
		'form': form,
		'page': page,
		'msg': msg,
		'resend_msg': resend_msg,
		'hashed_otp': hashed_otp,
	}
	return render(request, 'authentication/verify_email.html', context)



# ============================================================================
# ============================== agent list view =============================
# ============================================================================
@login_required(login_url='/signin/')
def agent_list(request):
	if request.session.get('success'):
		msg = 'deleted'
		try:
			del request.session['success']
		except KeyError:
			pass
	elif request.session.get('failed'):
		msg = 'not_deleted'
		try:
			del request.session['failed']
		except KeyError:
			pass
	elif request.session.get('added'):
		msg = 'added'
		try:
			del request.session['added']
		except KeyError:
			pass
	elif request.session.get('not_added'):
		msg = 'not_added'
		try:
			del request.session['not_added']
		except KeyError:
			pass
	else:
		msg = None

	agents = User.objects.filter(is_inspector=False).order_by('-id')
	context = {
		'agents': agents, 'msg':msg, 'segment': 'settings'
	}
	return render(request, 'authentication/agent_list.html', context) 



# ============================================================================
# ============================== agent add view ==============================
# ============================================================================
@login_required(login_url='/signin/')
def add_agent(request):
	template_name = 'authentication/add_agent.html'
	msg = None
	form = forms.AgentCreationForm(request.POST or None)

	if request.method == "POST":
		if form.is_valid():
			user = form.save(commit=False)
			user.verified = True
			user.save()
			request.session['added'] = True
			return redirect('authentication:agents')
		else:
			msg = 'Whoops! Something went wrong'

	context = {
		'form': form,
		'msg': msg
	}
	return render(request, template_name, context)



# ============================================================================
# ============= agent details, update and password chagne view ===============
# ============================================================================
@login_required(login_url='/signin/')
def agent_detail(request, id):
	agent = get_object_or_404(User, id=id)
	template_name = 'authentication/agent_detail.html'
	msg = None
	if request.session.get('update'):
		update = 'success'
		try:
			del request.session['update']
		except KeyError:
			pass
	elif request.session.get('update_fail'):
		update = 'failed'
		try:
			del request.session['update_fail']
		except KeyError:
			pass
	else:
		update = None

	tab_name = None 

	if request.method == 'POST':
		details_form = forms.AgentUpdateForm(request.POST or None, instance=agent)
		password_form = forms.AgentPasswordChangeForm(agent, request.POST)
		
		if request.POST.get('form_value') == 'details_form':
			if details_form.is_valid():
				details_form.save()
				request.session['update'] = True
				return redirect('authentication:agent_details', id=id)
			else:
				msg = 'Whoops! Something went wrong.'
				request.session['udpate_fail'] = True
				tab_name = 'details'

		if request.POST.get('form_value') == 'password_form':
			if password_form.is_valid():
				user = password_form.save()
				update_session_auth_hash(request, user)
				return redirect('authentication:agent_details', id=id)
			else:
				msg = 'Whoops! Something went wrong.'
				tab_name = 'password'

	else:
		details_form = forms.AgentUpdateForm(instance=agent)
		password_form = forms.AgentPasswordChangeForm(agent)

	context = {
		'agent': agent,
		'form': details_form,
		'password_form': password_form,
		'msg': msg,
		'update': update,
		'tab_name': tab_name,
	}
	return render(request, template_name, context)



# ============================================================================
# ============================= agent delete view ============================
# ============================================================================
@login_required(login_url="/signin/")
def delete_agent(request, id):
	try:
		agent = get_object_or_404(User, id=id)
		response = agent.delete()
		if response:
			request.session['success'] = True
		else: 
			request.session['failed'] = True
	except:
		request.session['failed'] = True

	return redirect('authentication:agents')



# ============================================================================
# =========================== forget password view ===========================
# ============================================================================
def forget_password(request):
	if request.method == 'POST':
		form = forms.ForgetPassword(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			user = User.objects.get(email__iexact=email)
			otp = generateOTP()
			hashed_otp = hash_OTP(otp, user.id)
			subject = 'Evaluari password reset assistance'
			text_content = f'Your security code {otp}. To authenticate, please use this One Time Password (OTP).'
			email_type = 'Password reset assistance'
			send_email(subject, text_content, otp, email_type, email)
			return redirect('authentication:verify_email', hashed_otp=hashed_otp)
	else:
		form = forms.ForgetPassword()
	return render(request, "authentication/forget_password.html", {'form': form})



# ============================================================================
# ============================= generate hashed otp ==========================
# ============================================================================
def hash_OTP(otp, id):
	uid = http.urlsafe_base64_encode(force_bytes(id))
	return hashlib.sha1(uid.encode()+otp.encode()).hexdigest() + ':' + uid



# ============================================================================
# ============================== otp verification ============================
# ============================================================================
def check_otp(hashed_otp, user_otp):
	otp, uid = hashed_otp.split(':')
	check = otp == hashlib.sha1(uid.encode()+user_otp.encode()).hexdigest()
	return check, uid



# ============================================================================
# ================== password reset email verification =======================
# ============================================================================
def verify_resetpass_email(request, hashed_otp):
	if request.session.get('resend_msg'):
		resend_msg = 'A new code has been sent to your email.'
		try:
			del request.session['resend_msg']
		except KeyError:
			pass
	else:
		resend_msg = None
	msg = None
	page='reset'
	form = forms.OTPForm()

	if request.method == 'POST':
		form = forms.OTPForm(request.POST)
		if form.is_valid():
			otp = form.cleaned_data.get('otp')
			check, uid = check_otp(hashed_otp, otp)
			if check:
				return redirect('authentication:reset_new', hashed_otp=hashed_otp)
			else:
				msg = 'We failed to verify your email. Please try again.'
	
	context = {
		'form': form,
		'page': page,
		'msg': msg,
		'resend_msg': resend_msg,
		'hashed_otp': hashed_otp,
	}
	return render(request, 'authentication/verify_email.html', context)



# ============================================================================
# ========================== reset new password view =========================
# ============================================================================
def reset_new_pass(request, hashed_otp):
	otp, uid = hashed_otp.split(':')
	uid = force_text(http.urlsafe_base64_decode(uid))
	user = User.objects.get(id=uid)

	if request.method == 'POST':
		form = forms.ResetNewPass(user, request.POST)
		if form.is_valid():
			form.save()
			return redirect('authentication:reset_success')
	else:
		form = forms.ResetNewPass(user)
	return render(request, 'authentication/reset_new_pass.html', {'form': form})



# ============================================================================
# ======================= password reset success view ========================
# ============================================================================
def reset_success(request):
	return render(request, 'authentication/reset_success.html')



# ============================================================================
# =============================== resend otp view ============================
# ============================================================================
def resend_code(request, hashed_otp):
	otp, uid = hashed_otp.split(':')
	uid = force_text(http.urlsafe_base64_decode(uid))
	user = get_object_or_404(User, id=uid)
	otp = generateOTP()
	hashed_otp = hash_OTP(otp, user.id)
	request.session['resend_msg'] = True
	htmlgen = f'<p>Your OTP is <strong>{otp}</strong></p>'
	send_mail('OTP request',otp,'send@email.com',[user.email], fail_silently=False, html_message=htmlgen)
	if request.GET.get('page') == 'signup':
		return redirect('authentication:signup_verify', hashed_otp=hashed_otp)
	else:
		return redirect('authentication:verify_email', hashed_otp=hashed_otp)



# ============================================================================
# =============================== send email =================================
# ============================================================================
def send_email(subject, text_content, otp, email_type, to_email):
    from_email = 'Evaluari <info@evaluari.co.uk>'
    htmly = get_template('authentication/verify_email_template.html')
    context = {
        'email_type': email_type,
        'otp': otp,
    }
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



@login_required(login_url='/signin/')
def inspectors_list(request):
	template_name = 'authentication/inspectors_list.html'

	if request.session.get('success'):
		msg = 'deleted'
		try:
			del request.session['success']
		except KeyError:
			pass
	elif request.session.get('failed'):
		msg = 'not_deleted'
		try:
			del request.session['failed']
		except KeyError:
			pass
	elif request.session.get('added'):
		msg = 'added'
		try:
			del request.session['added']
		except KeyError:
			pass
	elif request.session.get('not_added'):
		msg = 'not_added'
		try:
			del request.session['not_added']
		except KeyError:
			pass
	else:
		msg = None

	inspectors = User.objects.filter(is_inspector=True).order_by('-id')
	context = {
		'inspectors': inspectors, 
		'segment': 'settings'
	}
	return render(request, template_name, context)



@login_required(login_url='/signin/')
def add_inspector(request):
	template_name = 'authentication/add_inspector.html'
	msg = None
	if request.method == "POST":
		form = forms.AddInspectorForm(request.POST, request.FILES)
		if form.is_valid():
			user = form.save(commit=False)
			user.verified = True
			user.is_inspector = True
			user.save()
			request.session['added'] = True
			return redirect('authentication:inspectors')
		else:
			msg = 'Whoops! Something went wrong'
	else:
		form = forms.AddInspectorForm()
	context = {
		'form': form,
		'msg': msg
	}
	return render(request, template_name, context)


	 
@login_required(login_url='/signin/')
def inspector_details(request, id):
	inspector = get_object_or_404(User, id=id, is_inspector=True)
	template_name = 'authentication/inspector_detail.html'
	msg = None
	if request.session.get('update'):
		update = 'success'
		try:
			del request.session['update']
		except KeyError:
			pass
	elif request.session.get('update_fail'):
		update = 'failed'
		try:
			del request.session['update_fail']
		except KeyError:
			pass
	else:
		update = None

	tab_name = None 

	if request.method == 'POST':
		details_form = forms.InspectorUpdateForm(request.POST, request.FILES, instance=inspector)
		password_form = forms.AgentPasswordChangeForm(inspector, request.POST)
		
		if request.POST.get('form_value') == 'details_form':
			if details_form.is_valid():
				details_form.save()
				request.session['update'] = True
				return redirect('authentication:inspector_details', id=id)
			else:
				msg = 'Whoops! Something went wrong.'
				request.session['udpate_fail'] = True
				tab_name = 'details'

		if request.POST.get('form_value') == 'password_form':
			if password_form.is_valid():
				user = password_form.save()
				update_session_auth_hash(request, user)
				return redirect('authentication:inspector_details', id=id)
			else:
				msg = 'Whoops! Something went wrong.'
				tab_name = 'password'

	else:
		details_form = forms.InspectorUpdateForm(instance=inspector)
		password_form = forms.AgentPasswordChangeForm(inspector)

	context = {
		'inspector': inspector,
		'form': details_form,
		'password_form': password_form,
		'msg': msg,
		'update': update,
		'tab_name': tab_name,
	}
	return render(request, template_name, context)


from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt
@login_required(login_url='/signin/')
def change_picture(request):
	if request.method == 'POST':
		file = request.FILES.get('file')
		inspector = get_object_or_404(User, id=request.POST.get('id'))
		inspector.profile_picture = file 
		try:
			inspector.save()
			response = True 
		except: 
			response = False 
		if response:
			return JsonResponse({'success': 'true'})
	return JsonResponse({'success': "false"})