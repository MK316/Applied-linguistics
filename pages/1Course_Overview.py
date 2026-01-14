import streamlit as st
import streamlit.components.v1 as components
import requests
import base64

st.set_page_config(page_title="Course", layout="wide")

tab1, tab2, tab3 = st.tabs(["Syllabus", "Online Links", "TBA"])

PDF_URL = "https://raw.githubusercontent.com/MK316/Applied-linguistics/main/data/S26-appling.pdf"

@st.cache_data(show_spinner=False)
def load_pdf_bytes(url: str) -> bytes:
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.content

def render_pdf_with_pdfjs(pdf_bytes: bytes, height: int = 900):
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")

    html = f"""
    <div id="viewer" style="width:100%; height:{height}px; overflow:auto; background:#f7f7f7;"></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
    <script>
      const pdfData = atob("{b64}");
      const loadingTask = pdfjsLib.getDocument({{data: pdfData}});
      loadingTask.promise.then(async function(pdf) {{
        const viewer = document.getElementById("viewer");
        viewer.innerHTML = "";

        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {{
          const page = await pdf.getPage(pageNum);

          // scale: 화면에 보기 좋게 (필요시 1.2~1.8 등 조절)
          const scale = 1.4;
          const viewport = page.getViewport({{ scale }});

          const canvas = document.createElement("canvas");
          const context = canvas.getContext("2d");
          canvas.width = viewport.width;
          canvas.height = viewport.height;

          canvas.style.display = "block";
          canvas.style.margin = "12px auto";
          canvas.style.background = "white";
          canvas.style.boxShadow = "0 2px 10px rgba(0,0,0,0.08)";

          viewer.appendChild(canvas);

          await page.render({{ canvasContext: context, viewport }}).promise;
        }}
      }}).catch(function(err) {{
        document.getElementById("viewer").innerHTML =
          "<p style='padding:16px;color:#b00020;'>PDF render error: " + err + "</p>";
      }});
    </script>
    """
    components.html(html, height=height, scrolling=True)

with tab1:
    st.markdown("### 📄 Course Overview (PDF)")

    try:
        pdf_bytes = load_pdf_bytes(PDF_URL)

        # PDF.js 렌더
        render_pdf_with_pdfjs(pdf_bytes, height=900)

        # 항상 다운로드도 제공 (보험)
        st.download_button(
            "⬇️ Download PDF",
            data=pdf_bytes,
            file_name="Course_Overview.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    except Exception as e:
        st.error(f"PDF를 불러오지 못했습니다: {e}")

with tab2:
    st.write("여기는 탭 2입니다.")

with tab3:
    st.write("여기는 탭 3입니다.")
