from tkinter import *

# Codigo copiado de: https://docs.hektorprofe.net/python/interfaces-graficas-con-tkinter/widget-menu/
# El primer widget menú que creamos hace referencia a la barra de menú, de ahí que se le suele llamar menu_bar

def create_menu():
    menu_bar = Menu(root)
    root.config(menu = menu_bar)

    # Una vez creada la barra podemos comenzar a añadir submenús y comandos. Empecemos con los submenús
    file_menu = Menu(menu_bar)
    edit_menu = Menu(menu_bar)
    help_menu = Menu(menu_bar)

    # Bien ya tenemos nuestra barra con los 3 submenús funcionando bien, pero ocurre algo raro, 
    # nos aparece una especie de elemento por defecto. Podemos hacer que desaparezca si indicamos 
    # el parámetro tearoff=0

    file_menu = Menu(menu_bar, tearoff=0)
    edit_menu = Menu(menu_bar, tearoff=0)
    help_menu = Menu(menu_bar, tearoff=0)

    # Ahora sí que lo tenemos bien, ¿pero está demasiado vacío no? Vamos a añadir comandos de ejemplo
    # en nuestros submenús
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Nuevo") #, command=WidgetButton.main
    file_menu.add_command(label="Abrir")
    file_menu.add_command(label="Guardar")
    file_menu.add_command(label="Cerrar")

    # También podemos agregar un separador y un comando de salir con root.quit
    file_menu.add_separator()
    file_menu.add_command(label="Salir", command=root.quit)

    edit_menu = Menu(menu_bar, tearoff=0)
    edit_menu.add_command(label="Cortar")
    edit_menu.add_command(label="Copiar")
    edit_menu.add_command(label="Pegar")

    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Ayuda")
    help_menu.add_separator()
    help_menu.add_command(label="Acerca de...")

    # Ya tenemos los submenús, pero todavía nos falta añadirlos a la barra de menú
    menu_bar.add_cascade(label='Archivo', menu=file_menu)
    menu_bar.add_cascade(label='Editar', menu=edit_menu)
    menu_bar.add_cascade(label='Ayuda', menu=help_menu)

def print_option():
    print(f"Option: {tkvarq.get()}")

def option_menu():
    options = ['Continuous',
               'Single Frame',
               'Multi Frame']

    global tkvarq
    tkvarq = StringVar()
    tkvarq.set(options[0])
    OptionMenu(root, tkvarq, *options).pack()

    Button(root, width=30, text="Submit", command=print_option).pack()

  
root = Tk()
root.config(bd=25)

create_menu()
option_menu()

root.mainloop()
