const express = require("express");
const {request} = require("express");
const router = express.Router();

// 회원가입(/member/join)
router.post("/join", (req, res, next) => {
    res.json({"success": true, "msg": "회원가입 완료", "body": {...req.body}});
    console.log("/join", req.body);
});
// 회원 리스트(/member/list, /member/)
router.get(["/list", "/"], (req, res, next) => {
    res.json({"success": true, "data": []});
    console.log("/list");
});

// 회원정보 상세보기(/member/get/:id)
router.get("/get/:id", (req, res, next) => {
    const {id} = req.params;
    res.json({"success": true, "data": {"id": id, "msg": "상세보기 완료"}});
    console.log(`/get/:${id}`, req.params);
});
// 회원정보 수정(/member/update/:id)
router.put("/update/:id", (req, res, next) => {
    const {id} = req.params;
    res.json({"success": true, "data": {"id": id, "msg": "수정 완료"}});
    console.log(`/update/:${id}`, req.params);
});

// 회원정보 삭제(/member/delete/:id)
router.delete("/delete/:id", (req, res, next) => {
    const {id} = req.params;
    res.json({"success": true, "data": {"id": id, "msg": "회원삭제 완료"}});
    console.log(`/delete/:${id}`, req.params);
});

module.exports = router;