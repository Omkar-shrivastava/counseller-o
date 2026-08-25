from flask import Flask, request, redirect
import os
from urllib.parse import quote

app = Flask(__name__)

# ---------------------------------------------------------------
# EDIT YOUR COUNSELLORS LIST HERE
# id       -> unique short code (used internally in the URL)
# name     -> counsellor's name
# desc     -> short description
# whatsapp -> WhatsApp number with country code, no + or spaces
#             e.g. an Indian number 98765 43210 becomes "919876543210"
# ---------------------------------------------------------------
COUNSELLORS = [
    {
    "id": "raj-sir",
    "name": "Raj Sir",
        "desc": "Helping Doctors Make the Right PG Choices 8+ Years of Admission Experience Speciality College Counselling Admission.",
        "whatsapp": "916263381528",  # TEST NUMBER
    },
]

VIDEO_FILENAME = "Neetpg.mp4"


STYLE = """
* { box-sizing: border-box; }

:root {
  --primary: #0f6fb8;
  --primary-dark: #084e85;
  --accent: #25D366;
  --bg: #eef4fa;
  --card-bg: #ffffff;
  --text: #1c2b39;
  --muted: #5c6b78;
}

body {
  margin: 0;
  font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
}

.top-bar {
  background: linear-gradient(135deg, var(--primary-dark), var(--primary));
  color: #fff;
  padding: 26px 20px 34px;
  text-align: center;
  box-shadow: 0 4px 14px rgba(15, 111, 184, 0.25);
}

.top-bar img {
  height: 64px;
  margin-bottom: 10px;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.25));
}

.top-bar h1 {
  margin: 4px 0 6px;
  font-size: 26px;
  letter-spacing: 0.3px;
}

.top-bar p {
  margin: 0;
  opacity: 0.92;
  font-size: 15px;
  max-width: 560px;
  margin-left: auto;
  margin-right: auto;
}

.video-section {
  background: var(--card-bg);
  border-radius: 16px;
  padding: 18px;
  margin: 0 auto 28px;
  max-width: 720px;
  box-shadow: 0 6px 18px rgba(15, 40, 70, 0.08);
  text-align: center;
}

.video-section h2 {
  margin: 0 0 14px;
  color: var(--primary-dark);
  font-size: 19px;
}

.video-player {
  display: block;
  width: 100%;
  height: auto;
  max-height: 70vh;
  border-radius: 10px;
  background: #091521;
  object-fit: contain;
}

.video-missing {
  margin: 0;
  padding: 28px 16px;
  border: 1px dashed #b9c8d5;
  border-radius: 10px;
  color: var(--muted);
  font-size: 14px;
}

.wrap {
  max-width: 960px;
  margin: -18px auto 40px;
  padding: 0 20px;
}

.section-title {
  text-align: center;
  font-size: 20px;
  font-weight: 600;
  color: var(--primary-dark);
  margin: 30px 0 18px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 22px;
}

.card {
  background: var(--card-bg);
  border-radius: 16px;
  padding: 26px 22px;
  text-align: center;
  box-shadow: 0 6px 18px rgba(15, 40, 70, 0.08);
  border: 1px solid rgba(15, 111, 184, 0.08);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 24px rgba(15, 40, 70, 0.14);
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  font-size: 24px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 14px;
}

.card h3 { margin: 0 0 8px; font-size: 18px; color: var(--text); }
.desc { font-size: 13.5px; color: var(--muted); min-height: 52px; line-height: 1.5; }

.contact-btn {
  background: var(--accent);
  color: #fff;
  border: none;
  padding: 13px 18px;
  border-radius: 10px;
  font-size: 14.5px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 14px;
  width: 100%;
  transition: background 0.15s ease, transform 0.1s ease;
}
.contact-btn:hover { background: #1ebe5a; transform: translateY(-1px); }

/* Modal */
.modal-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(10, 25, 40, 0.55);
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 999;
}
.modal-box {
  background: #fff;
  border-radius: 16px;
  padding: 28px;
  width: 100%;
  max-width: 440px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 12px 40px rgba(0,0,0,0.25);
}
.modal-box h3 {
  margin: 0 0 4px;
  color: var(--primary-dark);
  font-size: 19px;
}
.modal-sub { color: var(--muted); font-size: 13px; margin: 0 0 18px; }

.field { display: flex; flex-direction: column; margin-bottom: 15px; }
.field label { font-size: 13.5px; font-weight: 600; margin-bottom: 6px; color: var(--text); }
.field input {
  padding: 11px 13px;
  border: 1px solid #d6dee6;
  border-radius: 9px;
  font-size: 14px;
  background: #fafcfe;
}
.field input:focus { outline: none; border-color: var(--primary); background: #fff; }

.modal-actions { display: flex; gap: 10px; margin-top: 6px; }
.cancel-btn, .submit-btn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 9px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
}
.cancel-btn { background: #eef1f4; color: var(--text); }
.submit-btn { background: var(--accent); color: #fff; }
.submit-btn:hover { background: #1ebe5a; }

.footer-note {
  text-align: center;
  font-size: 12.5px;
  color: var(--muted);
  margin-top: 36px;
}

"""


