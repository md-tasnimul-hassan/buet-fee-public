from playwright.sync_api import sync_playwright, Page, expect
from bs4 import BeautifulSoup
import json 
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

def sendMail(address, student_name, amount):
    subject = "Dining Fee Due !"

    # Plain-text fallback
    text = f"""
Dear {student_name},

This is a reminder that your dining fee currently has a due balance.

Amount Due: BDT {amount}

If you have already made this payment, please disregard this message.

Regards,
Md. Tasnimul Hassan

This is an automated notification. Please do not reply to this email.
""".strip()

    # HTML template from your final code
    html = f"""
<html>
  <body style="margin:0; padding:0; background-color:#f5f7fa; font-family: Arial, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f5f7fa; padding:20px;">
      <tr>
        <td align="center">
          <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.05);">

            <!-- Header -->
            <tr>
              <td style="background-color:#0d47a1; padding:20px; color:#ffffff; text-align:center;">
                <h2 style="margin:0; font-weight:normal;">Dining Fee Notification</h2>
              </td>
            </tr>

            <!-- Body -->
            <tr>
              <td style="padding:30px; color:#333333;">
                <p style="font-size:15px; margin-top:0;">Dear {student_name},</p>

                <p style="font-size:15px;">
                  This is a reminder that your dining fee currently has a due balance.
                </p>

                <table width="100%" cellpadding="0" cellspacing="0" style="margin:20px 0;">
                  <tr>
                    <td style="background-color:#f0f3f7; padding:15px; border-radius:6px; text-align:center;">
                      <p style="margin:0; font-size:14px; color:#555555;">Amount Due</p>
                      <p style="margin:5px 0 0 0; font-size:22px; font-weight:bold; color:#d32f2f;">
                        BDT {amount}
                      </p>
                    </td>
                  </tr>
                </table>

                <p style="font-size:15px;">
                  If you have already made this payment, please disregard this message.
                </p>

                <p style="font-size:15px; margin-bottom:0;">
                  Regards,<br>
                  <strong>Md. Tasnimul Hassan</strong>
                </p>
              </td>
            </tr>

            <!-- Footer -->
            <tr>
              <td style="background-color:#f0f3f7; padding:15px; text-align:center; font-size:12px; color:#777777;">
                This is an automated notification. Please do not reply to this email.
              </td>
            </tr>

          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""

    sender = "notify.tasnimul@gmail.com"
    app_password = os.getenv("MAIL_PASS")
    receiver = address

    # Create a multipart/alternative email (text + HTML)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    # Attach both plain text and HTML versions
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    # Send the email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, app_password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()


def errorMail(address, e):
    payload = f"{e}"
    payload += "\nMd. Tasnimul Hassan"

    sender = "notify.tasnimul@gmail.com"
    app_password = os.getenv("MAIL_PASS")
    receiver = address

    msg = MIMEText(payload)
    msg["Subject"] = "Error in dining-fee app"
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, app_password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()

def main():
    with open("db.json", "r") as f:
        db = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for student_id in db:
            try:
                page.goto(
                    "https://billpay.sonalibank.com.bd/BUET/Fee",
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                page.get_by_role("textbox", name="Student ID*").fill(student_id)
                page.get_by_label("Fee Type").select_option("DF")
                page.get_by_role("textbox", name="Mobile No*").fill("01500000000")
                page.get_by_role("button", name="Check").click()
                time.sleep(10)
                soup = BeautifulSoup(page.content(), "html.parser")
                name = soup.find("input", id="PayBillModel_StudentName")["value"]
                amount = soup.find("div", id="search_result")
                amount = float(soup.find("input", id="PayBillModel_Amount")["value"])
                if(amount > 0.00):
                   sendMail(db[student_id], name, amount) 
            except Exception as e:
                errorMail("hassan.21.mf@gmail.com", str(e))
                pass

        browser.close()


if __name__ == "__main__":
    main()
