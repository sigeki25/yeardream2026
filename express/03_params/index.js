const express = require("express");
const app = express();

// GET /rest/admin/pass
app.get("/rest/:id/:pw", (req, res) => {
    console.log(req.params); // post 에서는 이걸로 받을 수 없다.
    const {id, pw} = req.params;
    res.json({"msg": "잘 받았음", "params": {id, pw}});
});

// GET /get_method?id=admin&pw=pass
app.get("/get_method", (req, res) => {
    console.log(req.query);
    res.json({
        "msg": "잘 받았음",
        "query": {...req.query}
    });
});

// POST /login
// {id: "admin", pw: "pass"}
// request 의body 에 JSON 형태의 데이터를 받능 때 (예) Axios
app.use(express.json());
app.post("/login", (req, res) => {
    console.log(req.body);
    res.json({
        "msg": "잘 받았음",
        "body": {...req.body}
    });
});

// 위 URL 외의 것이 왔을 때 처리
app.use("/*path", (req, res) => {
    res.send("잘못된 요청 입니다.");
});


app.listen(80, () => console.log("http://localhost"));