const mongoose = require("mongoose");

let schema = new mongoose.Schema({
    id: {
        type: String,
        required: [true, "아이디는 필수입니다."],
        unique: true,
        trim: true,
        minLength: [6, "아이디는 6자 이상이어야 합니다."],
        maxLength: [30, "아이디는 30자 이하이어야 합니다."],
    },
    password: {
        type: String,
        required: [true, "비밀번호는 필수입니다."],
        trim: true,
        minLength: [6, "비밀번호는 6자 이상이어야 합니다."],
        maxLength: [30, "비밀번호는 30자 이하이어야 합니다."],
        select: false,
    },
    name: {
        type: String,
        trim: true,
        default: null
    },
    grade: {
        type: String,
        enum: ["user", "manager", "admin"],
        default: "user"
    },
}, {
    collection: "user",
    timestamps: true,
    id: false
});

schema.index({name:1});
module.exports = mongoose.model("user", schema);