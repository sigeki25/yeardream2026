const mongoose = require("mongoose");

let schema = new mongoose.Schema({
    user: {
        type: String,
        required: [true, "작성 유저 필요"],
    },
    title: {
        type: String,
        required: [true, "제목 필요"],
        maxLength: [30, "제목은 30자 이하이어야 합니다."],
    },
    body: {
        type: String,
        required: [true, "본문 작성 필요"],
        maxLength: [200, "본문은 200자 이하이어야 합니다."],
    },
    views: {
        type: Number,
        default: 0
    },
    deleted: {
        type: Boolean,
        default: false
    },
    view_login_only: {
        type: Boolean,
        default: false
    }
}, {
    collection: "board",
    timestamps: true
});

schema.index({id:1});
module.exports = mongoose.model("board", schema);