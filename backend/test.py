from app import app

def test_chatbot():
    test_client = app.test_client()
    response = test_client.get('/hello')

    print(f'status code: {response.status_code}')
    assert response.status_code ==  200, f"Expected 200, got {response.status_code}"    
    print("✓ Backend test passed!")


if __name__ == '__main__':
    test_chatbot()