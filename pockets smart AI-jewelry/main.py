from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return RedirectResponse("/login")

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse(request, "login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request):
    return RedirectResponse("/dashboard", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard.html", {"request": request})

@app.get("/planner/{cat}", response_class=HTMLResponse)
async def planner_get(request: Request, cat: str):
    return templates.TemplateResponse(request, f"{cat}.html", {"request": request, "budget": 0, "ideas": []})

@app.post("/planner/{cat}", response_class=HTMLResponse)
async def planner_post(request: Request, cat: str, budget: int = Form(0)):
    b = budget
    if cat == "home":
        ideas = [("Earthy Curtains", f"Rs. {int(b*0.12)}", "Cozy look varum da!"), ("Warm LED Lights", f"Rs. {int(b*0.15)}", "Veedu glow aagum da!"), ("Jute Rug", f"Rs. {int(b*0.18)}", "Natural vibe da!")] if b>0 else []
    elif cat == "jewellery":
        ideas = [("Gold Plated Bridal Jhumka", "Rs. 21000", "Perfect for wedding da!"), ("Kundan Choker", "Rs. 18000", "Trendy da!"), ("Temple Full Set", "Rs. 21000", "Antique da!")] if b>0 else []
    else:
        ideas = [("Balloon Decoration", f"Rs. {int(b*0.10)}", "Party mass look da!"), ("Snack Table", f"Rs. {int(b*0.25)}", "Enjoy da!"), ("DJ Lights", f"Rs. {int(b*0.20)}", "Kuthu dance da!")] if b>0 else []
    return templates.TemplateResponse(request, f"{cat}.html", {"request": request, "budget": b, "ideas": ideas})

@app.get("/planner", response_class=HTMLResponse)
async def old_planner_get(request: Request):
    return templates.TemplateResponse(request, "jewellery.html", {"request": request, "budget": 0, "ideas": []})

@app.post("/planner", response_class=HTMLResponse)
async def old_planner_post(request: Request, budget: int = Form(0)):
    b = budget
    ideas = [("Gold Plated Bridal Jhumka", "Rs. 21000", "Perfect for wedding da!"), ("Kundan Choker", "Rs. 18000", "Trendy da!"), ("Temple Full Set", "Rs. 21000", "Antique da!")] if b>0 else []
    return templates.TemplateResponse(request, "jewellery.html", {"request": request, "budget": b, "ideas": ideas})
