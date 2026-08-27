npm init

// 괄호의 내용은 기본값

package name: (01_start)    // 프로젝트 이름
version: (1.0.0)            // 프로젝트 버전
description:                // 프러젝트 설명
entry point: (index.js)     // 시작 파일명
test command:               // test 명령어 시 실행할 명령어
git repository:             // 공유할 github 주소
keywords:                   // npm 등록 시 사용할 키워드
author:                     // 개발자 이름 또는 이메일
license: (ISC)              // 라이센스
type: (commonjs)            // 모듈 호출 방식 commonjs(require) / module(import)
About to write to ...\package.json:

{
  "name": "01_start",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "ISC",
  "type": "commonjs"
}

Is this OK? (yes) 

// 위 질문이 귀찮다면 npm init -y

npm install express