from backend.app import create_app

def test_health_endpoint():
    app = create_app()
    client = app.test_client()
    res = client.get('/api/health')
    assert res.status_code == 200
    assert res.get_json().get('status') == 'ok'
