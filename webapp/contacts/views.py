from django.shortcuts import render, redirect
from api.crm import User, get_all_users


def index(request):
    return render(request, 'contacts/index.html', {'users': get_all_users()})


def add_contact(request):
    if request.method == 'POST':
        user = User(
            first_name = request.POST.get("first_name"), 
            last_name = request.POST.get("last_name"), 
            phone_number = request.POST.get("phone_number"), 
            address = request.POST.get("address")
        )
        user.save()
        return redirect('index')


def delete_contact(request, user_id):
    if request.method == 'POST':
        print("TRY TO DELETE : ", user_id)
        user_db = User.DB.get(doc_id=user_id)
        if user_db :
            user = User(**user_db, doc_id=user_db.doc_id)
            user.delete()
        return redirect('index')