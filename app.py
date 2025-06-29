<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Order Autodesk Software | Neo Education</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Order your Autodesk student license easily and securely with Neo Education. Fast processing, multiple payment methods, and full support.">
    <link rel="stylesheet" href="style.css">
    <link rel="icon" href="/favicon.ico" type="image/x-icon">
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(120deg, #fdf6e3 0%, #c0eaff 100%);
            margin: 0;
            min-height: 100vh;
        }
        .container {
            background: #fff;
            max-width: 500px;
            margin: 30px auto 20px auto;
            padding: 2rem 2.5rem 2.5rem 2.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 32px rgba(0,0,0,0.08);
        }
        h1 {
            text-align: center;
            color: #1957a8;
            margin-bottom: 0.4em;
        }
        .subtitle {
            text-align: center;
            margin-top: 0;
            color: #555;
            font-size: 1.09em;
            margin-bottom: 1.5em;
        }
        form label {
            font-size: 1em;
            color: #234;
            display: block;
            margin-bottom: 0.2em;
            margin-top: 1.2em;
        }
        input, select, textarea {
            width: 100%;
            padding: 0.65em 0.7em;
            font-size: 1em;
            border: 1px solid #b9d8f6;
            border-radius: 8px;
            margin-bottom: 0.35em;
            box-sizing: border-box;
            background: #fafdff;
            transition: border 0.2s;
        }
        input:focus, select:focus, textarea:focus {
            border: 1.5px solid #1957a8;
            outline: none;
        }
        button[type="submit"] {
            width: 100%;
            padding: 0.8em;
            margin-top: 1.2em;
            border: none;
            border-radius: 8px;
            background: linear-gradient(90deg, #1957a8 70%, #42c6ff 100%);
            color: #fff;
            font-size: 1.14em;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
            box-shadow: 0 2px 8px rgba(33, 85, 188, 0.08);
        }
        button[disabled] {
            background: #a6b3c2;
            cursor: not-allowed;
        }
        .success, .error {
            text-align: center;
            padding: 0.8em 0.3em;
            border-radius: 8px;
            margin-top: 1em;
            font-weight: 600;
        }
        .success { background: #e6fbec; color: #188142; }
        .error   { background: #ffeaea; color: #a52222; }
        .howto {
            margin: 2.5em auto 1.5em auto;
            background: #e3f1ff;
            border-left: 5px solid #1957a8;
            padding: 1.1em 1.3em;
            border-radius: 8px;
            font-size: 1.07em;
        }
        .contact-options {
            margin-top: 2em;
            text-align: center;
            font-size: 0.98em;
        }
        .contact-options a {
            color: #1957a8;
            text-decoration: underline;
            margin: 0 0.7em;
        }
        @media (max-width: 600px) {
            .container { max-width: 97vw; padding: 1.25em 0.7em 2em 0.7em;}
            .howto { font-size: 0.98em; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Order Your Autodesk License</h1>
        <div class="subtitle">Fast, secure, and verified student licenses with Neo Education</div>

        <form id="orderForm" autocomplete="off">
            <label for="prenom">First Name</label>
            <input type="text" id="prenom" name="prenom" required maxlength="32">

            <label for="nom">Last Name</label>
            <input type="text" id="nom" name="nom" required maxlength="32">

            <label for="email">Student Email</label>
            <input type="email" id="email" name="email" required maxlength="60" placeholder="your@student.edu">

            <label for="phone">Phone &amp; WhatsApp</label>
            <input type="tel" id="phone" name="phone" required maxlength="22" pattern="^\+?\d{8,22}$" placeholder="+213XXXXXXXXX">

            <label for="logiciel">Choose Software</label>
            <select id="logiciel" name="logiciel" required>
                <option value="" disabled selected>Select one</option>
                <option>AutoCAD</option>
                <option>Revit</option>
                <option>3ds Max</option>
                <option>Maya</option>
                <option>Navisworks</option>
                <option>Inventor</option>
                <option>MotionBuilder</option>
                <option>Fusion 360</option>
                <option>Flame</option>
                <option>Architecture Pack</option>
                <option>Construction and BIM</option>
                <option>Animation and VFX</option>
            </select>

            <label for="paiment">Payment Method</label>
            <select id="paiment" name="paiment" required>
                <option value="" disabled selected>Select payment method</option>
                <option>BaridiMob</option>
                <option>CIB</option>
                <option>CCP</option>
                <option>PayPal</option>
                <option>Wise</option>
                <option>Western Union</option>
            </select>

            <label for="contact_Method">Preferred Contact</label>
            <select id="contact_Method" name="contact_Method" required>
                <option value="" disabled selected>Select contact method</option>
                <option>Email</option>
                <option>WhatsApp</option>
                <option>Telegram</option>
                <option>Phone Call</option>
            </select>

            <label for="message">Any Notes? (optional)</label>
            <textarea id="message" name="message" rows="2" maxlength="300" placeholder="E.g. Need Revit 2024, urgent, etc."></textarea>

            <!-- Simple Math CAPTCHA -->
            <label id="captcha-label"></label>
            <input type="number" id="captcha-answer" name="captcha_answer" required placeholder="Your answer">
            <input type="hidden" id="captcha-num1" name="captcha_num1">
            <input type="hidden" id="captcha-num2" name="captcha_num2">

            <button type="submit" id="submitBtn">Send Order</button>
            <div id="formMessage"></div>
        </form>

        <div class="howto">
            <b>How to order?</b>
            <ol>
                <li>Fill out your details and select your Autodesk software.</li>
                <li>Choose your payment and contact preference.</li>
                <li>After submitting, our team will contact you to confirm your order and guide you through payment.</li>
                <li>You’ll receive your official student license in 1–12 hours after payment.</li>
            </ol>
            <div style="margin-top:0.7em; color:#1957a8;"><b>Questions?</b> Contact us anytime!</div>
        </div>

        <div class="contact-options">
            <a href="mailto:support@neoedu.xyz">Email Support</a>
            <a href="https://wa.me/213774338328" target="_blank">WhatsApp</a>
            <a href="https://t.me/neoedualgeria" target="_blank">Telegram</a>
        </div>
    </div>

    <script>
        // Pre-select logiciel if param in URL
        window.onload = function() {
            // Set up CAPTCHA
            setCaptcha();

            // Pre-select software
            const params = new URLSearchParams(window.location.search);
            const soft = params.get('logiciel');
            if (soft) {
                const select = document.getElementById('logiciel');
                for (let i = 0; i < select.options.length; i++) {
                    if (select.options[i].value.toLowerCase() === soft.toLowerCase()) {
                        select.selectedIndex = i;
                        break;
                    }
                }
            }
        };

        // Math CAPTCHA logic
        function setCaptcha() {
            const num1 = Math.floor(Math.random() * 8) + 2; // 2-9
            const num2 = Math.floor(Math.random() * 8) + 2;
            document.getElementById('captcha-label').innerText = `What is ${num1} + ${num2}?`;
            document.getElementById('captcha-num1').value = num1;
            document.getElementById('captcha-num2').value = num2;
        }

        // Form submission
        document.getElementById('orderForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const submitBtn = document.getElementById('submitBtn');
            const msgDiv = document.getElementById('formMessage');
            msgDiv.textContent = "";
            submitBtn.disabled = true;
            submitBtn.textContent = "Sending...";

            // Gather form data
            const formData = {
                prenom: document.getElementById('prenom').value.trim(),
                nom: document.getElementById('nom').value.trim(),
                email: document.getElementById('email').value.trim(),
                phone: document.getElementById('phone').value.trim(),
                logiciel: document.getElementById('logiciel').value,
                paiment: document.getElementById('paiment').value,
                contact_Method: document.getElementById('contact_Method').value,
                message: document.getElementById('message').value.trim(),
                captcha_num1: document.getElementById('captcha-num1').value,
                captcha_num2: document.getElementById('captcha-num2').value,
                captcha_answer: document.getElementById('captcha-answer').value.trim()
            };

            // Client-side basic validation
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
                msgDiv.innerHTML = '<div class="error">Please enter a valid email address.</div>';
                submitBtn.disabled = false; submitBtn.textContent = "Send Order"; return;
            }
            if (!/^\+?\d{8,22}$/.test(formData.phone)) {
                msgDiv.innerHTML = '<div class="error">Please enter a valid phone/WhatsApp number.</div>';
                submitBtn.disabled = false; submitBtn.textContent = "Send Order"; return;
            }

            // Submit to API
            try {
                const response = await fetch('/order', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                const data = await response.json();
                if (data.success) {
                    msgDiv.innerHTML = `<div class="success">Order received!<br>Your order number: <b>${data.commande_number}</b><br>We will contact you soon.</div>`;
                    document.getElementById('orderForm').reset();
                    setCaptcha();
                    setTimeout(() => { window.location.href = data.redirect || "/thankyou.html"; }, 2600);
                } else {
                    msgDiv.innerHTML = `<div class="error">${data.error || "Submission failed. Please try again."}</div>`;
                    setCaptcha();
                }
            } catch (err) {
                msgDiv.innerHTML = `<div class="error">Could not submit order. Try again later.</div>`;
                setCaptcha();
            }
            submitBtn.disabled = false;
            submitBtn.textContent = "Send Order";
        });
    </script>
</body>
</html>
