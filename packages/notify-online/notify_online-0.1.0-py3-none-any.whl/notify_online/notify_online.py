from flask import Flask, render_template_string
from jinja2.exceptions import *
from hashlib import sha256
import os
import time
from flask_cors import CORS
from flask_mail import Mail, Message
import socket
import requests
import logging

def create_app() -> Flask | None:
    app = Flask(__name__)
    CORS(app, support_credentials=True, resources={r"/api/*": {"origins": "*"}})
    app.secret_key = sha256(str(time.time()).encode("utf-8")).hexdigest()
    app.config.update(
        MAIL_SERVER=os.environ.get("MAIL_SERVER", "smtp.gmail.com"),
        MAIL_PORT=int(os.environ.get("MAIL_PORT", 587)),
        MAIL_USERNAME=os.environ.get("MAIL_USERNAME", None),
        MAIL_RECEIPIENT=os.environ.get("MAIL_RECEIPIENT", None),
        MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD", None),
        MAIL_USE_TLS=bool(int(os.environ.get("MAIL_USE_TLS", True))),
        MAIL_USE_SSL=bool(int(os.environ.get("MAIL_USE_SSL", False))),
        HOSTNAME=socket.gethostname(),
    )
    if (
        (app.config["MAIL_USERNAME"] is None)
        or (app.config["MAIL_RECEIPIENT"] is None)
        or (app.config["MAIL_PASSWORD"] is None)
    ):
        logging.error("Lack email information")
        return None
    else:
        return app

