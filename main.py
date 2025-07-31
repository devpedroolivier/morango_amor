from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import stripe
import os
from dotenv import load_dotenv

# 🔐 Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# 💳 Define a chave secreta do Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# 🚀 Inicia a aplicação FastAPI
app = FastAPI()

# 🌐 Middleware de CORS — ajuste depois para permitir só seu domínio real
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Recomendado: ["https://morango.posolutionstech.com.br"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend estático
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# 📦 Endpoint para criar a sessão de pagamento
@app.post("/create-checkout-session")
async def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "brl",
                    "product_data": {
                        "name": "eBook Morango do Amor",
                        "description": "3 receitas especiais com brigadeiro e caramelo rosé",
                    },
                    "unit_amount": 899,  # R$8,99 em centavos
                },
                "quantity": 1,
            }],
            success_url="https://posolutionstech.com.br/morango/sucesso.html",
            cancel_url="https://posolutionstech.com.br/morango/cancelado",
        )
        return JSONResponse({"url": session.url})
    except Exception as e:
        print("Erro ao criar sessão do Stripe:", str(e))  # para log em terminal
        return JSONResponse({"error": "Erro ao criar sessão de pagamento."}, status_code=500)
