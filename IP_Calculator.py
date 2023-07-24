# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 16:27:09 2023

@author: boyem
"""

from tkinter import *
import math
import ipaddress
import logging
import os

# Supprimer le fichier de journalisation s'il existe
if os.path.exists("app.log"):
    os.remove("app.log")


logging.basicConfig(filename="app.log",level=logging.DEBUG,filemode="w")

# Création de la fenêtre
window = Tk()

window.geometry("700x500")
window.title("IP-Calculator")
window.configure(background="#27b181")
window.resizable(height=False,width=False)
window.iconbitmap("lego.ico")

logging.debug("Fenêtre créé avec succés")


# Fonction pour calculer les adresses réseau
def CalculHostBits(X):
    necessary_host_bits=(math.log10(X+2)/math.log10(2))
    if isinstance(necessary_host_bits, float):
        return int(necessary_host_bits+1)
    return necessary_host_bits 

    
def Calcul_IP(subnet,ip_adress,host_numbers):
    
    ip_adress = ip_adress.get()
    subnet = subnet.get()
    host_numbers=host_numbers.get()
    
    sortie="" # variable pour stocker le résultat
    
    if host_numbers:
        host_numbers=[int(el) for el in host_numbers.split(",")]
    
        # Tri décroissant de host_numbers:
        
        host_numbers.sort(reverse=True)
    
    remaining_host_bits=32-subnet
    i=1
    for number in host_numbers:
     

        necessary_host_bits=CalculHostBits(number)   
        if necessary_host_bits > remaining_host_bits:
            logging.error("Le masque est trop grand pour le nombre d'hôtes spécifiés")
            break
        else:
            subnet=32-necessary_host_bits
        
        ip_adress=str(ip_adress)+"/"+str(subnet)
        sortie=sortie+f"Pour le réseau {i} avec {number} hôtes: ,{ip_adress}"+"\n"
        
        try:
            reseau=ipaddress.IPv4Network(ip_adress,strict=True)
            
            ip_adress=reseau.broadcast_address+1
            i+=1
        except Exception as e:
            logging.error(e)
       
        
    outpout.delete(1.0, END)  # Effacer le contenu existant de la zone de texte
    outpout.insert(END, sortie)
    
    

# Création du GUI

ip_adress = StringVar()
subnet = IntVar()
host_numbers = StringVar()


title = Label(window, text="Calculateur d'adresses réseau en fonction du nombres d'hôtes:", font=("Verdana",10,"underline italic"),bg="black",fg="white")                                            
title.pack(side=TOP, pady=30)

#
network_entry = Entry(window, textvariable=ip_adress)
network_entry.place(x=130,y=100)
label1= Label(window, text="Entrez l'adresse réseau: ").place(y=100)


subnet_entry = Entry(window,textvariable=subnet)
subnet_entry.place(x=460,y=100)
label2= Label(window, text="Entrez le masque (CIDR): ").place(y=100,x=320)

host_entry= Entry(window, textvariable=host_numbers)
host_entry.place(y=200,x=300)
label3= Label(window, text="Entrez les nombres d'hôtes séparés par des virgules ").place(y=200,x=0)

frame= Frame(window,bd=1,width=300,height=250)
frame.place(x=300,y=240)


outpout = Text(frame,bg="grey")
outpout.pack()


valid = Button(window, text="Calculer",bg="black",font=("verdana",15),fg="white",command=lambda:Calcul_IP(subnet, ip_adress,host_numbers))
valid.place(x=100,y=350)



window.mainloop()