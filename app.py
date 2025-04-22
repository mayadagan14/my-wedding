from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

@app.route("/")
def intro():
    html = """
    <!DOCTYPE html>
    <html lang="he">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ברוכים הבאים</title>
        <style>
            body {
                margin: 0;
                font-family: 'Varela Round', sans-serif;
                text-align: center;
                background-color: #dec8ae;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                overflow: hidden;
            }
            h1 {
                color: #7a3e3e;
                font-size: 32px;
                margin-top: 20px;
            }
            img {
                max-width: 90%;
                max-height: 80vh;
                border-radius: 16px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
            }
            @media screen and (max-width: 600px) {
                h1 {
                    font-size: 24px;
                }
            }
        </style>
        <script>
            setTimeout(() => {
                window.location.href = "/gallery";
            }, 4000);
        </script>
        <link href="https://fonts.googleapis.com/css2?family=Varela+Round&display=swap" rel="stylesheet">
    </head>
    <body>
        <img src="/static/cover.jpg" alt="תמונת פתיחה">
        <h1>החתונה של מאיה וסתיו – 28.04.2025 💍</h1>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/gallery")
def gallery():
    image_folder = "images"
    images = [f for f in os.listdir(image_folder) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]

    html = """
    <!DOCTYPE html>
    <html lang="he">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>גלריה</title>
        <link href="https://fonts.googleapis.com/css2?family=Varela+Round&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Varela Round', sans-serif;
                direction: rtl;
                background-color: #fdf7f2;
                text-align: center;
                margin: 0;
            }
            header {
                background-color: #dec8ae;
                color: #7a3e3e;
                padding: 30px 20px;
                text-align: center;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
                font-size: 26px;
                border-bottom: 10px solid #efe0c8;
            }
            .gallery {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                padding: 20px;
            }
           .gallery-item {
    aspect-ratio: 1 / 1;
    position: relative;
    border-radius: 14px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.05);
    overflow: hidden;
    background: white;
    border: 1px solid #f0e6e6;
    display: flex;
    align-items: center;
    justify-content: center;
}

.gallery-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    cursor: pointer;
}

          .download {
    position: absolute;
    bottom: 10px;
    right: 10px;
    font-size: 26px;
    color: white;
    background: transparent; /* ללא רקע */
    border: none;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    transition: transform 0.2s;
}
.download:hover {
    transform: scale(1.2);
}


            #modal {
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0; top: 0;
                width: 100%; height: 100%;
                background-color: rgba(0,0,0,0.9);
                justify-content: center;
                align-items: center;
            }
            #modal img {
                max-width: 80%;
                max-height: 80%;
                border-radius: 10px;
                transition: opacity 0.4s ease-in-out;
            }
            .close, .arrow {
                position: absolute;
                color: white;
                font-size: 40px;
                cursor: pointer;
                user-select: none;
            }
            .close { top: 20px; right: 30px; }
            .arrow.left { left: 30px; }
            .arrow.right { right: 30px; }

            @media screen and (max-width: 600px) {
                header {
                    font-size: 22px;
                    padding: 20px 10px;
                }
                .download {
                    font-size: 14px;
                    padding: 4px 8px;
                }
            }
        </style>
    </head>
    <body>
        <header>
          💍 החתונה של מאיה וסתיו – 28.04.2025 💍
        </header>
        <div class="gallery">
            {% for img in images %}
            <div class="gallery-item">
                <img src="/images/{{ img }}" alt="תמונה" onclick="openModal({{ loop.index0 }})">
                <a class="download" href="/images/{{ img }}" download title="הורדה"><svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="white">
  <path d="M5 20h14v-2H5v2zm7-18L5.33 9h3.92v6h5.5V9h3.92L12 2z" fill="black"/>
</svg>
</a>
            </div>
            {% endfor %}
        </div>

        <div id="modal" onclick="closeModal(event)">
            <span class="close" onclick="closeModal(event)">✖</span>
            <span class="arrow left" onclick="prevImage()">❮</span>
            <img id="modal-img">
            <span class="arrow right" onclick="nextImage()">❯</span>
        </div>

        <script>
            const images = [{% for img in images %}'/images/{{ img }}'{% if not loop.last %}, {% endif %}{% endfor %}];
            let currentIndex = 0;

            function openModal(index) {
                currentIndex = index;
                const modalImg = document.getElementById('modal-img');
                modalImg.style.opacity = 0;
                document.getElementById('modal').style.display = 'flex';
                setTimeout(() => {
                    modalImg.src = images[index];
                    modalImg.style.opacity = 1;
                }, 100);
            }

            function closeModal(event) {
                if (event.target.id === "modal" || event.target.className === "close") {
                    document.getElementById('modal').style.display = 'none';
                }
            }

            function nextImage() {
                currentIndex = (currentIndex + 1) % images.length;
                document.getElementById('modal-img').src = images[currentIndex];
            }

            function prevImage() {
                currentIndex = (currentIndex - 1 + images.length) % images.length;
                document.getElementById('modal-img').src = images[currentIndex];
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html, images=images)

@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(debug=True)
