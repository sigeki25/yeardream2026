const express = require("express");
const board = express.Router();
const Board = require("../model/board");
const jwt = require("jsonwebtoken");
const mongoose = require("mongoose");
const VIEW_LIMIT = 10;

board.get(["/list", "/list/:loc"], async (req, res, next) => {
    const loc = req.params.loc || "1";
    const offset = (loc - 1) * VIEW_LIMIT;
    const limit = VIEW_LIMIT;
    console.log("req.userData : ", req.userData);
    if (req.userData.login) {
        let result = await Board.find({deleted: false}).sort({"createdAt": -1}).skip(offset).limit(limit).lean();
        return res.json({"success": true, "data": result});
    }
    let result = await Board.find({
        view_login_only: false,
        deleted: false
    }).sort({"createdAt": -1}).skip(offset).limit(limit).lean();
    return res.json({"success": true, "data": result});
});

board.post("/new", async (req, res, next) => {
    const body = req.body;
    const headers = req.headers;
    const token = headers.authorization;
    const KEY = req.app.get("KEY");
    if (!req.userData.login) {
        return res.json({"success": false, "message": "로그인 필요"});
    }
    const id = req.userData.id;
    try {
        const {title, body, view_login_only} = req.body;
        let result = await Board.create({user: id, title, body, view_login_only});
        let object = result.toObject();
        console.log("글쓰기 완료", object)
        return res.json({"success": true, "msg": "글쓰기 완료", object: object});
    } catch (e) {
        console.error(e, "code: " + e.code, "message: " + e.message)
        return res.json({"success": false, "msg": "글쓰기 실패"});
    }
});

board.get("/detail/:_id", async (req, res, next) => {
    const {_id} = req.params;
    if (_id.length !== 24) {
        console.log(`입력 자릿수 다름 /detail/${_id}`);
        return res.json({"success": false, "msg": "작성된 글이 없습니다."});
    }
    const board = await Board.findOneAndUpdate({
            _id,
            deleted: false,
            $or: [
                {view_login_only: req.userData.login},
                {view_login_only: false}
            ]
        },
        {$inc: {views: 1}},
        {new: true, timestamps: false}
    ).lean();
    if (board == null) {
        console.log(`게시물이 없거나 권한이 없거나 삭제됨 /detail/${_id}`);
        return res.json({"success": false, "msg": "작성된 글이 없습니다."});
    }
    return res.json({"success": true, "data": board});
});

board.delete("/delete/:_id", async (req, res, next) => {
    if (!req.userData.login) {
        return res.json({"success": false, "msg": "로그인이 필요합니다."});
    }
    const {_id} = req.params;
    if (_id.length !== 24) {
        console.log(`입력 자릿수 다름 /delete/${_id}`);
        return res.json({"success": false, "msg": "작성된 글이 없습니다."});
    }
    const board = await Board.findOne({_id}).lean();
    if (board == null) {
        console.log(`게시물이 없음 /delete/${_id}`);
        return res.json({"success": false, "msg": "작성된 글이 없습니다."});
    }
    if (board.user === req.userData.id) {
        const deleted_board = await Board.findOneAndUpdate({_id}, {deleted: true}, {
            new: true, // 수정된 후의 문서를 보여준다.
            runValidators: true // update 후의 스키마 검증을 수행한다.
        }).lean();
        if (deleted_board == null) {
            console.log(`삭제 실패 /delete/${_id}`);
            return res.json({"success": false, "msg": "삭제에 실패하였습니다."});
        }
        console.log(`삭제 성공 /delete/${_id}`);
        return res.json({"success": true, "msg": "삭제 완료"});
    }
    console.log(`삭제하려는 게시물의 작성자가 다름 /delete/${_id}`);
    return res.json({"success": false, "msg": "삭제 권한이 없습니다."});
});

module.exports = board;