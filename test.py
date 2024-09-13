from opperations import login

a = login("admin", "password")
date, name, email, quote = a[0], a[1], a[2], a[3]
print(f"Name: {name}\nEmail: {email}\nDate: {date}\nQuote: {quote}")