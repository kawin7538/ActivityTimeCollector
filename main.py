from app.handlers import app
from ml_models import *
import os

if __name__ == '__main__':
    import uvicorn
    port=int(os.environ.get('PORT',5000))
    uvicorn.run(app,host='0.0.0.0',port=port,debug=True)