from application.controller import success, error
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from config.fastapi import FastapiConfig
import os, uvicorn
import pandas as pd
from pydantic import BaseModel


class LoginInputSchema(BaseModel):
    username: str
    password: str


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/auth/user/login")
async def login(word: LoginInputSchema):
    print(word)
    data = {
        'code': 200,
        'access': '04563be1c-de26-11eb-959c-b025aa405980'
    }
    return data


@app.get("/{name}")
async def redirect(name: str, request: Request):
    return templates.TemplateResponse(name + '.html', {"request": request})


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.post('/api/strategyFile')
async def upload_file(file: UploadFile = File(...)):
    """
    an example of uploading file
    :param file:
    :return:
    """
    try:
        filename = file.filename
        save_path = '%s' % FastapiConfig.MEDIA_ROOT  # pic.name 上传文件的源文件名
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        content = await file.read()
        with open(save_path + filename, 'wb') as f:
            f.write(content)
        f.close()
        data = pd.read_excel(save_path + filename)
        print(data)
        '''
        decoded_content = content.decode('utf-8')
        LOGGER.info('Received file %s:\n%s' % (
            filename,
            decoded_content
        ))
        '''
        return success(msg='Success')
    except Exception as e:
        # LOGGER.error(str(e))
        return error(msg=str(e))


if __name__ == '__main__':
    uvicorn.run(app='test-fastapi:app', reload=True, debug=True)
    # os.system('uvicorn test:app --reload')
