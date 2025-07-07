from fastapi import FastAPI, Request
import httpx
import asyncio

app = FastAPI()

@app.post("/tunnel")
async def tunnel(request: Request):
    try:
        # Recebe os dados encapsulados (JSON ou binário)
        data = await request.body()

        # Decodifica destino + conteúdo
        lines = data.decode(errors='ignore').split('\n')
        target_line = lines[0].strip()
        payload = '\n'.join(lines[1:]).encode()

        # target_line format: METHOD|host|port|path
        method, host, port, path = target_line.split('|')
        port = int(port)

        url = f"http://{host}:{port}{path}"

        async with httpx.AsyncClient() as client:
            if method.upper() == "GET":
                r = await client.get(url)
            elif method.upper() == "POST":
                r = await client.post(url, content=payload)
            else:
                return {"error": "Método inválido"}

        return r.content

    except Exception as e:
        return {"error": str(e)}
