import streamlit as st
import pandas as pd
import zipfile
from io import BytesIO
from datetime import datetime
import parameters as p
from num2words import num2words

report_final   = []
report_process = []

def print_report(lines):
    for line in lines:
        st.write(line)
        report_final.append(line)

def print_report_final(lines):
    for line in lines:
        st.write(line)
        report_process.append(line)

def print_error(msg, report):
    if "ATENÇÃO" in msg:
        st.warning(f"⚠️ {msg}")
        print_report(report)
    else:
        st.error(f"❌ {msg}")
        
# =========================================================
# Configuração da página
# =========================================================

st.set_page_config(
    page_title="DBB - Telefones",
    layout="wide",
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

st.write("### DBB Telefones - Padronização")

st.write(
    "Aplicativo que padroniza os números da base no formato: **XX XXXXXXXX** (11 digitos - Fixo) ou **XX 9XXXXXXXX** (12 digitos - Celular)"
)

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
    # Opção para incluir NAV
    # =========================================================

    usar_nav = st.checkbox("Incluir arquivos retornados do NAV")

    # =========================================================
    # Sidebar condicional (NAV)
    # =========================================================

    zip_file = None

    if usar_nav:
        st.sidebar.title("📂 Arquivos retornados do NAV")

        st.sidebar.write(
            "Selecione um ZIP contendo arquivos XLSX retornados do NAV.\n"
        )

        zip_file = st.sidebar.file_uploader(
            "Upload do ZIP NAV",
            type=["zip"]
        )

        st.sidebar.write(
            "\n***Instruções:***\n\n"
            "\nOs arquivos devem conter os campos:\n"
            "- NOME (Código do Cliente no SAP)\n- TELEFONE (Número Discado)\n- DISCAVEL (Retorno NAV)\n\n"
            "\nO campo DISCAVEL deve estar preenchido com:\n"
            "- Sim\n- Não"
            "\n\n*Obs.: Os números com DISCAVEL = 'Não' serão invalidados.*"
        )

    # =========================================================
    # Execução
    # =========================================================

    if st.button("Executar processo de padronização"):

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
            # Leitura do NAV (opcional)
            # -----------------------------------------
            if usar_nav:
                if zip_file is None:
                    st.error("❌ Você marcou a opção NAV, mas não enviou o arquivo ZIP.")
                    st.stop()

                with st.spinner("Lendo arquivos retornados do NAV..."):
                    dfs_nav = []

                    with zipfile.ZipFile(zip_file) as z:
                        for file_name in z.namelist():
                            if file_name.lower().endswith(".xlsx"):
                                with z.open(file_name) as file:
                                    df_temp = pd.read_excel(file)
                                    df_temp = df_temp[["NOME","TELEFONE","DISCAVEL"]]
                                    df_temp["arquivo_origem"] = file_name
                                    dfs_nav.append(df_temp)

                    if not dfs_nav:
                        st.error("❌ Nenhum arquivo XLSX encontrado no ZIP do NAV.")
                        st.stop()

                    df_nav = pd.concat(dfs_nav, ignore_index=True)
                    total_nav = df_nav.shape[0]
                    form = format(total_nav, ',').replace(',', '.')
                    st.success(f"Registros carregados do NAV: **{form}**    _({str(num2words(total_nav, lang="pt_BR")).title()})_")

            # -----------------------------------------
            # Processamento principal
            # -----------------------------------------
            
            # Classificação pela bibilioteca (phonenumbers.ipynb)
            with st.spinner("Processando classificação dos números pela biblioteca..."):
                msg, df_lib = f.class_lib_phone_numbers(df)

            if msg != "Sucesso":
                st.error(f"❌ {msg}")
                st.stop()

            # Validação da classificação pela biblioteca (01_validation.ipynb)
            with st.spinner("Processando validação dos números formatados pela biblioteca..."):
                msg, report, df_val_sujeira, df_val_validos, df_val_classif = f.valid_lib_phone_numbers(df, df_lib)
                
            if msg != "Sucesso":
                print_error(msg, report)
                st.stop()
            print_report(report)
                    
            # Classificação dos válidos pela bilbioteca (02_classification_valid.ipynb)
            with st.spinner("Processando classificação dos números válidos pela biblioteca..."):
                msg, report, df_padr, df_corr, df_invalidos = f.class_valid_lib_phone_numbers(df_val_validos)

            if msg != "Sucesso":
                print_error(msg, report)
                st.stop()
            print_report(report)
                    
            # Classificação dos números por range de caracteres (03_classification.ipynb)
            with st.spinner("Processando classificação dos números por range de caracteres..."):
                msg, report, df_07_09, df_10_11, df_12_15, df_16_30 = f.class_range_phone_numbers(df_val_classif)

            if msg != "Sucesso":
                print_error(msg, report)
                st.stop()
            print_report(report)               
            
            # Classificação dos números com range de caracteres 10 a 11 (04_processing_principal_numbers.ipynb)
            with st.spinner("Processando classificação dos números com range de caracteres 10 a 11..."):
                msg, report, df_10_11_valid, df_10_11_invalid = f.class_range_10_11_phone_numbers(df_10_11)

            if msg != "Sucesso":
                print_error(msg, report)
                st.stop()
            print_report(report)               
                    
            # Classificação dos números com range de caracteres 12 a 15 (06_processing_possibles_valids.ipynb)
            with st.spinner("Processando classificação dos números com range de caracteres 12 a 15..."):
                msg, report, df_12_15_valid, df_12_15_invalid = f.class_range_12_15_phone_numbers(df_12_15)

            if msg != "Sucesso":
                print_error(msg, report)
                st.stop()
            print_report(report)        
                    
            # Classificação dos números com range de caracteres 16 a 30 (05_processing_numbers_inline.ipynb)
            with st.spinner("Processando classificação dos números com range de caracteres 16 a 30..."):
                msg, report, df_16_30_valid, df_16_30_invalid = f.class_range_16_30_phone_numbers(df_16_30)

            if msg != "Sucesso":
                print_error(msg, report)
                st.stop()
            print_report(report)               
                    
            # Classificação dos números com range de caracteres 07 a 09 (08_processing_classifcs_with_fax_cep.ipynb)
            with st.spinner("Processando classificação dos números com range de caracteres 07 a 09..."):
                msg, report, df_07_09_valid_cep, df_07_09_valid_fax, df_07_09_valid_fax_dupl, df_07_09_invalid = f.class_range_07_09_phone_numbers(df_07_09)

            if msg != "Sucesso":
                print_error(msg, report)
                st.stop()
            print_report(report)               
 
            dfs_invalids = []
            dfs_invalids.append(df_invalidos)
            dfs_invalids.append(df_10_11_invalid)
            dfs_invalids.append(df_12_15_invalid)
            dfs_invalids.append(df_16_30_invalid)
            dfs_invalids.append(df_07_09_invalid)
                    
            df_invalids = pd.concat(dfs_invalids)
                    
            # Classificação dos números invalidos (07_processing_invalids_with_fax_cep.ipynb)
            with st.spinner("Processando classificação dos números invalidos relacionando ao CEP e ao FAX..."):
                msg, report, df_inv_valid_cep, df_inv_valid_fax, df_inv_valid_fax_dupl, df_inv_invalid = f.class_invalids_phone_numbers(df_invalids)

            if msg != "Sucesso":
                print_error(msg, report)
                st.stop()
            print_report(report)
            
            if usar_nav:
                # Criação do arquivo formatado com os numeros invalidos retornados pelo NAV
                with st.spinner("Processando arquivos retornados pelo NAV..."):
                    msg, df_nav_inv, df_nav_all = f.generate_base_nav(df_nav)
                
                if msg != "Sucesso":
                    st.error(f"❌ {msg}")
                    st.stop()
                
                fmt_qtd_valid   = format(df_nav_all.shape[0]-df_nav_inv.shape[0], ',').replace(',', '.')
                fmt_qtd_invalid = format(df_nav_inv.shape[0], ',').replace(',', '.')
                
                st.success(f"Telefones válidos pelo NAV: {fmt_qtd_valid} (Sim) / {fmt_qtd_invalid} (Não)")
            
            # Gera arquivos finais 
            dfs_src = {}
            
            dfs_src["df_padr"]                 = df_padr
            dfs_src["df_corr"]                 = df_corr
            dfs_src["df_16_30_valid"]          = df_16_30_valid
            dfs_src["df_10_11_valid"]          = df_10_11_valid
            dfs_src["df_12_15_valid"]          = df_12_15_valid
            dfs_src["df_07_09_valid_fax"]      = df_07_09_valid_fax
            dfs_src["df_07_09_valid_fax_dupl"] = df_07_09_valid_fax_dupl
            dfs_src["df_07_09_valid_cep"]      = df_07_09_valid_cep
            dfs_src["df_inv_valid_fax"]        = df_inv_valid_fax
            dfs_src["df_inv_valid_fax_dupl"]   = df_inv_valid_fax_dupl
            dfs_src["df_inv_valid_cep"]        = df_inv_valid_cep                             
            dfs_src["df_sujeira"]              = df_val_sujeira
            dfs_src["df_invalid"]              = df_inv_invalid  
            dfs_src["df_nav_all"]              = df_nav_all 
            dfs_src["df_nav_inv"]              = df_nav_inv
            dfs_src["df"]                      = df
            
            # Geração das bases e arquivos finais (99_generate_files_to_validate.ipynb)
            with st.spinner("Gerando bases e arquivos finais..."):
                msg, dfs, files = f.generate_final_files(dfs_src, usar_nav)
            
            if msg != "Sucesso":
                st.error(f"❌ {msg}")
                st.stop()
            
            # Geração do relatório final do processamento do arquivo enviado
            with st.spinner("Gerando relatório final do processamento do arquivo..."):
                msg, report = f.generate_final_report_process(dfs_src)

            if msg != "Sucesso":
                st.error(f"❌ {msg}")
                st.stop()
            print_report_final(report)               
            
            # Geração do relatório final do processamento do arquivo enviado com retorno do nav
            if usar_nav:
                with st.spinner("Gerando relatório final do processamento do arquivo com retorno do NAV..."):
                    dfs_src["df_invalid_nav"] = dfs["df_invalid_nav"]
                    dfs_src["df_valid"]       = dfs["df_valid"]
                    msg, report = f.generate_report_with_return_nav(dfs_src)

                if msg != "Sucesso":
                    st.error(f"❌ {msg}")
                    st.stop()
                print_report_final(report)               
            
            # -----------------------------------------
            # Monta conteúdo do relatório TXT
            # -----------------------------------------
            header = [
                "RELATÓRIO DE PROCESSAMENTO - PADRONIZAÇÃO DE TELEFONES\n",
                f"Data de execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n",
                "-" * 60,
                "\n",
                ]
            
            header_final = [
                "\n",
                "-" * 60,
                "\nRELATÓRIO FINAL DO PROCESSAMENTO DA BASE\n",
                "-" * 60,
                "\n",
                ]
            
            report_text = "\n".join(header + report_final + header_final + report_process)

            # -----------------------------------------
            # Cria ZIP em memória
            # -----------------------------------------
            zip_buffer = BytesIO()

            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr("relatorio_final.txt", report_text)
                zip_file.writestr("base_validos_total.csv", files["csv_valid"])
                zip_file.writestr("base_validos_sap.csv", files["csv_valid_sap"])
                zip_file.writestr("base_invalidos.csv", files["csv_invalid"])
                zip_file.writestr("base_sujeira.csv", files["csv_suj"])
                if usar_nav:
                    zip_file.writestr("base_invalidos_nav.csv", files["csv_inv_nav"])
                    zip_file.writestr("base_envio_nav.csv", files["csv_nav"])

            zip_buffer.seek(0)

            # -----------------------------------------
            # Botão único de download
            # -----------------------------------------
            st.download_button(
                label="⬇️ Baixar resultado (ZIP)",
                data=zip_buffer,
                file_name="resultado_padronizacao_telefones.zip",
                mime="application/zip"
            )

        except Exception as e:
            st.error("❌ Erro ao processar os arquivos")
            st.exception(e)
