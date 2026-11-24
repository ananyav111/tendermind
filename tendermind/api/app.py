import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from tendermind.api.routes_tenders import router as tenders_router
from tendermind.api.routes_company import router as company_router
from tendermind.api.routes_eligibility import router as eligibility_router
from tendermind.api.routes_bids import router as bids_router
from tendermind.api.routes_corrigenda import router as corrigenda_router
from tendermind.api.routes_mcp import router as mcp_router
from tendermind.api.routes_chat import router as chat_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="TenderMind API",
        description="The AI-Powered Government Tender Discovery, Eligibility Intelligence & Bid Preparation Agent for MSMEs",
        version="1.0.0"
    )

    # Enable CORS for local development and integration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routers
    app.include_router(tenders_router)
    app.include_router(company_router)
    app.include_router(eligibility_router)
    app.include_router(bids_router)
    app.include_router(corrigenda_router)
    app.include_router(mcp_router)
    app.include_router(chat_router)

    # Determine web directories
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    web_dir = os.path.join(base_dir, "web")
    static_dir = os.path.join(web_dir, "static")

    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/", include_in_schema=False)
    def serve_index():
        index_file = os.path.join(web_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"status": "TenderMind API is running. Visit /docs for OpenAPI documentation."}

    @app.get("/health")
    def health_check():
        return {
            "status": "HEALTHY",
            "system": "TenderMind AI & MCP Platform",
            "version": "1.0.0"
        }

    return app

app = create_app()
