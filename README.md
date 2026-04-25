# 📚 Sistema de Academia - Banco de Dados

Este projeto foi desenvolvido como trabalho prático da disciplina de Banco de Dados. O objetivo é demonstrar a integração entre uma aplicação em Python com interface gráfica (Tkinter) e um banco de dados PostgreSQL, realizando operações de CRUD e consultas com JOIN.

---

## 📌 Sobre o Projeto

O sistema simula uma academia, permitindo:

* Cadastro de alunos
* Listagem e pesquisa de alunos
* Atualização de dados (nome e telefone)
* Exclusão de alunos
* Visualização de matrículas com INNER JOIN
* Visualização de alunos com/sem matrícula usando LEFT JOIN

---

## 🛠️ Tecnologias Utilizadas

* Linguagem: Python 3
* Interface Gráfica: Tkinter
* Banco de Dados: PostgreSQL
* Driver de conexão: psycopg2

---

## 📂 Estrutura do Repositório

```
/ddl → Script de criação das tabelas  
/dml → Inserção de dados  
/dql → Consultas SQL (SELECT, JOINs)  
/projeto → Código Python (Tkinter + conexão com banco)
```

---

## 🗄️ Estrutura do Banco de Dados

O banco possui 3 tabelas principais:

* alunos
* planos
* matriculas

### 🔗 Relacionamentos

* Um aluno pode ter várias matrículas
* Um plano pode estar em várias matrículas

---

## ⚠️ Regra de Negócio Implementada

O sistema garante que:

👉 Um aluno não pode ter mais de uma matrícula ativa

Essa regra foi implementada de duas formas:

### ✔ No banco de dados (restrição real)

```sql
ALTER TABLE matriculas
ADD COLUMN ativa BOOLEAN DEFAULT TRUE;

CREATE UNIQUE INDEX idx_matricula_ativa
ON matriculas (id_aluno)
WHERE ativa = TRUE;
```

### ✔ No sistema (validação antes de inserir)

Evita erros e melhora a experiência do usuário.

---

## 🔍 Consultas Implementadas

### ✔ INNER JOIN

Lista apenas alunos que possuem matrícula:

```sql
SELECT a.nome, p.nome_plano, p.valor, m.data_inicio
FROM alunos a
INNER JOIN matriculas m ON a.id_aluno = m.id_aluno
INNER JOIN planos p ON p.id_plano = m.id_plano;
```

---

### ✔ LEFT JOIN

Lista todos os alunos, mesmo sem matrícula:

```sql
SELECT a.nome, m.id_matricula, m.data_inicio
FROM alunos a
LEFT JOIN matriculas m ON m.id_aluno = a.id_aluno;
```

---

## 🖥️ Funcionalidades do Sistema

* Interface gráfica com Tkinter
* Cadastro de alunos
* Pesquisa por nome ou CPF
* Atualização de dados
* Exclusão de alunos (com remoção automática das matrículas)
* Listagem em tabela (Treeview)

---

## 📸 Demonstração

Adicione aqui prints do sistema:

* Tela inicial
* Cadastro de aluno
* Listagem
* INNER JOIN
* LEFT JOIN

---

## 📺 Vídeo Demonstrativo

👉 Adicione aqui o link do seu vídeo (YouTube ou Google Drive)

---

## 🚀 Como Executar o Projeto

### 1. Banco de Dados

Execute os scripts SQL na seguinte ordem:

1. Criação das tabelas (DDL)
2. Alteração da tabela (coluna ativa)
3. Criação do índice
4. Inserção de dados (DML)

---

### 2. Python

Instale a dependência:

```bash
pip install psycopg2
```

Execute o sistema:

```bash
python sistema_academia.py
```

---

## 👤 Autor

* **Aluna Mikaella Martins Silva**
* Centro Universitário Santo Agostinho (UNIFSA)
* Disciplina: Banco de Dados
