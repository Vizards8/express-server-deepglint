# 配置文件：DbConfig
class FastapiConfig:
    debug = True
    title = 'FastAPI Base'
    description = '基于FastAPI的模板工程'
    version = '0.0.1.20201126'
    openapi_url = '/openapi.json'
    openapi_prefix = ''
    docs_url = '/docs'
    redoc_url = '/redoc'
    swagger_ui_oauth2_redirect_url = '/docs/oauth2-redirect'
    swagger_ui_init_oauth = None
    res_path = 'res'
    request_log_to_mongo = True
    MEDIA_ROOT = "./"   # excel保存目录
    express_addr = 'https://sfapi-sbox.sf-express.com/std/service'
    partnerID = 'GLSTXt'
    checkword = 'hojUhAJ6Q5Ta3WfMrITN1sa7zPW6r0op'
    monthlyCard = '7551234567'  #顺丰月结卡号