def send_email() -> bool:
    logging.basicConfig(
        format="%(asctime)s [%(levelname)-8s] %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    app = create_app()
    if app is None:
        return False

    mail = Mail(app)
    with app.app_context():
        try:
            msg = Message(f"{socket.gethostname()} is online", sender=app.config["MAIL_USERNAME"], recipients=[app.config["MAIL_RECEIPIENT"]])
            msg.body = "Your device is now online."
            msg.html =             render_template_string(
                """
                <!DOCTYPE html>
                <html lang="en">

                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Device Online Notification</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.11.3/font/bootstrap-icons.css">
                </head>

                <body style="font-family: 'Trebuchet MS', sans-serif;">
                    <div class="container-md mt-5">
                        <div class="row justify-content-center">
                            <div class="col">
                                <div class="col-md-8 border rounded-4 p-3 mx-auto align-items-center justify-content-center">
                                    <div class="mt-4 mb-5 navbar-brand d-flex align-items-center justify-content-center" href="#">
                                        <svg xmlns="http://www.w3.org/2000/svg" version="1.0" height="50" viewBox="0 0 1303.000000 503.000000" preserveAspectRatio="xMidYMid meet"  fill="#310443" data-darkreader-inline-fill="" style="--darkreader-inline-fill: #0054cc; padding-left: 12px;">
                                            <g transform="translate(0.000000,503.000000) scale(0.100000,-0.100000)" fill="#310443" stroke="none">
                                                <path d="M1167 4948 c20 -263 79 -1124 77 -1127 -1 -1 -220 143 -486 321 -266 178 -487 327 -493 330 -9 5 -235 -364 -243 -396 -1 -6 236 -130 528 -276 291 -146 530 -267 530 -270 0 -3 -239 -122 -530 -265 -292 -143 -530 -263 -530 -266 0 -21 211 -394 222 -393 7 1 233 144 502 318 269 174 490 315 492 314 3 -4 -60 -1022 -70 -1130 l-6 -58 250 0 c232 0 250 1 250 18 0 9 -18 276 -40 592 -21 316 -37 576 -36 578 2 1 219 -140 482 -314 263 -174 483 -318 490 -321 14 -5 247 398 236 408 -4 4 -239 118 -522 254 -283 136 -519 251 -524 256 -6 5 48 36 135 78 79 38 320 156 536 263 l392 194 -120 210 c-65 115 -125 208 -132 208 -6 -1 -230 -148 -496 -328 -266 -180 -484 -326 -485 -324 -1 2 17 260 40 573 24 314 43 580 43 593 l1 22 -249 0 -249 0 5 -62z"/>
                                                <path d="M10320 4545 l0 -75 238 -2 237 -3 3 -2117 2 -2118 -240 0 -240 0 0 -80 0 -80 555 0 555 0 0 80 0 80 -240 0 -240 0 0 2195 0 2195 -315 0 -315 0 0 -75z"/>
                                                <path d="M11910 4545 l0 -75 238 -2 237 -3 3 -2117 2 -2118 -240 0 -240 0 0 -80 0 -80 555 0 555 0 0 80 0 80 -240 0 -240 0 0 2195 0 2195 -315 0 -315 0 0 -75z"/>
                                                <path d="M5230 3280 c-286 -25 -500 -119 -688 -304 -98 -95 -157 -175 -222 -298 l-48 -90 -6 138 c-3 77 -9 221 -12 322 l-6 182 -304 0 -304 0 0 -80 0 -80 240 0 240 0 0 -1420 0 -1420 -240 0 -240 0 0 -80 0 -80 555 0 555 0 0 80 0 80 -240 0 -240 0 0 906 0 906 25 122 c55 274 160 498 310 666 75 83 144 137 242 188 243 125 613 148 860 53 169 -66 317 -201 396 -363 53 -107 78 -189 109 -349 21 -111 21 -136 25 -1121 l4 -1008 -235 0 -236 0 0 -80 0 -80 550 0 550 0 0 80 0 80 -234 0 -235 0 -3 978 c-4 872 -6 990 -22 1102 -74 519 -274 808 -641 923 -136 42 -341 62 -505 47z"/>
                                                <path d="M6740 3150 l0 -80 210 0 209 0 4 -982 c4 -1068 3 -1044 62 -1279 80 -318 229 -536 459 -671 264 -155 690 -171 1030 -36 212 83 409 249 522 441 l51 86 6 -77 c4 -42 9 -168 13 -279 l7 -203 303 0 304 0 0 80 0 80 -240 0 -240 0 0 1500 0 1500 -315 0 -315 0 0 -80 0 -80 240 0 240 0 0 -1004 0 -1003 -24 -96 c-53 -206 -137 -366 -266 -501 -199 -209 -431 -295 -795 -296 -244 0 -408 59 -561 203 -170 159 -260 362 -310 697 -15 101 -18 240 -21 1138 l-4 1022 -285 0 -284 0 0 -80z"/>
                                            </g>
                                        </svg>
                                    </div>
                                    <div class="col-md-12 indented-content">
                                        <h2 class="mb-5 d-flex align-items-center justify-content-center">
                                            <span>{{ device_name }} is online!</span>
                                        </h2>
                                    </div>
                                    <div class="offset-md-1 col-md-10 indented-content">
                                        <p style="color: #665c78; font-size: 16px" class="mb-3 d-flex">Dear Koi,</p>
                                        <p style="color: #665c78; font-size: 16px" class="mb-3 d-flex">We are pleased to inform you that your device is now online.</p>
                                        <p style="color: #665c78; font-size: 16px" class="mb-3 d-flex">Host Name: <strong>{{ hostname }}</strong></p>
                                    </div>
                                    <div class="offset-md-3 col-md-6 indented-content" style="margin-top: 5rem; margin-bottom: 5rem">
                                        <button id="submit-btn" type="button" class="btn btn-success btn-lg custom-btn w-100 d-flex align-items-center justify-content-center" onclick="window.location.href='#'">ONLINE</button>
                                    </div>
                                    <div class="offset-md-1 col-md-10 indented-content">
                                        <p style="color: #665c78; font-size: 16px" class="mb-3 d-flex">If you did not expect this notification, please check your device and network settings.</p>
                                    </div>
                                    <div class="offset-md-1 col-md-10 indented-content" style="margin-bottom: 4rem;">
                                        <p style="color: #665c78; font-size: 16px" class="mb-1 d-flex">REGARDS,</p>
                                        <p style="color: #665c78; font-size: 16px" class="mb-3 d-flex">nullptr team.</p>
                                    </div>
                                    <!-- Icon list -->
                                    <div class="d-flex justify-content-center">
                                        <a href="https://www.facebook.com/datlt4/" target="_blank"><i class="bi bi-facebook mx-2" style="color: #3b5997; font-size: 24px;"></i></a>
                                        <a href="https://www.instagram.com/datlt4/" target="_blank"><i class="bi bi-instagram mx-2" style="color: #fc5217; font-size: 24px;"></i></a>
                                        <a href="https://github.com/datlt4" target="_blank"></a><i class="bi bi-github mx-2" style="color: #010409; font-size: 24px;"></i></a>
                                        <a href="https://www.linkedin.com/in/luong-tan-dat-674277a1/" target="_blank"></a><i class="bi bi-linkedin mx-2" style="color: #0078b3; font-size: 24px;"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </body>

                </html>
                """,
                device_name=socket.gethostname().upper(),
                hostname=socket.gethostname()
            )

            mail.send(msg)
            logging.info("Sent email to " +  ", ".join([app.config["MAIL_RECEIPIENT"]]) + " successfully")
            return True
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            return False

def check_internet() -> bool:
    url = "http://www.google.com"
    timeout = 15
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
    except Exception:
        return False


def notify_online() -> None:
    logging.basicConfig(
        format="%(asctime)s [%(levelname)-8s] %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    previous_status = False

    while True:
        current_status = check_internet()
        logging.info(f"Current status: {'ONLINE' if current_status else 'ONLINE'}")
        if not previous_status and current_status:
            ec = send_email()
            if not ec:
                break

        previous_status = current_status
        time.sleep(60)  # Check every 60 seconds