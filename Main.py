import customtkinter as ctk
import sqlite3
import tkinter as tk
import tkinter.messagebox as messagebox
from ttkthemes import ThemedStyle



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

    def rechercher_contact_par_multi_critere(self, nom, prenom, telephone, email):
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


class CarnetAdressesUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Carnet d'adresses")
        self.geometry("800x600")

        self.frame_principal = ctk.CTkFrame(self, corner_radius=10)
        self.frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(self.frame_principal, text="Nom :").grid(row=0, column=0, pady=10, padx=10)
        ctk.CTkLabel(self.frame_principal, text="Prénom :").grid(row=1, column=0, pady=10, padx=10)
        ctk.CTkLabel(self.frame_principal, text="Email :").grid(row=2, column=0, pady=10, padx=10)
        ctk.CTkLabel(self.frame_principal, text="Téléphone :").grid(row=3, column=0, pady=10, padx=10)

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

        self.rechercher_multi_critere_button = ctk.CTkButton(self.frame_principal, text="Rechercher par critères", fg_color="#0000ff", hover_color="#00008b", command=self.rechercher_contact_par_multi_critere)
        self.rechercher_multi_critere_button.grid(row=0, column=2, rowspan=4, pady=10, padx=10)

        self.rechercher_button = ctk.CTkButton(self.frame_principal, text="Rechercher", fg_color="#0000ff", hover_color="#00008b", command=self.rechercher_contact)
        self.rechercher_button.grid(row=4, column=1, pady=10, padx=10)

        self.supprimer_button = ctk.CTkButton(self.frame_principal, text="Supprimer", fg_color="#0000ff", hover_color="#00008b", command=lambda: self.supprimer_contact())
        self.supprimer_button.grid(row=4, column=2, pady=10, padx=10)

        self.effacer_button = ctk.CTkButton(self.frame_principal, text="Effacer", fg_color="#0000ff", hover_color="#00008b", command=self.effacer_champs)
        self.effacer_button.grid(row=4, column=4, pady=10, padx=10)

        self.modifier_button = ctk.CTkButton(self.frame_principal, text="Modifier", fg_color="#0000ff", hover_color="#00008b", command=self.modifier_contact)
        self.modifier_button.grid(row=4, column=3, pady=10, padx=10)

        ctk.CTkLabel(self.frame_principal, text="ID du Contact :").grid(row=5, column=0, pady=10, padx=10)
        self.id_contact_entry = ctk.CTkEntry(self.frame_principal)
        self.id_contact_entry.grid(row=5, column=1, pady=10, padx=10)

        self.resultats_frame = ctk.CTkFrame(self.frame_principal, corner_radius=10)
        self.resultats_frame.grid(row=6, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")

        self.resultats_listbox = tk.Listbox(self.resultats_frame)
        self.resultats_listbox.pack(fill="both", expand=True)

        self.carnet = CarnetAdresses()
        self.contact_actuel = None  # Variable pour stocker les données du contact actuellement sélectionné

        self.afficher_tous_button = ctk.CTkButton(self.frame_principal, text="Afficher tous les contacts", fg_color="#0000ff", hover_color="#00008b", command=self.afficher_tous_les_contacts)
        self.afficher_tous_button.grid(row=7, column=0, columnspan=4, pady=10, padx=10)

    def effacer_champs(self):
        self.nom_entry.delete(0, tk.END)
        self.prenom_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telephone_entry.delete(0, tk.END)

    def ajouter_contact(self):
        contact = Contact(self.nom_entry.get(), self.prenom_entry.get(), self.email_entry.get(), self.telephone_entry.get())
        self.carnet.ajouter_contact(contact)
        messagebox.showinfo("Succès", "Contact ajouté avec succès")
        self.rechercher_contact()  # Actualiser la liste des contacts

    def rechercher_contact(self):
        id_contact = self.id_contact_entry.get()
        if id_contact:
            try:
                id_contact = int(id_contact)
                contact = self.carnet.rechercher_contact_par_id(id_contact)
                self.resultats_listbox.delete(0, tk.END)
                if contact:
                    self.resultats_listbox.insert(tk.END, f"ID: {contact[0][0]}, Nom: {contact[0][1]}, Prénom: {contact[0][2]}, Email: {contact[0][3]}, Téléphone: {contact[0][4]}")
                else:
                    messagebox.showwarning("Avertissement", "ID du contact introuvable")
            except ValueError:
                print("L'ID doit être un nombre entier.")

    def rechercher_contact_par_multi_critere(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        telephone = self.telephone_entry.get()
        email = self.email_entry.get()
        contacts = self.carnet.rechercher_contact_par_multi_critere(nom, prenom, telephone, email)
        self.resultats_listbox.delete(0, tk.END)
        for contact in contacts:
            self.resultats_listbox.insert(tk.END, f"ID: {contact[0]}, Nom: {contact[1]}, Prénom: {contact[2]}, Email: {contact[3]}, Téléphone: {contact[4]}")

    def afficher_tous_les_contacts(self):
        contacts = self.carnet.rechercher_contact_par_nom('')
        self.resultats_listbox.delete(0, tk.END)
        for contact in contacts:
            self.resultats_listbox.insert(tk.END, f"ID: {contact[0]}, Nom: {contact[1]}, Prénom: {contact[2]}, Email: {contact[3]}, Téléphone: {contact[4]}")

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
                        # Si c'est la première pression sur "Modifier", conservez les données du contact
                        self.contact_actuel = {
                            'id': id_contact,
                            'nom': contact_existant[0][1],
                            'prenom': contact_existant[0][2],
                            'email': contact_existant[0][3],
                            'telephone': contact_existant[0][4]
                        }

                        # Remplissez les champs avec les données du contact actuel
                        self.nom_entry.delete(0, tk.END)
                        self.nom_entry.insert(0, self.contact_actuel['nom'])
                        self.prenom_entry.delete(0, tk.END)
                        self.prenom_entry.insert(0, self.contact_actuel['prenom'])
                        self.email_entry.delete(0, tk.END)
                        self.email_entry.insert(0, self.contact_actuel['email'])
                        self.telephone_entry.delete(0, tk.END)
                        self.telephone_entry.insert(0, self.contact_actuel['telephone'])
                    else:
                        # Si c'est la deuxième pression sur "Modifier", mettez à jour les données du contact
                        self.carnet.modifier_contact(
                            self.contact_actuel['id'],
                            nouveau_nom,
                            nouveau_prenom,
                            nouveau_email,
                            nouveau_telephone
                        )
                        messagebox.showinfo("Succès", "Contact modifié avec succès")
                        self.contact_actuel = None  # Réinitialisez les données du contact actuel
                        self.rechercher_contact()  # Actualiser la liste des contacts
                else:
                    messagebox.showwarning("Avertissement", "ID du contact introuvable")
            except ValueError:
                print("L'ID doit être un nombre entier.")

#eazohezazl
if __name__ == "__main__":
    app = CarnetAdressesUI()
    app.mainloop()
