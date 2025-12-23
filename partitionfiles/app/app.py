import streamlit as st
import pandas as pd
import zipfile
from io import BytesIO
from datetime import datetime
import parameters as p
from num2words import num2words

# =========================================================
# Configuração da página
# =========================================================

st.set_page_config(
    page_title="DBB - Telefones - Particionamento de Arquivos",
    # layout="wide",
)

st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #3B7D23; /* verde */
        color: white;
        border-radius: 10px;
        height: 45px;
        width: 260px;
        font-size: 16px;
        border: none;
        cursor: pointer;
    }

    div.stButton > button:hover {
        background-color: #1B5E20;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <style>
    .app-header {{
        background-image: url("data:image/png;base64,{p.img_to_base64("auxiliar/img/fundo.png")}");
        background-size: cover;
        background-position: center;
        height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        margin-bottom: 20px;
    }}

    .app-header img {{
        height: 80px;
    }}
    </style>

    <div class="app-header">
        <img src="data:image/png;base64,{p.img_to_base64("auxiliar/img/logo.png")}">
    </div>
    """,
    unsafe_allow_html=True
)

st.write("### DBB Telefones - Particionamento de Arquivo")

st.write( "Aplicativo que particiona um arquivo, com um limite de registros para cada arquivo particionado, e com os registros agrupados por cliente." )

opcoes = {
    " 10 Mil": 10000,
    " 20 Mil": 20000,
    " 30 Mil": 30000,
    " 40 Mil": 40000,
    " 50 Mil": 50000,
    " 60 Mil": 60000,
    " 70 Mil": 70000,
    " 80 Mil": 80000,
    " 90 Mil": 90000,
    "100 Mil": 100000
}

label = st.selectbox(
    "Selecione a quantidade limite de registros por arquivo:",
    list(opcoes.keys()),
    index=2
)

valor_numerico = opcoes[label]

if label:                
    # =========================================================
    # Upload obrigatório do CSV
    # =========================================================
    uploaded_csv = st.file_uploader(
        "Selecione o arquivo CSV base",
        type=["csv", "txt"]
    )

    if uploaded_csv is None:
        st.info("Selecione uma base de telefones para continuar.")
    else:
        # =========================================================
        # Execução
        # =========================================================
        if st.button("Executar processo de particionamento"):
            try:
                # -----------------------------------------
                # Leitura do CSV base
                # -----------------------------------------
                with st.spinner("Lendo arquivo CSV base..."):
                    df = p.ler_arquivo(uploaded_csv, "latin1")
                    total_csv = df.shape[0]
                
                form = format(total_csv, ',').replace(',', '.')
                st.success(f"Registros carregados da Base de Telefones: **{form}**    _({str(num2words(total_csv, lang="pt_BR")).title()})_")

                # -----------------------------------------
                # Particionamento do CSV base
                # -----------------------------------------
                with st.spinner("Particionando o arquivo CSV base..."):
                    files_part = p.partition_files(df, valor_numerico)
                
                form = format(len(files_part), ',').replace(',', '.')
                st.success(f"Total de arquivos particionados: **{form}**")

                # -------------------------------------------------
                # Criar ZIP em memória
                # -------------------------------------------------
                zip_buffer = BytesIO()

                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for item in files_part:
                        zip_file.writestr(
                            item["nome"],     # nome do arquivo dentro do ZIP
                            item["arq"]       # conteúdo CSV (string)
                        )

                zip_buffer.seek(0)

                # -------------------------------------------------
                # Botão de download
                # -------------------------------------------------
                st.download_button(
                    label="⬇️ Baixar arquivos particionados (ZIP)",
                    data=zip_buffer,
                    file_name=f"arquivos_particionados.zip",
                    mime="application/zip"
                )
            except Exception as e:
                st.error("❌ Erro ao processar o arquivo")
                st.exception(e)
