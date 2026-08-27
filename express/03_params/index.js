const express = require("express");
const app = express();

// GET /rest/admin/pass
app.get("/rest/:id/:pw", (req, res) => {
    console.log(req.params);
    const {id, pw} = req.params;
    res.json({"msg": "잘 받았음", "params": {id, pw}});
});

// GET /get_method?id=admin&pw=pass

// POST /login
// {id: "admin", pw: "pass"}

// 위 URL 외의 것이 왔을 때 처리

app.listen(80, () => console.log("http://localhost"));