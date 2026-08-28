const express = require("express");
const router = express.Router();
const Member = require("./model");

// 회원가입(/member/join)
router.post("/join", async (req, res, next) => {
    const body = req.body;
    const {id, pw, name, phone} = req.body;
    try {
        let result = await Member.create({id, pw, name, phone});
        let object = result.toObject();
        console.log("create user", id, pw, name, phone);
        delete object.pw; // pw 는 경과값에서 제거
        res.json({"success": true, "msg": "회원가입 완료", "data": object});
        console.log("/join", req.body);
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
// 회원 리스트(/member/list, /member/)
router.get(["/list", "/"], async (req, res, next) => {
    let list = await Member.find()
        .sort({"createdAt": -1}) // 생성일 내림차순으로 정렬
        .lean(); // 순수 JSON 으로 반환
    res.json({"success": true, "data": list});
    console.log("/list");
});

// 회원정보 상세보기(/member/get/:id)
router.get("/get/:id", async(req, res, next) => {
    const {id} = req.params;
    // 찾는 내용이 하나일 경우(unique 속성이 있음) findOne({filter}) 사용
    let member = await Member.findOne({id}).lean();
    if (member == null) {
        res.json({"success": false, "data": {"info": {}, "message": "없는 회원"}});
        return;
    }
    res.json({"success": true, "data": {"info": member, "message": "상세보기 완료"}});
    console.log(`/get/:${id}`, req.params);
});
// 회원정보 수정(/member/update/:id)
router.put("/update/:id", (req, res, next) => {
    const {id} = req.params;
    const body = req.body;
    res.json({"success": true, "data": {"id": id, "body": body}});
    console.log(`/update/:${id}`, req.params);
});

// 회원정보 삭제(/member/delete/:id)
router.delete("/delete/:id", (req, res, next) => {
    const {id} = req.params;
    res.json({"success": true, "data": {"id": id, "msg": "회원삭제 완료"}});
    console.log(`/delete/:${id}`, req.params);
});

module.exports = router;