# HCLtech-Hackathon

# Create virtual env
python -m venv venv

# Activate Scripts
venv\Scripts\activate

# To start the Server(Backend)
> uvicorn main:app --reload

# Packages to install
pip install fastapi uvicorn sqlalchemy mysql-connector-python pydantic


# Project Planning

 # Requirement gathering and analysis

1.user registration and kyc
 > customer registration/signup
    --> store Registred/login credentials in firebas
    --> Email verification (on clickof email link the registration details will be stored in firebas)
    --> if stored registratio credentials and login details are same then user will login
    --> Once login Ui will be like top navbar profile info
    --> home page, there will be options called complete kyc and Apply for loan(initially will be   freezed till kyc validation is completed by the auditor)

2. Accout creation -curret savings
3. Audit Logging
    > Audit the KYC details
    --> once user submits the kyc then auditor will audit
    --> If kyc details are correct then approve the user or else kyc must be updaed again with message to them in user frontend

3.Loan application and EMI Calculator (If time is remaining)
4.reporting ad dashbord
    
# system design
    Tech stack used : React+vite , Tailwindcss, Python Fast API, Mysql(kyc files, etc..), firebase(login credentails),Postman or swaggerUI for testing

# implementation
# testing
# deployment
# presentation


# fastapi intractive docs
Interactive docs: http://127.0.0.1:8000/docs
