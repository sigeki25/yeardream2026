const mongo = require("mongoose");

function connectDB() {
    mongo.set("debug", true); // 실행되는 쿼리를 로그에 출력(개발용)
    const url = "mongodb://localhost:27017/self_project";
    mongo.connect(url);
    const db = mongo.connection;

    db.on("error", () => console.log("DB 접속 실패"));
    db.on("open", () => console.log("DB 접속 완료"));
}

module.exports = connectDB;