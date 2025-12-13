from django.shortcuts import render, redirect
from django.contrib import messages
from api.crm import User, get_all_users


def index(request):
    return render(request, 'contacts/index.html', {'users': get_all_users()})


def add_contact(request):
    if request.method == 'POST':
        try:
            user = User(
                first_name = request.POST.get("first_name"), 
                last_name = request.POST.get("last_name"), 
                phone_number = request.POST.get("phone_number"), 
                address = request.POST.get("address")
            )
            user.save()
        except ValueError as e:
            messages.error(request, str(e))
        return redirect('index')

def modify_contact(request, user_id):
    if request.method == 'POST':
        try:
            user_db = User.DB.get(doc_id=user_id)
            if user_db :
                # Modify the existing user
                user = User(
                    first_name = request.POST.get("first_name"), 
                    last_name = request.POST.get("last_name"), 
                    phone_number = request.POST.get("phone_number"), 
                    address = request.POST.get("address"),
                    doc_id = user_db.doc_id     
                )
            else:
                # Create a new user
                user = User(
                    first_name = request.POST.get("first_name"), 
                    last_name = request.POST.get("last_name"), 
                    phone_number = request.POST.get("phone_number"), 
                    address = request.POST.get("address")
                )
            user.save()
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('index')

def delete_contact(request, user_id):
    if request.method == 'POST':
        try:
            user_db = User.DB.get(doc_id=user_id)
            if user_db :
                user = User(**user_db, doc_id=user_db.doc_id)
                user.delete()
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('index')