def find_counsellor(counsellor_id):
    for c in COUNSELLORS:
        if c["id"] == counsellor_id:
            return c
    return None


@app.route("/")
def index():
    cards_html = ""
    for c in COUNSELLORS:
        cards_html += f"""
        <div class="card">
          <div class="avatar">{c['name'][0]}</div>
          <h3>{c['name']}</h3>
          <p class="desc">{c['desc']}</p>
          <button type="button" class="contact-btn" onclick="openModal('{c['id']}', '{c['name']}')">
            Contact on WhatsApp
          </button>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Sky Education - PG Counselling</title>
      <style>{STYLE}</style>
    </head>
    <body>
      <div class="top-bar">
        <img src="/static/SKYLOGO.png" alt="Sky Education">
        <h1>Sky Education</h1>
        <p> Fill in a few quick details and you'll be connected on WhatsApp instantly.</p>
      </div>

      <main class="wrap">
        <section class="video-section">
          <h2>About Us</h2>
          {f'''<video class="video-player" controls preload="metadata">
            <source src="/static/{VIDEO_FILENAME}" type="video/mp4">
            Your browser does not support video.
          </video>''' if os.path.exists(os.path.join(app.static_folder, VIDEO_FILENAME)) else f'''<p class="video-missing">Add {VIDEO_FILENAME} to the static folder to display the video.</p>'''}
        </section>
        <div class="section-title">Admission Consultant</div>
        <div class="grid">
          {cards_html}
        </div>
        <p class="footer-note">Sky Education &mdash; Guiding students to the right PG accommodation and career path.</p>
      </main>

      <!-- Modal: the details form opens here when a counsellor button is clicked -->
      <div id="modalOverlay" class="modal-overlay">
        <div class="modal-box">
          <h3 id="modalTitle">Share your details</h3>
          <p class="modal-sub">We'll pass these on so your counsellor can assist you better.</p>
          <form id="contactForm" method="POST">
            <div class="field">
              <label>Full Name *</label>
              <input type="text" name="visitor_name" required placeholder="e.g. Ankit Kumar">
            </div>
            <div class="field">
              <label>UG College &amp; Branch *</label>
              <input type="text" name="ug_branch" required placeholder="e.g. XYZ College, Computer Science">
            </div>
            <div class="field">
              <label>Budget for PG *</label>
              <input type="text" name="budget" required placeholder="e.g. 10,000 - 15,000 / month">
            </div>
            <div class="field">
              <label>Preferred Appointment Time *</label>
              <input type="datetime-local" name="appointment_time" required>
            </div>
            <div class="modal-actions">
              <button type="button" class="cancel-btn" onclick="closeModal()">Cancel</button>
              <button type="submit" class="submit-btn">Submit &amp; Continue on WhatsApp</button>
            </div>
          </form>
        </div>
      </div>

      <script>
        function openModal(counsellorId, counsellorName) {{
          document.getElementById('modalTitle').innerText = "Connect with " + counsellorName;
          document.getElementById('contactForm').action = "/contact/" + counsellorId;
          document.getElementById('modalOverlay').style.display = "flex";
        }}
        function closeModal() {{
          document.getElementById('modalOverlay').style.display = "none";
        }}
      </script>
    </body>
    </html>
    """
    return html


@app.route("/contact/<counsellor_id>", methods=["POST"])
def contact(counsellor_id):
    counsellor = find_counsellor(counsellor_id)
    if not counsellor:
        return "Counsellor not found", 404

    visitor_name = request.form.get("visitor_name", "").strip()
    ug_branch = request.form.get("ug_branch", "").strip()
    budget = request.form.get("budget", "").strip()
    appointment_time = request.form.get("appointment_time", "").strip()

    message_lines = [
        f"New Enquiry - for {counsellor['name']}",
        f"Name: {visitor_name or '-'}",
        f"UG College / Branch: {ug_branch or '-'}",
        f"PG Budget: {budget or '-'}",
        f"Appointment Time: {appointment_time or '-'}",
    ]
    base_message = "\n".join(message_lines)

    wa_link = f"https://wa.me/{counsellor['whatsapp']}?text={quote(base_message)}"
    return redirect(wa_link)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)