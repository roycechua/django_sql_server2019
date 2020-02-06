from django.shortcuts import render, redirect
from django.db import connection
# Create your views here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def index(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM accounts")
        rows = dictfetchall(cursor)

    return render(request, template_name="app1/index.html", context={"records":rows})

def register(request):
    if request.method == "GET":
        return render(request, template_name="app1/registration.html", context={})
    elif request.method == "POST":
        id = int(request.POST.get("account_id"))
        name = request.POST.get("name")
        email = request.POST.get("email")

        # code to save to database
        with connection.cursor() as cursor:
            params = (id, name, email)
            cursor.execute("{CALL usp_insert_to_accounts (%s,%s,%s)}", params)

        return redirect("/")

def update(request, id):
    if request.method == "GET":
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM accounts WHERE id=%s",[id])
            record = dictfetchall(cursor)[0]
        print(record)
        return render(request, template_name="app1/update.html", context={"record":record})
    elif request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        # code to save to database
        with connection.cursor() as cursor:
            cursor.execute("UPDATE accounts SET name=%s, email=%s WHERE id=%s",[name, email,id])

        return redirect("/")

def delete(request, id):
    with connection.cursor() as cursor:
            params = (id,)
            cursor.execute("{CALL usp_delete_from_account (%s)}", params)
    return redirect("/")        