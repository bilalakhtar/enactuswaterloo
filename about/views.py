from django.shortcuts import render
from about.models import Person, ProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    people = Person.objects.filter(public=True, approved=True).order_by("-priority")

    return render(request, "about/index.html", {"people": people})

@login_required
def profile(request):
	if request.method != 'POST':
		initialDict = {
				'first_name': request.user.first_name,
				'last_name': request.user.last_name
			}
		try:
			initialDict += {
				'program': request.user.profile.program,
				'year': request.user.profile.year,
				'position': request.user.profile.position,
				'bio':request.user.profile.bio
			}
		except:
			pass


		profileForm = ProfileForm(initial=initialDict)
		return render(request, "about/member.html", {"profileForm": profileForm})

	# POST response to form
	if 'password' in request.POST:
		# Password changing
		if request.user.check_password(request.POST['oldpassword']):
			request.user.set_password(request.POST['password'])
		else:
			return render(request, "about/member.html", {error: "Incorrect password"})
	elif 'first_name' in request.POST:
		profileForm = ProfileForm(request.POST, request.FILES)
		if profileForm.is_valid():

			person = Person.objects.get_or_create(user=request.user)

			request.user.first_name = profileForm.cleaned_data["first_name"]
			request.user.last_name = profileForm.cleaned_data["last_name"]
			request.user.save()

			person.program 	= profileForm.cleaned_data["program"]
			person.public 	= profileForm.cleaned_data["public"]
			person.year 	= profileForm.cleaned_data["year"]
			person.position	= profileForm.cleaned_data["position"]
			person.bio 		= profileForm.cleaned_data["bio"]

			if "picture" in request.FILES:
				person.picture = request.FILES["picture"]

			person.save()
		else:
			return render(request, "about/member.html", {error: "Invalid input"})

	return HttpResponseRedirect("/about/")
