from app.handlers import app
from ml_models import *

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host='0.0.0.0',port=5000,debug=True)