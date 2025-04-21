from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from database.database import get_db
from models.company import Company
from models.investor import Investor
from schemas.company import CompanyCreate, CompanyResponse
from schemas.investor import InvestorCreate, InvestorResponse
from schemas.auth import Token
from typing import Union

# 🔐 Konstanter
SECRET_KEY = "mysecretkey"  # Skift denne i produktion
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 🔑 Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🛠 OAuth2 Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 🚀 FastAPI Router
auth_router = APIRouter(tags=["Auth"])

# ✅ Hashing og verifikation af passwords
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# ✅ Hent investor via email
async def get_investor_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Investor).where(Investor.email == email))
    return result.scalars().first()

# ✅ Hent company via email
async def get_company_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Company).where(Company.business_email == email))
    return result.scalars().first()

# ✅ SIGNUP FOR INVESTOR (kun nødvendige felter)
@auth_router.post("/signup/investor", response_model=InvestorResponse)
async def signup_investor(investor_data: InvestorCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_investor_by_email(db, investor_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Investor already exists")

    hashed_pw = get_password_hash(investor_data.password)
    new_investor = Investor(
        name=investor_data.name,
        firstname=investor_data.firstname,
        lastname=investor_data.lastname,
        email=investor_data.email,
        password=hashed_pw,
        country=investor_data.country
    )

    db.add(new_investor)
    await db.commit()
    await db.refresh(new_investor)
    
    return new_investor

# ✅ SIGNUP FOR COMPANY (kun nødvendige felter)
@auth_router.post("/signup/company", response_model=CompanyResponse)
async def signup_company(company_data: CompanyCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_company_by_email(db, company_data.business_email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Company already exists")

    hashed_pw = get_password_hash(company_data.password)
    new_company = Company(
        name=company_data.name,
        business_email=company_data.business_email,
        country=company_data.country,
        firstname=company_data.firstname,
        lastname=company_data.lastname,
        password=hashed_pw
    )

    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)
    return new_company

# ✅ LOGIN (Fungerer for både Investor og Company)
@auth_router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    email = form_data.username  
    user = await get_investor_by_email(db, email) or await get_company_by_email(db, email)
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_type = "company" if isinstance(user, Company) else "investor"
    
    access_token = create_access_token(
        data={"sub": email, "type": user_type, "id": user.id}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer", "user_type": user_type}

# ✅ TOKEN FUNKTIONER
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    print(f"Incoming token: {token}")  # 🔥 Debugging: Se om frontend sender tokenet korrekt

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        print(f"Decoded token: {payload}")  # 🔥 Debugging: Se hvad der kommer ud af token

        if email is None:
            raise credentials_exception
    except JWTError as e:
        print(f"JWT Error: {e}")  # 🔥 Debugging: Hvis token ikke kan valideres
        raise credentials_exception
    
    user = await get_investor_by_email(db, email) or await get_company_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user


# ✅ GET CURRENT USER INFO
@auth_router.get("/user")
async def get_user_data(current_user: Union[Company, Investor] = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "firstname": current_user.firstname,
        "lastname": current_user.lastname,
        "email": current_user.business_email if isinstance(current_user, Company) else current_user.email,
        "user_type": "company" if isinstance(current_user, Company) else "investor"
    }
