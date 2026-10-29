import customtkinter as ctk
import requests
from PIL import Image
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Currency Converter")
app.geometry("700x800")

currencies = {
"India – Indian Rupee (INR)": "INR",
"United States – US Dollar (USD)": "USD",
"United Kingdom – Pound Sterling (GBP)": "GBP",
"European Union – Euro (EUR)": "EUR",
"Japan – Japanese Yen (JPY)": "JPY",
"China – Chinese Yuan (CNY)": "CNY",
"Australia – Australian Dollar (AUD)": "AUD",
"Canada – Canadian Dollar (CAD)": "CAD",
"Switzerland – Swiss Franc (CHF)": "CHF",
"Singapore – Singapore Dollar (SGD)": "SGD",
"United Arab Emirates – UAE Dirham (AED)": "AED",
"Saudi Arabia – Saudi Riyal (SAR)": "SAR",
"Pakistan – Pakistani Rupee (PKR)": "PKR",
"Bangladesh – Bangladeshi Taka (BDT)": "BDT",
"Nepal – Nepalese Rupee (NPR)": "NPR",
"Sri Lanka – Sri Lankan Rupee (LKR)": "LKR",
"South Korea – Korean Won (KRW)": "KRW",
"Thailand – Thai Baht (THB)": "THB",
"Malaysia – Malaysian Ringgit (MYR)": "MYR",
"Indonesia – Indonesian Rupiah (IDR)": "IDR",
"Philippines – Philippine Peso (PHP)": "PHP",
"Vietnam – Vietnamese Dong (VND)": "VND"
}

currency_names = list(currencies.keys())
all_currencies = currency_names.copy()

# 🔍 SEARCH FUNCTION
def filter_currency(event=None):
    typed = from_box.get().lower()

    filtered = [c for c in all_currencies if typed in c.lower()]

    if filtered:
        from_box.configure(values=filtered)
    else:
        from_box.configure(values=all_currencies)

# FLAG
def get_flag(code):
    flag_map = {"INR":"in","USD":"us","GBP":"gb","JPY":"jp","EUR":"eu"}
    if not os.path.exists("flags"):
        os.makedirs("flags")

    country = flag_map.get(code)
    if not country:
        return None

    path = f"flags/{country}.png"

    if not os.path.exists(path):
        try:
            url = f"https://flagcdn.com/w80/{country}.png"
            img = requests.get(url).content
            open(path,"wb").write(img)
        except:
            return None

    img = Image.open(path).resize((50,30))
    return ctk.CTkImage(light_image=img, dark_image=img)

# FEE
def calculate_fee(result):
    fee = result * 0.02
    return fee, result - fee

# THEME
def change_theme(mode):
    if mode == "Dark":
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")

# CONVERT
def convert():
    try:
        amount = float(amount_entry.get())
    except:
        result_label.configure(text="Enter valid number")
        return

    from_code = currencies[from_box.get()]
    to_code = currencies[to_box.get()]

    data = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_code}").json()

    rate = data["rates"][to_code]
    result = amount * rate

    result_label.configure(text=f"{amount} {from_code} = {result:.2f} {to_code}", font=("Arial",28,"bold"))
    rate_label.configure(text=f"1 {from_code} = {rate:.2f} {to_code}", font=("Arial",16,"bold"))

    fee, final = calculate_fee(result)
    fee_label.configure(text=f"Fee: {fee:.2f} | Final: {final:.2f} {to_code}", font=("Arial",16,"bold"))

    f1 = get_flag(from_code)
    f2 = get_flag(to_code)

    if f1 and f2:
        flag_frame.pack(pady=10)
        flag1.configure(image=f1)
        flag2.configure(image=f2)

# SWAP
def swap():
    a = from_box.get()
    b = to_box.get()
    from_box.set(b)
    to_box.set(a)
    convert()

# CALCULATOR
def press(x):
    amount_entry.insert("end", str(x))

def equal():
    try:
        value = eval(amount_entry.get())
        amount_entry.delete(0,"end")
        amount_entry.insert(0,value)
    except:
        amount_entry.delete(0,"end")
        amount_entry.insert(0,"Error")

def clear():
    amount_entry.delete(0,"end")

# UI
title = ctk.CTkLabel(app, text="Currency Converter", font=("Arial",30))
title.pack(pady=20)

amount_entry = ctk.CTkEntry(app, placeholder_text="Enter Amount", width=300)
amount_entry.pack(pady=10)

from_box = ctk.CTkComboBox(app, values=currency_names, width=350)
from_box.set(currency_names[0])
from_box.pack(pady=5)
from_box.bind("<KeyRelease>", filter_currency)  # 🔥 search enabled

to_box = ctk.CTkComboBox(app, values=currency_names, width=350)
to_box.set(currency_names[1])
to_box.pack(pady=5)

theme = ctk.CTkComboBox(app, values=["Dark","Light"], command=change_theme)
theme.set("Dark")
theme.pack(pady=10)

result_label = ctk.CTkLabel(app, text="")
result_label.pack(pady=10)

rate_label = ctk.CTkLabel(app, text="")
rate_label.pack()

fee_label = ctk.CTkLabel(app, text="")
fee_label.pack(pady=5)

flag_frame = ctk.CTkFrame(app)
flag_frame.pack_forget()

flag1 = ctk.CTkLabel(flag_frame, text="")
flag1.grid(row=0,column=0,padx=40)

flag2 = ctk.CTkLabel(flag_frame, text="")
flag2.grid(row=0,column=1,padx=40)

frame = ctk.CTkFrame(app)
frame.pack(pady=20)

buttons = [
["7","8","9"],
["4","5","6"],
["1","2","3"],
["C","0","="]
]

for i,row in enumerate(buttons):
    for j,val in enumerate(row):

        if val == "C":
            cmd = clear
        elif val == "=":
            cmd = equal
        else:
            cmd = lambda v=val: press(v)

        ctk.CTkButton(frame,text=val,width=60,command=cmd)\
            .grid(row=i,column=j,padx=5,pady=5)

ctk.CTkButton(app,text="Convert",command=convert).pack(pady=10)
ctk.CTkButton(app,text="Swap",command=swap).pack(pady=5)

app.mainloop()