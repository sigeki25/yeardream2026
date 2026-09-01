const express = require("express");
const router = express.Router();
const User = require("./model");
const jwt = require("jsonwebtoken");

router.post("/join", async (req, res, next) => {
    const body = req.body;
    const {id, password, name} = req.body;
    try {
        let result = await User.create({id, password, name});
        let object = result.toObject();
        delete object.password; // pw 는 경과값에서 제거
        console.log("회원가입 완료", object)
        return res.json({"success": true, "msg": "회원가입 완료"});
    } catch (e) {
        console.error(e, "code: " + e.code, "message: " + e.message)
        let msg = "";
        switch (e.code) {
            case 11000:
                msg = "이미 사용중인 아이디 입니다."
                break;
            default:
                msg = ".0필수값을 확인해 주세요."
                break;
        }
        res.json({"success": false, message: msg})
    }
});

router.post("/login", async (req, res, next) => {
    const body = req.body;
    const {id, password} = req.body;
    const user = await User.findOne({id}).select('+password');
    if (user == null) {
        console.log("user/login", "id not found")
        return res.json({"success": false, "message": "아이디나 비밀번호가 다릅니다."});
    }
    if (user.password !== password) {
        console.log("user/login", `password different: ${user.password} to ${password}`)
        return res.json({"success": false, "message": "아이디나 비밀번호가 다릅니다."});
    }
    const KEY = req.app.get("KEY");
    const token = jwt.sign({id, password}, KEY, {expiresIn: "30m"});
    return res.json({"success": true, "message": "로그인 성공", "token": token});
});

module.exports = router;