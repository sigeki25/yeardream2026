// npm install express jsonwebtoken bcrypt
// express, JWT, 암호화 관련
const express = require("express");
const app = express();
const jwt = require("jsonwebtoken");
const crypto = require("crypto");

app.use(express.json());
//app.use(cors());

const KEY = crypto.randomBytes(64).toString("hex");
console.log("sign key : " + KEY);

app.post("/login", (req, res, next) => {
    const {id, pw} = req.body;
    console.log(`{${id} 와 ${pw} 를 이용해 db 안에 회원이 있는지 확인`);
    // 로그인 했다고 가정
    // 토큰 생성(payload, key, expire)
    // expiresIn : s, m, h, d, w, y 사용 가능, 1.5h 같은 것도 가능
    const token = jwt.sign({id, pw}, KEY, {expiresIn: "30m"});
    res.json({"success": true, "token": token});
});

app.post("/check", (req, res, next) => {
    const headers = req.headers;
    console.log("headers", headers);
    const token = headers.authorization;
    if(token == null) {
        return res.json({"loginYN": false, "message": "토큰이 없습니다."});
    }
    try {
        const info = jwt.verify(token, KEY);
        console.log("info", info);
        //요청했던 일을 한다.
        return res.json({"loginYN": true, "data": "추가작업 결과"});
    } catch (e) {
        //만료되거나 올바르지 않은 토큰이라면 에러가 발생한다.
        return res.json({"loginYN": false, "message": "유효하지 않은 토큰입니다."});
    }
});

app.listen(80, () => console.log("http://localhost"));