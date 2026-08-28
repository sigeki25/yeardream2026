// mongoose 는 스키마 설정이 가능하다.(테이블 형태)
const mongoose = require("mongoose");

let schema = new mongoose.Schema({
    id: {
        type: String,
        required: [true, "아이디는 필수입니다."],
        unique: true, // 중복허용 안함
        trim: true, // 앞뒤 공백을 잘라서 가져옴
        minLength: [4, "아이디는 4자 이상입니다."],
        maxLength: [25, "아이디는 25자 이하입니다."]
    },
    pw: {
        type: String,
        required: [true, "비밀번호는 필수입니다."],
        trim: true, // 앞뒤 공백을 잘라서 가져옴
        select: false, // 조회할 때 기본적으로 빼고 가져온다.
    },
    name: {
        type: String,
        required: [true, "이름은 필수입니다."],
        trim: true,
    },
    phone: {
        type: String,
        trim: true,
    },
    grade: {
        type: String,
        default: "user",
        enum: ["user", "admin"],
    },
}, {
    collation: "member", // 적용할 컬렉션
    timestamps: true, // 특정 액션이 일어난 요일, 시간을 기록하는 기능
    // mongo db 는 기본적으로 _id 를 만든다.
    // mongoose 에서는 이 _id 를 id 로 기록한다.
    // 이 기능을 비활성화
    id: false
});

schema.index({name:1});

// model 명은 단수형 파스칼 표기법을 사용한다.
module.exports = mongoose.model("Member", schema);