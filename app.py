import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# Estilo personalizado preto e roxo
st.markdown("""
    <style>
    .stApp {
        background-color: #1e1b2e;
        color: #f5f5f5;
    }
    h1, h2, h3, label, .st-bc {
        color: #d0a9f5;
    }
    .stTextInput input, .stNumberInput input, .stSelectbox div div, .stTextArea textarea {
        background-color: #2c2a3f;
        color: #fff;
        border: 1px solid #6e44ff;
    }
    .stButton button {
        background-color: #6e44ff;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💜 Meu Menu Fit")
st.subheader("Seu cardápio semanal personalizado e feminino 🌸")

# Formulário de dados pessoais
st.header("👩 Dados Pessoais")

nome = st.text_input("Nome completo")
idade = st.number_input("Idade", min_value=10, max_value=100, step=1)
genero = st.selectbox("Gênero", ["Feminino", "Masculino", "Outro"])
altura = st.number_input("Altura (ex: 1.65 m)", min_value=1.0, max_value=2.5, step=0.01, format="%.2f")
peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, step=0.1)
objetivo = st.radio("Objetivo:", ["Perder peso", "Ganhar massa", "Manter peso"])

# Alimentos
st.header("🍎 Alimentos Disponíveis")
alimentos_input = st.text_area("Digite no mínimo 10 alimentos separados por vírgula (ex: arroz, frango, abobrinha...)")

def gerar_pdf(dados, alimentos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(110, 68, 255)
    pdf.cell(0, 10, "Meu Menu Fit - Cardápio Semanal", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)

    # Dados pessoais
    for key, val in dados.items():
        pdf.cell(0, 10, f"{key}: {val}", ln=True)

    pdf.ln(10)
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

    for dia in dias:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"{dia}-feira", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 8, f"""
🍽 Café da manhã:
- Omelete com espinafre e tomate
- Modo de preparo: Bata os ovos, adicione os ingredientes e grelhe em frigideira antiaderente.

🥗 Almoço:
- Frango grelhado com arroz integral e salada de legumes
- Modo de preparo: Grelhe o frango, cozinhe o arroz, prepare uma salada com os alimentos informados.

🍵 Jantar:
- Sopa leve de legumes com carne magra
- Modo de preparo: Cozinhe os legumes e carne com temperos naturais até amaciar.

""")
        pdf.ln(5)

    file_name = f"meu_menu_fit_{nome.lower().replace(' ', '_')}.pdf"
    file_path = os.path.join("/mnt/data", file_name)
    pdf.output(file_path)
    return file_path

if st.button("📄 Gerar Cardápio em PDF"):
    lista_alimentos = [a.strip().capitalize() for a in alimentos_input.split(',') if a.strip()]
    
    if len(lista_alimentos) < 10:
        st.error("❗ Por favor, insira ao menos 10 alimentos diferentes.")
    elif not nome:
        st.error("❗ Por favor, preencha o campo de nome.")
    else:
        dados_usuario = {
            "Nome": nome,
            "Idade": f"{idade} anos",
            "Gênero": genero,
            "Altura": f"{altura:.2f} m",
            "Peso": f"{peso:.1f} kg",
            "Objetivo": objetivo
        }
        caminho_pdf = gerar_pdf(dados_usuario, lista_alimentos)
        st.success("✅ Cardápio gerado com sucesso!")
        with open(caminho_pdf, "rb") as pdf_file:
            st.download_button(
                label="📥 Baixar Cardápio em PDF",
                data=pdf_file,
                file_name="cardapio_meu_menu_fit.pdf",
                mime="application/pdf"
            )
