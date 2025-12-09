from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from repo.categoria_repo import obter_todos, obter_por_id, inserir, alterar, excluir
from model.categoria_model import Categoria

admin_categorias_router = APIRouter(prefix="/admin/categorias", tags=["Admin - Categorias"])

# LISTAR CATEGORIAS
@admin_categorias_router.get("/", response_class=HTMLResponse)
async def listar_categorias(request: Request):
    categorias = obter_todos()
    return request.app.templates.TemplateResponse(
        "admin/categorias/listar.html",
        {"request": request, "categorias": categorias}
    )

# TELA DE NOVA CATEGORIA
@admin_categorias_router.get("/novo", response_class=HTMLResponse)
async def nova_categoria(request: Request):
    return request.app.templates.TemplateResponse(
        "admin/categorias/form.html",
        {"request": request, "categoria": None}
    )

# SALVAR NOVA CATEGORIA
@admin_categorias_router.post("/novo")
async def salvar_categoria(nome: str = Form(...), descricao: str = Form(None)):
    categoria = Categoria(nome=nome, descricao=descricao)
    inserir(categoria)
    return RedirectResponse("/admin/categorias/", status_code=302)

# TELA EDITAR
@admin_categorias_router.get("/editar/{id}", response_class=HTMLResponse)
async def editar_categoria(request: Request, id: int):
    categoria = obter_por_id(id)
    return request.app.templates.TemplateResponse(
        "admin/categorias/form.html",
        {"request": request, "categoria": categoria}
    )

# SALVAR EDIÇÃO
@admin_categorias_router.post("/editar/{id}")
async def salvar_edicao(id: int, nome: str = Form(...), descricao: str = Form(None)):
    categoria = Categoria(id=id, nome=nome, descricao=descricao)
    alterar(categoria)
    return RedirectResponse("/admin/categorias/", status_code=302)

# EXCLUIR
@admin_categorias_router.get("/excluir/{id}")
async def excluir_categoria(id: int):
    excluir(id)
    return RedirectResponse("/admin/categorias/", status_code=302)
