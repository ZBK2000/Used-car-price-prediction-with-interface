import tkinter
from tkinter import ttk
import numpy as np
import pandas as pd


def filter():
    """ this function makes it possible that you can not only choose, but write in the 'márka' combobox"""
    available_choices1 = []
    letters1 = var1.get()
    print(list(data[label1].value_counts().index))
    for i in list(data[label1].value_counts().index):
        n = 0
        check = True
        for b in letters1:
            try:
                if b != i[n]:
                    check = False
            except:
                check = False
            n += 1
            print(f"{n}")
        if check:
            print("yees")
            available_choices1.append(i)
    Entry1["values"] = available_choices1


def filter1():
    """ this function makes it possible that you can not only choose, but write in the 'típus' combobox"""
    available_choices = []
    letters = var2.get()
    for i in list(data[label2].value_counts().index):
        n = 0
        check = True
        for b in letters:
            try:
                if b != i[n]:
                    check = False
            except:
                check = False
            n += 1
        if check:
            available_choices.append(i)
    Entry2["values"] = available_choices


def take_inputs():
    """ This function does the filtering, the regression and the prediction based on the users inputs"""
    global entry_list
    global data
    text = ""
    b = 0
    input_values = []
    label_values = []
    label_values_without_dummys = []

    for entry, label in entry_list:
        if entry.get():
            if Param.get():  # this parameter sets the plus-minus filtering range of the numerical values
                x = float(Param.get())
            else:
                x = 0.05
            try:  # this block takes the categorical values from the users input and filter the database accordingly
                data1 = data2[label].value_counts(normalize=True)[entry.get()]
                text += f"{str(format(float(data1) * 100, '.2f'))} percentage of the cars has the '{entry.get()}' " \
                        f"attribute\n------------------\n"
                if b == 0:
                    sliced_df = data2[data2[label] == entry.get()]
                else:
                    sliced_df = sliced_df[sliced_df[label] == entry.get()]
                input_values += ([1 if x == entry.get() else 0 for x in list(data[label].value_counts().index)])
                label_values += ([f"{label}_{x}" for x in list(data[label].value_counts().index)])
                label_values_without_dummys.append(label)

            except:  # this block takes the numerical values from the users input and filter the database accordingly
                if label == "Évjárat:": # The release year variable handled differently
                    data1 = data2[label].value_counts(normalize=True)[float(entry.get())]
                    text += f"The {str(format(float(data1) * 100, '.2f'))} percent of the cars were registered in the " \
                            f"year of {entry.get()} \n------------------\n"
                    if b == 0:
                        sliced_df = data2[data2[label] == float(entry.get())]
                    else:
                        sliced_df = sliced_df[sliced_df[label] == float(entry.get())]
                else:
                    text += f"Regarding the '{label}',  {format((data2[(data2[label] > (1 - 0.01*x) * float(entry.get())) & (data2[label] < (1 + 0.01*x) * float(entry.get()))].index.nunique()) / data2[label].index.nunique() * 100, '.2f')} " \
                            f"percent of the cars are in the {x * 100} percent range of {entry.get()}\n------------------\n"

                    if b == 0:
                        sliced_df = data2[(data2[label] > (1 - x) * float(entry.get())) & (
                                    data2[label] < (1 + x) * float(entry.get()))]
                    else:
                        sliced_df = sliced_df[(sliced_df[label] > (1 - x) * float(entry.get())) & (
                                    sliced_df[label] < (1 + x) * float(entry.get()))]
                input_values.append(float(entry.get()))
                label_values.append(label)
                label_values_without_dummys.append(label)

            b += 1
    # in this block the function splits the filtered database (only those columns included, where value was given by the
    # user) into train and test datasets and after that makes the regression only on the given variables columns
    data3 = data[label_values_without_dummys]
    data4 = pd.get_dummies(data3)
    targets = data['Vételár EUR:']
    inputs = data4
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(inputs, targets, test_size=0.2, random_state=365)
    from sklearn.linear_model import LinearRegression
    reg = LinearRegression()
    reg.fit(x_train, y_train)

    # Here the function makes a one row database with the given inputs, concatenate it with the database, which the
    # regression was made on, then makes the prediction on that line and putting it into a new database
    predicton_df = pd.DataFrame([input_values], columns=label_values)
    data5 = pd.concat([data4, predicton_df])
    predict_values = data5.iloc[-1:]
    y_hat_test = reg.predict(predict_values)
    df_pf = pd.DataFrame(np.exp(y_hat_test), columns=['Prediction'])
    from sklearn.metrics import explained_variance_score
    predicted_values = reg.predict(x_test)
    r_squared = explained_variance_score(y_test, predicted_values)

    # In this block the texts was defined which are going to appear on the interface ( based on the results)
    tkinter.Label(mainWindow, text=text, background="grey", fg="black").grid(row=1, column=2, rowspan=2, sticky="wesn")
    tkinter.Label(mainWindow, font=20,
                  text=f'-------------------\nThis car would cost {str(format(df_pf["Prediction"][0], ".2f"))} Euro, '
                       f'estimated with multiple linear regression, which has a R_squared (explaining power) of {format(r_squared, ".2f")}\n-------------------',
                  background="grey", fg="black").grid(row=1, column=3, sticky="wesn")
    tkinter.Label(mainWindow, font=20,
                  text=f'-------------------\n There are {str(sliced_df.index.nunique())} similar cars on the hungarian used car market\n-------------------',
                  background="grey", fg="black").grid(row=2, column=3, sticky="wesn")
    tkinter.Label(mainWindow, font=20,
                  text=f'-------------------\n{str(format(np.exp(sliced_df["Vételár EUR:"].mean()), ".2f"))} Euro is the average price of the similar cars on the used car market\n-------------------',
                  background="grey", fg="black").grid(row=3, column=3, sticky="wesn")


