from app import main


def client():
    main.app.config["TESTING"] = True
    return main.app.test_client()


def test_health():
    assert client().get("/health").get_json() == {"status": "ok"}


def test_empty_message():
    r = client().post("/chat", json={"message": ""})
    assert r.status_code == 400


def test_too_long():
    r = client().post("/chat", json={"message": "a" * 501})
    assert r.status_code == 400


def test_dialogflow_answer(monkeypatch):
    monkeypatch.setattr(main, "ask_dialogflow", lambda t, s: {
        "reply": "hi", "intent": "x", "is_fallback": False})
    r = client().post("/chat", json={"message": "hello"})
    assert r.get_json()["reply"] == "hi"


def test_dialogflow_down(monkeypatch):
    def boom(t, s):
        raise RuntimeError("down")
    monkeypatch.setattr(main, "ask_dialogflow", boom)
    r = client().post("/chat", json={"message": "hello"})
    assert r.status_code == 502
    assert "issues@internee.pk" in r.get_json()["reply"]


def test_fallback_uses_llm(monkeypatch):
    monkeypatch.setattr(main, "ask_dialogflow", lambda t, s: {
        "reply": "", "intent": "Default Fallback Intent", "is_fallback": True})
    monkeypatch.setattr(main, "ask_llm", lambda q: "Email info@internee.pk.")
    r = client().post("/chat", json={"message": "who do I email"})
    assert r.get_json()["source"] == "llm"


def test_fallback_when_llm_off(monkeypatch):
    monkeypatch.setattr(main, "ask_dialogflow", lambda t, s: {
        "reply": "", "intent": "Default Fallback Intent", "is_fallback": True})
    monkeypatch.setattr(main, "ask_llm", lambda q: None)
    r = client().post("/chat", json={"message": "anything"})
    assert "issues@internee.pk" in r.get_json()["reply"]