import streamlit as st
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from decouple import config

This_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
ASSETS_DIR =This_DIR / "assets"
STYLES_DIR = This_DIR / "styles"
CSS_FILE = STYLES_DIR / "main.css"

CONTACT_EMAIL = "info@worthy-works.com"
PRODUCT_NAME = "Certificate Generating Software"

PRODUCT_DESCRIPTION = """
This app is tailored to generate certificates for individuals who have completed participation in a suitable event.
Here are the features that you will find irresistible:
- Displays on-screen so errors can be corrected
- Does not store information online
- Convenient and quick
- Easy to navigate
- Download, email, or print off as required
***This is the new system for continuing professional development support. Why wait any longer?***
"""
def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
# Your email configuration
email_sender = "info@gworthy-works.com"
email_password = "uwakdjvktacfqqji"

load_css_file(CSS_FILE)

def generate_certificate(participant_name, event_name, event_date):
    certificate_template = Image.open('certificate_template.png')

    # Font size for the text
    font_size = 60  # Adjust the font size as needed

    # Create a copy of the template
    certificate = certificate_template.copy()

    # Draw text on the certificate
    draw = ImageDraw.Draw(certificate)

    # Load a font with the desired size
    font = ImageFont.truetype("font.ttf", size=font_size)

    # Calculate the bounding box of the text to center it
    text_width, text_height = draw.textbbox((20, 20), participant_name, font=font)[:2]
    text_x = 100 + (certificate.width - text_width) // 2
    text_y = 400

    draw.text((720, 760), participant_name, fill=(0, 0, 0), font=font)
    
    # Draw the event name
    formatted_event_name = event_name
    draw.text((180, 880), f"being an enthusiastic participant at {formatted_event_name} course", fill=(0, 0, 0), font=font)
    
    # Add 'on' before the event date
    formatted_event_date = event_date.strftime("%B %d, %Y")
    draw.text((720, 1000), f"Date: {formatted_event_date}", fill=(0, 0, 0), font=font)

    # Convert the certificate image to bytes and Base64 encode it
    img_buf = io.BytesIO()
    certificate.save(img_buf, format='PNG')
    b64 = base64.b64encode(img_buf.getvalue()).decode()

    return certificate, b64


#st.title("Certificate Generator")
st.header(PRODUCT_NAME)
left_col, right_col = st.columns((2,1))
with left_col:
    st.text("")
    st.write(PRODUCT_DESCRIPTION)
    st.header("Use this free certificate generator")

    participant_name = st.text_input("Participant Name")
    event_name_options = ["Annual General Meeting", "Scientific Meeting", "Update Course", "Support Work"]
    event_name = st.selectbox("Select Event Name", event_name_options)
    event_date = st.date_input("Event Date")

    # Enable the Generate Certificate button only when all fields are filled
    if participant_name and event_name and event_date:
        if st.button("Generate Certificate"):
            certificate, b64 = generate_certificate(participant_name, event_name, event_date)
            st.image(certificate, caption="Generated Certificate", use_column_width=True)
            
            # Center and make the "Download Certificate" link prominent
            st.markdown(
                f'<p style="text-align:center; font-size:24px;"><a href="data:image/png;base64,{b64}" download="certificate.png" style="color:#FF5733;">Download Certificate</a></p>',
                unsafe_allow_html=True
            )
            
            
    else:
        st.warning("Please fill in all fields to enable certificate generation.")
with right_col:
    product_image = Image.open(ASSETS_DIR / "certificate_template.png")
    st.image(product_image,width=450)
    
# Customization Section
st.markdown("---")
st.header("Need Customization?")
st.write("Looking for a tailored certificate generator to match your brand or unique requirements? We offer custom solutions that meet your needs.")


left_col, right_col = st.columns((1,1))
with left_col:
            
    #---CONTACT FORM--
    st.write("")
    st.write("---")
    st.subheader(":mailbox: Contact us")
    contact_form = f"""
    <form action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit" class="button">Send 📧</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)

with right_col:
    #---FAQ---
    st.write("")
    st.write("---")
    st.subheader(":raising_hand: FAQ")

    faq = {
        "Will my information be visible online?": "No information is saved on the server or anywhere on the internet, unless whatever you share with people.",
        "Are there hidden fees?": "This free version has no fee attached to it.",
        "Why can't I send the certificate directly to others via the app?": "This is available to those who seek to have customised premium app.",
        "Can I generate bulk certificates for my course attendees?": "Not with this version. Please contact our team to discuss a customised app for your organisation."
    }
    for question, answer in faq.items():
        with st.expander(question):
            st.write(answer)

# Footer
st.markdown("---")
st.write("Privacy Policy: [Link to Privacy Policy](https://www.worthy-works.com/privacy-document)")
st.write("Terms and Conditions: [Link to Terms and Conditions](https://www.worthy-works.com/terms-conditions)")
st.write("© 2023 Worthy Works Ltd. All rights reserved.")

