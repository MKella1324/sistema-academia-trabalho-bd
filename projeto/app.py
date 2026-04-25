import tkinter as tk
from tkinter import ttk, messagebox
from conexao import conectar


def configurar_tabela(tree, colunas, titulos, dados):
    tree.delete(*tree.get_children())

    tree["columns"] = colunas
    tree["show"] = "headings"

    for col in colunas:
        tree.heading(col, text=titulos[col])
        tree.column(col, width=140, anchor="center")

    for i, row in enumerate(dados):
        if i % 2 == 0:
            tree.insert("", "end", values=row, tags=("par",))
        else:
            tree.insert("", "end", values=row, tags=("impar",))

    tree.tag_configure("par", background="#f2f2f2")
    tree.tag_configure("impar", background="#ffffff")


def abrir_tela_cadastro():
    janela = tk.Toplevel(root)
    janela.title("Cadastrar Aluno")
    janela.geometry("400x250")

    tk.Label(janela, text="Nome").pack(pady=5)
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="CPF").pack(pady=5)
    entry_cpf = tk.Entry(janela)
    entry_cpf.pack()

    tk.Label(janela, text="Telefone").pack(pady=5)
    entry_telefone = tk.Entry(janela)
    entry_telefone.pack()

    def salvar():
        nome = entry_nome.get()
        cpf = entry_cpf.get()
        telefone = entry_telefone.get()

        if not nome or not cpf or not telefone:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        conn = conectar()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO alunos (nome, cpf, telefone)
                VALUES (%s, %s, %s)
            """, (nome, cpf, telefone))

            conn.commit()
            messagebox.showinfo("Sucesso", "Aluno cadastrado!")
            janela.destroy()

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Erro", str(e))

        finally:
            conn.close()

    tk.Button(janela, text="Cadastrar", command=salvar).pack(pady=15)


def abrir_tela_listagem():
    janela = tk.Toplevel(root)
    janela.title("Lista de Alunos")
    janela.geometry("750x450")

    frame_top = tk.Frame(janela)
    frame_top.pack(fill="x", pady=10)

    tk.Label(frame_top, text="Pesquisar").pack(side="left", padx=5)
    entry_busca = tk.Entry(frame_top)
    entry_busca.pack(side="left", padx=5)

    tree = ttk.Treeview(janela)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def carregar_dados(filtro=""):
        conn = conectar()
        cur = conn.cursor()

        if filtro:
            cur.execute("""
                SELECT id_aluno, nome, cpf, telefone
                FROM alunos
                WHERE nome ILIKE %s OR cpf ILIKE %s
                ORDER BY id_aluno
            """, (f"%{filtro}%", f"%{filtro}%"))
        else:
            cur.execute("""
                SELECT id_aluno, nome, cpf, telefone
                FROM alunos
                ORDER BY id_aluno
            """)

        dados = cur.fetchall()
        conn.close()

        configurar_tabela(
            tree,
            ("id", "nome", "cpf", "telefone"),
            {"id": "ID", "nome": "Nome", "cpf": "CPF", "telefone": "Telefone"},
            dados
        )

    def pesquisar():
        carregar_dados(entry_busca.get())

    def excluir():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno")
            return

        dados = tree.item(item)["values"]
        id_aluno = dados[0]

        confirm = messagebox.askyesno("Confirmação", "Deseja excluir este aluno?")
        if not confirm:
            return

        conn = conectar()
        cur = conn.cursor()

        try:
            cur.execute("DELETE FROM alunos WHERE id_aluno = %s", (id_aluno,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Aluno excluído!")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Erro", str(e))
        finally:
            conn.close()

        carregar_dados()

    def atualizar():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno")
            return

        dados = tree.item(item)["values"]
        id_aluno, nome_atual, cpf, telefone_atual = dados

        janela_update = tk.Toplevel(janela)
        janela_update.title("Atualizar Aluno")
        janela_update.geometry("300x200")

        tk.Label(janela_update, text="Nome").pack(pady=5)
        entry_nome = tk.Entry(janela_update)
        entry_nome.insert(0, nome_atual)
        entry_nome.pack()

        tk.Label(janela_update, text="Telefone").pack(pady=5)
        entry_telefone = tk.Entry(janela_update)
        entry_telefone.insert(0, telefone_atual)
        entry_telefone.pack()

        def salvar():
            novo_nome = entry_nome.get()
            novo_tel = entry_telefone.get()

            if not novo_nome or not novo_tel:
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return

            conn = conectar()
            cur = conn.cursor()

            try:
                cur.execute("""
                    UPDATE alunos
                    SET nome = %s, telefone = %s
                    WHERE id_aluno = %s
                """, (novo_nome, novo_tel, id_aluno))

                conn.commit()
                messagebox.showinfo("Sucesso", "Aluno atualizado!")
                janela_update.destroy()

            except Exception as e:
                conn.rollback()
                messagebox.showerror("Erro", str(e))

            finally:
                conn.close()

            carregar_dados()

        tk.Button(janela_update, text="Salvar", command=salvar).pack(pady=10)

    tk.Button(frame_top, text="Buscar", command=pesquisar).pack(side="left", padx=5)
    tk.Button(frame_top, text="Atualizar", command=atualizar).pack(side="left", padx=5)
    tk.Button(frame_top, text="Excluir", command=excluir).pack(side="left", padx=5)

    carregar_dados()


def inner_join():
    janela = tk.Toplevel(root)
    janela.title("INNER JOIN")
    janela.geometry("700x400")

    tree = ttk.Treeview(janela)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT a.nome, p.nome_plano, p.valor, m.data_inicio
        FROM alunos a
        INNER JOIN matriculas m ON a.id_aluno = m.id_aluno
        INNER JOIN planos p ON p.id_plano = m.id_plano
        ORDER BY a.id_aluno
    """)

    dados = cur.fetchall()
    conn.close()

    configurar_tabela(
        tree,
        ("aluno", "plano", "valor", "data"),
        {
            "aluno": "Aluno",
            "plano": "Plano",
            "valor": "Valor",
            "data": "Data Início"
        },
        dados
    )


def left_join():
    janela = tk.Toplevel(root)
    janela.title("LEFT JOIN")
    janela.geometry("700x400")

    tree = ttk.Treeview(janela)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT a.nome, m.id_matricula, m.data_inicio
        FROM alunos a
        LEFT JOIN matriculas m ON m.id_aluno = a.id_aluno
        ORDER BY a.id_aluno
    """)

    dados = cur.fetchall()
    conn.close()

    configurar_tabela(
        tree,
        ("aluno", "matricula", "data"),
        {
            "aluno": "Aluno",
            "matricula": "Matrícula",
            "data": "Data Início"
        },
        dados
    )


root = tk.Tk()
root.title("Sistema Academia")
root.state("zoomed")

frame = tk.Frame(root)
frame.pack(expand=True)

tk.Label(frame, text="Sistema Academia", font=("Arial", 20)).pack(pady=20)

tk.Button(frame, text="Cadastrar Aluno", width=25, command=abrir_tela_cadastro).pack(pady=10)
tk.Button(frame, text="Listar / Pesquisar Alunos", width=25, command=abrir_tela_listagem).pack(pady=10)
tk.Button(frame, text="INNER JOIN", width=25, command=inner_join).pack(pady=10)
tk.Button(frame, text="LEFT JOIN", width=25, command=left_join).pack(pady=10)

root.mainloop()
