const express = require("express");
const app = express();
const jwt = require("jsonwebtoken");
const crypt = require("bcrypt");
const cors = require("cors");
const connectDB = require("./db");
const crypto = require("crypto");

app.use(cors());
const KEY = crypto.randomBytes(64).toString("hex");
console.log("sign key : " + KEY);
app.set("KEY", KEY);
app.use(express.json()); // BODY 로 보내는 JSON 형태로 받기

connectDB();

//로그 시작 부분
app.use ((req, res, next) => {
    console.log(`\n===== ${req.originalUrl} =====`);
    next();
});

//로그인 확인
app.use((req, res, next) => {
    const headers = req.headers;
    const token = headers.authorization;
    try {
        const KEY = req.app.get("KEY");
        const info = jwt.verify(token, KEY);
        req.userData = {
            ...req.userData,
            id: info.id,
            login: true
        };
    } catch (e) {
        req.userData = {
            ...req.userData,
            id: "",
            login: false
        };
    }
    console.log("login check : ", req.userData)
    next(); // 인자 없이 호출해야 정상적으로 다음 핸들러로 이동합니다.
});

app.use("/user", require("./src/user/router"));
app.use("/board", require("./src/board/router"));

app.listen(80, () => console.log(("http:///localhost")));