# _____________________________________ pandas stuff __________________________________________________
# In this block data was cleaned regarding unneceseary spaces, letters and making datatypes right
data = pd.read_csv('jarmuvek1.csv')
data.drop(list(data.loc[data["Évjárat:"] == "Évjárat:"].index), inplace=True)
data["Vételár:"].replace(["\xa0", "Ft"], "", regex=True, inplace=True)
data["Vételár EUR:"].replace(["\xa0", "€"], "", regex=True, inplace=True)
data["Kilométeróra állása:"].replace(["\xa0", "km"], "", regex=True, inplace=True)
data["Hengerűrtartalom:"].replace(["\xa0", "cm³"], "", regex=True, inplace=True)
data["Szállítható szem. száma:"].replace(["\xa0", "fő"], "", regex=True, inplace=True)
data["Teljesítmény:"].replace(["kW", "LE"], "", regex=True, inplace=True)
data["Csomagtartó:"].replace(["\xa0", "liter"], "", regex=True, inplace=True)
data["Teljes tömeg:"].replace(["\xa0", "kg"], "", regex=True, inplace=True)
data["Vételár:"] = pd.to_numeric(data["Vételár:"], errors="coerce")
data["Vételár EUR:"] = pd.to_numeric(data["Vételár EUR:"], errors="coerce")
data["Kilométeróra állása:"] = pd.to_numeric(data["Kilométeróra állása:"], errors="coerce")
data["Hengerűrtartalom:"] = pd.to_numeric(data["Hengerűrtartalom:"], errors="coerce")
data["Szállítható szem. száma:"] = pd.to_numeric(data["Szállítható szem. száma:"], errors="coerce")
data["Ajtók száma:"] = pd.to_numeric(data["Ajtók száma:"], errors="coerce")
data["Csomagtartó:"] = pd.to_numeric(data["Csomagtartó:"], errors="coerce")
data["Teljes tömeg:"] = pd.to_numeric(data["Teljes tömeg:"], errors="coerce")
data["Évjárat:"] = data["Évjárat:"].str.split("/").str[0]
data["Évjárat:"] = pd.to_numeric(data["Évjárat:"], errors="coerce")
data["Műszaki vizsga érvényes:"] = data["Műszaki vizsga érvényes:"].str.split("/").str[0]
data["Műszaki vizsga érvényes:"] = pd.to_numeric(data["Műszaki vizsga érvényes:"], errors="coerce")
data["Teljesítmény:"] = data["Teljesítmény:"].str.split(",").str[1]
data["Teljesítmény:"] = pd.to_numeric(data["Teljesítmény:"], errors="coerce")
data["Sebességváltó fajtája:"] = data["Sebességváltó fajtája:"].apply(
    lambda x: "automata" if "automata" in str(x).lower() else ("manuális" if "manuális" in str(x).lower() else "egyéb"))

# The sale price column may have been scraped wrongly, all value missing, so dropping the column, also dropping the price column in Forint, because working with the Euro price
data.drop(["Akciós ár:","Vételár:"], axis=1, inplace=True)
# transforming the price variable with logarithms, because it was heavily right skewed
log_price = np.log(data['Vételár EUR:'])
data['Vételár EUR:'] = log_price

#making a copy from the database before dropping the missing values, because, for some i need that for showing interesting facts
data2 = data.copy()
#dropping all the missing values
data.dropna(inplace=True)

# _______________________________ tkinter stuff _________________________________________________________
mainWindow = tkinter.Tk()
mainWindow.geometry("1920x1040")
mainWindow.title("Used car price prediction")
mainWindow.configure(background="grey")

mainWindow.columnconfigure(0, weight=1)
mainWindow.columnconfigure(1, weight=1)
mainWindow.columnconfigure(2, weight=1)
mainWindow.columnconfigure(3, weight=1)
mainWindow.columnconfigure(4, weight=1)
mainWindow.columnconfigure(5, weight=1)

mainWindow.rowconfigure(0, weight=1)
mainWindow.rowconfigure(1, weight=1)
mainWindow.rowconfigure(2, weight=1)
mainWindow.rowconfigure(3, weight=1)
mainWindow.rowconfigure(4, weight=1)
mainWindow.rowconfigure(5, weight=1)
mainWindow.rowconfigure(6, weight=1)
column_list = ['Állapot:', 'Kivitel:', 'Üzemanyag:', 'Sebességváltó fajtája:', 'Okmányok jellege:', 'Szín:', 'Hajtás:',
               'Klíma fajtája:',
               'márka', 'típus', 'Évjárat:', 'Hengerűrtartalom:', 'Műszaki vizsga érvényes:', 'Teljesítmény:',
               'Teljes tömeg:',
               'Ajtók száma:', 'Szállítható szem. száma:',
               'Kilométeróra állása:', 'Csomagtartó:'
               ]

