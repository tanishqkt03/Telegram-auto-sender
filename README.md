
# Telegram Auto Sender

A Python-based Telegram auto-texting utility that sends messages at an exact scheduled time with millisecond precision. It includes a GUI for user-friendly scheduling.

## Features
- Sends messages at a precise scheduled time.
- Supports ultra-low latency messaging.
- GUI-based scheduling for easy use.
- Supports stopping and restarting the process.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tanishqkt03/Telegram-auto-sender.git
   cd Telegram-auto-sender
   ```

2. **Install dependencies**:
   ```bash
   pip install telethon tk
   ```

---

## Setup

### Get API Credentials from Telegram
1. Go to [my.telegram.org](https://my.telegram.org).
2. Log in with your Telegram account.
3. Navigate to **API Development Tools**.
4. Create a new application and note your **API ID** and **API Hash**.

### Configure API Credentials
- Open `auto_text_telegram.py` and `getchats.py`.
- Replace:
  ```python
  API_ID = # Your API ID
  API_HASH = ""  # Your API Hash
  ```
  with your actual API credentials.

---

## Usage

### Step 1: Retrieve Chat ID
1. Run the following command to get chat IDs:
   ```bash
   python getchats.py
   ```
2. Copy the **Chat ID** of the target conversation.

### Step 2: Configure Auto Texter
- Open `auto_text_telegram.py`.
- Replace:
  ```python
  TARGET_USER = # Your chat ID
  ```
  with the copied **Chat ID**.

### Step 3: Run the Auto Texter
1. Start the script:
   ```bash
   python auto_text_telegram.py
   ```
2. Enter your phone number when prompted.
3. Enter the OTP sent to your Telegram account to establish a session.

### Step 4: Schedule Messages
- Enter the **hour, minute, and second** for message scheduling.
- Type your message in the text box.
- Click **Start** to schedule the message.
  
  ![UI](https://github.com/user-attachments/assets/aa615bd9-176b-4bfa-9d7f-aa887e00433d)
  ![Success](https://github.com/user-attachments/assets/25f51528-4457-4253-b077-9ba80eabefd2)



---

## Notes
- The script maintains an active session after OTP verification.
- Restarting the script will not require OTP unless the session expires.
- Ensure the target time is set correctly to avoid missed messages.

---

## License
This project is open-source and available under the MIT License.

