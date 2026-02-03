import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

def main():
    st.caption("💙 Class Notes: Google doc")
    st.write("➡️ Share your ideas.")
    # Padlet embed URL (you need to replace this with your actual Padlet embed URL)
    padlet_url = "https://docs.google.com/document/d/1olgbyInMLUFaYPjt8G_V-tNtb1Kfhjts4gq4hxPYNmQ/preview"


    # Create an iframe to embed the Padlet
    padlet_iframe = f"<iframe src='{padlet_url}' width='100%' height='600' frameborder='0' allow='autoplay'></iframe>"

    # Display the iframe in Streamlit
    components.html(padlet_iframe, height=800)

if __name__ == "__main__":
    main()
