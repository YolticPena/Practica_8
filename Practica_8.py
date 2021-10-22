#!/bin/bash python
import os
import tkinter
from tkinter import *
from functools import partial
from tkinter.ttk import Combobox, Entry,Button
from tkinter import messagebox as mb
import json

# import tkinter as tk



def main():
    LARGEFONT = ("Verdana", 35)

    class tkinterApp(Tk):
        def __init__(self, *args, **kwargs):
            Tk.__init__(self, *args, **kwargs)
            container = Frame(self)
            container.pack(side="top", fill="both", expand=True)
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)
            menubar = Menu(self)
            self['menu'] = menubar
            file_menu = Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Register", menu=file_menu)
            get_user = Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Consult", menu=get_user)
            file_menu.add_command(label="New", command=partial(self.change_frame, Registro))
            get_user.add_command(label="Consult", command=partial(self.change_frame, Consulta))
            self.frames = {}
            for F in (Registro, Consulta, Blank):
                frame = F(container, self)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            self.change_frame(Blank)

        def change_frame(self, cont):
            frame = self.frames[cont]
            frame.tkraise()

    # first window frame startpage

    class Registro(Frame):
        from os import path

        def __init__(self, parent, controller):
            Frame.__init__(self, parent)
            label = Label(self, text="Startpage", font=LARGEFONT)
            self.DicCategory = {"Infantil": 50, "Aficionado": 150, "Avanzados": 200, "Libre": 100}
            self.elements1()

        def elements1(self):
            self.name = StringVar()
            self.sexo = IntVar()
            self.LName = StringVar()
            self.Address = StringVar()
            self.CURP = StringVar()
            self.SchoolName = StringVar()
            self.costo = None
            self.SEXO =None

            self.NameLabel = Label(self, text="*Nombre:")
            self.NameLabel.place(x=10, y=10)
            self.NameEntry = Entry(self, width=13, textvariable=self.name)
            self.NameEntry.place(x=130, y=10)

            self.LnameLabel = Label(self, text="*Apellido:")
            self.LnameLabel.place(x=10, y=40)
            self.LNameEntry = Entry(self, width=13, textvariable=self.LName)
            self.LNameEntry.place(x=130, y=40)

            self.Sex = Label(self, text="Sexo:")
            self.Sex.place(x=250, y=10)
            self.rF = Radiobutton(self, text="Femenino", value=1, variable=self.sexo)
            self.rM = Radiobutton(self, text="Masculino", value=2, variable=self.sexo)
            self.rF.place(x=290, y=10)
            self.rM.place(x=290, y=40)

            self.AddressLabel = Label(self, text="Direccion:")
            self.AddressLabel.place(x=10, y=70)
            self.AddressEntry = Entry(self, width=13, textvariable=self.Address)
            self.AddressEntry.place(x=130, y=70)

            self.CURPLabel = Label(self, text="*CURP:")
            self.CURPLabel.place(x=10, y=100)
            self.CURPEntry = Entry(self, width=13, textvariable=self.CURP)
            self.CURPEntry.place(x=130, y=100)

            self.NameSchoolLabel = Label(self, text="Nombre Escuela:")
            self.NameSchoolLabel.place(x=10, y=130)
            self.NameSchoolEntry = Entry(self, width=13, textvariable=self.SchoolName)
            self.NameSchoolEntry.place(x=130, y=130)

            self.CategoryLabel = Label(self, text="*Categoria:")
            self.CategoryLabel.place(x=250, y=70)
            self.ValCategory = Combobox(self, width=10)
            self.ValCategory['state'] = 'readonly'
            vals = self.DicCategory.keys()
            self.ValCategory['values'] = list(vals)
            self.ValCategory.place(x=320, y=70)
            self.ValCategory.bind('<<ComboboxSelected>>', self.UpdatePrice)

            self.CostoPerCategoryLabel = Label(self, text="Costo:")
            self.CostoPerCategoryLabel.place(x=250, y=100)
            self.CostoPerCategoryPrice = Label(self, width=5, text="$")
            self.CostoPerCategoryPrice.place(x=320, y=100)

            self.btnRegister = Button(self, text="Registrar", command=self.CheckForm)
            self.btnRegister.place(x=130, y=170)

        def UpdatePrice(self, event):
            self.costo = self.DicCategory[self.ValCategory.get()]
            self.CostoPerCategoryPrice['text'] = "$" + str(self.costo)

        def CheckForm(self):
            data = []
            if self.CURP.get() == '' or self.LName.get() == "" or self.name == "" or self.ValCategory.get() == "":
                mensaje = mb.showinfo("Cuidado","Llenar los campos con (*)")
            else:
                if self.sexo.get() == 1:
                    self.SEXO = "Mujer"
                elif self.sexo.get() == 2:
                    self.SEXO = "Hombre"
                else:
                    self.SEXO = "Rarito"
                data.append({"CURP":self.CURP.get(), "Nombre":self.name.get(), "Apellido":self.LName.get(), "Costo":self.costo, "Categoria":self.ValCategory.get(), "Sexo":self.SEXO, "Direccion":self.Address.get()})
                with open("registro.json", "r+") as file:
                    dato = json.load(file)
                    dato["Registro"].append(data)
                    file.seek(0)
                    json.dump(dato, file, indent=4, separators=(',', ': '))


    # second window frame page1
    class Consulta(Frame):
        def __init__(self, parent, controller):
            Frame.__init__(self, parent)
            self.DicCategory = {"Infantil": 50, "Aficionado": 150, "Avanzados": 200, "Libre": 100}
            self.elements2()

        def elements2(self):
            self.rvname = StringVar()
            self.rvCURP = StringVar()
            self.rvSex = IntVar()
            self.Option = IntVar()


            self.LRegistrados = Listbox(self, selectmode=tkinter.BROWSE)
            self.LRegistrados.place(x=340, y=10)
            self.LRegistrados.bind('<<ListboxSelect>>', self.ShowInfo)
            self.FName = Label(self, text="Filtrar:")
            self.FName.place(x=10, y=10)

            self.rSexo = Radiobutton(self, text="Sexo", value=1, variable=self.Option, command=self.ChangeStatus)
            self.rSexo.place(x=50, y=40)
            self.rvSexM = Radiobutton(self, text="Mujer", value=1, variable=self.rvSex, state='disable')
            self.rvSexH = Radiobutton(self, text="Hombre", value=2, variable=self.rvSex, state='disable')
            self.rvSexM.place(x=160, y=40)
            self.rvSexH.place(x=240, y=40)

            self.rNombre = Radiobutton(self, text="Nombre", value=2, variable=self.Option, command=self.ChangeStatus)
            self.rNombre.place(x=50, y=70)
            self.inName = Entry(self,  width=13, textvariable=self.rvname, state="disable")
            self.inName.place(x=160, y=70)

            self.rCURP = Radiobutton(self, text="CURP", value=3, variable=self.Option, command=self.ChangeStatus)
            self.rCURP.place(x=50, y=100)
            self.inCURP = Entry(self,  width=13, textvariable=self.rvCURP, state='disable')
            self.inCURP.place(x=160, y=100)

            self.rCategory = Radiobutton(self, text="Category", value=4, variable=self.Option, command=self.ChangeStatus)
            self.rCategory.place(x=50, y=130)
            #self.inCategory
            self.inCategory = Combobox(self, width=10)
            self.inCategory['state'] = 'disable'
            vals = self.DicCategory.keys()
            self.inCategory['values'] = list(vals)
            self.inCategory.place(x=160, y=130)

            self.CajaInfo = Text(self, height=8, width=40, state='normal')
            self.CajaInfo.place(x=10, y=190)
            self.FilterBoton = Button(self, text="Filter", command=self.filter)
            self.FilterBoton.place(x=50,y=160)
            self.PutInList()

        def filter(self):
            self.CajaInfo.delete("1.0", tkinter.END)
            self.LRegistrados.delete(0,tkinter.END)
            typeIflter = self.Option.get()
            if typeIflter == 1:
                sexVal = self.rvSex.get()
                if sexVal == 1:
                    lnew = self.UpdateList('Mujer', "Sexo")
                    self.LRegistrados.insert(0, *lnew)
                    self.CajaInfo.insert(tkinter.INSERT, self.SearchJsonInfo('Mujer', "Sexo"))
                if sexVal == 2:
                    self.CajaInfo.insert(tkinter.INSERT, self.SearchJsonInfo('Hombre', "Sexo"))
                    lnew = self.UpdateList('Hombre', "Sexo")
                    self.LRegistrados.insert(0, *lnew)
            elif typeIflter == 2:
                lnew = self.UpdateList(self.inName.get(), "Nombre")
                self.LRegistrados.insert(0, *lnew)
                self.CajaInfo.insert(tkinter.INSERT, self.SearchJsonInfo(self.inName.get(), "Nombre"))
            elif typeIflter == 3:
                lnew = self.UpdateList(self.inCURP.get(), "CURP")
                self.LRegistrados.insert(0, *lnew)
                self.CajaInfo.insert(tkinter.INSERT, self.SearchJsonInfo(self.inCURP.get(), "CURP"))
            elif typeIflter == 4:
                lnew = self.UpdateList(self.inCategory.get(), "Categoria")
                self.LRegistrados.insert(0, *lnew)
                self.CajaInfo.insert(tkinter.INSERT, self.SearchJsonInfo(self.inCategory.get(), "Categoria"))

        def ShowInfo(self, event):
            self.CajaInfo.delete("1.0", tkinter.END)
            try:
                InfoSelected = self.LRegistrados.curselection()
                info = self.SearchJsonInfo(self.Listnames[InfoSelected[0]], "Nombre")
                self.CajaInfo.insert(tkinter.INSERT, info)
            except:
                KeyError("Error de seleccion")
            #self.CajaInfo.insert(tkinter.END,  self.SearchJsonInfo(InfoSelected, "Nombre"))

        def SearchJsonInfo(self, Compare, Campo):
            result = ""
            for data in self.JsonData['Registro']:
                if Compare == data[0][Campo]:
                    result = result + str("Nombre:\t\t {}\n"
                               "Apellido:\t\t {}\n"
                               "CURP:\t\t {}\n"
                               "Sexo:\t\t {}\n"
                               "Direccion:\t\t {}\n"
                               "Categoria:\t\t {}\n"
                               "Costo:\t\t {}\n".format(data[0]["Nombre"],data[0]["Apellido"],data[0]["CURP"],data[0]["Sexo"],data[0]["Direccion"],data[0]["Categoria"],data[0]["Costo"]))
            return result

        def PutInList(self):
            self.JsonData = self.JsonRegistrers()
            self.Listnames = []
            for i in self.JsonData["Registro"]:
                self.Listnames.append(i[0]["Nombre"])
            self.LRegistrados.insert(0, *self.Listnames)

        def UpdateList(self, val, campo):
            listUpdate = []
            for i in self.JsonData["Registro"]:
                if val == i[0][campo]:
                    listUpdate.append(i[0]["Nombre"])
            return listUpdate


        def JsonRegistrers(self):
            #valor = lambda  x: jsona with open("registro.json", "r+") as file: jsonRegister=json.load(file)
            with open("registro.json","r+") as file:
                jsonRegister = json.load(file)
                return jsonRegister


        def ChangeStatus(self):
            value = self.Option.get()
            if value ==1:
                self.rvSexM['state'] = "normal"
                self.rvSexH['state'] = "normal"
                self.inName['state'] = "disable"
                self.inCategory['state'] = "disable"
                self.inCURP['state'] = "disable"
            if value == 2:
                self.rvSexM['state'] = "disable"
                self.rvSexH['state'] = "disable"
                self.inName['state'] = "normal"
                self.inCategory['state'] = "disable"
                self.inCURP['state'] = "disable"
            if value == 3:
                self.rvSexM['state'] = "disable"
                self.rvSexH['state'] = "disable"
                self.inName['state'] = "disable"
                self.inCategory['state'] = "disable"
                self.inCURP['state'] = "normal"
            if value == 4:
                self.rvSexM['state'] = "disable"
                self.rvSexH['state'] = "disable"
                self.inName['state'] = "disable"
                self.inCategory['state'] = "normal"
                self.inCURP['state'] = "disable"

    class Blank(Frame):
        def __init__(self, parent, controller):
            Frame.__init__(self, parent)

    app = tkinterApp()
    app.geometry("700x500")
    app.title("Torneo")
    app.mainloop()



if __name__ == "__main__":
    main()