tkinter.Label(mainWindow, text='***Predicting the price of your used car***', font=("Courier", 20),
              background="grey").grid(row=0, column=2, columnspan=2)
i = 0
a = 0
label_frame = tkinter.Frame(mainWindow, background="grey", relief="sunken", borderwidt=1)
label_frame.grid(row=4, column=1, sticky="nsew", columnspan=4)
entry_list = []
for label in column_list: ## putting entries or comboboxes of the explaining variables into the interface
    if label == "márka":
        var1 = tkinter.StringVar(mainWindow)
        Entry1 = ttk.Combobox(label_frame, textvariable=var1, values=[""] + list(data[label].value_counts().index))
        Entry1.bind('<KeyRelease>', lambda x: filter())
        Entry1.grid(row=0, column=i, sticky="nsew")
        tkinter.Label(label_frame, text=label, font=12, background="grey", fg="black").grid(row=1, column=i,
                                                                                            sticky="wesn")
        label1 = label
        entry_list.append((var1, label))

    elif label == "típus":
        var2 = tkinter.StringVar(mainWindow)
        Entry2 = ttk.Combobox(label_frame, textvariable=var2, values=[""] + list(data[label].value_counts().index))
        Entry2.grid(row=0, column=i, sticky="nsew")
        Entry2.bind('<KeyRelease>', lambda x: filter1())
        tkinter.Label(label_frame, text=label, font=12, background="grey", fg="black").grid(row=1, column=i,
                                                                                            sticky="wesn")
        label2 = label
        entry_list.append((var2, label))

    elif data[label].dtype == "O":
        if i < 10:
            var = tkinter.StringVar(mainWindow)
            Entry = ttk.Combobox(label_frame, textvariable=var, values=[""] + list(data[label].value_counts().index),
                                 state="readonly")
            Entry.grid(row=0, column=i, sticky="nsew")
            tkinter.Label(label_frame, font=12, text=label, background="grey", fg="black").grid(row=1, column=i,
                                                                                                sticky="wesn")
        else:
            var = tkinter.StringVar(mainWindow)
            Entry = ttk.Combobox(label_frame, textvariable=var, values=[""] + list(data[label].value_counts().index),
                                 state="readonly")
            Entry.grid(row=2, column=a, sticky="nsew")
            tkinter.Label(label_frame, text=label, font=12, background="grey", fg="black").grid(row=3, column=a,
                                                                                                sticky="wesn")
            a += 1
        entry_list.append((var, label))

    else:
        if i < 10:
            Entry = tkinter.Entry(label_frame, background="grey")
            Entry.grid(row=0, column=i, sticky="nsew")
            tkinter.Label(label_frame, font=12, text=label, background="grey", fg="black").grid(row=1, column=i,
                                                                                                sticky="wesn")
        else:
            Entry = tkinter.Entry(label_frame, background="grey")
            Entry.grid(row=2, column=a, sticky="nsew")
            tkinter.Label(label_frame, font=12, text=label, background="grey", fg="black").grid(row=3, column=a,
                                                                                                sticky="wesn")
            a += 1
        entry_list.append((Entry, label))
    i += 1
## making an entry for the hyperparameter for changing filtering range
Paramframe = tkinter.Frame(mainWindow, background="grey")
Paramframe.grid(row=2, column=0)
Param = tkinter.Entry(Paramframe, background="grey")
Param.grid(row=1, column=0)
Paramlabel = tkinter.Label(Paramframe,
                           text="You can set a hyperparameter, which sets the plus-minus percent range of the numerical values, when filtering",
                           wraplength=150, background="grey", fg="black")
Paramlabel.grid(row=0, column=0)
# Making the button which calls the take_inputs function
tkinter.Button(mainWindow, background="grey", font=30, text="predict", command=take_inputs).grid(row=6, column=2, columnspan=2,
                                                                                        sticky="wesn")
#additional important notes
tkinter.Label(mainWindow, text="****\n Notes:\n - Currently working with a 2022.03.26 hungarian used car database"
                               "\n - the EUR/FT exchange rate was 374\n - you can also filter by writing in at the "
                               "'márka' and 'típus' attribute, but you have to do it uppercase\n - The explaining power was"
                               " optimized for writing in all the attributums and was tested on a test database, so it"
                               " can show strange results when doing the regression with only a few attribute\n - the"
                               " units of measure are: hoursepower, Km, kg, per head, Liter, cm^3\n "
                               "- defining 'similar': categorical details filtered by exact match, numerical ones based on the"
                               " hyperparameter (by default 5 percent range)\n ****", wraplength=200,background="grey", fg="black").grid(row=1, column=0)


mainWindow.mainloop()
