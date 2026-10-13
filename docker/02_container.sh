# 이미지 -> 설치파일 원본
# 컨테이너 ->이미지를 실행할 수 있는 프로그램으로 설치한 상태
# docker run [옵션들] [사용 이미지]
# --name : 컨테이너 이름(지정 안하면 임의의 이름으로 제작)
# -d : background 실행
# -p [호출 포트(실제 호출]]:[실제 포트(프로그램 내에서 인식)]
# --restart=always : (선택 옵션)도커가 켜지면 항상 실행
# -e : 환경설정(설치전에 정해야 하는 것들)
docker run --name mariadb -d -p 3306:3306 --restart=always -e MYSQL_ROOT_PASSWORD=1111 mariadb:11.8.3

# 컨테이너 실행 여부
# -a : (all) 죽어있거나 살아있거나 모두 보여줌(없으면 살아있는것만 보여줌)
docker ps -a

# 컨테이너 정지
# docker stop [컨테이너 이름 또는 아이디]
docker stop mariadb
# docker start mariadb
# docker restart mariadb

# 컨테이너 삭제 - 이때 컨테이너 내의 모든 데이터가 소실된다.
# -f : 강제적으로 지운다.(무조건 삭제)
# docker container rm -f [컨테이너 이름]
docker container rm -f mariadb