def test_create_portfolio_success(client):
    payload = {
        "username": "test_user",
        "risk_preference": "Medium",
        "total_investment": 10000,
        "assets": [
            {"ticker_symbol": "AAPL", "allocation_percentage": 50},
            {"ticker_symbol": "MSFT", "allocation_percentage": 50}
        ]
    }
    response = client.post("/portfolios/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["total_investment"] == 10000
    assert len(data["assets"]) == 2


def test_create_portfolio_invalid_allocation_sum(client):
    payload = {
        "username": "test_user2",
        "risk_preference": "High",
        "total_investment": 5000,
        "assets": [
            {"ticker_symbol": "AAPL", "allocation_percentage": 70},
            {"ticker_symbol": "MSFT", "allocation_percentage": 50}
        ]
    }
    response = client.post("/portfolios/", json=payload)
    assert response.status_code == 400


def test_get_portfolio_by_id(client):
    payload = {
        "username": "test_user3",
        "risk_preference": "Low",
        "total_investment": 2000,
        "assets": [{"ticker_symbol": "GOOG", "allocation_percentage": 100}]
    }
    create_resp = client.post("/portfolios/", json=payload)
    portfolio_id = create_resp.json()["id"]

    get_resp = client.get(f"/portfolios/{portfolio_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == portfolio_id


def test_get_nonexistent_portfolio_returns_404(client):
    response = client.get("/portfolios/9999")
    assert response.status_code == 404
