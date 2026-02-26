import streamlit as st
from services.viacep import buscar_cep, ViaCepError
from utils.validators import limpar_cep, cep_valido

st.set_page_config(page_title="Busca CEP", page_icon="📮", layout="centered")
st.title("📮 Buscar Endereço por CEP")

cep_input = st.text_input("Digite o CEP", placeholder="Ex.: 01001-000")

col1, col2 = st.columns([1, 1])
with col1:
    btn_buscar = st.button("Buscar", use_container_width=True)
with col2:
    btn_limpar = st.button("Limpar", use_container_width=True)

if btn_limpar:
    st.rerun()

if btn_buscar:
    cep = limpar_cep(cep_input)

    if not cep_valido(cep):
        st.error("CEP inválido. Digite 8 números.")
    else:
        try:
            with st.spinner("Consultando ViaCEP..."):
                data = buscar_cep(cep)

            st.success("Endereço encontrado!")

            st.write("**Logradouro:**", data.get("logradouro", ""))
            st.write("**Bairro:**", data.get("bairro", ""))
            st.write("**Cidade:**", data.get("localidade", ""))
            st.write("**UF:**", data.get("uf", ""))
            st.write("**CEP:**", data.get("cep", ""))

            with st.expander("Ver JSON completo"):
                st.json(data)

        except ViaCepError as e:
            st.error(str(e))