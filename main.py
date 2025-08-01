from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import stripe
import os
from dotenv import load_dotenv

# Carrega as variáveis .env
load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ideal: ["https://morango.posolutionstech.com.br"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota para a home (index.html)
@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

# Rota para o sucesso (sucesso.html)
@app.get("/sucesso.html")
def serve_sucesso():
    return FileResponse("static/sucesso.html")

# Rota do Stripe
@app.post("/create-checkout-session")
async def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "brl",
                    "unit_amount": 899,  # R$8,99 em centavos
                    "product_data": {
                        "name": "eBook Morango do Amor",
                        "description": "3 receitas com recheios cremosos, caldas brilhantes e acabamento gourmet — incluindo brigadeiro de maracujá e caramelo rosé.",
                        "images": ["https://morango.posolutionstech.com.br/static/capa_ebook_morango.png"]  # URL pública da imagem
                    },
                },
                "quantity": 1,
            }],
            success_url="https://morango.posolutionstech.com.br/success.html",
            cancel_url="https://morango.posolutionstech.com.br",
        )

        return JSONResponse({"url": session.url})
    except Exception as e:
        print("❌ Stripe Error:", str(e))
        return JSONResponse({"error": str(e)}, status_code=500)
