# Welcome to your VerifyNg 👋

## Step 1: Install Dependencies
1. Open your terminal.
2. Navigate to the directory where you want to clone the repository.
3. Run the following command to clone the repository:

   ```bash
   git clone https://github.com/Oluwateezzy/verifyNg
   ```

4. Navigate into the cloned directory:

   ```bash
   cd verifyNg
   ```

## Step 2: Install Dependencies
Ensure you have Python installed (>= 3.8). Then, create a virtual environment and install dependencies:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
pip install -r requirements.txt
```


## Step 3: Configure `.env` File
Create a `.env` file with the following content:
```ini
# DATABASE_URL=postgresql://oluwatobiloba@localhost:5432/verifyNG
DATABASE_URL=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SECRET_KEY=your_secret_key_here

DO_SPACES_ACCESS_KEY=
DO_SPACES_REGION=
DO_SPACES_ENDPOINT=
DO_SPACES_SECRET=
DO_SPACES_BUCKET=

MAILTRAP_USERNAME=7ac01ce26691b8
MAILTRAP_PASSWORD=d7c1093d0fa9ca
MAILTRAP_HOST=sandbox.smtp.mailtrap.io
MAILTRAP_PORT=2525

TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
ENCRYPTOR_SECRET_KEY=
REDIS_URL=
```

## Step 4: Run Database Migrations
Initialize Alembic and run migrations:
```sh
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Step 4: Run the Application
Start FastAPI with Uvicorn:
```sh
uvicorn app.main:app --reload
```
