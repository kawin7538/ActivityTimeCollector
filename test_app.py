from fastapi.testclient import TestClient
from app.handlers import app

client = TestClient(app)

def test_main():
    response=client.get('/')
    assert response.status_code==200
    assert response.json()=="This is the first page"

def test_get_activities():
    response=client.get('/activities')
    assert response.status_code==200
    # assert response.json()=templates.TemplateResponse('activities.html',{"request": request,'data':data})