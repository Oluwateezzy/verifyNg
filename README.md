# Welcome to your Expo app 👋

## Get started
784355c7423829aa89b9ce48855924c04abe54f4
### Cloning the Repository

1. Open your terminal.
2. Navigate to the directory where you want to clone the repository.
3. Run the following command to clone the repository:

   ```bash
   git clone https://github.com/johnny-emp/thedrops-mobile
   ```

4. Navigate into the cloned directory:

   ```bash
   cd thedrops-mobile/client
   ```

### Install Dependencies

1. Install the required dependencies by running:

   ```bash
   npm install
   ```

### Start the App

1. Start the Expo app with the following command:

   ```bash
   npx expo start
   ```

In the output, you'll find options to open the app in a



# FastAPI Backend

## Step 1: Install Dependencies
Ensure you have Python installed (>= 3.8). Then, create a virtual environment and install dependencies:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
pip install -r requirements.txt
```


## Step 2: Configure `.env` File
Create a `.env` file with the following content:
```ini
DATABASE_URL=postgresql://olashina@localhost:5432/thedrop
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
INFURA_PROJECT_ID=your_infura_project_id
EXTERNAL_WALLET_ADDRESS=your_external_wallet_address
EXTERNAL_WALLET_PRIVATE_KEY=your_external_wallet_private_key
COINBASE_API_KEY=your_coinbase_api_key
COINBASE_API_SECRET=your_coinbase_api_secret
ALCHEMY_API_KEY=7-h454pdM5pPDxjmCfHaK1Ne_9VeMQgi

MAILTRAP_USERNAME=823daaeee8adb9
MAILTRAP_PASSWORD=69c365369ac1c8
MAILTRAP_HOST=sandbox.smtp.mailtrap.io
MAILTRAP_PORT=2525

TWITTER_CONSUMER_KEY=your_twitter_consumer_key
TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
GOOGLE_CLIENT_ID=your_google_client_id
```

## Step 3: Run Database Migrations
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
<!-- 
## API Endpoints
### Authentication
| Method | Endpoint          | Description |
|--------|------------------|-------------|
| POST   | `/auth/register` | Register a user |
| POST   | `/auth/login`    | User login |
| POST   | `/auth/2fa`      | Enable/verify 2FA |
| POST   | `/auth/logout`   | Logout user |

### Wallet & Transactions
| Method | Endpoint                   | Description |
|--------|---------------------------|-------------|
| GET    | `/wallet/{user_id}`        | Get user's wallet balance |
| GET    | `/wallet/{user_id}/transactions` | Get transaction history |
| POST   | `/wallet/send-crypto`      | Send crypto to another wallet |
| POST   | `/wallet/deposit-fiat`     | Deposit fiat using Onramper |
| POST   | `/wallet/withdraw-fiat`    | Withdraw fiat to a bank account |

### Trading
| Method | Endpoint     | Description |
|--------|-------------|-------------|
| POST   | `/trade/buy`  | Execute buy order |
| POST   | `/trade/sell` | Execute sell order |
| GET    | `/trade/orders` | Get user’s past trades |
 -->

uvicorn app.main:app --reload


