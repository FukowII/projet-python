import customtkinter as ctk
import sqlite3
import tkinter as tk
import tkinter.messagebox as messagebox
import re
from tkinter import ttk

class Contact:
    def __init__(self, nom, prenom, email, telephone):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone


class CarnetAdresses:
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cursor = self.conn.cursor()
        self.creer_table_contacts() 

    def creer_table_contacts(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                prenom TEXT,
                email TEXT,
                telephone TEXT
            )
        ''')
        self.conn.commit()

    def ajouter_contact(self, contact):
        self.cursor.execute('''
            INSERT INTO contacts (nom, prenom, email, telephone)
            VALUES (?, ?, ?, ?)
        ''', (contact.nom, contact.prenom, contact.email, contact.telephone))
        self.conn.commit()

    def rechercher_contact_par_nom(self, nom):
        self.cursor.execute('SELECT * FROM contacts WHERE nom LIKE ?', ('%' + nom + '%',))
        return self.cursor.fetchall()

    def rechercher_contact_par_id(self, id_contact):
        self.cursor.execute('SELECT * FROM contacts WHERE id = ?', (id_contact,))
        return self.cursor.fetchall()

    def rechercher_perso(self, nom, prenom, telephone, email):
        self.cursor.execute('''
            SELECT * FROM contacts
            WHERE nom LIKE ? AND prenom LIKE ? AND telephone LIKE ? AND email LIKE ?
        ''', ('%' + nom + '%', '%' + prenom + '%', '%' + telephone + '%', '%' + email + '%'))
        return self.cursor.fetchall()

    def modifier_contact(self, id_contact, nouveau_nom, nouveau_prenom, nouveau_email, nouveau_telephone):
        self.cursor.execute('''
            UPDATE contacts
            SET nom=?, prenom=?, email=?, telephone=?
            WHERE id=?
        ''', (nouveau_nom, nouveau_prenom, nouveau_email, nouveau_telephone, id_contact))
        self.conn.commit()

    def supprimer_contact(self, id_contact):
        self.cursor.execute('DELETE FROM contacts WHERE id=?', (id_contact,))
        self.conn.commit()

class Carnet_adresses(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Carnet d'adresses")
        self.geometry("800x600")

        self.frame_principal = ctk.CTkFrame(self, corner_radius=10)
        self.frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(self.frame_principal, text="Nom :").grid(row=0, column=0, pady=10, padx=10)
        self.nom_entry = ctk.CTkEntry(self.frame_principal)
        self.nom_entry.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(self.frame_principal, text="Prénom :").grid(row=1, column=0, pady=10, padx=10)
        self.prenom_entry = ctk.CTkEntry(self.frame_principal)
        self.prenom_entry.grid(row=1, column=1, pady=10, padx=10)

        ctk.CTkLabel(self.frame_principal, text="Email :").grid(row=2, column=0, pady=10, padx=10)
        self.email_entry = ctk.CTkEntry(self.frame_principal)
        self.email_entry.grid(row=2, column=1, pady=10, padx=10)

        ctk.CTkLabel(self.frame_principal, text="Téléphone :").grid(row=3, column=0, pady=10, padx=10)
        self.telephone_entry = ctk.CTkEntry(self.frame_principal)
        self.telephone_entry.grid(row=3, column=1, pady=10, padx=10)

        self.ajouter_button = ctk.CTkButton(self.frame_principal, text="Ajouter", fg_color="#0000ff", hover_color="#00008b", command=self.ajouter_contact)
        self.ajouter_button.grid(row=4, column=0, pady=10, padx=10)

        self.rechercher_multi_critere_button = ctk.CTkButton(self.frame_principal, text="Rechercher par critères", fg_color="#0000ff", hover_color="#00008b", command=self.rechercher_perso)
        self.rechercher_multi_critere_button.grid(row=0, column=2, rowspan=4, pady=10, padx=10)

        self.rechercher_button = ctk.CTkButton(self.frame_principal, text="Rechercher", fg_color="#0000ff", hover_color="#00008b", command=self.rechercher_contact)
        self.rechercher_button.grid(row=5, column=2, pady=10, padx=10)

        self.supprimer_button = ctk.CTkButton(self.frame_principal, text="Supprimer", fg_color="#0000ff", hover_color="#00008b", command=lambda: self.supprimer_contact())
        self.supprimer_button.grid(row=4, column=1, pady=10, padx=10)

        self.effacer_button = ctk.CTkButton(self.frame_principal, text="Effacer", fg_color="#0000ff", hover_color="#00008b", command=self.effacer_champs)
        self.effacer_button.grid(row=4, column=3, pady=10, padx=10)

        self.modifier_button = ctk.CTkButton(self.frame_principal, text="Modifier", fg_color="#0000ff", hover_color="#00008b", command=self.modifier_contact)
        self.modifier_button.grid(row=4, column=2, pady=10, padx=10)

        ctk.CTkLabel(self.frame_principal, text="ID du Contact :").grid(row=5, column=0, pady=10, padx=10)
        self.id_contact_entry = ctk.CTkEntry(self.frame_principal)
        self.id_contact_entry.grid(row=5, column=1, pady=10, padx=10)

        self.resultats_frame = ctk.CTkFrame(self.frame_principal, corner_radius=10)
        self.resultats_frame.grid(row=6, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")

        self.carnet = CarnetAdresses()
        self.contact_actuel = None  

        self.afficher_tous_button = ctk.CTkButton(self.frame_principal, text="Afficher tous les contacts", fg_color="#0000ff", hover_color="#00008b", command=self.afficher_tous)
        self.afficher_tous_button.grid(row=7, column=0, columnspan=4, pady=10, padx=10)

        style = ttk.Style()

    
        style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"), foreground="blue")  

        
        self.resultats_treeview = ttk.Treeview(
            self.resultats_frame,
            columns=("ID", "Nom", "Prénom", "Email", "Téléphone"),
            show='headings',
            style="Custom.Treeview"  
        )
        self.resultats_treeview.pack(fill="both", expand=True)

        
        for col in self.resultats_treeview["columns"]:
            self.resultats_treeview.heading(col, text=col, anchor="center", command=lambda c=col: self.trier_treeview(self.resultats_treeview, c, False))
            self.resultats_treeview.column(col, width=100, anchor="center")

        style.configure("Custom.Treeview", font=("arial", 12))  

        
        self.resultats_treeview.config(style="Custom.Treeview")
        self.resultats_treeview["padding"] = 5

    def ajouter_contact(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        email = self.email_entry.get()
        telephone = self.telephone_entry.get()

        if not all([nom, prenom, email, telephone]):
            messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs")
            return

        if not self.valider_email(email):
            messagebox.showwarning("Avertissement", "Adresse e-mail non valide")
            return

        if not self.valider_numero_telephone(telephone):
            messagebox.showwarning("Avertissement", "Numéro de téléphone non valide")
            return

        telephone_formate = ' '.join([telephone[i:i+2] for i in range(0, len(telephone), 2)])

        contact = Contact(nom, prenom, email, telephone_formate)
        self.carnet.ajouter_contact(contact)
        messagebox.showinfo("Succès", "Contact ajouté avec succès")
        self.rechercher_contact()  

    def valider_numero_telephone(self, numero_telephone):
        pattern = r"^\d{10}$"  
        return bool(re.match(pattern, numero_telephone))

    def valider_email(self, email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, email))
    

    def rechercher_contact(self):
        id_contact = self.id_contact_entry.get()
        if id_contact:
            try:
                id_contact = int(id_contact)
                contact = self.carnet.rechercher_contact_par_id(id_contact)
                self.resultats_treeview.delete(*self.resultats_treeview.get_children())  # Effacez les anciens résultats
                if contact:
                    self.resultats_treeview.insert("", tk.END, values=contact[0])
                else:
                    messagebox.showwarning("Avertissement", "ID du contact introuvable")
            except:
                messagebox.showwarning("Avertissement","L'ID doit être un nombre entier.")


    def rechercher_perso(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        telephone = self.telephone_entry.get()
        email = self.email_entry.get()
        
        contacts = self.carnet.rechercher_perso(nom, prenom, telephone, email)
        
        for row in self.resultats_treeview.get_children():
            self.resultats_treeview.delete(row)

        for contact in contacts:
            self.resultats_treeview.insert("", tk.END, values=contact)

    def afficher_tous(self):
        contacts = self.carnet.rechercher_contact_par_nom('')
        self.resultats_treeview.delete(*self.resultats_treeview.get_children())
        for contact in contacts:
            self.resultats_treeview.insert("", tk.END, values=contact)

    def modifier_contact(self):
        id_contact = self.id_contact_entry.get()
        nouveau_nom = self.nom_entry.get()
        nouveau_prenom = self.prenom_entry.get()
        nouveau_email = self.email_entry.get()
        nouveau_telephone = self.telephone_entry.get()

        if id_contact:
            try:
                id_contact = int(id_contact)
                contact_existant = self.carnet.rechercher_contact_par_id(id_contact)

                if contact_existant:
                    if self.contact_actuel is None:
                        self.contact_actuel = {
                            'id': id_contact,
                            'nom': contact_existant[0][1],
                            'prenom': contact_existant[0][2],
                            'email': contact_existant[0][3],
                            'telephone': contact_existant[0][4]
                        }

                        self.nom_entry.delete(0, tk.END)
                        self.nom_entry.insert(0, self.contact_actuel['nom'])
                        self.prenom_entry.delete(0, tk.END)
                        self.prenom_entry.insert(0, self.contact_actuel['prenom'])
                        self.email_entry.delete(0, tk.END)
                        self.email_entry.insert(0, self.contact_actuel['email'])
                        self.telephone_entry.delete(0, tk.END)
                        self.telephone_entry.insert(0, self.contact_actuel['telephone'])
                    else:
                        self.carnet.modifier_contact(
                            self.contact_actuel['id'],
                            nouveau_nom,
                            nouveau_prenom,
                            nouveau_email,
                            nouveau_telephone
                        )
                        messagebox.showinfo("Succès", "Contact modifié avec succès")
                        self.contact_actuel = None  
                        self.rechercher_contact() 
                else:
                    messagebox.showwarning("Avertissement", "ID du contact introuvable")
            except:
               messagebox.showwarning("Avertissement","L'ID doit être un nombre entier.")


    def supprimer_contact(self):
        id_contact = self.id_contact_entry.get()
        if id_contact:
            try:
                id_contact = int(id_contact)
                contact_existant = self.carnet.rechercher_contact_par_id(id_contact)
                if contact_existant:
                    confirmation = messagebox.askyesno("Confirmation de suppression", "Êtes-vous sûr de vouloir supprimer ce contact?")
                    if confirmation:
                        self.carnet.supprimer_contact(id_contact)
                        messagebox.showinfo("Succès", "Contact supprimé avec succès")
                else:
                    messagebox.showwarning("Avertissement", "ID du contact introuvable")
            except ValueError:
                messagebox.showwarning("Avertissement", "L'ID doit être un nombre entier.")
        else:
            messagebox.showwarning("Avertissement", "Veuillez entrer un ID du contact à supprimer.")


    def trier_treeview(self, tv, col, reverse):
        
        liste = [(tv.set(k, col), k) for k in tv.get_children('')] # données colonne 
       
        liste.sort(reverse=reverse)

        
        for index, (val, k) in enumerate(liste):
            tv.move(k, '', index)

        
        tv.heading(col, command=lambda: self.trier_treeview(tv, col, not reverse))

    def effacer_champs(self):
        self.nom_entry.delete(0, tk.END)
        self.prenom_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telephone_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = Carnet_adresses()
    app.mainloop()
