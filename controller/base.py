import time

from application.controller import success, error
from application.logger import get_controller_logger
from application import config
from fastapi import APIRouter, UploadFile, File, Request
from application.util import md5hash
from config.fastapi import FastapiConfig
import os.path
from starlette.responses import FileResponse
import asyncio
import pandas as pd

app_name = config.get('APP_NAME')

router = APIRouter()

LOGGER = get_controller_logger('BASE')

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


@router.get('/index')
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/{name}")
async def redirect(name: str, request: Request):
    return templates.TemplateResponse(name + '.html', {"request": request})


@router.get('/v1/health')
def health_check():
    """
    basic example
    :return:
    """
    return success(data={
        'name': app_name,
        'hash': md5hash(app_name),
    }, msg='Yes OK~')


@router.post('/api/strategyFile')
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
        '''
        decoded_content = content.decode('utf-8')
        LOGGER.info('Received file %s:\n%s' % (
            filename,
            decoded_content
        ))
        '''
        return success(msg='Success')
    except Exception as e:
        LOGGER.error(str(e))
        return error(msg=str(e))


@router.get('/api/strategyFile')
async def download_file():
    """
    an example of uploading file
    :param file:
    :return:
    """
    try:
        save_path = '%s' % FastapiConfig.MEDIA_ROOT  # pic.name 上传文件的源文件名
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_name = save_path + "/" + "strategy.xml"

        if os.path.isfile(file_name):
            response = FileResponse(file_name, media_type='application/octet-stream', filename="strategy.xml")
            return response
        else:
            return error("empty!")
    except Exception as e:
        LOGGER.error(str(e))
        return error(msg=str(e))


@router.post('/api/health')
async def health_test():
    """
    basic example
    :return:
    """
    time.sleep(2)
    return success(data={
        'name': app_name,
        'hash': md5hash(app_name),
    }, msg='Yes OK~')
