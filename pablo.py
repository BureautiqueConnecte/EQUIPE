 tkinter as tk
from tkinter import messagebox, ttk
import cx_Oracle
from tkinter import font as tkfont

# Connexion à la base de données Oracle
def get_db_connection():
    return cx_Oracle.connect(user='Pablo', password='Pablo', dsn='localhost:1521/XE')

class UserManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des utilisateurs")
        self.root.geometry("400x300")
        self.root.configure(bg="#f5f5f5")
        
        self.custom_font = tkfont.Font(family="Helvetica", size=12)
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()

        header_frame = tk.Frame(self.root, bg="#009688", padx=10, pady=10)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="Gestion des utilisateurs", bg="#009688", fg="#ffffff", font=("Helvetica", 18)).pack(pady=10)

        button_frame = tk.Frame(self.root, bg="#f5f5f5", pady=20)
        button_frame.pack(expand=True, fill=tk.BOTH)

        button_style = {'bg': "#009688", 'fg': "#ffffff", 'font': self.custom_font, 'width': 20, 'height': 2, 'relief': 'flat'}
        button_hover_style = {'bg': "#00796B", 'fg': "#ffffff"}

        tk.Button(button_frame, text="Afficher les utilisateurs", command=self.show_display_page, **button_style).pack(pady=10)
        tk.Button(button_frame, text="Créer un utilisateur", command=self.show_create_page, **button_style).pack(pady=10)
        tk.Button(button_frame, text="Modifier un utilisateur", command=self.show_update_page, **button_style).pack(pady=10)
        tk.Button(button_frame, text="Supprimer un utilisateur", command=self.show_delete_page, **button_style).pack(pady=10)
        tk.Button(button_frame, text="Rechercher un utilisateur", command=self.show_search_page, **button_style).pack(pady=10)

        # Bind hover effects
        for button in button_frame.winfo_children():
            button.bind("<Enter>", lambda e, b=button: b.config(**button_hover_style))
            button.bind("<Leave>", lambda e, b=button: b.config(**button_style))

    def show_create_page(self):
        CreateUserWindow(self.root)

    def show_display_page(self):
        DisplayUsersWindow(self.root)

    def show_update_page(self):
        UpdateUserWindow(self.root)

    def show_delete_page(self):
        DeleteUserWindow(self.root)

    def show_search_page(self):
        SearchUserWindow(self.root)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class CreateUserWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Créer un utilisateur")
        self.geometry("350x250")
        self.configure(bg="#f5f5f5")
        self.custom_font = tkfont.Font(family="Helvetica", size=12)
        self.create_widgets()

    def create_widgets(self):
        form_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        form_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(form_frame, text="Nom:", bg="#f5f5f5", fg="#333333", font=self.custom_font).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_name = tk.Entry(form_frame, bg="#ffffff", font=self.custom_font, bd=2, relief='groove')
        self.entry_name.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Email:", bg="#f5f5f5", fg="#333333", font=self.custom_font).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_email = tk.Entry(form_frame, bg="#ffffff", font=self.custom_font, bd=2, relief='groove')
        self.entry_email.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        button_frame = tk.Frame(self, bg="#f5f5f5")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Créer", command=self.create_user, bg="#009688", fg="#ffffff", font=self.custom_font, width=15, relief='flat').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Retour", command=self.destroy, bg="#e64a19", fg="#ffffff", font=self.custom_font, width=15, relief='flat').pack(side=tk.RIGHT, padx=5)

    def create_user(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Utilisateur (name, email) VALUES (:name, :email)", {'name': name, 'email': email})
            connection.commit()
            messagebox.showinfo("Succès", "Utilisateur créé avec succès!")
            self.entry_name.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Erreur de base de données", str(e))
        finally:
            cursor.close()
            connection.close()

class DisplayUsersWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Afficher les utilisateurs")
        self.geometry("450x350")
        self.configure(bg="#f5f5f5")
        self.custom_font = tkfont.Font(family="Helvetica", size=12)
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("Name", "Email"), show='headings', style="Treeview")
        self.tree.heading("Name", text="Nom")
        self.tree.heading("Email", text="Email")
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        style = ttk.Style()
        style.configure("Treeview", background="#ffffff", foreground="#000000", font=self.custom_font, rowheight=30)
        style.configure("Treeview.Heading", background="#009688", foreground="#ffffff", font=self.custom_font)

        button_frame = tk.Frame(self, bg="#f5f5f5")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Rafraîchir", command=self.load_users, bg="#009688", fg="#ffffff", font=self.custom_font, width=15, relief='flat').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Retour", command=self.destroy, bg="#e64a19", fg="#ffffff", font=self.custom_font, width=15, relief='flat').pack(side=tk.RIGHT, padx=5)

        self.load_users()

    def load_users(self):
        self.tree.delete(*self.tree.get_children())
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT name, email FROM Utilisateur")
            users = cursor.fetchall()
            for user in users:
                self.tree.insert("", tk.END, values=user)
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Erreur de base de données", str(e))
        finally:
            cursor.close()
            connection.close()

class UpdateUserWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Modifier un utilisateur")
        self.geometry("350x300")
        self.configure(bg="#f5f5f5")
        self.custom_font = tkfont.Font(family="Helvetica", size=12)
        self.create_widgets()

    def create_widgets(self):
        form_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        form_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(form_frame, text="Nom d'utilisateur:", bg="#f5f5f5", fg="#333333", font=self.custom_font).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_username = tk.Entry(form_frame, bg="#ffffff", font=self.custom_font, bd=2, relief='groove')
        self.entry_username.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Nouveau nom:", bg="#f5f5f5", fg="#333333", font=self.custom_font).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_new_name = tk.Entry(form_frame, bg="#ffffff", font=self.custom_font, bd=2, relief='groove')
        self.entry_new_name.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Nouvel email:", bg="#f5f5f5", fg="#333333", font=self.custom_font).grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_new_email = tk.Entry(form_frame, bg="#ffffff", font=self.custom_font, bd=2, relief='groove')
        self.entry_new_email.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        button_frame = tk.Frame(self, bg="#f5f5f5")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Modifier", command=self.confirm_update_user, bg="#009688", fg="#ffffff", font=self.custom_font, width=15, relief='flat').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Retour", command=self.destroy, bg="#e64a19", fg="#ffffff", font=self.custom_font, width=15, relief='flat').pack(side=tk.RIGHT, padx=5)

    def confirm_update_user(self):
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir modifier cet utilisateur ?"):
            self.update_user()

    def update_user(self):
        username = self.entry_username.get()
        new_name = self.entry_new_name.get()
        new_email = self.entry_new_email.get()
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE Utilisateur SET name = :new_name, email = :new_email WHERE name = :username",
                           {'new_name': new_name, 'new_email': new_email, 'username': username})
            connection.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Succès", "Utilisateur mis à jour!")
            else:
                messagebox.showwarning("Erreur", "Utilisateur non trouvé!")
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Erreur de base de données", str(e))
        finally:
            cursor.close()
            connection.close()

class DeleteUserWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Supprimer un utilisateur")
        self.geometry("350x200")
        self.configure(bg="#f5f5f5")
        self.custom_font = tkfont.Font(family="Helvetica", size=12)
        self.create_widgets()

    def create_widgets(self):
        form_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        form_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(form_frame, text="Email de l'utilisateur:", bg="#f5f5f5", fg="#333333", font=self.custom_font).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_email = tk.Entry(form_frame, bg="#ffffff", font=self.custom_font, bd=2, relief='groove')
        self.entry_email.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        button_frame = tk.Frame(self, bg="#f5f5f5")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Supprimer", command=self.confirm_delete_user, bg="#009688", fg="#ffffff", font=self.custom_font, width=15, relief='flat').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Retour", command=self.destroy, bg="#e64a19", fg="#ffffff", font=self.custom_font, width=15, relief='flat').pack(side=tk.RIGHT, padx=5)

    def confirm_delete_user(self):
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cet utilisateur ?"):
            self.delete_user()

    def delete_user(self):
        email = self.entry_email.get()
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM Utilisateur WHERE email = :email", {'email': email})
            connection.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Succès", "Utilisateur supprimé!")
            else:
                messagebox.showwarning("Erreur", "Utilisateur non trouvé!")
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Erreur de base de données", str(e))
        finally:
            cursor.close()
            connection.close()

class SearchUserWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Rechercher un utilisateur")
        self.geometry("350x250")
        self.configure(bg="#f5f5f5")
        self.custom_font = tkfont.Font(family="Helvetica", size=12)
        self.create_widgets()

    def create_widgets(self):
        form_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        form_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(form_frame, text="Rechercher par nom ou email:", bg="#f5f5f5", fg="#333333", font=self.custom_font).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_search = tk.Entry(form_frame, bg="#ffffff", font=self.custom_font, bd=2, relief='groove')
        self.entry_search.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        button_frame = tk.Frame(self, bg="#f5f5f5")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Rechercher", command=self.search_user, bg="#009688", fg="#ffffff", font=self.custom_font, width=15, relief='flat').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Retour", command=self.destroy, bg="#e64a19", fg="#ffffff", font=self.custom_font, width=15, relief='flat').pack(side=tk.RIGHT, padx=5)

    def search_user(self):
        search_term = self.entry_search.get()
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT name, email FROM Utilisateur WHERE name LIKE :search_term OR email LIKE :search_term", {'search_term': f'%{search_term}%'})
            users = cursor.fetchall()
            if users:
                self.show_search_results(users)
            else:
                messagebox.showinfo("Résultat", "Aucun utilisateur trouvé.")
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Erreur de base de données", str(e))
        finally:
            cursor.close()
            connection.close()

    def show_search_results(self, users):
        results_window = tk.Toplevel(self)
        results_window.title("Résultats de la recherche")
        results_window.geometry("350x250")
        results_window.configure(bg="#f5f5f5")
        custom_font = tkfont.Font(family="Helvetica", size=12)

        tree = ttk.Treeview(results_window, columns=("Name", "Email"), show='headings', style="Treeview")
        tree.heading("Name", text="Nom")
        tree.heading("Email", text="Email")
        tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        style = ttk.Style()
        style.configure("Treeview", background="#ffffff", foreground="#000000", font=custom_font, rowheight=30)
        style.configure("Treeview.Heading", background="#009688", foreground="#ffffff", font=custom_font)

        for user in users:
            tree.insert("", tk.END, values=user)

if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagementApp(root)
    root.mainloop()
