# HCLtech-Hackathon

# Create virtual env
python -m venv venv

# Activate Scripts
venv\Scripts\activate

# To start the Server(Backend)
> uvicorn main:app --reload

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

4. Loan application and EMI Calculator
    --> users enter loan details
    --> admin will handel check the documents and approve or reject the loan status, initially it will be on pending
5. reporting ad dashbord
    --> fetch details from the databases and give sum count or any needed informaton in the dashboard
    
# system design
    Tech stack used :  Python Fast API, Mysql, Postman or swaggerUI for api testing, pytest library for unit testing

# implementation

developed registration api (main.py)
developed login api (main.py)
developed savingsaccount api (main.py)
developed currentaccount api (main.py)
developed apply for loan api (users) (main.py)
developed admin api for handeling loan application approval (Only for admin Use) (main.py)


# testing
done unit testing passed all the test cases used pytest library (test>test_main.py)

# deployment
Local deployment



# fastapi intractive docs
Interactive docs: http://127.0.0.1:8000/docs
